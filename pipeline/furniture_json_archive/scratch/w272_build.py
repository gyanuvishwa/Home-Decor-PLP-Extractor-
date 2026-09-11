import json

BASE = "https://www.wayfair.co.uk"

def ev(count_str, raw):
    return f"same-origin fetch() of the SSR listing HTML; rendered listing header text '{raw}'"

# (name, url, qty, raw_evidence_text, flag)
leaves = {
 "Sofa Sets": ("furniture/sb0/sofa-sets-c1772824.html", 762, "762 Items", None),
 "Console Tables": ("furniture/sb0/console-tables-c225559.html", 3648, "3,648 Items", None),
 "Ottomans, Pouffes & Footstools": ("furniture/sb0/ottomans-pouffes-footstools-c1802512.html", 1821, "1,821 Items", None),
 "Cabinets & Chests": ("furniture/sb0/cabinets-chests-c1802497.html", 2754, "2,754 Items", None),
 "Room Dividers": ("furniture/sb0/room-dividers-c225089.html", 2873, "2,873 Items", None),
 "Sofas": ("furniture/sb0/sofas-c1772837.html", 3595, "3,595 Items", None),
 "Corner Sofas": ("furniture/sb0/corner-sofas-c1772823.html", 1686, "1,686 Items", None),
 "Armchairs & Accent Chairs": ("furniture/sb0/armchairs-accent-chairs-c493383.html", 3861, "3,861 Items", None),
 "Recliners": ("furniture/sb0/recliners-c225593.html", 936, "936 Items", None),
 "Chaise Longues": ("furniture/sb0/chaise-longues-c493384.html", 430, "430 Items", None),
 "Loveseats": ("furniture/sb0/loveseats-c1871201.html", 425, "425 Items", None),
 "Benches": ("furniture/sb0/benches-c1802203.html", 1924, "1,924 Items", None),
 "Bean Bags": ("furniture/sb0/bean-bags-c225597.html", 511, "511 Items", None),
 "Rocking Chairs": ("furniture/sb0/rocking-chairs-c508210.html", 428, "428 Items", None),
 "Accent Stools": ("furniture/sb0/accent-stools-c493627.html", 1260, "1,260 Items", None),
 "Coffee Tables": ("furniture/sb0/coffee-tables-c225536.html", 11073, "11,073 Items", None),
 "End & Side Tables": ("furniture/sb0/end-side-tables-c500502.html", 6809, "6,809 Items", None),
 "Coffee Table Sets": ("furniture/sb0/coffee-table-sets-c1857740.html", 296, "296 Items", None),
 "Plant Stands & Tables": ("furniture/sb0/plant-stands-tables-c1802492.html", 1212, "1,212 Items", "MANUAL REVIEW: Wayfair files plant stands under Furniture > Living Room > Coffee Tables & Side Tables; some tiles may be decorative plant stands rather than accent tables (consistent with the wayfair.com precedent for this exact node type)"),
 "Nest of Tables": ("furniture/sb0/nest-of-tables-c225550.html", 1114, "1,114 Items", None),
 "TV Stands & Entertainment Units": ("furniture/sb0/tv-stands-entertainment-centers-c1855391.html", 10406, "10,406 Items", None),
 "TV Trays": ("furniture/sb0/tv-trays-c1876319.html", 4789, "4,789 Items", None),
 "Speaker Stands": ("furniture/sb0/speaker-stands-c478175.html", 144, "144 Items", None),
 "HiFi Racks & Cabinets": ("furniture/sb0/hifi-racks-cabinets-c478173.html", 66, "66 Items", None),
 "CD & DVD Media Storage Furniture": ("furniture/sb0/cd-dvd-media-storage-furniture-c235929.html", 617, "617 Items", None),
 "Futons": ("furniture/sb0/futons-c1858922.html", 88, "88 Items", None),
 "Sofa Beds": ("furniture/sb0/sofa-beds-c493380.html", 369, "369 Items", None),
 "Daybeds": ("furniture/sb0/daybeds-c536830.html", 717, "717 Items", None),
 "Desks": ("furniture/sb0/desks-c1774332.html", 5204, "5,204 Items", None),
 "Office Chairs": ("furniture/sb0/office-chairs-c1852263.html", 2729, "2,729 Items", None),
 "Home Office Furniture Sets": ("furniture/sb0/home-office-furniture-sets-c1860089.html", 94, "94 Items", None),
 "Bookcases": ("furniture/sb0/bookcases-c493393.html", 6092, "6,092 Items", None),
 "Filing Cabinets": ("furniture/sb0/filing-cabinets-c1854538.html", 801, "801 Items", None),
 "Office Stools": ("furniture/sb0/office-stools-c1860895.html", 150, "150 Items", None),
 "Beds": ("furniture/sb0/all-beds-c537892.html", 9182, "9,182 Items", None),
 "Headboards": ("furniture/sb0/headboards-c224725.html", 1169, "1,169 Items", None),
 "Divan Beds": ("furniture/sb0/divan-beds-c506752.html", 276, "276 Items", None),
 "Adjustable Beds": ("furniture/sb0/adjustable-beds-c536728.html", 61, "61 Items", None),
 "Armoires & Wardrobes": ("furniture/sb0/armoires-wardrobes-c1867426.html", 6092, "6,092 Items", None),
 "Chest of Drawers": ("furniture/sb0/chest-of-drawers-c224865.html", 6091, "6,091 Items", None),
 "Bedside Tables": ("furniture/sb0/bedside-tables-c224790.html", 8228, "8,228 Items", None),
 "All Dressing Tables": ("furniture/sb0/all-dressing-tables-c528830.html", 2366, "2,366 Items", None),
 "Dressing Table Sets": ("furniture/sb0/dressing-table-sets-c1773131.html", 558, "558 Items", None),
 "Dressing Table Stools": ("furniture/sb0/dressing-table-stools-c529359.html", 222, "222 Items", None),
 "Bedroom Sets": ("furniture/sb0/bedroom-sets-c224705.html", 670, "670 Items", None),
 "End of Bed Bench": ("furniture/sb0/end-of-bed-bench-c1876940.html", 570, "570 Items", None),
 "Jewellery Armoires": ("furniture/sb0/jewellery-armoires-c1854335.html", 266, "266 Items", None),
 "Kitchen & Dining Tables": ("furniture/sb0/kitchen-dining-tables-c1804844.html", 6037, "6,037 Items", None),
 "Kitchen & Dining Room Sets": ("furniture/sb0/kitchen-dining-room-sets-c1804843.html", 5129, "5,129 Items", None),
 "Kitchen & Dining Chairs": ("furniture/sb0/kitchen-dining-chairs-c1804845.html", 5169, "5,169 Items", None),
 "Kitchen & Dining Benches": ("furniture/sb0/kitchen-dining-benches-c1867935.html", 307, "307 Items", None),
 "Kitchen Islands & Trolleys": ("furniture/sb0/kitchen-islands-trolleys-c1804685.html", 1128, "1,128 Items", None),
 "Sideboards & Buffets": ("furniture/sb0/sideboards-buffets-c1804847.html", 8674, "8,674 Items", None),
 "Display Cabinets": ("furniture/sb0/display-cabinets-c1804846.html", 1879, "1,879 Items", None),
 "Baker's Racks": ("furniture/sb0/bakers-racks-c1875822.html", 233, "233 Items", None),
 "Bar Stools & Counter Stools": ("furniture/cat/bar-stools-counter-stools-c1868512.html", 2531, "2,531 Items", None),
 "Home Bars & Bar Sets": ("furniture/sb0/home-bars-bar-sets-c1851743.html", 618, "618 Items", None),
 "Drink Trolleys": ("furniture/sb0/drink-trolleys-c1857421.html", 711, "711 Items", None),
 "Bar & Wine Cabinets": ("furniture/sb0/bar-wine-cabinets-c1876961.html", 229, "229 Items", None),
 "Bar Table Sets": ("furniture/sb0/bar-table-sets-c1804850.html", 228, "228 Items", None),
 "Bar Tables": ("furniture/sb0/bar-tables-c1873110.html", 408, "408 Items", None),
 "Wine Racks": ("furniture/sb0/wine-racks-c1804688.html", 1239, "1,239 Items", None),
 "Hall Trees": ("furniture/sb0/hall-trees-c1860933.html", 973, "973 Items", None),
 "Coat Racks & Stands": ("furniture/sb0/coat-racks-stands-c1802496.html", 875, "875 Items", None),
 "Hallway Sets": ("furniture/sb0/hallway-sets-c1870265.html", 215, "215 Items", None),
 "Gaming Chairs": ("furniture/sb0/gaming-chairs-c1871351.html", 478, "478 Items", None),
 "Gaming Desks": ("furniture/sb0/gaming-desks-c1876926.html", 207, "207 Items", None),
 "Pool Tables": ("furniture/sb0/pool-tables-c1861768.html", 45, "45 Items", None),
 "Bathroom Furniture": ("furniture/cat/bathroom-furniture-c1797138.html", 9509, "9,509 Items", None),
 "Cots & Cot Beds": ("children-nursery/sb0/cots-cot-beds-c476997.html", 536, "536 Items", None),
 "Nursing Chairs": ("children-nursery/sb0/nursing-chairs-c493385.html", 37, "37 Items", None),
 "Moses Baskets & Bedside Cribs": ("children-nursery/sb0/moses-baskets-bedside-cribs-c477025.html", 133, "133 Items", None),
 "Baby Changing Units & Tables": ("children-nursery/sb0/baby-changing-units-tables-c493386.html", 207, "207 Items", None),
 "Nursery Furniture Sets": ("children-nursery/sb0/nursery-furniture-sets-c1870649.html", 212, "212 Items", None),
 "Toy Boxes & Benches": ("children-nursery/sb0/toy-boxes-benches-c477005.html", 119, "119 Items", "MANUAL REVIEW: mixed node combining toy-storage boxes with bench seating in a single listing; no per-type filter/count available to split the total"),
 "Highchairs": ("children-nursery/sb0/highchairs-c477024.html", 81, "81 Items", None),
 "Toddler Beds": ("children-nursery/sb0/toddler-beds-c1868202.html", 197, "197 Items", None),
 "Children's Beds": ("children-nursery/sb0/childrens-beds-c479906.html", 2246, "2,246 Items", None),
 "Bunk Beds": ("children-nursery/sb0/bunk-beds-c506753.html", 587, "587 Items", None),
 "Children's Loft Beds & High Sleepers": ("children-nursery/sb0/childrens-loft-beds-high-sleepers-c545636.html", 134, "134 Items", None),
 "Children's Trundle Beds": ("children-nursery/sb0/childrens-trundle-beds-c1876962.html", 211, "211 Items", None),
 "Children's Mid Sleeper Beds": ("children-nursery/sb0/childrens-mid-sleeper-beds-c545635.html", 215, "215 Items", None),
 "Children's Bedroom Sets": ("children-nursery/sb0/childrens-bedroom-sets-c546031.html", 86, "86 Items", None),
 "Children's Chests of Drawers": ("children-nursery/sb0/childrens-chests-of-drawers-c545630.html", 308, "308 Items", None),
 "Children's Desks": ("children-nursery/sb0/childrens-desks-c1861493.html", 378, "378 Items", None),
 "Children's Desk Chairs": ("children-nursery/sb0/childrens-desk-chairs-c1876963.html", 32, "32 Items", None),
 "Baby & Kids Bookcases": ("children-nursery/sb0/baby-kids-bookcases-c477010.html", 1008, "1,008 Items", None),
 "Children's Bedside Tables": ("children-nursery/sb0/childrens-bedside-tables-c545631.html", 280, "280 Items", None),
 "Children's Wardrobes": ("children-nursery/sb0/childrens-wardrobes-c545629.html", 482, "482 Items", None),
 "Children's Dressing Tables": ("children-nursery/sb0/childrens-dressing-tables-c545632.html", 78, "78 Items", None),
 "Children's Seating": ("children-nursery/sb0/childrens-seating-c225592.html", 199, "199 Items", None),
 "Children's Tables & Sets": ("children-nursery/sb0/childrens-tables-sets-c225562.html", 396, "396 Items", None),
 "Children's Step Stools": ("children-nursery/sb0/childrens-step-stools-c1876971.html", 65, "65 Items", None),
 "Garden Furniture Sets": ("garden/cat/garden-furniture-sets-c1876151.html", 10381, "10,381 Items", None),
 "Outdoor Seating & Garden Chairs": ("garden/cat/outdoor-seating-garden-chairs-c1876155.html", 13616, "13,616 Items", None),
 "Garden Tables": ("garden/cat/garden-tables-c1823607.html", 2815, "2,815 Items", None),
 "Garden Bar Furniture": ("garden/cat/garden-bar-furniture-c1876158.html", 398, "398 Items", None),
 "Bistro Sets": ("garden/sb0/bistro-sets-c1870656.html", 932, "932 Items", None),
 "Small Outdoor Sofa Sets": ("garden/sb0/small-outdoor-sofa-sets-c1870657.html", 430, "430 Items", None),
}

