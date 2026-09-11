import json

BASE = "https://www.lampsplus.com/c/furniture/type_"

def leaf(sub, slug, qty, evidence_label=None):
    label = evidence_label or sub
    return {
        "category": "Furniture",
        "sub_category": sub,
        "qty": qty,
        "link": f"{BASE}{slug}/",
        "is_group": False,
        "evidence": f'listing header "{label} Furniture" / "{qty:,} results" on {BASE}{slug}/ (matches Type filter facet count \'{label} {qty}\' on parent /c/furniture/ listing page)',
        "flag": None,
    }

def group(sub):
    return {
        "category": "Furniture",
        "sub_category": sub,
        "qty": None,
        "link": None,
        "is_group": True,
        "evidence": None,
        "flag": None,
    }

def flagged(sub, note):
    return {
        "category": "Furniture",
        "sub_category": sub,
        "qty": None,
        "link": None,
        "is_group": False,
        "evidence": None,
        "flag": f"MANUAL REVIEW: {note}",
    }

rows = []

# Seating group (confirmed via mega-menu: Furniture > Seating)
rows.append(group("Seating"))
rows.append(leaf("Occasional Chairs", "occasional-chairs", 282))
rows.append(leaf("Barstools", "barstools", 535))
rows.append(leaf("Sofas", "sofas", 82))

# Tables group (confirmed via mega-menu: Furniture > Tables)
rows.append(group("Tables"))
rows.append(leaf("Accent Tables", "accent-tables", 1042))
rows.append(leaf("Coffee Tables", "coffee-tables", 248))
rows.append(leaf("Sofa - Console Tables", "sofa-@-console-tables", 217))
rows.append(leaf("Dining Tables", "dining-tables", 110))

# Cabinets & Storage group (confirmed via mega-menu: Furniture > Cabinets and Chests, page h1 "Cabinets & Storage")
rows.append(group("Cabinets & Storage"))
rows.append(leaf("Nightstands", "nightstands", 310))
rows.append(leaf("Bathroom Vanities", "bathroom-vanities", 291))
rows.append(leaf("Chests", "chests", 225))

# Beds group (confirmed via category sitemap: /c/beds/, h1 "Beds", 215 results umbrella)
rows.append(group("Beds"))
rows.append(leaf("Complete Beds", "complete-beds", 149))
rows.append(leaf("Platform", "platform", 67))
rows.append(leaf("Headboards", "headboards", 36))
rows.append(leaf("Canopy", "canopy", 3))
rows.append(leaf("Sofa Beds", "sofa-beds", 1))

# Flat leaves directly under Furniture (found only via the Type facet on /c/furniture/,
# not shown in any confirmed nav parent, so no grouping row invented for them)
flat = [
    ("End Tables", "end-tables", 568),
    ("Dining Chairs", "dining-chairs", 398),
    ("Office Chairs", "office-chairs", 164),
    ("Ottomans", "ottomans", 158),
    ("Benches", "benches", 135),
    ("Buffets", "buffets", 132),
    ("Entertainment Centers", "entertainment-centers", 116),
    ("Dining Sets", "dining-sets", 110),
    ("Dressers", "dressers", 103),
    ("Desks", "desks", 84),
    ("Recliners", "recliners", 59),
    ("Room Dividers", "room-dividers", 50),
    ("Bar Carts", "bar-carts", 34),
    ("Pedestal Tables", "pedestal-tables", 34),
    ("Loveseats", "loveseats", 32),
    ("Hall Trees", "hall-trees", 28),
    ("Armoires", "armoires", 27),
    ("Club Chairs", "club-chairs", 23),
    ("China Cabinets", "china-cabinets", 19),
    ("Pub Tables", "pub-tables", 18),
    ("Sectionals", "sectionals", 18),
    ("Coat Racks", "coat-racks", 14),
    ("Kitchen Storage", "kitchen-storage", 14),
    ("Kitchen Island - Carts", "kitchen-island-@-carts", 12),
    ("Parsons Chairs", "parsons-chairs", 11),
    ("Kitchen Islands", "kitchen-islands", 10),
    ("Bar - Wine Cabinets", "bar-@-wine-cabinets", 9),
    ("Gathering Tables", "gathering-tables", 9),
    ("Bistro Tables", "bistro-tables", 8),
    ("File Cabinets", "file-cabinets", 8),
    ("Outdoor", "outdoor", 8),
    ("Chaises", "chaises", 6),
    ("Commercial", "commercial", 6),
    ("Bathroom Cabinets", "bathroom-cabinets", 4),
    ("Plant Stands", "plant-stands", 4),
    ("Rocking Chairs", "rocking-chairs", 3),
    ("Vanity Tables", "vanity-tables", 3),
    ("Game Tables", "game-tables", 1),
    ("Garden Stools", "garden-stools", 1),
    ("Settees", "settees", 1),
    ("Slipper Chairs", "slipper-chairs", 1),
]
for sub, slug, qty in flat:
    rows.append(leaf(sub, slug, qty))

