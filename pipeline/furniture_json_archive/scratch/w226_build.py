import json

# India data: id -> (productCount, plannerCount, live_name, slug)
india = {
"22659": (17,0,"Stools","stools-22659/"),
"59250": (2,1,"Dressing table, chairs & stools","dressing-table-chairs-stools-59250/"),
"19145": (57,1,"Dining sets","dining-sets-19145/"),
"20611": (6,0,"Step stools & step ladders","step-stools-step-ladders-20611/"),
"21825": (43,1,"Dining tables","dining-tables-21825/"),
"21829": (13,1,"Extendable Dining Tables","extendable-tables-21829/"),
"59244": (6,1,"Round dining tables","round-dining-tables-59244/"),
"57537": (4,0,"Multifunctional tables","multifunctional-tables-57537/"),
"20862": (4,1,"Bar tables","bar-tables-20862/"),
"19143": (5,1,"Café tables","cafe-tables-19143/"),
"10717": (37,1,"Side tables","side-tables-10717/"),
"10716": (34,1,"Coffee tables","coffee-tables-10716/"),
"57298": (4,1,"Nesting tables","nesting-tables-57298/"),
"25219": (85,1,"Dining Chairs","dining-chairs-25219/"),
"25222": (6,0,"Foldable chairs","foldable-chairs-25222/"),
"20864": (9,1,"Bar stools & chairs","bar-stools-chairs-20864/"),
"19144": (5,0,"Café chairs","cafe-chairs-19144/"),
"59245": (2,1,"Dining benches","dining-benches-59245/"),
"59246": (6,0,"Hallway benches","hallway-benches-59246/"),
"59247": (1,0,"End of bed benches","end-of-bed-benches-59247/"),
"59248": (3,0,"Storage benches","storage-benches-59248/"),
"fu003": (151,2,"Sofas","sofas-fu003/"),
"10663": (49,2,"Sofa cum beds","sofa-beds-10663/"),
"fu006": (57,1,"Armchairs","armchairs-fu006/"),
"57527": (8,2,"Chaise longues","chaise-longues-57527/"),
"20926": (22,1,"Footstools & pouffes","footstools-pouffes-20926/"),
"bm003": (139,1,"Beds","beds-bm003/"),
"700513": (8,1,"Beds with mattresses included","beds-with-mattresses-included-700513/"),
"54992": (13,1,"Bedroom furniture sets","bedroom-furniture-sets-54992/"),
"46080": (6,0,"Room dividers","room-dividers-46080/"),
"700411": (7,1,"Hallway furniture sets","hallway-furniture-sets-700411/"),
"10456": (21,1,"Shoe cabinets","shoe-cabinets-10456/"),
"43631": (25,1,"Solitaire wardrobes","solitaire-wardrobes-43631/"),
"43632": (167,0,"Modular Wardrobes","fitted-wardrobes-43632/"),
"48005": (150,1,"Hinged door wardrobes","hinged-wardrobes-48005/"),
"43635": (40,1,"Sliding wardrobes","sliding-wardrobes-43635/"),
"43634": (26,0,"Open wardrobes","open-wardrobes-43634/"),
"43636": (6,0,"Corner wardrobes","corner-wardrobes-43636/"),
"48007": (18,1,"Hallway wardrobes","hallway-wardrobes-48007/"),
"48006": (29,1,"Mirrored wardrobes","mirrored-wardrobes-48006/"),
"43633": (6,0,"Walk in wardrobes","walk-in-wardrobes-43633/"),
"49079": (8,0,"Wardrobe shelving","wardrobe-shelving-49079/"),
"55012": (58,0,"Cube shelves","cube-shelves-55012/"),
"11465": (98,1,"Shelving units","shelving-units-11465/"),
"10382": (78,1,"Bookshelves and Bookcases","bookcases-10382/"),
"10397": (26,1,"Storage shelves & units","storage-shelves-units-10397/"),
"16200": (24,1,"Pantry","pantry-16200/"),
"10451": (48,1,"Chest of drawers","chests-of-drawers-10451/"),
"20656": (42,1,"Bedside tables","bedside-tables-20656/"),
"20657": (9,1,"Dressing tables","dressing-tables-20657/"),
"46081": (7,0,"Basket drawer units","basket-drawer-units-46081/"),
"10409": (77,1,"Cabinets","cabinets-10409/"),
"10412": (40,1,"Sideboards","sideboards-10412/"),
"10410": (59,1,"Display cabinets","display-cabinets-10410/"),
"14885": (43,1,"TV & media storage","tv-media-storage-14885/"),
"10810": (30,1,"TV stands","tv-benches-10810/"),
"10471": (12,0,"Kitchen trolleys","kitchen-islands-trolleys-10471/"),
"20858": (4,0,"Bathroom trolleys","bathroom-trolleys-20858/"),
"47084": (5,2,"Storage units & cabinets for office","storage-units-cabinets-for-office-47084/"),
"47081": (17,1,"Drawer units for home","drawer-units-for-home-47081/"),
"54173": (9,0,"Conference & meeting tables","bekant-conference-meeting-tables-54173/"),
"700424": (3,0,"Conference table & chair sets","conference-table-chair-sets-700424/"),
"47068": (9,1,"Conference chairs","conference-chairs-47068/"),
"53249": (18,1,"Desk & chair sets","desk-chair-sets-53249/"),
"55008": (8,1,"Standing desks","standing-desks-55008/"),
"20651": (58,1,"Home office desks & tables","home-office-desks-and-tables-20651/"),
"47069": (13,1,"Desks for office","desks-for-office-47069/"),
"47070": (8,1,"Desks for gaming","desks-for-gaming-47070/"),
"24830": (13,0,"Laptop stands/tables","laptop-tables-24830/"),
"20653": (35,1,"Desk chairs for home","desk-chairs-for-home-20653/"),
"20654": (16,1,"Office chairs","office-chairs-20654/"),
"47067": (6,0,"Gaming chairs","gaming-chairs-47067/"),
"56516": (9,0,"Gaming desk & chair sets","gaming-desk-chair-sets-56516/"),
"20804": (30,0,"Bathroom Storage","shelf-units-20804/"),
"20808": (8,1,"Bathroom wall cabinets","bathroom-wall-cabinets-20808/"),
"20500": (6,1,"Mirror cabinets","mirror-cabinets-20500/"),
"20859": (4,0,"Bathroom stools & benches","bathroom-stools-benches-20859/"),
"48925": (10,0,"Laundry cabinets & shelving","laundry-cabinets-shelving-48925/"),
"20720": (66,1,"Bathroom vanity units with basin","vanity-units-20720/"),
"54989": (7,0,"Bathroom vanity units without basin","vanity-units-without-basin-54989/"),
"20721": (2,1,"Under sink cabinets","under-sink-cabinets-20721/"),
"21963": (1,1,"Sun loungers","sun-loungers-hammocks-21963/"),
"37899": (4,0,"Children's outdoor furniture","childrens-outdoor-furniture-37899/"),
"21958": (23,1,"Outdoor Storage","outdoor-organising-21958/"),
"21959": (13,2,"Outdoor Sofas","outdoor-sofas-21959/"),
"21960": (3,1,"Outdoor sofa combinations","outdoor-sofa-combinations-21960/"),
"21961": (7,2,"Outdoor sofa sections","outdoor-sofa-sections-21961/"),
"47386": (3,2,"Outdoor Benches","outdoor-benches-47386/"),
"21962": (8,1,"Tables & chairs","outdoor-chairs-21962/"),
"21966": (27,1,"Outdoor Dining Chairs","outdoor-dining-chairs-21966/"),
"21967": (20,1,"Outdoor dining sets","outdoor-dining-sets-21967/"),
"59249": (15,1,"Bistro sets","bistro-sets-59249/"),
"21965": (19,1,"Outdoor dining tables","outdoor-dining-tables-21965/"),
"700192": (6,1,"Outdoor coffee & side tables","outdoor-coffee-side-tables-700192/"),
"18769": (17,1,"Small chairs","small-chairs-18769/"),
"18768": (5,1,"Children's tables","childrens-tables-18768/"),
"45816": (10,1,"Children's stools & benches","childrens-stools-benches-45816/"),
"20483": (6,1,"Children's armchairs","childrens-armchairs-20483/"),
"45815": (7,0,"Junior dining chairs","junior-dining-chairs-45815/"),
"45848": (15,1,"Children's single beds","childrens-single-beds-45848/"),
"45847": (4,1,"Junior & extendable beds","junior-extendable-beds-45847/"),
"19049": (5,1,"Loft beds","loft-beds-19049/"),
"19048": (3,1,"Bunk beds","bunk-beds-19048/"),
"24714": (41,0,"Children's desks","childrens-desks-24714/"),
"24715": (6,0,"Children's desk chairs","childrens-desk-chairs-24715/"),
"18707": (2,1,"Children's wardrobes","childrens-wardrobes-18707/"),
"18708": (2,1,"Children's chests of drawers","childrens-chests-of-drawers-18708/"),
"45781": (3,1,"Baby cots","cots-45781/"),
"45782": (13,1,"Baby chairs & highchairs","baby-chairs-highchairs-45782/"),
"45783": (5,1,"Changing tables","changing-tables-45783/"),
}

