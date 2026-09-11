import json

BASE = "https://www.jcpenney.com"

def url(path, id_=None, item_type=None):
    q = []
    if item_type:
        q.append("item_type=" + item_type.replace(" ", "+"))
    if id_:
        q.append("id=" + id_)
    qs = "&".join(q)
    return BASE + path + ("?" + qs if qs else "")

rows = []

def group(sub):
    rows.append({
        "category": "Furniture", "sub_category": sub, "qty": None, "link": None,
        "is_group": True, "evidence": None, "flag": None
    })

def leaf(sub, qty, path, id_=None, item_type=None, evidence=None, flag=None):
    rows.append({
        "category": "Furniture", "sub_category": sub, "qty": qty,
        "link": url(path, id_, item_type), "is_group": False,
        "evidence": evidence, "flag": flag
    })

API_EV = ("ac.cnstrc.com/browse/group_id/{id} response.total_num_results (Constructor.io public index "
          "key_xT77K5VmpiVduqnj; JCPenney PLP grid is client-rendered so no count exists in static/initial "
          "HTML -- same backend + method verified exact by the prior Home-Decor pass on this company via "
          "facet-sum and direct-filter cross-checks)")

# ---------------- Bedroom Furniture ----------------
group("Bedroom Furniture")
leaf("Beds & Headboards", 637, "/g/home-store/furniture-store/beds-headboards", "cat100250035",
     evidence=API_EV.format(id="cat100250035"))
leaf("Bed Frames & Adjustable Bases", 162, "/g/mattresses/bed-frames-adjustable-bases", "cat1009550007",
     evidence=API_EV.format(id="cat1009550007"),
     flag=None)
leaf("Dressers & Chests", 195, "/g/home-store/furniture-store/dressers-chests", "cat100250036",
     evidence=API_EV.format(id="cat100250036"))
leaf("Nightstands & Bedside Tables", 218, "/g/home-store/furniture-store/nightstands-bedside-tables", "cat1006240005",
     evidence=API_EV.format(id="cat1006240005"))
leaf("Kids & Teens Furniture", 522, "/g/home-store/furniture-store/kids-teens-furniture", "cat100330047",
     evidence=API_EV.format(id="cat100330047"))

# ---------------- Living Room Furniture ----------------
group("Living Room Furniture")
leaf("Sofas", 352, "/g/home-store/furniture-store/sofas", "cat100250026",
     evidence=("rendered page text '352 results' on the loaded PLP (document.body.innerText); corroborated "
               "against ac.cnstrc.com total_num_results=357 for the same group_id cat100250026 -- the ~1.4% "
               "gap matches the project's known stock-gated-header pattern (rendered header = in-stock count, "
               "API = published catalogue), so the rendered in-stock header is used per Rule 4 priority"))
leaf("Chairs & Recliners", 664, "/g/home-store/furniture-store/chairs-recliners", "cat100250025",
     evidence=API_EV.format(id="cat100250025"))
leaf("Accent Tables", 963, "/g/home-store/furniture-store/accent-tables", "cat100250024",
     evidence=API_EV.format(id="cat100250024"))
leaf("Ottomans & Benches", 543, "/g/home-store/furniture-store/ottomans-benches", "cat1001290032",
     evidence=API_EV.format(id="cat1001290032"))

group("Media & TV Storage")
leaf("Entertainment Centers", 10, "/g/home-store/furniture-store/media-storage-furniture/entertainment-centers", "cat100300117",
     evidence=API_EV.format(id="cat100300117"))
leaf("Media Seating", 12, "/g/home-store/furniture-store/media-storage-furniture/media-seating", "cat100300120",
     evidence=API_EV.format(id="cat100300120"))
leaf("Shelves (Media)", 33, "/g/home-store/furniture-store/media-storage-furniture/shelves", "cat1003720009",
     evidence=API_EV.format(id="cat1003720009"))
leaf("Gaming Chairs & Beanbags", 92, "/g/home-store/furniture-store/media-storage-furniture/gaming-chairs-beanbags", "cat1006160050",
     evidence=API_EV.format(id="cat1006160050"))
leaf("Trunks & Chests", 10, "/g/home-store/furniture-store/media-storage-furniture/trunks-chests", "cat1004070024",
     evidence=API_EV.format(id="cat1004070024"))
leaf("TV Stands", 145, "/g/home-store/furniture-store/media-storage-furniture/tv-stands", "cat100300118",
     evidence=API_EV.format(id="cat100300118"))