# Flagged rows - Type facet exists with a real count, but the canonical slug could not
# be resolved to a matching page within the browser-call budget for this session (bad-slug
# trap: tried slug served the PARENT listing or an unrelated facet, not a 404)
rows.append(flagged(
    "Curio Cabinets",
    "Type facet on /c/furniture/ shows 'Curio Cabinets 6'. Tried "
    "/c/furniture/type_curio-cabinets/ -> served the PARENT 'Home Furniture' listing "
    "(8,019 results, wrong node) and /c/cabinets-and-storage/type_curio-cabinets/ -> "
    "served the PARENT 'Cabinets & Storage' listing (1,544 results, wrong node). "
    "Classic bad-slug-serves-parent trap; true slug unresolved."
))
rows.append(flagged(
    "Sofa Tables",
    "Type facet on /c/furniture/ shows 'Sofa Tables 3' as a DISTINCT value from "
    "'Sofa - Console Tables 217'. Tried /c/furniture/type_sofa-tables/ -> resolved to "
    "the 'Sofa - Console Tables' page (217 results), not the 3-count node. True slug "
    "for the 3-product 'Sofa Tables' facet unresolved."
))
rows.append(flagged(
    "Upholstered",
    "Type facet on /c/furniture/ shows 'Upholstered 16'. Tried "
    "/c/furniture/type_upholstered/ -> resolved to an unrelated 'Upholstered Furniture' "
    "page with 1,357 results (a different, broader facet scope, not the 16-count Type "
    "value) and /c/furniture/type_upholstered-beds/ -> 404. True slug unresolved."
))