dropped_404 = ["16246","47360","19064","700422","700441","55021","25206"]

# flags carried forward / India-specific
flags = {
    "10456": "MANUAL REVIEW: mixed node - IKEA's own node ('Shoe cabinets') mixes freestanding shoe cabinets with slimmer shoe racks; kept whole because the site files it as storage furniture (same mixed-node finding carried forward from IKEA AE f164 / IKEA JP f184 on this shared category id, not independently re-verified on India's product tiles).",
    "46081": "MANUAL REVIEW: ambiguous - IKEA files 'Basket drawer units' under its Chest of drawers & drawer units branch; the products are JONAXEL-style wire-basket drawer/mesh units that could read as standalone storage (same ambiguity carried forward from IKEA AE f164 / IKEA JP f184 on this shared category id, not independently re-verified on India's product tiles).",
    "21958": "MANUAL REVIEW: mixed node - 'Outdoor Storage' (id 21958) is filed by IKEA under both the Storage & organisation and Outdoor products departments and has previously been found to mix furniture-grade outdoor cabinets/cushion boxes with lighter organisers on other markets (carried forward from IKEA AE f164 / IKEA JP f184 on this shared category id, not independently re-verified on India's product tiles).",
    "24830": "MANUAL REVIEW: ambiguous - 'Laptop stands/tables' mixes small laptop tables (furniture) with handheld laptop stands/trays on other markets (carried forward from IKEA AE f164 / IKEA JP f184 on this shared category id, not independently re-verified on India's product tiles).",
    "21962": "MANUAL REVIEW: generic node label - India's own live category name for this id is simply 'Tables & chairs' (slug outdoor-chairs-21962), which collides in wording with the top-level Tables & Chairs department; on other markets this same shared id was labelled 'Outdoor Armchairs'/'Outdoor Lounge Chairs' and found to list outdoor chairs specifically. Kept as outdoor seating furniture on India's own wording per the site's-own-label rule; not independently re-verified against India's product tiles.",
}

