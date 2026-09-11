import json

groups = json.load(open('kmart_full_tree.json', encoding='utf-8'))
home_living = groups[0]

def walk_path(*names):
    cur_list = groups
    node = None
    for name in names:
        node = next((n for n in cur_list if n['display_name'] == name), None)
        if node is None:
            raise KeyError(f"not found: {names}")
        cur_list = node.get('children', [])
    return node

def leaf(names, sub_category=None, confidence="HIGH", flag=None):
    node = walk_path(*names)
    url = "https://www.kmart.com.au" + node['data']['url']
    return {
        "category": None,
        "sub_category": sub_category or node['display_name'],
        "qty": node['count'],
        "link": url,
        "is_group": False,
        "evidence": f"Constructor.io browse API (ac.cnstrc.com/browse/group_id/{node['group_id']}) total_num_results={node['count']}, path: {' > '.join(names)}",
        "flag": flag,
        "confidence": confidence,
    }

def group(name, flag=None):
    return {
        "category": None,
        "sub_category": name,
        "qty": None,
        "link": None,
        "is_group": True,
        "evidence": None,
        "flag": flag,
        "confidence": "HIGH",
    }

HL = "Home & Living"

textile_rows = []
T = textile_rows

T.append(group("Bedding"))
T.append(group("Quilt Cover Sets"))
for nm in ["King Quilt Cover Sets", "Queen Quilt Cover Sets", "Double Quilt Cover Sets", "Single Quilt Cover Sets", "Super King Quilt Cover Sets", "Gingham Quilt Cover Sets", "Stripe Quilt Cover Sets", "Linen Cotton Bed Linen"]:
    T.append(leaf([HL, "Bedroom", "Bedding", "Quilt Cover Sets", nm]))

T.append(group("Quilts"))
for nm in ["Queen", "Double", "Single", "King", "Super King", "Medium Warmth Quilts", "High Warmth Quilts", "Low Warmth Quilts"]:
    T.append(leaf([HL, "Bedroom", "Bedding", "Quilts", nm]))

T.append(group("Bed Sheets"))
for nm in ["Sheet Sets", "Queen Sheets", "King Sheets", "King Single Sheets", "Double Sheets", "Single Sheets", "Super King Sheets", "Fitted Sheets", "Pillowcases", "Flannelette Sheets", "Stonewashed Bed Linen", "Bamboo Bed Linen", "Cotton Sheets", "Polyester Cotton Sheets", "Gingham Sheets"]:
    T.append(leaf([HL, "Bedroom", "Bedding", "Bed Sheets", nm]))

T.append(leaf([HL, "Bedroom", "Bedding", "Indoor Cushions"]))
T.append(leaf([HL, "Bedroom", "Bedding", "Cushion Covers"]))
T.append(leaf([HL, "Bedroom", "Bedding", "Blankets & Throws"]))
T.append(leaf([HL, "Bedroom", "Bedding", "Pillows"]))
T.append(leaf([HL, "Bedroom", "Bedding", "Coverlets & Comforters"]))
T.append(leaf([HL, "Bedroom", "Bedding", "Mattress Protectors"]))
T.append(leaf([HL, "Bedroom", "Bedding", "Pillow Protectors"]))
T.append(leaf([HL, "Bedroom", "Bedding", "Premium Bed Accessories"], confidence="LOW",
              flag="Ambiguous grouping name; contents not individually verified (category page direct fetch blocked by Akamai). Included as a bedding-adjacent textile accessory line."))

T.append(leaf([HL, "Bedroom", "Mattress Toppers & Underlays"], confidence="MEDIUM",
              flag="Name combines 'Mattress Toppers' (textile per rules) with 'Underlays' (ambiguous term); node sits under the Bedroom nav so treated as a bed/mattress textile line, not a rug underlay."))

T.append(group("Kids Bedding"))
for nm in ["Kids Blankets", "Kids Quilt Covers & Comforters"]:
    T.append(leaf([HL, "Bedroom", "Kids Room", "Kids Bedding", nm]))