out = {
    "sr": 205,
    "company": "Lamps Plus",
    "brand_site": "lampsplus.com",
    "country": "USA",
    "site_url": "https://www.lampsplus.com/",
    "status": "ok",
    "failure_reason": None,
    "notes": (
        "ACCESS: robots.txt (fetched in-tab) has no Claude-specific disallow (generic "
        "User-agent:* plus a Pinterestbot group only) so a full crawl was in scope. The prior "
        "Home-Decor pass on this same site hit a hard Akamai Bot Manager block via curl_cffi "
        "after ~2 requests; that access route is forbidden here anyway. Loading the site through "
        "the Claude-in-Chrome browser worked cleanly end to end -- homepage, category pages and "
        "~65 same-origin fetch() calls from the page context all returned normal 200s with no "
        "challenge encountered, confirming (again) that a real browser session avoids the bot "
        "wall entirely on this domain. "
        "TREE SOURCE: the top nav has a 'Furniture' item (https://www.lampsplus.com/c/furniture/, "
        "'Home Furniture', 8,019 results). Its mega-menu explicitly lists three parent groups -- "
        "Seating (Accent/Occasional Chairs, Barstools, Sofas), Tables (Accent, Coffee, Console, "
        "Dining Tables) and Cabinets and Chests / 'Cabinets & Storage' (Nightstands, Bathroom "
        "Vanities, Chests) -- plus 'Hardware' (excluded: furniture knobs/pulls, not furniture "
        "itself). Per the brief's Trap #1 (mega-menu under-reports the tree), the category "
        "sitemap (sitemap-category.xml) was also cross-checked and surfaced a 4th real "
        "department, /c/beds/ ('Beds', 215 results), that the compact mega-menu never displayed "
        "at all. Beyond that, the 'Furniture' landing page's own left-rail 'Type' filter facet "
        "(expanded in-browser) turned out to hold a much larger flat list of ~68 product-type "
        "values with exact per-value counts -- this is the same trap again at a finer grain: the "
        "curated mega-menu shows only 10 of these as 'featured' links, but the facet panel is "
        "the site's true, complete Type taxonomy. Every value was resolved to a canonical "
        "listing page of the shape https://www.lampsplus.com/c/furniture/type_<slug>/ (special "
        "characters '&' encode as '@' in the slug, matching the site's own convention seen on "
        "/c/tables/type_sofa-@-console-tables/ etc.) and each page's own rendered listing header "
        "('<Label> Furniture' / 'N results') was read directly and cross-checked against the "
        "Type facet's own count on the /c/furniture/ root -- every resolved node matched exactly "
        "(sanity check per Rule 4, corroborating the header against an independent site-reported "
        "source; no drift found). "
        "EXCLUSIONS: 'Electric Fireplaces' (22, appliance), 'Slipcovers' (11, furniture "
        "care/cover), 'Storage Bins' (8, standalone storage goods per the brief's storage-vs-"
        "furniture line), 'Mattress' (1, bedding) and 'Fireplace Screens' (2, fireplace "
        "accessory) were all excluded as non-furniture per section 1. 'Chairs' (853, its own "
        "Type value distinct from the more specific chair subtypes) was also excluded as a row: "
        "opening its listing showed a Barstool product mixed into the results (a "
        "'Roark...Swivel Barstool' appeared under /c/furniture/type_chairs/, which also has its "
        "own dedicated 'Barstools' facet at 535), and the sum of the specific chair subtypes "
        "(Occasional 282 + Dining 398 + Office 164 + Club 23 + Parsons 11 + others) tracks close "
        "to 853 -- strong evidence 'Chairs' is a fragmentary catch-all that cross-tags into the "
        "more specific buckets rather than a clean sibling category, so it was dropped rather "
        "than risk double-counting the same physical products under two rows. "
        "AMBIGUOUS/UNRESOLVED: three Type values could not be pinned to a working canonical URL "
        "within the session and are flagged MANUAL REVIEW with qty null rather than guessed -- "
        "'Curio Cabinets' (6, slug guess served the parent listing both under /c/furniture/ and "
        "/c/cabinets-and-storage/, the classic bad-slug-serves-parent trap), 'Sofa Tables' (3, "
        "slug guess resolved instead to the unrelated 'Sofa - Console Tables' node at 217), and "
        "'Upholstered' (16, slug guess resolved to an unrelated 1,357-result page, and an "
        "'upholstered-beds' guess 404'd). "
        "GROUPING: only the four departments the site itself demonstrably groups (Seating, "
        "Tables, Cabinets & Storage via the mega-menu; Beds via the category sitemap) are "
        "emitted as grouping rows with their confirmed children nested beneath. The remaining "
        "~40 Type values have no site-confirmed parent grouping (they only surfaced via the "
        "flat Type facet, not via any nav path), so they are emitted as flat leaf rows directly "
        "under Furniture rather than invented into artificial sub-groups. "
        "SCOPE: no products were double-verified beyond the header-vs-facet-count cross-check; "
        "given ~55 leaves individually confirmed with a 100% match rate against the facet panel "
        "and zero silent-parent-redirect surprises outside the three flagged nodes, no further "
        "sampling was judged necessary per the efficiency rules (repeat verification of an "
        "established fact is wasteful, not additional accuracy)."
    ),
    "rows": rows,
}

path = r"C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\furniture_json_archive\f205.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

leaf_rows = [r for r in rows if not r["is_group"]]
group_rows = [r for r in rows if r["is_group"]]
null_qty = [r for r in leaf_rows if r["qty"] is None]
flagged_rows = [r for r in leaf_rows if r["flag"]]
print("status:", out["status"])
print("total rows:", len(rows))
print("leaf rows:", len(leaf_rows))
print("group rows:", len(group_rows))
print("null qty leaf rows:", len(null_qty))
print("flagged rows:", len(flagged_rows))
