import json

BASE = "https://www.woodenstreet.com"
EV = "__NEXT_DATA__ props.pageProps.apiResData.data.product_count={} (same-origin fetch of category page; this field matches the site's rendered '(N Products)' heading per prior-pass verification for this domain)"

def leaf(cat, sub, qty, path, flag=None):
    return {
        "category": cat,
        "sub_category": sub,
        "qty": qty,
        "link": BASE + path,
        "is_group": False,
        "evidence": EV.format(qty),
        "flag": flag,
    }

def group(cat, sub):
    return {
        "category": cat,
        "sub_category": sub,
        "qty": None,
        "link": None,
        "is_group": True,
        "evidence": None,
        "flag": None,
    }

F = "Furniture"
rows = []

rows.append(group(F, "Sofas"))
rows += [
    leaf(F, "Fabric Sofas", 239, "/fabric-sofas"),
    leaf(F, "Wooden Sofa Sets", 63, "/wooden-sofa"),
    leaf(F, "3 Seater Sofas", 150, "/three-seater-sofas"),
    leaf(F, "2 Seater Sofas", 53, "/two-seater-sofas"),
    leaf(F, "1 Seater Sofas", 87, "/one-seater-sofas"),
    leaf(F, "3+1+1 Sofa Sets", 35, "/3-1-1-sofa-set"),
    leaf(F, "L Shape Sofa", 68, "/l-shaped-sofas"),
    leaf(F, "Leather Sofas", 6, "/leather-sofas"),
    leaf(F, "Chaise Lounges", 14, "/chaise-lounges"),
    leaf(F, "Outdoor Sofas", 92, "/outdoor-sofas"),
    leaf(F, "Diwan Beds", 10, "/divan-beds"),
]

rows.append(group(F, "Sofa Cum Beds"))
rows += [
    leaf(F, "All Sofa Cum Beds", 61, "/all-sofa-cum-beds"),
    leaf(F, "Wooden Sofa Cum Beds", 18, "/wooden-sofa-cum-beds"),
    leaf(F, "Fabric Sofa Cum Beds", 40, "/fabric-sofa-cum-beds"),
    leaf(F, "L Shape Sofa Cum Bed", 9, "/l-shape-sofa-cum-bed"),
]

rows.append(group(F, "Recliners"))
rows += [
    leaf(F, "All Recliners", 36, "/all-recliners"),
    leaf(F, "1 Seater Recliners", 20, "/1-seater-recliners"),
    leaf(F, "2 Seater Recliners", 9, "/2-seater-recliners"),
    leaf(F, "3 Seater Recliners", 13, "/3-seater-recliners"),
]

rows.append(group(F, "Seating"))
rows += [
    leaf(F, "All Chairs", 215, "/all-chairs", "MANUAL REVIEW: aggregate listing overlapping with the individual chair-type rows below (Lounge/Accent/Arm/Wing/Swing/Rocking sum ~232, close but not identical) - kept as an independently reported sibling per project precedent, not summed"),
    leaf(F, "Lounge Chairs", 81, "/lounge-chairs"),
    leaf(F, "Accent Chairs", 56, "/accent-chairs"),
    leaf(F, "Armchairs", 42, "/arm-chairs"),
    leaf(F, "Wing Chairs", 29, "/wing-chairs"),
    leaf(F, "Swing Chairs", 17, "/swing-chairs"),
    leaf(F, "Rocking Chairs", 7, "/rocking-chairs"),
    leaf(F, "Loveseats", 6, "/loveseats"),
    leaf(F, "Benches", 33, "/benches"),
    leaf(F, "Ottomans", 16, "/ottomans"),
    leaf(F, "Stools", 10, "/stools"),
    leaf(F, "Room Dividers", 92, "/room-dividers"),
]

rows.append(group(F, "Living Room Tables"))
rows += [
    leaf(F, "Coffee & Centre Table", 55, "/coffee-tables"),
    leaf(F, "Coffee Table with Stool", 6, "/coffee-table-sets"),
    leaf(F, "Side & End Tables", 35, "/side-tables"),
    leaf(F, "Nesting Tables", 7, "/nest-of-tables"),
    leaf(F, "Console Tables", 14, "/console-tables"),
    leaf(F, "Laptop Tables", 11, "/laptop-tables"),
]