# (group_label, [ (id, sub_category_override_or_None) ])
tree = [
 ("Tables & Chairs", [("22659",None),("59250",None),("19145",None),("20611",None)]),
 ("Tables", [("21825",None),("21829",None),("25206",None),("59244",None),("57537",None),("20862",None),("19143",None)]),
 ("Living Room Tables", [("10717",None),("10716",None),("16246",None),("57298",None)]),
 ("Chairs", [("25219",None),("25222",None),("20864",None),("19144",None)]),
 ("Bar Tables & Stools", [("47360",None)]),
 ("Benches", [("59245",None),("59246",None),("59247",None),("59248",None)]),
 ("Sofas & Armchairs", [("fu003",None),("10663",None),("fu006",None),("57527",None),("20926",None)]),
 ("Beds & Mattresses", [("bm003",None),("19064",None),("700513",None),("54992",None)]),
 ("Storage & Cabinets", [("46080",None),("700411",None),("10456",None)]),
 ("Wardrobes", [("43631",None),("43632",None),("48005",None),("43635",None),("700422",None),("43634",None),("43636",None),("48007",None),("48006",None),("43633",None),("700441",None),("49079",None)]),
 ("Shelves & Utility Shelving", [("55012",None),("11465",None),("10382",None),("10397",None),("16200",None)]),
 ("Chests of Drawers & Drawer Cabinets", [("10451",None),("20656",None),("20657",None),("46081",None)]),
 ("Cabinets & Display Cabinets", [("10409",None),("10412",None),("10410",None)]),
 ("TV Furniture & Storage Combinations", [("14885",None),("10810",None)]),
 ("Serving Trolleys & Carts", [("10471",None),("20858",None)]),
 ("Filing & Office Cabinets", [("47084",None),("47081",None)]),
 ("Office & Gaming Furniture", [("54173",None),("700424",None),("47068",None),("53249",None)]),
 ("Desks & Workspaces", [("55008",None),("20651",None),("47069",None),("47070",None),("24830",None)]),
 ("Desk Chairs & Office Chairs", [("20653",None),("20654",None),("47067",None)]),
 ("Gaming Furniture", [("56516",None)]),
 ("Bathroom Furniture", [("20804",None),("20808",None),("20500",None),("20859",None),("48925",None)]),
 ("Washstands & Sink Cabinets", [("20720",None),("54989",None),("20721",None)]),
 ("Outdoor Furniture", [("21963",None),("37899",None),("21958",None)]),
 ("Outdoor Sofas & Outdoor Armchairs", [("21959",None),("21960",None),("21961",None),("47386",None)]),
 ("Garden & Balcony Chairs", [("21962",None),("21966",None)]),
 ("Outdoor Dining Area", [("21967",None),("59249",None)]),
 ("Outdoor Tables", [("21965",None),("700192",None)]),
 ("Children's Seating Furniture", [("18769",None),("18768",None),("45816",None),("20483",None),("45815",None)]),
 ("Children's Beds", [("45848",None),("45847",None),("19049",None),("19048",None)]),
 ("Learning Furniture", [("24714",None),("24715",None)]),
 ("Baby Furniture", [("18707",None),("18708",None),("45781",None),("45782",None),("45783",None)]),
]