T.append(group("Rugs"))
for nm in ["Large Rugs", "Extra Extra Large Rugs", "Extra Large Rugs", "Medium Rugs", "Small Rugs", "Round Rugs", "Runner Rugs", "Rectangular Rugs", "Bohemian Rugs", "Traditional Rugs", "Asymmetrical Rugs", "Wool Rich Rugs", "Washable Rugs, Runners & Mats"]:
    T.append(leaf([HL, "Rugs & Home Furnishings", "Rugs", nm]))

T.append(group("Curtains & Rods"))
T.append(leaf([HL, "Home Decor", "Curtains & Rods", "Blockout Curtains"]))
T.append(leaf([HL, "Home Decor", "Curtains & Rods", "Sheer Curtains"]))

T.append(leaf([HL, "Bathroom", "Shower Curtains"]))
T.append(leaf([HL, "Home Decor", "Door Mats"], confidence="MEDIUM",
              flag="Kmart's taxonomy lists two different 'Door Mats' nav placements for the same URL slug with conflicting counts (48 under Rugs & Home Furnishings > Door Mats vs 191 under Home Decor > Door Mats). Used 191 (Home Decor placement, real merchandising sequence=14000) as canonical; the 48-count node carries a sentinel/fallback sequence value suggesting it is the orphaned duplicate. Manual spot-check recommended."))
T.append(leaf([HL, "Home Decor", "Cushions", "Outdoor Cushions"]))

T.append(leaf([HL, "Dining", "Tableware", "Table Runners"]))
T.append(leaf([HL, "Dining", "Tableware", "Tablecloths"]))
T.append(leaf([HL, "Dining", "Tableware", "Napkins"]))
T.append(leaf([HL, "Dining", "Tableware", "Placemats & Coasters"], confidence="MEDIUM",
              flag="Combined category also includes coasters (often non-textile cork/wood); included as primarily a textile placemat line per site grouping."))

T.append(group("Kitchen Linen & Tea Towels"))
for nm in ["Tea Towels", "Pot Holders & Oven Mitts", "Aprons"]:
    T.append(leaf([HL, "Dining", "Kitchen Linen & Tea Towels", nm]))

T.append(group("Towels"))
for nm in ["Bath Towels", "Hand Towels", "Bath Sheets", "Mega Towel", "Face Washers", "Bamboo Towels"]:
    T.append(leaf([HL, "Bathroom", "Towels", nm]))
T.append(leaf([HL, "Bathroom", "Towels", "Beach Towels"], confidence="MEDIUM",
              flag="URL is under /category/sport-and-outdoor/ but the node is nested in the Bathroom > Towels menu; treated as a genuine towel/textile product line."))

T.append(leaf([HL, "Bathroom", "Bath Mats"]))

for r in T:
    r["category"] = "Textile"

storage_rows = []
S = storage_rows

S.append(group("Storage & Organisation"))
S.append(group("Bedroom Storage"))
for nm in ["Wardrobe Organisers", "Drawer Organisers", "Storage Drawers & Trolleys", "Garment Racks", "Shoe Storage"]:
    S.append(leaf([HL, "Storage & Organisation", "Bedroom Storage", nm]))

S.append(group("Kitchen Storage"))
for nm in ["Pantry Storage", "Food Storage Containers", "Fridge Storage", "Jars & Canisters", "Glass Food Storage", "Kitchen Drawer Organisers"]:
    S.append(leaf([HL, "Storage & Organisation", "Kitchen Storage", nm]))
S.append(leaf([HL, "Storage & Organisation", "Kitchen Storage", "Dish Racks"], confidence="MEDIUM",
              flag="Not explicitly named in storage rules; included as a kitchen organization item that holds/drains dishes, per site placement under Kitchen Storage."))
S.append(leaf([HL, "Storage & Organisation", "Kitchen Storage", "Kitchen Trolley"], confidence="MEDIUM",
              flag="Rolling kitchen storage cart; storage.md section 20 explicitly includes 'Kitchen Storage Carts'."))