rows.append(group(F, "TV Units"))
rows += [
    leaf(F, "TV Units and Stands", 50, "/tv-units"),
    leaf(F, "Solid Wood TV Units", 26, "/solid-wood-tv-units"),
    leaf(F, "Modular TV Unit", 22, "/modular-tv-units"),
]

rows.append(group(F, "Living Room Storage"))
rows += [
    leaf(F, "Bookshelves", 36, "/bookshelves"),
    leaf(F, "Chest Of Drawers", 19, "/chest-of-drawers"),
    leaf(F, "Cabinet & Sideboard", 32, "/cabinet-sideboards"),
    leaf(F, "Display Units", 18, "/display-units"),
    leaf(F, "Wooden Wall Shelf & Racks", 16, "/wall-shelves",
         "MANUAL REVIEW: ambiguous shelving - this node is cross-listed under multiple furniture-storage menus (Living Storage / general Storage / Study&Office Storage) AND under the site's Wall Decor mega-menu column; product name 'Wooden Wall Shelf & Racks' reads as a functional storage rack, so kept as furniture, but the dual placement is a judgement call"),
    leaf(F, "Shoe Racks", 32, "/shoe-racks"),
]

rows.append(group(F, "Beds"))
rows += [
    leaf(F, "All Beds", 186, "/all-beds"),
    leaf(F, "Solid Wood Beds", 66, "/solid-wood-beds"),
    leaf(F, "Engineered Wood Beds", 27, "/engineered-wood-beds"),
    leaf(F, "Upholstered Beds", 33, "/upholstered-beds"),
    leaf(F, "Hydraulic Storage Beds", 47, "/hydraulic-storage-beds"),
    leaf(F, "Poster Beds", 11, "/poster-beds"),
    leaf(F, "Kids Beds", 2, "/kids-beds"),
    leaf(F, "King Size Beds", 90, "/king-size-beds"),
    leaf(F, "Queen Size Beds", 74, "/queen-size-beds"),
    leaf(F, "Double Beds", 111, "/double-beds"),
    leaf(F, "Single Beds", 20, "/single-beds"),
]

rows.append(group(F, "Wardrobes"))
rows += [
    leaf(F, "All Wardrobes", 71, "/all-wardrobes"),
    leaf(F, "Solid Wood Wardrobes", 23, "/solid-wood-wardrobes"),
    leaf(F, "Modular Wardrobes", 48, "/modular-wardrobes"),
    leaf(F, "Single Door Wardrobe", 10, "/single-door-wardrobe"),
    leaf(F, "2 Door Wardrobe", 30, "/2-door-wardrobe"),
    leaf(F, "3 Door Wardrobe", 12, "/3-door-wardrobe"),
    leaf(F, "4 Door Wardrobe", 18, "/4-door-wardrobe"),
    leaf(F, "Sliding Door Wardrobes", 3, "/sliding-door-wardrobes"),
]

rows.append(group(F, "Bedroom Tables & Storage"))
rows += [
    leaf(F, "Bedside Tables", 71, "/bedside-tables"),
    leaf(F, "Dressing Tables", 23, "/dressing-tables"),
    leaf(F, "Breakfast Tables", 5, "/breakfast-tables"),
    leaf(F, "Trunk & Blanket Box", 4, "/trunk-blanket-boxes"),
    leaf(F, "Bedroom Cabinets", 33, "/bedroom-cabinets"),
    leaf(F, "Wooden Showcase", 6, "/wooden-showcase"),
]

rows.append(group(F, "Dining Table Sets"))
rows += [
    leaf(F, "6 Seater Dining Table Sets", 33, "/6-seater-dining-table-sets"),
    leaf(F, "4 Seater Dining Table Sets", 18, "/4-seater-dining-table-sets"),
    leaf(F, "2 Seater Dining Table Sets", 3, "/2-seater-dining-table-sets"),
    leaf(F, "8 Seater Dining Table Sets", 2, "/8-seater-dining-table-sets"),
    leaf(F, "Folding Dining Table Sets", 6, "/folding-dining-table-sets"),
    leaf(F, "Wooden Dining Table Set", 56, "/wooden-dining-table-set"),
    leaf(F, "Marble Dining Table", 13, "/marble-dining-table-sets"),
    leaf(F, "Metal Dining Table Set", 1, "/metal-dining-table-set"),
]

rows.append(leaf(F, "Dining Tables", 44, "/dining-tables"))