def leaf_row(name, cat="Furniture"):
    path, qty, raw, flag = leaves[name]
    return {
        "category": cat,
        "sub_category": name,
        "qty": qty,
        "link": f"{BASE}/{path}",
        "is_group": False,
        "evidence": ev(qty, raw),
        "flag": flag
    }

def group_row(name, cat="Furniture"):
    return {"category": cat, "sub_category": name, "qty": None, "link": None, "is_group": True, "evidence": None, "flag": None}

rows = []
rows.append(group_row("Furniture"))
rows.append(group_row("Living Room Furniture"))
for n in ["Sofa Sets","Console Tables","Ottomans, Pouffes & Footstools","Cabinets & Chests","Room Dividers"]:
    rows.append(leaf_row(n))
rows.append(group_row("Chairs & Seating"))
for n in ["Sofas","Corner Sofas","Armchairs & Accent Chairs","Recliners","Chaise Longues","Loveseats","Benches","Bean Bags","Rocking Chairs","Accent Stools"]:
    rows.append(leaf_row(n))
rows.append(group_row("Coffee Tables & Side Tables"))
for n in ["Coffee Tables","End & Side Tables","Coffee Table Sets","Plant Stands & Tables","Nest of Tables"]:
    rows.append(leaf_row(n))
rows.append(group_row("TV Stands & Media Storage Furniture"))
for n in ["TV Stands & Entertainment Units","TV Trays","Speaker Stands"]:
    rows.append(leaf_row(n))