S.append(leaf([HL, "Kitchen", "Kitchen Storage", "Glass Jars & Canisters"], confidence="MEDIUM",
              flag="Distinct URL/leaf found only via the Kitchen top-nav branch of Kitchen Storage (not present in the Storage & Organisation branch's child list, though both branches share the same parent count of 1858)."))

S.append(group("Bathroom Storage"))
S.append(leaf([HL, "Storage & Organisation", "Bathroom Storage", "Shower Caddies"]))
S.append(leaf([HL, "Storage & Organisation", "Bathroom Storage", "Bathroom Cabinets & Shelves"], confidence="MEDIUM",
              flag="Could be read as bathroom furniture; included as Storage because Kmart's own nav places it under Storage & Organisation > Bathroom Storage."))
S.append(leaf([HL, "Storage & Organisation", "Bathroom Storage", "Bathroom Trolleys"]))

S.append(group("Laundry"))
S.append(group("Laundry Storage"))
S.append(leaf([HL, "Storage & Organisation", "Laundry", "Laundry Storage", "Storage Tins & Containers"]))
S.append(leaf([HL, "Storage & Organisation", "Laundry", "Laundry Storage", "Hooks & Hanger Solutions"], confidence="MEDIUM",
              flag="Hanging/hook-based laundry organization solution; borderline hardware vs organization product."))
S.append(leaf([HL, "Storage & Organisation", "Laundry", "Laundry Baskets & Hampers"]))

S.append(group("Storage Tubs, Boxes & Bags"))
for nm in ["Storage Tubs", "Storage Boxes", "Storage Bags"]:
    S.append(leaf([HL, "Storage & Organisation", "Storage Tubs, Boxes & Bags", nm]))

S.append(leaf([HL, "Storage & Organisation", "Baskets"]))
S.append(leaf([HL, "Storage & Organisation", "White Storage"]))
S.append(leaf([HL, "Storage & Organisation", "Linen Look Storage"], confidence="MEDIUM",
              flag="Fabric/linen-look storage boxes and baskets; primary purpose is storage (storage.md section 25: Fabric Storage Basket/Box -> Storage)."))
S.append(leaf([HL, "Storage & Organisation", "Clear Storage Solutions"]))
S.append(leaf([HL, "Storage & Organisation", "Entryway Storage"]))
S.append(leaf([HL, "Storage & Organisation", "Jewellery Storage"]))
S.append(leaf([HL, "Storage & Organisation", "Beauty Storage"]))
S.append(leaf([HL, "Storage & Organisation", "Garage Storage"]))
S.append(leaf([HL, "Storage & Organisation", "Felt Storage"], sub_category="Felt Storage (Fabric Storage)", confidence="MEDIUM",
              flag="Site display name is 'Felt Storage' but the URL slug is /fabric-storage/; fabric storage boxes/bins, primary purpose is storage per storage.md section 25."))
S.append(leaf([HL, "Storage & Organisation", "Bookshelves"], confidence="MEDIUM",
              flag="Bookshelves are often Furniture, but Kmart's own nav places this specific node under Storage & Organisation (a separate node from Furniture > Office Furniture > Bookshelves), so Storage is used per the site's explicit categorization."))

S.append(group("Kids Storage"))
S.append(leaf([HL, "Storage & Organisation", "Kids Storage", "Kids Toy Storage"]))

S.append(group("Filing"))
for nm in ["Expanding Files & Carry Files", "Binders & Document Wallets"]:
    S.append(leaf([HL, "Home Office & Stationery", "Filing", nm]))
S.append(leaf([HL, "Home Office & Stationery", "Filing", "Display Books & Sheet Protectors"], confidence="LOW",
              flag="Borderline stationery/document-display product rather than a storage container; included per ambiguity-handling rule (site places it under the Filing/organization menu)."))

S.append(group("Desk Organisation & Accessories"))
for nm in ["Desk Drawers Organisers & Trays", "Magazine Holders", "File Holder"]:
    S.append(leaf([HL, "Home Office & Stationery", "Desk Organisation & Accessories", nm]))

for r in S:
    r["category"] = "Storage"

