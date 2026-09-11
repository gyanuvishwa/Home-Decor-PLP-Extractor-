import json

CAP_FLAG = ("MANUAL REVIEW: listing paginates to Walmart's hard display cap (25 pages / ~1000 items); "
            "the site's own totalItemCount field drifted between reads at this scale (e.g. Sofas & Couches "
            "read 40298 then 40301 within a minute) and is not exhaustion-checkable - treated as unreliable "
            "per this project's established Walmart convention (see prior Home-Decor pass notes/194.md).")

def leaf(name, url, t, m):
    capped = (m == 25)
    if capped:
        return {
            "category": "Furniture",
            "sub_category": name,
            "qty": None,
            "link": url,
            "is_group": False,
            "evidence": None,
            "flag": CAP_FLAG
        }
    else:
        return {
            "category": "Furniture",
            "sub_category": name,
            "qty": t,
            "link": url,
            "is_group": False,
            "evidence": "page's own totalItemCount field = {}, maxPage = {} (under the 25-page/1000-item cap, so pagination reaches the true end)".format(t, m),
            "flag": None
        }

def group(name):
    return {
        "category": "Furniture",
        "sub_category": name,
        "qty": None,
        "link": None,
        "is_group": True,
        "evidence": None,
        "flag": None
    }

rows = []

rows.append(group("Living Room"))
living_room = [
    ("Sofas & Couches","https://www.walmart.com/browse/home/sofas-couches/4044_103150_4038_1431634",40301,25),
    ("TV Stands","https://www.walmart.com/browse/home/tv-stands/4044_103150_635499_133114",26119,25),
    ("Coffee Tables","https://www.walmart.com/browse/home/all-coffee-tables/4044_103150_4038_8869666_2502404",35281,25),
    ("Accent Chairs","https://www.walmart.com/browse/home/accent-chairs/4044_103150_4038_7389568",33813,25),
    ("Ottomans","https://www.walmart.com/browse/home/all-ottomans/4044_103150_4038_9082960_8193767",16961,25),
    ("End Tables","https://www.walmart.com/browse/home/end-tables/4044_103150_4038_4991400",44527,25),
    ("Bookshelves","https://www.walmart.com/browse/home/bookshelves/4044_103150_97116_91849",33472,25),
    ("Accent Cabinets & Chests","https://www.walmart.com/browse/home/accent-cabinets-chests/4044_103150_4038_7305584_4108220",11940,25),
    ("Benches","https://www.walmart.com/browse/home/benches/4044_103150_468234",9971,25),
    ("Recliners","https://www.walmart.com/browse/home/recliners/4044_103150_4038_2105992",14053,25),
    ("Console Tables","https://www.walmart.com/browse/home/console-sofa-tables/4044_103150_4038_9926610",12972,25),
    ("Chaise Lounge Chairs","https://www.walmart.com/browse/home/chaise-lounge-chairs",1756,25),
    ("Futons","https://www.walmart.com/browse/home/futons/4044_103150_4038_2217176",1640,25),
    ("Loveseats","https://www.walmart.com/browse/home/loveseats",9916,25),
    ("Massage Chairs","https://www.walmart.com/browse/home/massage-chairs",2567,25),
    ("Papasan Chairs","https://www.walmart.com/browse/home/papasan-chairs",351,9),
    ("Reclining Sectional Sofas","https://www.walmart.com/browse/home/reclining-sectional-sofas",2168,25),
    ("Rocking Chairs","https://www.walmart.com/browse/home/rocking-chairs",16,1),
    ("Sectional Sofas","https://www.walmart.com/browse/home/sectional-sofas-couches/4044_103150_4038_8106416",26351,25),
    ("Sleeper Sectionals","https://www.walmart.com/browse/home/sleeper-sectional-sofas/4044_103150_4038_8106416_9932194",13,1),
    ("Sofa Beds & Sleepers","https://www.walmart.com/browse/home/sofa-beds/4044_103150_4038_7525715",110,3),
    ("Fireplace TV Stands","https://www.walmart.com/browse/home/fireplace-tv-stands/4044_103150_635499_1431603",514,13),
    ("Entertainment Centers","https://www.walmart.com/browse/home/entertainment-centers/4044_103150_635499_91848",1696,25),
    ("Record Player Stand","https://www.walmart.com/browse/home/record-player-stand/4044_103150_4059585",979,25),
    ("Coffee Table Sets","https://www.walmart.com/browse/home/coffee-table-sets/4044_103150_4038_8869666_1267473",2969,25),
    ("C Tables","https://www.walmart.com/browse/home/c-tables",18,1),
    ("Lift-Top Coffee Tables","https://www.walmart.com/browse/home/lift-top-coffee-tables",39,1),
    ("Nesting Tables","https://www.walmart.com/browse/home/nesting-tables",17,1),
    ("TV Trays","https://www.walmart.com/browse/home/tv-trays",1050,25),
    ("Blanket Ladders","https://www.walmart.com/browse/home/blanket-ladders",268,7),
    ("Poufs","https://www.walmart.com/browse/home/poufs-floor-pillows/4044_133012_1157472",3754,25),
]
for n,u,t,m in living_room:
    rows.append(leaf(n,u,t,m))