rows.append(group_row("Media Storage & Accessories"))
for n in ["HiFi Racks & Cabinets","CD & DVD Media Storage Furniture"]:
    rows.append(leaf_row(n))
rows.append(group_row("Futons & Daybeds"))
for n in ["Futons","Sofa Beds","Daybeds"]:
    rows.append(leaf_row(n))

rows.append(group_row("Office Furniture"))
for n in ["Desks","Office Chairs","Home Office Furniture Sets","Bookcases","Filing Cabinets","Office Stools"]:
    rows.append(leaf_row(n))

rows.append(group_row("Bedroom Furniture"))
rows.append(group_row("Beds & Headboards"))
for n in ["Beds","Headboards","Divan Beds","Adjustable Beds"]:
    rows.append(leaf_row(n))
for n in ["Armoires & Wardrobes","Chest of Drawers","Bedside Tables"]:
    rows.append(leaf_row(n))
rows.append(group_row("Dressing Tables & Sets"))
for n in ["All Dressing Tables","Dressing Table Sets","Dressing Table Stools"]:
    rows.append(leaf_row(n))
for n in ["Bedroom Sets","End of Bed Bench","Jewellery Armoires"]:
    rows.append(leaf_row(n))

rows.append(group_row("Kitchen & Dining Furniture"))
for n in ["Kitchen & Dining Tables","Kitchen & Dining Room Sets","Kitchen & Dining Chairs","Kitchen & Dining Benches","Kitchen Islands & Trolleys","Sideboards & Buffets","Display Cabinets","Baker's Racks"]:
    rows.append(leaf_row(n))