print("textile rows:", len(textile_rows), "leaf:", sum(1 for r in textile_rows if not r['is_group']))
print("storage rows:", len(storage_rows), "leaf:", sum(1 for r in storage_rows if not r['is_group']))

notes = (
    "ACCESS: Tier (a) HTTP fetch via curl_cffi (chrome impersonation). robots.txt (User-agent: * / Allow: /) "
    "and the XML sitemaps loaded fine (200), but direct fetches of /category/* pages returned Akamai "
    "'Access Denied' (403) for both curl_cffi and Playwright/CDP (tier b), even with a warmed session/referer. "
    "Recovered by finding the site's own client-side product-discovery API (Constructor.io, ac.cnstrc.com) "
    "referenced in the homepage HTML (public key key_GZTqlLr41FS2p7AY). This is the exact API Kmart's own "
    "frontend calls to render category pages, so its counts are the site's real numbers, not a scrape/estimate. "
    "Chrome (tier c) was not needed. "
    "TREE: Built via one consistent snapshot: GET https://ac.cnstrc.com/browse/group_id/dddaa894234df841cfb678463562e055 "
    "(Home & Living root) with fmt_options[groups_max_depth]=5, returning the full ~695-node taxonomy tree in one call. "
    "Verified that a child's 'count' field equals total_num_results when that group_id is browsed directly (spot-checked "
    "on Queen Quilts, Curtains & Rods). Cross-referenced against category-sitemap.xml. "
    "QTY: total_num_results / group count field from the Constructor.io browse response for each node's own group_id. "
    "Kmart's taxonomy places some categories (Rugs, Cushions, Curtains & Rods, Door Mats, Kids Storage, Bookshelves, "
    "Lighting, DIY, etc.) under multiple parent menus simultaneously, sometimes with conflicting counts for the same URL "
    "(a real site data quirk, not a fetch error). Resolved by preferring the node flagged defaultCategory=true; where no "
    "duplicate carried that flag (Door Mats), preferred the one with a real merchandising sequence number over the one "
    "carrying an int32-sentinel/fallback sequence (2147483647 etc.), and flagged the row confidence MEDIUM. "
    "EXCLUDED: Furniture (Bedroom Furniture, Bed Frames & Bedheads, Wardrobes, Drawers, Bedside Tables, Shelving Units "
    "[explicitly under Furniture>Office Furniture, unlike the separate Storage&Org>Bookshelves node which was kept], "
    "Console/Coffee/Side/Dining Tables, Bed Mattresses); Lighting (all); Kitchen & Dining non-textile (Dinnerware, "
    "Glassware, Serveware, Cookware, Bakeware, Appliances, Rubbish Bins); Decorative Home Accessories (Vases, Candles, "
    "Frames & Albums, Wall Art, Clocks, Mirrors, Trays/Bowls/Objects, Artificial Plants, Pots & Planters); Bathroom "
    "fixtures (Toilet Accessories, Bathroom Scales, Bathroom Mirrors); pet products (Cat/Dog Beds, Pet Blankets, Pet "
    "Feeding Mats); apparel/general merchandise (Lunch Boxes, Stationery Supplies ex-Filing/Desk-org, Data Storage & "
    "Hard Drives [electronic storage, out of scope], Computer Accessories); hardware/accessories excluded from Textile "
    "(Curtain Rods, Rug Accessories, Rugs Buying Guide, 'How to organise your X' guide pages); non-storage utility "
    "items excluded from Storage (Clothes Airers & Pegs, Ironing Boards & Covers, Hangers, Rubbish Bins, Clipboards, "
    "Binder Dividers, Pen Cups, 'Storage & Organisation Essentials' promo page, garage/camping/data storage). "
    "Low/medium-confidence rows are individually flagged per row."
)

out = {
    "sr": 176,
    "company": "Kmart Australia",
    "brand_site": "kmart.com.au",
    "country": "Australia",
    "site_url": "https://www.kmart.com.au/",
    "status": "ok",
    "failure_reason": None,
    "notes": notes,
    "textile_rows": textile_rows,
    "storage_rows": storage_rows,
}

with open('ts176.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=True)

print("WROTE ts176.json")