rows.append(group("Bedroom"))
bedroom = [
    ("Beds","https://www.walmart.com/browse/bedroom-furniture/beds/4044_103150_102547_91837",45233,25),
    ("Dressers","https://www.walmart.com/browse/bedroom-furniture/dressers/4044_103150_102547_91839",35545,25),
    ("Nightstands","https://www.walmart.com/browse/home/nightstands/4044_103150_102547_91838",38220,25),
    ("Armoires & Wardrobes","https://www.walmart.com/browse/home/armoires-wardrobes/4044_103150_102547_91846",4415,25),
    ("Headboards","https://www.walmart.com/browse/home/headboards/4044_103150_102547_470314",3208,25),
    ("Bed Frames","https://www.walmart.com/browse/home/bed-frames/4044_103150_102547_96991",37472,25),
    ("Bedroom Sets","https://www.walmart.com/browse/home/bedroom-sets/4044_103150_102547_1043812",9694,25),
    ("Murphy Beds","https://www.walmart.com/browse/home/murphy-beds/4044_103150_102547_6512511",771,20),
    ("Daybeds","https://www.walmart.com/browse/home/daybeds/4044_103150_102547_5907928",7923,25),
    ("Entryway Furniture","https://www.walmart.com/browse/home/entryway-furniture/4044_103150_6858258",30482,25),
]
for n,u,t,m in bedroom:
    rows.append(leaf(n,u,t,m))

rows.append(group("Dining Room / Kitchen Furniture"))
dining = [
    ("Dining Room Sets","https://www.walmart.com/browse/home/dining-room-sets/4044_103150_4037_3500031",47130,25),
    ("Dining Chairs","https://www.walmart.com/browse/home/dining-chairs/4044_103150_4037_6472288",46067,25),
    ("Dining Tables","https://www.walmart.com/browse/home/dining-tables/4044_103150_4037_6952918",24838,25),
    ("Bar Stools & Counter Stools","https://www.walmart.com/browse/kitchen-dining-furniture/bar-stools-counter-stools/4044_103150_4037_8102642",79344,25),
    ("Dining Benches","https://www.walmart.com/browse/home/dining-benches/4044_103150_4037_4569290",916,23),
    ("Sideboards & Buffets","https://www.walmart.com/browse/home/sideboards-buffets/4044_103150_4037_231975",15301,25),
    ("China Cabinets","https://www.walmart.com/browse/home/china-cabinets/4044_103150_4037_4944655",3122,25),
    ("Bakers Racks","https://www.walmart.com/browse/home/bakers-racks/4044_103150_4037_6138309",2104,25),
    ("Pantries","https://www.walmart.com/browse/home/pantry-cabinets/4044_103150_4037_3781179",9994,25),
    ("Bar & Wine Cabinets","https://www.walmart.com/browse/home/bar-cabinets/4044_103150_4037_3598046_2736468",4285,25),
    ("Home Bars","https://www.walmart.com/browse/home/home-bars/4044_103150_4037_3598046_5019871",165,4),
    ("Wine Cabinets","https://www.walmart.com/browse/home/wine-cabinets/4044_103150_4037_3598046_1043802",1330,25),
    ("Coffee Bar Cabinets","https://www.walmart.com/browse/home/coffee-bar-cabinets/4044_103150_4037_3598046_4347749",4562,25),
]
for n,u,t,m in dining:
    rows.append(leaf(n,u,t,m))

rows.append(group("Home Office"))
office = [
    ("Desks","https://www.walmart.com/browse/home/desks/4044_103150_97116_91851",25713,25),
    ("Office Chairs","https://www.walmart.com/browse/home/desk-chairs/4044_103150_97116_91853",17542,25),
    ("Gaming Chairs","https://www.walmart.com/browse/home/gaming-chairs/4044_103150_97116_9559238",3331,25),
    ("Gaming Desks","https://www.walmart.com/browse/home/gaming-desks/4044_103150_97116_9962249",5110,25),
]
for n,u,t,m in office:
    rows.append(leaf(n,u,t,m))