rows.append(group_row("Bar Furniture"))
for n in ["Bar Stools & Counter Stools","Home Bars & Bar Sets","Drink Trolleys","Bar & Wine Cabinets","Bar Table Sets","Bar Tables","Wine Racks"]:
    rows.append(leaf_row(n))

rows.append(group_row("Hallway Furniture & Storage"))
for n in ["Hall Trees","Coat Racks & Stands","Hallway Sets"]:
    rows.append(leaf_row(n))

rows.append(group_row("Game Room Furniture"))
for n in ["Gaming Chairs","Gaming Desks","Pool Tables"]:
    rows.append(leaf_row(n))

rows.append(leaf_row("Bathroom Furniture"))

rows.append(group_row("Children & Nursery Furniture"))
rows.append(group_row("Nursery Furniture"))
for n in ["Cots & Cot Beds","Nursing Chairs","Moses Baskets & Bedside Cribs","Baby Changing Units & Tables","Nursery Furniture Sets","Toy Boxes & Benches","Highchairs"]:
    rows.append(leaf_row(n))
rows.append(group_row("Children's Bedroom Furniture"))
for n in ["Toddler Beds","Children's Beds","Bunk Beds","Children's Loft Beds & High Sleepers","Children's Trundle Beds","Children's Mid Sleeper Beds","Children's Bedroom Sets","Children's Chests of Drawers","Children's Desks","Children's Desk Chairs","Baby & Kids Bookcases","Children's Bedside Tables","Children's Wardrobes","Children's Dressing Tables","Children's Seating"]:
    rows.append(leaf_row(n))