rows.append(group(F, "Dining Seating"))
rows += [
    leaf(F, "Dining Chairs", 60, "/dining-chairs"),
    leaf(F, "Wooden Dining Chairs", 14, "/wooden-dining-chairs"),
    leaf(F, "Fabric Dining Chairs", 22, "/fabric-dining-chairs"),
]

rows.append(group(F, "Kitchen Storage"))
rows += [
    leaf(F, "Kitchen Cabinets", 23, "/kitchen-cabinets"),
    leaf(F, "Kitchen Racks", 3, "/kitchen-racks"),
    leaf(F, "Microwave Stand", 1, "/microwave-stand"),
    leaf(F, "Kitchen Trolleys", 4, "/kitchen-trolley"),
    leaf(F, "Crockery Units", 22, "/crockery-units"),
    leaf(F, "Hutch Cabinets", 14, "/hutch-cabinets"),
]

rows.append(group(F, "Bar Furniture"))
rows += [
    leaf(F, "Bar Cabinets", 8, "/bar-cabinets"),
    leaf(F, "Bar Trolleys", 4, "/bar-trolleys"),
    leaf(F, "Bar Table Sets", 8, "/bar-sets"),
]

rows.append(group(F, "Study Tables"))
rows += [
    leaf(F, "All Study Tables", 53, "/all-study-tables"),
    leaf(F, "Computer Tables", 15, "/computer-tables"),
    leaf(F, "Folding Study Tables", 11, "/folding-study-table"),
    leaf(F, "Corner Study Table", 4, "/corner-study-table"),
    leaf(F, "Wall Mounted Study Table", 2, "/wall-mounted-study-table"),
    leaf(F, "Height Adjustable Table", 1, "/height-adjustable-table"),
]

rows.append(leaf(F, "Office Tables", 12, "/office-tables"))

rows.append(group(F, "Office & Study Seating"))
rows += [
    leaf(F, "Office Chairs", 27, "/office-chairs"),
    leaf(F, "Study Chairs", 21, "/study-chairs"),
    leaf(F, "Gaming Chairs", 11, "/gaming-chair"),
    leaf(F, "Executive Chairs", 16, "/executive-chair"),
    leaf(F, "Cafe Chairs", 3, "/cafe-chairs"),
    leaf(F, "Office Sofas", 118, "/office-sofas"),
]

rows.append(leaf(F, "File Cabinets", 5, "/file-cabinets"))

rows.append(group(F, "Balcony Furniture"))
rows += [
    leaf(F, "Balcony Sets", 100, "/balcony-sets"),
    leaf(F, "Balcony Chairs", 42, "/balcony-chairs"),
    leaf(F, "Balcony Tables", 15, "/balcony-tables"),
]

rows.append(group(F, "Outdoor Furniture"))
rows += [
    leaf(F, "Outdoor Sets", 192, "/outdoor-sets"),
    leaf(F, "Outdoor Table & Chair Sets", 213, "/outdoor-table-and-chair-sets"),
    leaf(F, "Outdoor Loungers", 31, "/outdoor-loungers"),
]

