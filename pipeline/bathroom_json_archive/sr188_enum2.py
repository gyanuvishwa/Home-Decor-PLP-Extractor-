import sys, os, re, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import probe

def extract_product_list(html):
    key = '"productList":['
    i = html.find(key)
    if i == -1:
        return None
    start = i + len(key) - 1
    depth = 0
    in_str = False
    esc = False
    j = start
    while j < len(html):
        c = html[j]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    j += 1
                    break
        j += 1
    arr_text = html[start:j]
    return json.loads(arr_text)

TOTAL_RE = re.compile(r'"productTotalCount":(\d+)')

def enumerate_ids(url, label):
    ids = set()
    total = None
    page = 1
    while True:
        sep = '&' if '?' in url else '?'
        u = f"{url}{sep}pageNumber={page}"
        st, html, fu = probe.fetch(u)
        if st != 200:
            print(f"  [{label}] page {page}: HTTP {st} -- ABORT")
            break
        m = TOTAL_RE.search(html)
        this_total = int(m.group(1)) if m else None
        if total is None:
            total = this_total
        arr = extract_product_list(html)
        if not arr:
            print(f"  [{label}] page {page}: no productList -- stop")
            break
        page_ids = [p.get('id') for p in arr]
        before = len(ids)
        ids |= set(page_ids)
        print(f"  [{label}] page {page}: total={this_total} on_page={len(page_ids)} new={len(ids)-before} running_unique={len(ids)}")
        if total and page * 48 >= total:
            break
        if len(page_ids) < 48:
            break
        page += 1
        if page > 30:
            print("  SAFETY STOP")
            break
        time.sleep(0.4)
    print(f"  [{label}] FINAL: productTotalCount={total} unique_ids_enumerated={len(ids)}")
    return total, ids

if __name__ == "__main__":
    print("=== BATHROOM ACCESSORIES PARENT ===")
    pa_total, pa_ids = enumerate_ids("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories", "PARENT-Accessories")

    print("\n=== children of Bathroom Accessories ===")
    org_total, org_ids = enumerate_ids("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/acessories-854100-1", "Organisation")
    tb_total, tb_ids = enumerate_ids("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/toilet-brushes", "ToiletBrushes")
    sd_total, sd_ids = enumerate_ids("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/soap-dispensers", "SoapDispensers")
    bm_total, bm_ids = enumerate_ids("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/bathroom-mirrors", "BathroomMirrors")
    bs_total, bs_ids = enumerate_ids("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/bathroom-scales", "BathroomScales")

    child_union = org_ids | tb_ids | sd_ids | bm_ids | bs_ids
    residue_ids = pa_ids - child_union
    print(f"\nPARENT total={pa_total} unique={len(pa_ids)}")
    print(f"children totals: org={org_total} tb={tb_total} sd={sd_total} bm={bm_total} bs={bs_total}")
    print(f"children unique counts: org={len(org_ids)} tb={len(tb_ids)} sd={len(sd_ids)} bm={len(bm_ids)} bs={len(bs_ids)}")
    print(f"children sum = {len(org_ids)+len(tb_ids)+len(sd_ids)+len(bm_ids)+len(bs_ids)}")
    print(f"children UNION = {len(child_union)}")
    print(f"RESIDUE (parent - child union) = {len(residue_ids)}")

    out = {
        "parent_total": pa_total, "parent_unique": len(pa_ids),
        "org_total": org_total, "org_unique": len(org_ids),
        "tb_total": tb_total, "tb_unique": len(tb_ids),
        "sd_total": sd_total, "sd_unique": len(sd_ids),
        "bm_total": bm_total, "bm_unique": len(bm_ids),
        "bs_total": bs_total, "bs_unique": len(bs_ids),
        "children_union": len(child_union),
        "residue_count": len(residue_ids),
        "residue_ids": sorted(residue_ids),
    }
    with open(os.path.join(os.path.dirname(__file__), "sr188_accessories_result2.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("\n\n=== BATHROOM FURNITURE PARENT ===")
    pf_total, pf_ids = enumerate_ids("https://www.myer.com.au/c/home/all-furniture/furniture-bathroom", "PARENT-Furniture")
    print("\n=== children of Bathroom Furniture ===")
    cv_total, cv_ids = enumerate_ids("https://www.myer.com.au/c/home/all-furniture/furniture-bathroom/cabinets-vanities", "CabinetsVanities")
    ft_total, ft_ids = enumerate_ids("https://www.myer.com.au/c/home/all-furniture/furniture-bathroom/fittings", "Fittings")

    fchild_union = cv_ids | ft_ids
    fresidue_ids = pf_ids - fchild_union
    print(f"\nPARENT total={pf_total} unique={len(pf_ids)}")
    print(f"children totals: cv={cv_total} ft={ft_total}")
    print(f"children unique: cv={len(cv_ids)} ft={len(ft_ids)}")
    print(f"children UNION = {len(fchild_union)}")
    print(f"RESIDUE (parent - child union) = {len(fresidue_ids)}")

    out2 = {
        "parent_total": pf_total, "parent_unique": len(pf_ids),
        "cv_total": cv_total, "cv_unique": len(cv_ids),
        "ft_total": ft_total, "ft_unique": len(ft_ids),
        "children_union": len(fchild_union),
        "residue_count": len(fresidue_ids),
        "residue_ids": sorted(fresidue_ids),
    }
    with open(os.path.join(os.path.dirname(__file__), "sr188_furniture_result2.json"), "w", encoding="utf-8") as f:
        json.dump(out2, f, indent=1)