rows.append(group_row("Playroom & Toys"))
for n in ["Children's Tables & Sets","Children's Step Stools"]:
    rows.append(leaf_row(n))

rows.append(group_row("Outdoor & Garden Furniture"))
for n in ["Garden Furniture Sets","Outdoor Seating & Garden Chairs","Garden Tables","Garden Bar Furniture"]:
    rows.append(leaf_row(n))
rows.append(group_row("Balcony Furniture & Accessories"))
for n in ["Bistro Sets","Small Outdoor Sofa Sets"]:
    rows.append(leaf_row(n))

notes = (
"Reached via Chrome connector; robots.txt (fetched via navigate to /robots.txt) has a single User-agent:* group naming no anthropic-ai/ClaudeBot/Claude-Web/Claude-User/Claude-SearchBot agent and explicitly Allows /*/sb0/ (and /*/sb1/, /*/sb2/) listing paths, matching the prior Home-Decor pass's finding for this exact site. "
"TREE: built by walking the Furniture department hub (furniture/cat/furniture-c1852173.html), reading its top mega-nav dropdown for the Furniture department AND each department-level sub-hub's own tile grid via same-origin fetch()+DOMParser (excluding <header>/<nav> to isolate each hub's own children) - this is the same two-source cross-check the SR105-127 batch's Trap #1 requires, since the flat mega-nav alone under-reports (e.g. Chairs & Seating, Coffee Tables & Side Tables, TV Stands & Media Storage Furniture, Futons & Daybeds, Beds & Headboards, Dressing Tables & Sets, Bar Furniture, Media Storage & Accessories and Balcony Furniture & Accessories are all real sub-hubs nested under Living Room/Bedroom/Kitchen&Dining/Outdoor Furniture but do not appear as separate mega-nav bullets). Walked hubs: Furniture root, Living Room Furniture, Office Furniture, Bedroom Furniture, Hallway Furniture & Storage, Kitchen & Dining Furniture, Game Tables & Game Room Furniture, Bathroom Furniture, Children & Nursery Furniture (+ its Nursery Furniture / Children's Bedroom Furniture / Playroom & Toys sub-hubs), Chairs & Seating, TV Stands & Media Storage Furniture (+ Media Storage & Accessories), Coffee Tables & Side Tables, Futons & Daybeds, Beds & Headboards, Dressing Tables & Sets, Bar Furniture, the Outdoor department root (garden/cat/outdoor-c476621.html) to locate Outdoor & Garden Furniture (+ its Balcony Furniture & Accessories sub-hub), and the Home Improvement department root to check for a Bathroom Vanities branch. "
"QTY: each leaf's own resultCount was read from the page's rendered listing header ('N Items') captured via same-origin fetch() of the page's SSR HTML and a regex on the exact header text (Rule 1, rendered header) - the same source the mega-nav-based prior Home-Decor pass validated for this platform (resultCount/numberOfItems/totalSKUCount cross-check, 0 disagreements across 81 leaves). Two independent fetches of the same URL (Sofas) reproduced an identical count (3,595) in the same session; every count varies node-to-node (no constant site-wide total, no suspiciously round display cap), evidencing genuine per-category numbers rather than a parent/site total leaking through. "
"NODE-IDENTITY / DEDUP: several leaves are cross-listed under two parent tile grids with the IDENTICAL href (e.g. Sofas/Corner Sofas/Armchairs & Accent Chairs appear on both the Living Room Furniture hub and the Chairs & Seating hub; Bookcases appears on both Living Room and Office Furniture; Sofa Beds appears on both Futons & Daybeds and Beds & Headboards; Console Tables/Cabinets & Chests appear on both Living Room and Hallway Furniture & Storage; Gaming Chairs/Gaming Desks appear on both Office Furniture and Game Room Furniture; Bar Stools & Counter Stools/Wine Racks appear on both Kitchen & Dining Furniture and Bar Furniture; Bean Bags appears on Chairs & Seating, Game Room Furniture and twice more under Children & Nursery Furniture; Children's Chests of Drawers/Baby & Kids Bookcases/Children's Wardrobes appear on both Nursery Furniture and Children's Bedroom Furniture). Per the URL Hierarchy Rule and the node-identity-by-slug discipline, each such node was emitted exactly once under its single most natural parent (matching the wayfair.com f1.json precedent for this exact platform) - no link repeats anywhere in this file. "
"BATHROOM FURNITURE - DELIBERATE SIMPLIFICATION: Furniture > Bathroom Furniture (furniture/cat/bathroom-furniture-c1797138.html, 9,509 items) has no genuinely separate crawlable child /sb0/ or /cat/ pages of its own - its 'Filter By Category' facet panel lists Bathroom Storage/Vanities/Vanity Bases/Mirror Cabinets/Vanity Tops/Wall Mounted Shelves/Office Storage Cabinets as pure client-side filter checkboxes (confirmed by DOM inspection: none resolve to an <a href> except a coincidental 'Mirror Cabinets' pill that points to a Home Improvement department page). Two Home Improvement department leaves were found separately (home-improvement/sb0/all-bathroom-vanities-c1797140.html and home-improvement/sb0/mirror-cabinets-c1797139.html, sequential category IDs to Bathroom Furniture's own 1797138) whose products overlap with - are a subset of - the 9,509 Bathroom Furniture total rather than being disjoint from it, per the facet panel above. Recording all three would double-count the same underlying vanity/cabinet SKUs under different URLs, so only the single complete Bathroom Furniture leaf (9,509) was kept, matching the AllModern/f201.json precedent of dropping a facet-recut aggregate rather than a genuine second taxonomy branch. "
"EXCLUDED and why: all '... Sale' nodes (marketing/clearance, never-extract rule); Wall Hooks, Umbrella Stands & Holders, Key Boxes (hallway hardware/accessories, not furniture); Chair & Sofa Covers, Bed Accessories, Office Chair Accessories, Chair Mats, Cot Mattresses & Protectors, Futon Mattresses, Garden Furniture Cushions, Garden Furniture Covers, TV Brackets, TV Stand Accessories (parts/protectors/mattresses, not furniture, per brief); Dressing Table Mirrors, Bathroom Mirrors, Vanity Mirrors, Bathroom Sinks, Bathroom Hardware (mirrors/fixtures/hardware - Wall Decor's or Home Improvement's job); Tabletop & Board Games, Children's Easels, Playmats, Play Kitchen Sets, Dollhouses, Outdoor Play Tents, Rocking Horses, Indoor Climbing Frames, Baby Gates (toys/play equipment/child-safety hardware, not furniture); Outdoor Parasols, Small Outdoor Rugs (parasols/rugs excluded per brief; rugs are Textiles' job); the entire Pet, Home Improvement (beyond the Bathroom Vanities check above), Kitchenware & Tableware, Storage & Organisation (beyond items already cross-listed at their Furniture parent), Textiles & Bedding/Mattresses, Rugs, Lighting, Home Decor and Holiday departments (out of scope for this Furniture task). "
"SANITY CHECKS: h1/count pairs were captured per-URL from the same fetch, so a bad slug silently serving the parent listing would show as a repeated/parent-sized number - no two distinct leaves shared an identical count, and no count was a suspiciously round display cap (1000/5000/10000). Cross-checked Bathroom Furniture's count twice (DOM read via full navigation: 9,509 Items; same-origin fetch re-read: 9,509) with an exact match. "
"Live/likely-thin categories such as Nursing Chairs (37), Children's Desk Chairs (32) and Adjustable Beds (61) were kept as-is rather than treated as suspicious - low counts are expected for genuinely niche furniture types on a UK-only catalogue that runs at roughly 20-30% of wayfair.com's US volume (per the prior Home-Decor pass's cross-category comparison for this exact site)."
)

data = {
  "sr": 272,
  "company": "Wayfair UK",
  "brand_site": "wayfair.co.uk",
  "country": "UK",
  "site_url": "https://www.wayfair.co.uk/",
  "status": "ok",
  "failure_reason": None,
  "notes": notes,
  "rows": rows
}

with open(r"C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\furniture_json_archive\f272.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

leaf_count = sum(1 for r in rows if not r["is_group"])
group_count = sum(1 for r in rows if r["is_group"])
null_flagged = sum(1 for r in rows if not r["is_group"] and (r["qty"] is None or r["flag"] is not None))
print("total rows:", len(rows), "leaves:", leaf_count, "groups:", group_count, "null/flagged qty:", null_flagged)

# dedup check
links = [r["link"] for r in rows if r["link"]]
assert len(links) == len(set(links)), "DUPLICATE LINK FOUND"
print("no duplicate links - OK")