notes = (
    "Reached via Chrome connector, direct HTTP 200 throughout, no WAF/challenge encountered "
    "(robots.txt allows Googlebot fully and names no Claude-specific disallow). Site is Next.js "
    "SSR; every category listing page embeds __NEXT_DATA__.props.pageProps.apiResData.data.product_count, "
    "which the prior Home-Decor pass on this same domain verified matches the visible '(N Products)' "
    "heading word-for-word - used here as the sole qty source, fetched via same-origin fetch() from "
    "the loaded page (javascript_tool), never via an outside HTTP client. Tree built from the desktop "
    "mega-menu's 9 top-level department columns (Sofas, Living, Bedroom, Mattress, Dining, Storage, "
    "Study & Office, Outdoor, Decor & Furnishing) parsed directly out of the DOM "
    "(ul.style_headerMenu__YKf8q > li > div.style_subMenu__u5CPr > ul.style_submenuRow__Y_V4X > "
    "li.style_subMenucard__HM6tf), each card's first list-item being the column's own hub link and "
    "the rest its real children. 'Mattress' department excluded wholesale (bedding, not furniture, "
    "per Rule 1). 'Decor & Furnishing' department inspected in full (Wall Decor, Spiritual/Mirrors, "
    "Lamps, Furnishing cards) and confirmed non-furniture (wall art, mirrors, clocks, spiritual/pooja, "
    "lighting, textiles) except a duplicate-link 'Home Temples' node already seen elsewhere - matches "
    "the prior Home-Decor pass's own exclusion of this same department. Excluded per Rule 3/1: pure "
    "'View All'/hub landing pages that returned no apiResData.product_count and type:'information' "
    "in __NEXT_DATA__ (verified pattern, e.g. /sofas, /sofa-sets, /recliners, /sofa-cum-beds, "
    "/wardrobes, /beds, /chairs, /tables, /dining-table-sets, /kitchen-furniture, /bar-furniture, "
    "/study-tables, /home-temple) - these were kept ONLY as grouping rows (qty null, link null), never "
    "as leaves, since a real browser fetch confirmed they carry no product count and are marketing/room "
    "landing pages, not product listings - this differs from superficially similar 'All X' nodes such "
    "as /all-chairs, /all-recliners, /all-sofa-cum-beds, /all-wardrobes, /all-beds and /all-study-tables "
    "which DID return real, distinct apiResData counts and were kept as leaves. 'Home Temples' (religious "
    "pooja-mandir furniture, /home-temple) excluded - it is also a no-count landing page, consistent with "
    "the prior pass's finding that this node is mostly dead/marketing. Textile/bedding/mattress/kitchenware "
    "items interleaved in furniture-department menus were dropped per Rule 1 (Sofa/Chair/Table Covers, "
    "Cushion items, Rugs & Carpets, Table Runners/Mats/Linen, Bedsheets, Pillows, Serveware, Cutlery "
    "Holders, Chopping Boards, Tissue Box). Artificial Flowers/Plants under Outdoor>Home Garden excluded "
    "per the artificial-plant rule. Duplicate URLs reached via more than one menu path (e.g. Chest of "
    "Drawers, Cabinet & Sideboards, Bedside Tables, Dressing Tables, Trunk & Blanket Box, Bookshelves/"
    "Office Bookcases, Wall Shelves, Kitchen Cabinets/Racks/Trolleys/Microwave Stand, Bar Cabinets/"
    "Trolleys, Outdoor Sofas, Swing Chairs) were recorded exactly once, filed under the department where "
    "they most naturally belong. 'Wooden Wall Shelf & Racks' (/wall-shelves) is genuinely ambiguous - it "
    "sits in three different furniture-storage menus AND in the Wall Decor department; kept as furniture "
    "with a MANUAL REVIEW flag per the shelving-line rule. 'Room Dividers' is also cross-listed under Wall "
    "Decor but is unambiguously a physical furniture partition, so kept without a flag. 'All Chairs' (215) "
    "sits close to but not exactly the sum of its own sibling chair-type rows (~232), so both were kept as "
    "independently-reported rows per the Ceiling/Pendant-Lights precedent from a prior batch, flagged for "
    "the record. 'Dining Chairs' (60) similarly has its own distinct product_count larger than the sum of "
    "its two material children (Wooden 14 + Fabric 22 = 36), so all three were kept as siblings rather than "
    "treating the parent as a pure grouping row. Sanity checks: every count above was read straight off "
    "each URL's own apiResData.data.product_count without ever reusing a number across categories; no "
    "count is a suspiciously round display cap; h1/name field in the same JSON payload was cross-checked "
    "against the slug for every row to guard against a mis-served parent listing. Categories outside "
    "Furniture scope entirely absent from the mega-menu (never checked further): none - the whole desktop "
    "menu was walked."
)

data = {
    "sr": 231,
    "company": "WoodenStreet",
    "brand_site": "woodenstreet.com",
    "country": "India",
    "site_url": "https://www.woodenstreet.com/",
    "status": "ok",
    "failure_reason": None,
    "notes": notes,
    "rows": rows,
}

out_path = r"C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\furniture_json_archive\f231.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

leaf_count = sum(1 for r in rows if not r["is_group"])
group_count = sum(1 for r in rows if r["is_group"])
null_qty = sum(1 for r in rows if not r["is_group"] and r["qty"] is None)
flagged = sum(1 for r in rows if r["flag"])
print("leaf_count", leaf_count)
print("group_count", group_count)
print("null_qty", null_qty)
print("flagged", flagged)
print("total_rows", len(rows))