rows.append(group("Kids' Furniture"))
kids = [
    ("Kids Beds & Headboards","https://www.walmart.com/browse/home/kids-beds-headboards/4044_1154295_1155958_7251917",26139,25),
    ("Kids Dressers & Armoires","https://www.walmart.com/browse/home/kids-dressers-armoires/4044_1154295_1155958_1156012",1488,25),
    ("Kids Nightstands","https://www.walmart.com/browse/home/kids-nightstands/4044_1154295_1155958_1156033",2267,25),
    ("Kids Chairs","https://www.walmart.com/browse/home/kids-chairs/4044_1154295_1155958_7203266",4287,25),
    ("Toddler Beds","https://www.walmart.com/browse/toddler-beds/all-toddler-beds/5427_978579_3990478_164204_2749797",537,14),
    ("Kids Desk & Chair Sets","https://www.walmart.com/browse/home/kids-desks-chairs/4044_1154295_1155958_1155993",34,1),
    ("Loft Beds","https://www.walmart.com/browse/home/loft-beds/4044_1154295_1155958_4960120",8444,25),
]
for n,u,t,m in kids:
    rows.append(leaf(n,u,t,m))

rows.append(group("Outdoor / Patio Furniture"))
outdoor = [
    ("Outdoor Dining Furniture","https://www.walmart.com/browse/patio-garden/outdoor-dining-furniture/5428_91416_2653548",36342,25),
    ("Outdoor Sofas & Sectionals","https://www.walmart.com/browse/patio-garden/outdoor-sofas-sectionals/5428_91416_3986806_2302419",4927,25),
    ("Patio Chairs","https://www.walmart.com/browse/patio-garden/patio-chairs/5428_91416_3986806_4843476",76804,25),
    ("Outdoor Benches","https://www.walmart.com/browse/patio-garden/outdoor-benches/5428_91416_3986806_3555950",6387,25),
    ("Patio Tables","https://www.walmart.com/browse/patio-garden/patio-tables/5428_91416_6040372",23578,25),
    ("Adirondack Chairs","https://www.walmart.com/browse/patio-garden/adirondack-chairs/5428_91416_3986806_8355696",3809,25),
    ("Outdoor Rocking Chairs","https://www.walmart.com/browse/patio-garden/outdoor-rocking-chairs/5428_91416_3986806_4843476_1556654",3450,25),
    ("Porch Swings","https://www.walmart.com/browse/patio-garden/porch-swings/5428_91416_3986806_3782919",4433,25),
]
for n,u,t,m in outdoor:
    rows.append(leaf(n,u,t,m))

rows.append(group("Bathroom Furniture"))
bathroom = [
    ("Bathroom Vanities","https://www.walmart.com/browse/home-improvement/bathroom-vanities/1072864_1045879_1230843_9176721",36662,25),
]
for n,u,t,m in bathroom:
    rows.append(leaf(n,u,t,m))

