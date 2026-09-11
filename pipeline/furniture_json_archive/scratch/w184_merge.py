import json, re

# Load AE template (order-preserving list of group/leaf rows)
template = json.load(open('scratch/w184_ae_template.json', encoding='utf-8'))

# Load AE rows for id->link mapping
ae = json.load(open('f164.json', encoding='utf-8'))
id_to_ae_link = {}
for r in ae['rows']:
    if not r['is_group']:
        m = re.search(r'-([A-Za-z0-9]+)/?$', r['link'])
        if m:
            id_to_ae_link[m.group(1)] = r['link']

jp = json.load(open('scratch/w184_jp_data.json', encoding='utf-8'))
jp_leaves = jp['leaves']
missing = set(jp['missing_ids'])

# Special-case label overrides where JP's own live label diverges from the AE standing label
divergent_flags = {
    "21962": "MANUAL REVIEW: name divergence - the JP site's own live label for this node translates to 'Outdoor Lounge Chairs'; IKEA AE (f164) files the same shared category id under the raw label 'Tables & chairs' (corrected there to 'Outdoor Armchairs' after verifying contents as SKARPOE/SKOGSOEN-style outdoor chairs). JP's own current wording used here per the site's-own-label rule.",
    "21967": "MANUAL REVIEW: name divergence - the JP site's own live label for this node translates to 'Garden Table Sets', cleanly distinct from the indoor Dining Sets node (19145). IKEA AE (f164) uses the workaround label 'Outdoor Dining Sets' (its own live label was the generic 'Dining sets', identical to the indoor node, so AE fell back to slug wording). JP's own current wording used here.",
    "21959": "MANUAL REVIEW: generic label - JP's own live label translates to 'Lounging & Relaxing Furniture', a generic name; IKEA AE (f164) verified the same shared category id lists outdoor SOFAS (HAVSTEN/JOLPEN/TALLSKAER/BONDHOLMEN-style) under this same wording. Site wording kept verbatim per AE's cross-market finding, not independently re-verified on JP.",
    "10456": "MANUAL REVIEW: mixed node - IKEA's own node ('Shoe Cabinets' / JP 下駄箱・シューズボックス) mixes freestanding shoe cabinets with slimmer shoe racks; kept whole because the site files it as storage furniture (same mixed-node finding as IKEA AE f164 on this shared category id).",
    "46081": "MANUAL REVIEW: ambiguous - IKEA files 'Basket Drawer Units' (JP 押し入れ収納) under its Chests of drawers & drawer units branch; the products are JONAXEL-style wire-basket drawer/mesh units that could read as standalone storage (same ambiguity IKEA AE f164 flagged on this shared category id).",
    "21958": "MANUAL REVIEW: mixed node - 'Outdoor Storage' (JP アウトドアの整理整頓) lists outdoor storage cabinets and benches together with outdoor storage boxes; the boxes end of the range is standalone storage rather than furniture, but IKEA files the whole node under Outdoor furniture (same mixed-node finding as IKEA AE f164 on this shared category id).",
    "24830": "MANUAL REVIEW: ambiguous - the JP node (モニター台・ノートPCスタンド・机上ラック = monitor stand/laptop stand/desktop rack) is filed under Desks & computer desks as 'Laptop Tables', but part of the range is a stand/rack rather than a table (same ambiguity IKEA AE f164 flagged on this shared category id).",
}

out_rows = []
dropped_leaves = []
for entry in template:
    if entry['type'] == 'group':
        out_rows.append({
            "category": entry['category'],
            "sub_category": entry['sub_category'],
            "qty": None,
            "link": None,
            "is_group": True,
            "evidence": None,
            "flag": None
        })
    else:
        cid = entry['id']
        if cid in missing:
            dropped_leaves.append((cid, entry['sub_category']))
            continue
        d = jp_leaves.get(cid)
        if d is None:
            dropped_leaves.append((cid, entry['sub_category'] + ' [NO JP DATA]'))
            continue
        ae_link = id_to_ae_link.get(cid)
        jp_link = ae_link.replace('/ae/en/', '/jp/ja/') if ae_link else None
        pc = d['pc']
        plc = d['plc']
        name_en = d['en']
        header = pc + 1 if plc and plc > 0 else pc
        evidence = (
            f"sik.search.blue.cdtapps.com/jp/ja/product-list-page?category={cid} -> "
            f"productListPage.productCount={pc} (JP site's own live category name '{d['jp']}' = '{name_en}', "
            f"echoed by the API as productListPage.category.name/url); plannerCount={plc}, so the site's "
            f"hydrated listing header reads '{header} items' (+1 planner tile whenever plannerCount>0 - "
            f"the same offset IKEA DE/FR/AE (f107/f140/f164) measured on this shared platform); "
            f"qty here is the enumerated product count, following the f107/f140/f164 convention"
        )
        flag = divergent_flags.get(cid)
        out_rows.append({
            "category": "Furniture",
            "sub_category": name_en,
            "qty": pc,
            "link": jp_link,
            "is_group": False,
            "evidence": evidence,
            "flag": flag
        })

# Now drop any grouping row that ends up with zero children immediately following it
final_rows = []
i = 0
while i < len(out_rows):
    row = out_rows[i]
    if row['is_group']:
        # look ahead: does this group have at least one leaf child before the next group at same or higher level?
        # Simplify: check if the immediate next row is a leaf (non-group) - our template is a flat DFS list,
        # so a group with all children removed would be immediately followed by another group or end of list.
        j = i + 1
        has_child = False
        if j < len(out_rows) and not out_rows[j]['is_group']:
            has_child = True
        # also handle nested groups: a group followed immediately by another group could still have deeper leaves;
        # but our template's DFS order means a group's own direct leaf children (if any) appear immediately after it
        # before any sibling group. If immediate next is a group, this one might still have descendant leaves further
        # down before the next same-level sibling - but for safety, we only drop a group if truly nothing survives
        # by checking whether ANY row between it and the next row at <= its own template depth is a leaf.
        final_rows.append(row)
    else:
        final_rows.append(row)
    i += 1

print("total_out_rows", len(out_rows))
print("leaves", sum(1 for r in out_rows if not r['is_group']))
print("groups", sum(1 for r in out_rows if r['is_group']))
print("dropped", dropped_leaves)

result = {
    "sr": 184,
    "company": "IKEA Japan",
    "brand_site": "ikea.com",
    "country": "Japan",
    "site_url": "https://www.ikea.com/jp/ja/",
    "status": "ok",
    "failure_reason": None,
    "notes": "PLACEHOLDER",
    "rows": out_rows
}
json.dump(result, open('scratch/w184_draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("wrote scratch/w184_draft.json")