leaf("Armoires (Media)", 0, "/g/home-store/furniture-store/media-storage-furniture/armoires", "cat100300119",
     evidence=API_EV.format(id="cat100300119"),
     flag="MANUAL REVIEW: qty=0 confirmed only via API total_num_results; the site's own empty-state text on the "
          "rendered PLP was not captured (grid is client-rendered/virtualized and get_page_text did not surface it)")
leaf("TV Tray Tables", 6, "/g/home-store/furniture-store/media-storage-furniture/tv-tray-tables", "cat1005540004",
     evidence=API_EV.format(id="cat1005540004"))

# ---------------- Kitchen & Dining Furniture ----------------
group("Kitchen & Dining Furniture")
leaf("Dining Sets", 334, "/g/home-store/furniture-store/dining-sets", "cat100250054",
     evidence=API_EV.format(id="cat100250054"))
leaf("Dining Room Tables", 220, "/g/home-store/furniture-store/dining-room-tables", "cat100250055",
     evidence=API_EV.format(id="cat100250055"))
leaf("Dining Room Chairs", 560, "/g/home-store/furniture-store/dining-room-chairs", "cat100250056",
     evidence=API_EV.format(id="cat100250056"))
leaf("Buffets & Storage", 72, "/g/home-store/furniture-store/buffets-storage", "cat100250057",
     evidence=API_EV.format(id="cat100250057"))
leaf("Kitchen Carts & Islands", 148, "/g/home-store/furniture-store/kitchen-carts-islands", "cat100250058",
     evidence=API_EV.format(id="cat100250058"))
leaf("Bar Stools", 577, "/g/home-store/furniture-store/barstools", "cat100240134",
     evidence=API_EV.format(id="cat100240134"))

group("Bar Furniture")
BARFURN_EV = ("ac.cnstrc.com/browse/group_id/cat1009850002 item_type facet count (Constructor.io); node total "
              "(682) not used directly because its dominant item_type 'bar stools'=575 duplicates the dedicated "
              "Bar Stools node (cat100240134=577, same population) -- kept only under the dedicated Bar Stools "
              "row per the project's cross-listing dedup rule, remaining item_types recorded here")
leaf("Bar Sets", 58, "/g/home-store/furniture-store/bar-furniture", "cat1009850002", item_type="bar sets",
     evidence=BARFURN_EV)
leaf("Bar Tables", 29, "/g/home-store/furniture-store/bar-furniture", "cat1009850002", item_type="bar tables",
     evidence=BARFURN_EV)
leaf("Pub Sets", 7, "/g/home-store/furniture-store/bar-furniture", "cat1009850002", item_type="pub sets",
     evidence=BARFURN_EV)
leaf("Bars", 7, "/g/home-store/furniture-store/bar-furniture", "cat1009850002", item_type="bars",
     evidence=BARFURN_EV)
leaf("Wine Cabinets", 4, "/g/home-store/furniture-store/bar-furniture", "cat1009850002", item_type="wine cabinets",
     evidence=BARFURN_EV)

# ---------------- Patio & Outdoor Furniture ----------------
group("Patio & Outdoor Furniture")
PATIO_EV = ("ac.cnstrc.com/browse/group_id/cat100240095 item_type facet count (Constructor.io); node total "
            "(1808) reachable at this id because the department's own sub-tile links (Conversation Sets, "
            "Chairs & Loungers, Patio Dining Furniture, Accent Furniture, Sofas & Sectionals, Umbrellas, "
            "Benches) are broken on this site and all resolve back to this same parent id -- so item_type is "
            "the only real sub-category axis available; facet sum (1809) matches total (1808) within 1 unit")