notes = (
    "Reached walmart.com directly via Chrome (no WAF/challenge encountered, matching prior Home-Decor pass which also had "
    "no block). robots.txt checked live: no Claude/ClaudeBot-specific disallow, no full-site block; /cp/, /browse/ paths "
    "allowed (only /search, /store/*, account/API endpoints disallowed). "
    "TREE SOURCE: walked the Furniture department hub (walmart.com/cp/furniture/103150) to its six room hubs (Living Room "
    "4038, Bedroom 102547, Dining/Kitchen 4037, Home Office 97116, Kids' Furniture under Kids' Rooms 1154295/1155958, "
    "Outdoor/Patio under the separate Patio & Garden dept 5428/91416) plus one Bathroom node (Bathroom Vanities, under "
    "Home Improvement dept 1072864/1045879/1230843). Cross-checked walmart.com/sitemap_category.xml (from robots.txt, "
    "12,344 URLs) per brief Rule 7b#1 to recover categories missing from the curated hub pages - this is how Armoires & "
    "Wardrobes, Headboards, Bed Frames, Bedroom Sets, Murphy Beds, Daybeds, Entryway Furniture, the Dining bar/wine/coffee "
    "cabinet trio, all 6 Kids' Furniture sub-nodes, and all 8 Outdoor/Patio nodes were found (none were on the sparse "
    "curated hub pages alone). Applied the deepest-node rule throughout: e.g. Bookshelves (4044_103150_97116_91849) is "
    "recorded once even though three different hub pages (Living Room, Home Office, and a 'Room Dividers' promo tile) all "
    "link to the identical URL/catId; 'All Benches' under Bedroom was dropped as the same duplicate for the same reason. "
    "EXCLUDED as non-taxonomy: 'Shop all'/'Shop all furniture' navigation links; brand-filter tiles (Better Homes & "
    "Gardens, Mainstays); on the Dining hub, roughly 45 material/style/size promo tiles (Farmhouse/Glass/Marble/Wood/"
    "Velvet/Rattan/Wicker/Round/Oval/Pedestal/Extendable Dining Tables, Set-Of-N Chairs/Bar Stools, Dining Table Sets For "
    "N, etc.) that are faceted-search variants of the 13 real Dining category nodes, not distinct categories (brief Rule "
    "3). EXCLUDED as not-furniture: Trunks (Walmart's own taxonomy files this under Storage & Organization dept 90828, "
    "not Furniture 103150); Wine Racks (filed under Kitchen & Dining dept 623679, a kitchen accessory not furniture); "
    "Cube storage (standalone storage product); Closet Organizers (closet shelving/rod systems, not freestanding "
    "furniture); Kitchen Islands (a genuine candidate seen on the Dining hub page but its link text was merged with a "
    "promo subtitle in the DOM and no clean URL/count could be recovered in the time available - dropped rather than "
    "guess); Filing Cabinets (cp/91852 fetch returned no totalItemCount/maxPage, could not verify, dropped rather than "
    "guess); Hammocks (ambiguous leisure item, not chased given time constraints). Mattresses were excluded per brief "
    "(bedding, not furniture). "
    "QTY METHOD: every candidate leaf was fetched (same-origin fetch from a Chrome tab already on walmart.com) and its "
    "embedded page JSON was read for totalItemCount and maxPage. Walmart's browse pages hard-cap pagination at 25 pages "
    "(~1000 items); when maxPage==25 the totalItemCount field is NOT a stable exact count - two reads of Sofas & Couches "
    "60 seconds apart returned 40298 and then 40301 for the identical URL, proving the field drifts/estimates at this "
    "scale, consistent with the prior Home-Decor pass's finding for this same site (notes/194.md: capped totalItemCount "
    "'not exhaustion-checkable', converted to null+flag). All leaves that hit this 25-page cap are recorded as qty:null "
    "with a MANUAL REVIEW flag rather than reporting an unstable number. The remaining leaves paginate to genuinely fewer "
    "than 25 pages (maxPage 1-23) - for these the totalItemCount field is corroborated by the page's own pagination "
    "actually terminating there, so it is accepted as exact (e.g. Papasan Chairs 351/maxPage 9, Rocking Chairs 16/maxPage "
    "1, Dining Benches 916/maxPage 23, Home Bars 165/maxPage 4, Murphy Beds 771/maxPage 20, Toddler Beds 537/maxPage 14, "
    "Kids Desk & Chair Sets 34/maxPage 1). Sanity checks per brief Rule 4: none of the accepted exact counts are "
    "suspiciously round; the redirected/canonical URL of every fetched page was confirmed to still name the requested "
    "node (no silent parent-listing substitution observed). "
    "SCOPE CAVEAT: this is a MASSIVE general-merchandise marketplace per the brief itself; given the efficiency mandate "
    "this pass covers the seven room departments Walmart itself organizes Furniture into (Living Room, Bedroom, Dining/"
    "Kitchen, Home Office, Kids', Outdoor/Patio, one Bathroom node) at the granularity the site's own curated hub pages "
    "plus sitemap expose, but is not a claim of 100% exhaustive coverage of every possible Walmart furniture sub-slug; "
    "Kitchen Islands and Filing Cabinets are known gaps."
)

data = {
    "sr": 194,
    "company": "Walmart US",
    "brand_site": "walmart.com",
    "country": "USA",
    "site_url": "https://www.walmart.com/",
    "status": "partial",
    "failure_reason": ("Most leaf rows carry qty:null because Walmart's browse pages hard-cap pagination at 25 pages "
                        "(~1000 items) and the underlying totalItemCount field was shown to drift/estimate at that "
                        "scale (two reads of the same URL 60s apart differed) - consistent with the prior Home-Decor "
                        "pass's finding for this same site. This is a data-availability limit of the source, not a "
                        "site block; every affected node is still recorded with its verified canonical URL and a "
                        "MANUAL REVIEW flag. Two candidate nodes (Kitchen Islands, Filing Cabinets) could not be "
                        "resolved to a clean URL/count in the time available and were dropped rather than guessed - "
                        "see notes."),
    "notes": notes,
    "rows": rows
}

out_path = r"C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\furniture_json_archive\f194.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("rows:", len(rows))
print("leaf rows:", sum(1 for r in rows if not r["is_group"]))
print("group rows:", sum(1 for r in rows if r["is_group"]))
print("null qty:", sum(1 for r in rows if not r["is_group"] and r["qty"] is None))
print("flagged:", sum(1 for r in rows if r["flag"]))