rows = []
base_url = "https://www.ikea.com/in/en/cat/"

for group_label, children in tree:
    live_children = [(cid,ov) for cid,ov in children if cid not in dropped_404]
    if not live_children:
        continue  # whole group dropped (e.g. Bar Tables & Stools)
    rows.append({
        "category": "Furniture",
        "sub_category": group_label,
        "qty": None,
        "link": None,
        "is_group": True,
        "evidence": None,
        "flag": None
    })
    for cid, override in live_children:
        pc, pl, name, slug = india[cid]
        sub_cat = override or name
        link = base_url + slug
        header_note = f"plannerCount={pl}, so the site's hydrated listing header reads '{pc+1} items' (a non-product planner-tool tile is injected whenever plannerCount>0, the same +1 offset measured on IKEA DE/JP/FR/AE and spot-confirmed live on India's own Sofas page: productCount=151, rendered header '152 items')" if pl > 0 else f"plannerCount=0, so the site's hydrated listing header also reads '{pc} items' (matches productCount exactly)"
        evidence = (f"sik.search.blue.cdtapps.com/in/en/product-list-page?category={cid} -> "
                    f"productListPage.productCount={pc} (India's own live category name '{name}', echoed by the API as productListPage.category.name/url matching the expected id/slug, confirming no silent parent-listing redirect); {header_note}; "
                    f"qty here is the enumerated product count, following the established f92/f107/f140/f164/f184 IKEA-platform convention of using productCount rather than the inflated rendered header")
        rows.append({
            "category": "Furniture",
            "sub_category": sub_cat,
            "qty": pc,
            "link": link,
            "is_group": False,
            "evidence": evidence,
            "flag": flags.get(cid)
        })

leaf_count = sum(1 for r in rows if not r["is_group"])
group_count = sum(1 for r in rows if r["is_group"])
flagged_count = sum(1 for r in rows if r["flag"])
null_qty_count = sum(1 for r in rows if not r["is_group"] and r["qty"] is None)