patio_items = [
    ("Conversation Sets", "conversation sets", 252),
    ("Accent Tables (Patio)", "accent tables", 136),
    ("Benches (Patio)", "benches", 105),
    ("Dining Chairs (Patio)", "dining chairs", 82),
    ("Chaise Lounges", "chaise lounges", 74),
    ("Lounge Chairs", "lounge chairs", 65),
    ("Accent Chairs (Patio)", "accent chairs", 62),
    ("Adirondack Chairs", "adirondack chairs", 59),
    ("Dining Tables (Patio)", "dining tables", 46),
    ("Dining Sets (Patio)", "dining sets", 45),
    ("Hammocks", "hammocks", 43),
    ("Bar Stools (Patio)", "bar stools", 42),
    ("Rocking Chairs", "rocking chairs", 36),
    ("Bar Sets (Patio)", "bar sets", 27),
    ("Bistro Sets", "bistro sets", 25),
    ("Swings", "swings", 21),
    ("Loveseats (Patio)", "loveseats", 18),
    ("Folding Chairs", "folding chairs", 17),
    ("Ottomans (Patio)", "ottomans", 16),
    ("Picnic Tables", "picnic tables", 15),
    ("Sofas (Patio)", "sofas", 14),
    ("Gliders", "gliders", 13),
    ("Sectionals (Patio)", "sectionals", 10),
    ("Bistro Tables", "bistro tables", 8),
    ("Bar Tables (Patio)", "bar tables", 8),
    ("Lounge Sets", "lounge sets", 7),
    ("Chair Hammocks", "chair hammocks", 7),
    ("Table & Chair Sets", "table & chair sets", 7),
    ("Patio Shelves", "patio shelves", 6),
    ("Hammock Stands", "hammock stands", 5),
    ("Serving Carts", "serving carts", 4),
    ("Hammock Swing Chairs", "hammock swing chairs", 4),
    ("Sling Chairs", "sling chairs", 4),
    ("Patio Daybeds", "patio daybeds", 3),
    ("Bars (Patio)", "bars", 2),
    ("Garden Stools", "garden stools", 2),
    ("Chair Hammock Stands", "chair hammock stands", 2),
    ("Office Chairs (Patio)", "office chairs", 2),
    ("Alcapulco Chairs", "alcapulco chairs", 1),
    ("Seating Sets", "seating sets", 1),
]
for label, itype, qty in patio_items:
    leaf(label, qty, "/g/furniture", "cat100240095", item_type=itype, evidence=PATIO_EV)

# ---------------- Office Furniture ----------------
group("Office Furniture")
OFFICE_EV = ("ac.cnstrc.com/browse/group_id/cat100240127 item_type facet count (Constructor.io); node total "
             "(1015) matches facet sum (1018, within 3 units); facet 'runners' (rugs, qty 2) excluded as "
             "textile/non-furniture")
leaf("Bookcases", 603, "/g/home-store/furniture-store/home-office-furniture", "cat100240127", item_type="bookcases",
     evidence=OFFICE_EV)
leaf("Desks", 167, "/g/home-store/furniture-store/home-office-furniture", "cat100240127", item_type="desks",
     evidence=OFFICE_EV)
leaf("File Cabinets", 115, "/g/home-store/furniture-store/home-office-furniture", "cat100240127", item_type="file cabinets",
     evidence=OFFICE_EV)
leaf("Office Chairs", 110, "/g/home-store/furniture-store/home-office-furniture", "cat100240127", item_type="office chairs",
     evidence=OFFICE_EV)
leaf("Standing Desks", 15, "/g/home-store/furniture-store/home-office-furniture", "cat100240127", item_type="standing desks",
     evidence=OFFICE_EV)
leaf("Accent Cabinets", 3, "/g/home-store/furniture-store/home-office-furniture", "cat100240127", item_type="accent cabinets",
     evidence=OFFICE_EV)
leaf("Printer Carts", 3, "/g/home-store/furniture-store/home-office-furniture", "cat100240127", item_type="printer carts",
     evidence=OFFICE_EV)

# ---------------- Bathroom / Entryway (standalone leaves) ----------------
leaf("Bathroom Furniture", 170, "/g/home-store/furniture-store/bathroom-furniture", "cat100240130",
     evidence=API_EV.format(id="cat100240130"))
leaf("Entryway Furniture", 382, "/g/home-store/furniture-store/entryway-furniture", "cat1003600032",
     evidence=API_EV.format(id="cat1003600032"))

notes = (
    "Reached via Chrome connector, no block encountered. robots.txt (jcpenney.com/robots.txt) has no "
    "Claude/anthropic-ai/ClaudeBot disallow -- checked first. Tree source: the Furniture department landing "
    "page (jcpenney.com/d/home-store/furniture-store) mega-menu/tile list gives the live top-level taxonomy "
    "(Mattresses, Bedroom, Living Room, Kitchen & Dining, Patio & Outdoor, More Furniture incl. Accent/"
    "Bathroom/Entryway/Office). The category-for-the-home.xml sitemap was cross-checked for coverage (union "
    "with the nav) per the mandatory sitemap-cross-check rule; it surfaced the Media & TV Storage sub-tree "
    "children. Counts: JCPenney's PLP grid is client-rendered (get_page_text/article extraction returns only "
    "footer nav, no product grid or count text), so counts came from the same Constructor.io browse API "
    "(ac.cnstrc.com/browse/group_id/<id>, public key key_xT77K5VmpiVduqnj) verified exact by the prior "
    "Home-Decor pass on this exact company. One rendered-header spot-check was still done (Sofas: page text "
    "'352 results' vs API total_num_results=357, ~1.4% lower) confirming the known stock-gated-header pattern; "
    "the in-stock rendered number (352) was used for that one row per Rule 4 priority, API totals used "
    "elsewhere since the header could not be extracted from the client-rendered grid on other pages.\n"
    "TRAP CAUGHT: navigating to a guessed id (cat100210003) under a plausible-looking Patio Furniture URL "
    "silently served the Luggage category instead (200 OK, wrong content) -- confirms id, not slug/path, "
    "determines content and that bad/guessed ids do not 404. All ids actually used were taken from real crawled "
    "links (department nav or sitemap), never guessed.\n"
    "BROKEN SUB-NAV: two levels of second-tier tile menus on this site (Patio & Outdoor Furniture's own tile "
    "strip: Conversation Sets/Chairs & Loungers/Patio Dining Furniture/Accent Furniture/Sofas & Sectionals/"
    "Umbrellas/Benches; and Accent Furniture's own tile strip) all point back to their own parent id -- the "
    "links are non-functional. Where this happened, the parent's item_type facet (from the same Constructor.io "
    "browse response) was used as the real sub-category axis instead, mirroring the exact technique the prior "
    "Home-Decor pass used for this company's Lighting department. Facet-sum-vs-total cross-checks: Patio "
    "1809 vs 1808 (off by 1), Office 1018 vs 1015 (off by 3) -- both within normal multi-tag tolerance.\n"
    "CROSS-LISTING DEDUP: 'Bar Furniture' (cat1009850002, total 682) is dominated by a 'bar stools' item_type "
    "(575) that is the same population as the dedicated 'Bar Stools' node (cat100240134, total 577) -- kept "
    "only under the dedicated Bar Stools row, Bar Furniture's other item_types (bar sets/tables/pub sets/bars/"
    "wine cabinets) recorded separately. The broad 'Accent Furniture' node (cat100240133, total 3957) was "
    "excluded entirely: its item_type facets (bar stools 575, ottomans 214, tv stands 145, etc.) are almost "
    "entirely the same populations already counted under their own dedicated nodes (Bar Stools, Ottomans & "
    "Benches, Media & TV Storage) or belong to other departments (bathroom cabinets, electric fireplaces, file "
    "cabinets, wine cabinets, portable closets) -- it is a merchandising rollup, not a clean taxonomy node, and "
    "recording it would have double-counted most of the catalogue. Its own dedicated 'Accent Tables' entry "
    "(cat11100022555, from the old sitemap) returned 0 via the API -- confirmed dead/stale, not used. Two more "
    "sitemap-only category ids ('Living Room Sets' and 'Bedroom Sets', each appearing under two different stale "
    "ids) were excluded because neither appears anywhere in the current live department nav -- treated as "
    "decommissioned legacy sitemap entries, not live categories.\n"
    "SCOPE: excluded per brief -- Mattresses/Mattress & Box Spring Sets/Mattress In A Box (bedding, not "
    "furniture; kept only 'Bed Frames & Adjustable Bases' from that section), Quick Ship Furniture (a delivery-"
    "speed filter cutting across all categories, not a product-type category), 'Fireplaces & Accessories' and "
    "'Furniture On Sale' (both broken links resolving to the bare department id, and fireplace accessories are "
    "not furniture), Umbrellas/Patio Umbrella Bases/Fire Pits/Gazebos/Beach Umbrellas/Grill Covers/Patio "
    "Coolers/Storage Boxes/Trash Cans/Chair Protectors (excluded item_types under Patio -- not furniture or are "
    "care/parts/storage), 'runners' under Office Furniture (a rug facet leak, textile)."
)

data = {
    "sr": 195,
    "company": "JCPenney Home",
    "brand_site": "jcpenney.com",
    "country": "USA",
    "site_url": "https://www.jcpenney.com/",
    "status": "ok",
    "failure_reason": None,
    "notes": notes,
    "rows": rows
}

out_path = r"C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\furniture_json_archive\f195.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

leaf_count = sum(1 for r in rows if not r["is_group"])
group_count = sum(1 for r in rows if r["is_group"])
null_qty = sum(1 for r in rows if not r["is_group"] and r["qty"] is None)
flagged = sum(1 for r in rows if r["flag"])
print("written:", out_path)
print("total rows:", len(rows), "leaf:", leaf_count, "group:", group_count, "null_qty:", null_qty, "flagged:", flagged)