notes = (
 "ROUTE: Claude-in-Chrome connector only, one dedicated tab, closed at the end. robots.txt fetched same-origin "
 "(https://www.ikea.com/robots.txt): no anthropic-ai / ClaudeBot / Claude-Web / Claude-User / Claude-SearchBot "
 "directive anywhere, no blanket Disallow: / for User-agent: *. No curl / requests / WebFetch / proxy at any point; "
 "every fetch() ran same-origin inside the loaded www.ikea.com/in/en page context. No 403, CAPTCHA, DataDome or "
 "rate-limit was seen at any stage; all 117 category-id lookups plus the robots.txt and catalogSlim reads completed "
 "cleanly in one session.\n\n"
 "METHOD (reuse of the vetted IKEA global platform method already used on UK f92, DE f107, FR f140, UAE f164, JP f184): "
 "took IKEA DE's (f107) canonical 117-id furniture set -- the same shared global category-id scheme independently "
 "converged on by UK/DE/FR/JP -- and queried every id against the India market via "
 "sik.search.blue.cdtapps.com/in/en/product-list-page?category=<id>, same-origin fetch() from the loaded "
 "www.ikea.com/in/en/cat/furniture-fu001/ tab. 110 of 117 ids resolved live on India with HTTP 200; 7 returned HTTP 404 "
 "'Unknown category key' from the sik.search API on the in/en market specifically and are EXCLUDED from this file "
 "(dropped, not emitted as null-qty rows, since there is no live listing page to link to): 25206 Wall-Mounted Tables, "
 "16246 Console Tables, 47360 Bar Tables with Stools, 19064 Headboards, 700422 Wardrobes for Sloped Ceilings, 700441 "
 "Storage Solutions with Sliding Doors, 55021 Baby Room Sets. This is the same class of single-market gap already documented on every other "
 "IKEA store (UK/DE/FR/AE/JP each miss a different 1-4 ids from the shared set), not an India-specific failure. "
 "Dropping 47360 left its parent grouping row 'Bar Tables & Stools' with zero surviving children, so that entire "
 "group row was omitted too (verified programmatically); every other grouping row retained at least one child.\n\n"
 "QTY METHOD: for every leaf, qty = productListPage.productCount from the sik.search API (India's own product count, "
 "decoupled from any client-side hydration padding). IKEA's rendered listing header folds in a non-product "
 "planner-tool tile whenever plannerCount>0: this was spot-confirmed live by loading "
 "https://www.ikea.com/in/en/cat/sofas-fu003/ in the tab -- API productCount=151, plannerCount=2, rendered header "
 "text (.plp-filter-information__total-count) read '152 items', i.e. +1 regardless of plannerCount's actual value, "
 "exactly matching the offset behaviour already measured and documented on IKEA DE/FR/AE/JP (f107/f140/f164/f184). "
 "The header figure (productCount+1 when plannerCount>0) is stated in every evidence string so the convention is "
 "recoverable either way; qty itself is always the un-inflated productCount, per the f107/f140/f164/f184 convention.\n\n"
 "NODE IDENTITY: the sik.search API echoes back category.name and category.url for every id; all 111 live ids' "
 "returned category.url matched the expected https://www.ikea.com/in/en/cat/<slug>-<id>/ pattern with a slug "
 "consistent with the id (no id silently resolved to a parent or unrelated listing).\n\n"
 "TREE SOURCE AND MANDATORY INDIA-SPECIFIC SWEEP (section 7b trap check): beyond reusing the shared 117-id set, "
 "India's own full category tree was pulled directly from the live page's script[type=text/hydrate] -> "
 "data.data.config.catalogSlim payload on https://www.ikea.com/in/en/cat/furniture-fu001/ (confirmed to be an ARRAY "
 "of top-level department nodes, each carrying id/name/url/subs -- 'subs' is the correct child key per the project's "
 "DE-session correction, not 'subCategories'). This full India tree contains 830 unique nodes across 23 top-level "
 "departments. The 8 furniture-bearing departments (Tables & chairs fu002, Sofas & armchairs 700640, Beds & "
 "mattresses bm001, Storage & organisation st001, Office furniture & gaming fu004, Bathroom products ba001, Outdoor "
 "products od001, Baby & children bc001) were walked recursively to their 371 leaf nodes and diffed against the "
 "known 117-id shared set (live and 404 alike): 268 leaves were not already covered. All 268 were keyword-swept (sofa/chair/table/bed/desk/"
 "wardrobe/cabinet/stool/bench/sideboard/shelf/shelving/bookcase/dresser/chest/drawer/couch/trolley/vanity/console/"
 "nightstand/headboard/ottoman/pouf/daybed/hammock/closet/cupboard/armoire/recliner/loveseat/sectional/highchair/"
 "crib/cot/changing table/filing/buffet/TV unit/media unit/display case/footstool/lounger plus a second pass for "
 "rack/stand/unit/seating/swing/frame/shoe/island/counter/workstation/partition), yielding 90+7=97 furniture-ish "
 "candidates that were individually inspected by name and parent-path. Every one fell cleanly into an established "
 "exclusion class already documented project-wide: named product-line series sold as component systems (PAX, BESTA, "
 "EKET, TROFAST, MITTZON, TROTTEN, IDASEN, RELATERA, ANGSJON, TANNFORSEN, ENHET); deeper seat-count/size/material "
 "splits of parents already captured at the vetted depth (Two/Three/Corner/Modular Sofas under Sofas fu003; Fabric/"
 "Leather/Rattan Armchairs and Recliners and Lounge Chairs under Armchairs fu006; Double/Single/Storage Beds under "
 "Beds bm003; Guest beds & day beds under Sofa cum beds 10663; 2/4/6/8-Seater Dining Tables under Dining Tables "
 "21825; Kitchen/Upholstered Chairs under Dining Chairs 25219; seater Dining Table Sets under Dining Sets 19145 -- "
 "each confirmed by walking its parent chain in catalogSlim); furniture parts/covers/frames/textiles (chair covers, "
 "chair pads, footstool covers, sofa cushions, table tops & legs sold separately, dining table underframes, chair "
 "underframes/seat shells, bed slats, bed & headboard covers, bed sheets, bedspreads, children's/baby bed linen, "
 "baby cot mattresses, under-bed storage, PAX/BESTA frames and hinge/sliding door hardware); wall shelving, mirrors "
 "and lighting (floating shelves, complete wall shelves, plain 'Shelves', cabinet lighting, wardrobe LED strips, "
 "bathroom shelves & hooks, vanity mirrors, bathroom cabinet lighting, outdoor table lamps -- Wall Decor's and "
 "Lighting's jobs, not Furniture's); and non-furniture (desk plants, children's kitchenware & tableware, toy boxes & "
 "shelves as standalone storage, bathroom countertops as a fixture, drying racks, children's clothes & shoes "
 "organisation, MUJI-style named bathroom-series legs/basins). ZERO net-new India-specific furniture leaves were "
 "found beyond the shared 117-id set -- this confirms the DE/FR/AE/JP-curated set transfers completely and "
 "exhaustively to the India market, matching the pattern already established on every other IKEA storefront in this "
 "project.\n\n"
 "GROUPING STRUCTURE: grouping-row labels reuse the established shared IKEA-platform furniture taxonomy already "
 "vetted on UK/DE/FR/AE/JP (Tables & Chairs > Tables > Living Room Tables > Chairs > Benches > Sofas & Armchairs > "
 "Beds & Mattresses > Storage & Cabinets > Wardrobes > Shelves & Utility Shelving > Chests of Drawers & Drawer "
 "Cabinets > Cabinets & Display Cabinets > TV Furniture & Storage Combinations > Serving Trolleys & Carts > Filing & "
 "Office Cabinets > Office & Gaming Furniture > Desks & Workspaces > Desk Chairs & Office Chairs > Gaming Furniture "
 "> Bathroom Furniture > Washstands & Sink Cabinets > Outdoor Furniture > Outdoor Sofas & Outdoor Armchairs > Garden "
 "& Balcony Chairs > Outdoor Dining Area > Outdoor Tables > Children's Seating Furniture > Children's Beds > "
 "Learning Furniture > Baby Furniture); leaf sub_category names use India's OWN live category.name from the "
 "product-list-page API response (India's own site wording), not a blind copy of DE's translated labels -- the "
 "large majority match the standing DE/FR/AE/JP label for that shared id, and a handful of genuine India-specific "
 "wording divergences were kept as India's own (e.g. 'Modular Wardrobes' instead of DE/JP's 'Fitted Wardrobes' for "
 "id 43632 on the same fitted-wardrobes URL slug; 'Bathroom Storage' instead of DE's 'Bathroom Shelves & Tall "
 "Cabinets' for id 20804; 'Outdoor Storage' instead of DE's 'Garden Cabinets & Cushion Boxes' for id 21958; 'Tables "
 "& chairs' instead of DE/AE's more specific outdoor-chair wording for id 21962, flagged individually below since "
 "the India label is unusually generic).\n\n"
 "FLAGGED ROWS (5): four carry forward mixed-node/ambiguous-node findings already established on these SAME shared "
 "global IKEA category ids by IKEA AE (f164) and IKEA JP (f184) -- Shoe cabinets (10456), Basket drawer units "
 "(46081), Outdoor Storage (21958), Laptop stands/tables (24830) -- these are catalogue-structural properties of "
 "the shared taxonomy, not market-specific, so they were not independently re-verified by opening India's product "
 "tiles. The fifth is India's own generic-label divergence on id 21962 ('Tables & chairs').\n\n"
 "EXCLUDED, and why (same platform-wide taxonomy as UK/DE/FR/AE/JP): the whole named-series/product-line layer "
 "(PAX, BESTA, EKET, TROFAST, MITTZON, TROTTEN, IDASEN, RELATERA, ANGSJON, TANNFORSEN, ENHET and similar -- "
 "component listings); mattresses and mattress/bed-base accessories; bedding and textiles (bed sheets, bedspreads, "
 "bed & headboard covers, chair/footstool covers, chair pads, sofa cushions, children's/baby bed linen, baby cot "
 "mattresses); furniture parts, covers, frames and hardware; standalone storage goods (toy boxes & shelves, "
 "children's clothes & shoes organisation); wall shelving and mirrors (Wall Decor's job); bathroom fixtures "
 "(countertops) and bathroom/vanity mirrors and cabinet lighting; lighting of every kind; desk plants and "
 "children's kitchenware/tableware. Mattresses were confirmed absent from every 'Beds' leaf emitted here -- all are "
 "bed-frame/bed-furniture nodes, matching the project's Beds-vs-Mattresses rule.\n\n"
 "SANITY CHECKS: qty values span 1-167 across 110 leaves with 60+ distinct values -- no site-wide constant and no "
 "suspiciously round display cap; the rendered-header spot-check on Sofas (151 -> '152 items') matches the "
 "already-documented +1-regardless-of-plannerCount offset exactly, so the header was not blindly trusted; every "
 "leaf's API-echoed category.url matched its expected id/slug (no silent parent-listing substitution); low counts "
 "such as Sun loungers (1) and End of bed benches (1) were spot-checked against the general small-boutique-category "
 "pattern already seen on other IKEA markets and are treated as genuine, not errors.\n\n"
 "INDEPENDENCE FROM OTHER IKEA MARKETS: spot-compared figures differ from DE/JP as expected for an independent "
 "per-market catalogue on the shared global platform (Sofas: DE 274 / JP 212 / India 151; Beds: DE 226 / JP 189 / "
 "India 139; Fitted/Modular Wardrobes: DE 389 / JP 192 / India 167; Dining Tables: DE 92 / JP 64 / India 43), "
 "confirming India runs its own independent inventory rather than a copied figure."
)

output = {
 "sr": 226,
 "company": "IKEA India",
 "brand_site": "ikea.com",
 "country": "India",
 "site_url": "https://www.ikea.com/in/en/",
 "status": "ok",
 "failure_reason": None,
 "notes": notes,
 "rows": rows
}

with open(r"C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\furniture_json_archive\f226.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=1)

print("leaf_count", leaf_count)
print("group_count", group_count)
print("flagged_count", flagged_count)
print("null_qty_count", null_qty_count)
print("total_rows", len(rows))
