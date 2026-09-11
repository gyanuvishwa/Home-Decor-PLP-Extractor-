# -*- coding: utf-8 -*-
import json

def grow(name, cat="Textile"):
    return {"category": cat, "sub_category": name, "qty": None, "link": None,
            "is_group": True, "evidence": None, "flag": None, "confidence": "HIGH"}

def row(cat, name, qty, link, conf, evidence, flag=None):
    return {"category": cat, "sub_category": name, "qty": qty, "link": link,
            "is_group": False, "evidence": evidence, "flag": flag, "confidence": conf}

EV = lambda n: f"Category listing page state (cx-state.product.search.results.pagination.totalResults) = {n}"

textile_rows = []

# Group: Futon & Bedding
textile_rows.append(grow("Futon & Bedding"))
textile_rows += [
 row("Textile","Cool-Touch Bedding (N-Cool)",91,"https://www.nitori-net.jp/ec/cat/Shingu/Ncool/1/","HIGH",EV(91)),
 row("Textile","Mattress Pads & Bed Pads",116,"https://www.nitori-net.jp/ec/cat/Shingu/PadSikiBed/1/","HIGH",EV(116)),
 row("Textile","Fitted Sheets, Bed Sheets & Futon Mattress Covers",96,"https://www.nitori-net.jp/ec/cat/Shingu/Boxsheet_FutonSikiSheet/1/","HIGH",EV(96)),
 row("Textile","Futon Mattress & Folding Mattress",74,"https://www.nitori-net.jp/ec/cat/Shingu/futonsiki-mattressfolding/1/","MEDIUM",EV(74),"Borders Mattress/Furniture boundary; included as Japanese-style padded futon bedding, not a rigid spring mattress"),
 row("Textile","Duvet Covers",195,"https://www.nitori-net.jp/ec/cat/Shingu/FutonKakeCover/1/","HIGH",EV(195)),
 row("Textile","Duvets, Down Duvets, Blankets & Throws",221,"https://www.nitori-net.jp/ec/cat/Shingu/FutonKakeseries/1/","HIGH",EV(221)),
 row("Textile","Pillows & Body Pillows",142,"https://www.nitori-net.jp/ec/cat/Shingu/Pillow/1/","MEDIUM",EV(142),"Sleep pillows not explicitly named in rules.md bedding list but closely analogous to included Duvets/Comforters"),
 row("Textile","Pillowcases",298,"https://www.nitori-net.jp/ec/cat/Shingu/PillowCover/1/","HIGH",EV(298)),
 row("Textile","Bedding Sets",40,"https://www.nitori-net.jp/ec/cat/Shingu/FutonSet/1/","HIGH",EV(40)),
 row("Textile","Duvet Cover & Bed Cover Sets",21,"https://www.nitori-net.jp/ec/cat/Shingu/CoveringSet/1/","HIGH",EV(21)),
 row("Textile","Kids Beds & Futons",27,"https://www.nitori-net.jp/ec/cat/Shingu/m1KidsShingu/1/","MEDIUM",EV(27),"Mixed beds(furniture)+futons(textile) naming; kept as textile per site's bedding-group placement"),
 row("Textile","Wearable Blankets",37,"https://www.nitori-net.jp/ec/cat/Shingu/m1BlanketWears/1/","MEDIUM",EV(37)),
 row("Textile","Warm Bedding (N-Warm)",59,"https://www.nitori-net.jp/ec/cat/Shingu/Nwarm/1/","HIGH",EV(59)),
]

# Group: Curtains
textile_rows.append(grow("Curtains"))
textile_rows += [
 row("Textile","Drape Curtains",534,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtain/1/","HIGH",EV(534)),
 row("Textile","Blackout Curtains",519,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainLightshiel/1/","HIGH",EV(519)),
 row("Textile","Lace Curtains",199,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/LaceCurtain/1/","HIGH",EV(199)),
 row("Textile","Curtain & Lace Sets",114,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/CurtainLaceSet/1/","HIGH",EV(114)),
 row("Textile","Roll Screens & Roll Curtains",40,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/RollScreen/1/","MEDIUM",EV(40)),
 row("Textile","Jacquard Curtains",89,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainjacquard/1/","HIGH",EV(89)),
 row("Textile","Made-to-Order Curtains",290,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/OrdCurtain/1/","HIGH",EV(290)),
 row("Textile","Made-to-Order Lace Curtains",91,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/OrdLacecurtain/1/","HIGH",EV(91)),
 row("Textile","Made-to-Order Roll Screens",233,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/OrderRollScreen/1/","MEDIUM",EV(233)),
 row("Textile","Cafe Curtains & Bay Window Curtains",61,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/CafeCurtainCafe/1/","HIGH",EV(61)),
 row("Textile","Noren Door Curtains, Sudare & Room Dividers",64,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/Noren/1/","MEDIUM",EV(64),"Mixed with non-textile sudare/partition items"),
 row("Textile","Shade Curtains",57,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/Screen/1/","MEDIUM",EV(57)),
 row("Textile","Shower Curtains",4,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/m1BathArticleShowercurt/1/","HIGH",EV(4)),
 row("Textile","Heat-Shielding Curtains",409,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainHeatshield/1/","HIGH",EV(409)),
 row("Textile","Soundproof Curtains",65,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainSoundproofing/1/","HIGH",EV(65)),
 row("Textile","Deodorizing Curtains",8,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainDeodorize/1/","HIGH",EV(8)),
 row("Textile","Fireproof Curtains",137,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainFireretard/1/","HIGH",EV(137)),
 row("Textile","Pollen-Blocking Curtains",6,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainPollencatch/1/","HIGH",EV(6)),
 row("Textile","Easy-Order Curtains",362,"https://www.nitori-net.jp/ec/cat/CurtainRailBlind/EOCurtain/1/","HIGH",EV(362)),
]

# Group: Carpets, Rugs & Mats
textile_rows.append(grow("Carpets, Rugs & Mats"))
textile_rows += [
 row("Textile","Cool-Touch Rugs (N-Cool)",10,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/Cooling_contact_rug/1/","HIGH",EV(10)),
 row("Textile","Rugs",395,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/Rug/1/","HIGH",EV(395)),
 row("Textile","Thick Rugs",59,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/ThickRug/1/","HIGH",EV(59)),
 row("Textile","Carpets",67,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/Carpet/1/","HIGH",EV(67)),
 row("Textile","Carpet Tiles & Adhesive Tile Mats",41,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/JointMatTileCarpetTile-adhesive-tilemat/1/","MEDIUM",EV(41)),
 row("Textile","Natural Fiber Rugs & Tatami Units",130,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/Tatami/1/","MEDIUM",EV(130)),
 row("Textile","Floor Mats",174,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/FloorMatEntranceLong/1/","HIGH",EV(174)),
 row("Textile","Kitchen Mats",125,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/FloorMat/1/","HIGH",EV(125)),
 row("Textile","Entrance Mats",71,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/FloorMatEntranceEntrance/1/","HIGH",EV(71)),
 row("Textile","Stair Mats & Soundproof Mats",7,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/SoundproofSlipSheetSound/1/","MEDIUM",EV(7)),
 row("Textile","Door Mats",13,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/FloorMatEntranceDoor/1/","HIGH",EV(13)),
 row("Textile","Warm Heat-Generating Rugs (N-Warm)",14,"https://www.nitori-net.jp/ec/cat/CarpetRugMat/NwarmRug/1/","HIGH",EV(14)),
]

# Group: Cushions & Covers
textile_rows.append(grow("Cushions & Covers"))
textile_rows += [
 row("Textile","Cool-Touch Cushions & Sofa Covers",13,"https://www.nitori-net.jp/ec/cat/Cushion/cool-cushion-sofa-cover/1/","HIGH",EV(13)),
 row("Textile","Cushion Covers",119,"https://www.nitori-net.jp/ec/cat/Cushion/CushionCover/1/","HIGH",EV(119)),
 row("Textile","Bead Cushions & Covers",62,"https://www.nitori-net.jp/ec/cat/Cushion/BeadsCushion/1/","HIGH",EV(62)),
 row("Textile","Sofa Covers",41,"https://www.nitori-net.jp/ec/cat/Cushion/SofaMultiCoverSofa/1/","HIGH",EV(41)),
 row("Textile","Squishy Cushions",35,"https://www.nitori-net.jp/ec/cat/Cushion/SheetCushionMochimochi/1/","HIGH",EV(35)),
 row("Textile","Seat Cushions & Donut Cushions",94,"https://www.nitori-net.jp/ec/cat/Cushion/SheetCushionSheetcushi/1/","HIGH",EV(94)),
 row("Textile","Long Floor Cushions & Covers",32,"https://www.nitori-net.jp/ec/cat/Cushion/ZabutonLong/1/","HIGH",EV(32)),
 row("Textile","Floor Cushions",24,"https://www.nitori-net.jp/ec/cat/Cushion/SheetCushionFloorcushi/1/","HIGH",EV(24)),
 row("Textile","Jumbo Cushions & Covers",18,"https://www.nitori-net.jp/ec/cat/Cushion/JumboCushion/1/","HIGH",EV(18)),
 row("Textile","Multi-Purpose Furniture Covers",27,"https://www.nitori-net.jp/ec/cat/Cushion/SofaMultiCoverMulti/1/","HIGH",EV(27)),
 row("Textile","Low-Rebound Cushions",13,"https://www.nitori-net.jp/ec/cat/Cushion/SheetCushionLowrepulsi/1/","HIGH",EV(13)),
 row("Textile","Floor Cushions & Covers",23,"https://www.nitori-net.jp/ec/cat/Cushion/ZabutonCoverZabuton/1/","HIGH",EV(23)),
 row("Textile","Mini Cushions",7,"https://www.nitori-net.jp/ec/cat/Cushion/CushionMinicushio/1/","HIGH",EV(7)),
 row("Textile","Cushions",38,"https://www.nitori-net.jp/ec/cat/Cushion/CushionCushion/1/","HIGH",EV(38)),
 row("Textile","Animal & Character Cushions",52,"https://www.nitori-net.jp/ec/cat/Cushion/character-animal-cushion/1/","HIGH",EV(52)),
 row("Textile","Made-to-Order Cushion Covers",209,"https://www.nitori-net.jp/ec/cat/Cushion/CushionOrder/1/","HIGH",EV(209)),
 row("Textile","Warm Cushions & Sofa Covers",34,"https://www.nitori-net.jp/ec/cat/Cushion/warm-cushion-sofa-cover/1/","HIGH",EV(34)),
]

# Group: Bath & Washroom Goods (textile)
textile_rows.append(grow("Bath & Washroom Goods"))
textile_rows += [
 row("Textile","Towels",258,"https://www.nitori-net.jp/ec/cat/BathToiletLaundry/m1Towel/1/","HIGH",EV(258)),
 row("Textile","Bath Mats",89,"https://www.nitori-net.jp/ec/cat/BathToiletLaundry/BathMat/1/","HIGH",EV(89)),
 row("Textile","Body Towels & Body Brushes",90,"https://www.nitori-net.jp/ec/cat/BathToiletLaundry/BathArticleBodycare/1/","MEDIUM",EV(90),"Mixed with non-textile body brushes"),
]

# Group: Daily Necessities (textile)
textile_rows.append(grow("Daily Necessities"))
textile_rows += [
 row("Textile","Towels",279,"https://www.nitori-net.jp/ec/cat/LifeSuppliesDailyNecessities/Towel/1/","HIGH",EV(279),"Distinct catalog/count from the Bath & Washroom Towels node; kept separately per differing totals"),
]

# Group: Baby & Kids Items (textile)
textile_rows.append(grow("Baby & Kids Items"))
textile_rows += [
 row("Textile","Baby Beds, Futons & Bedding",90,"https://www.nitori-net.jp/ec/cat/Baby/BabyBed/1/","MEDIUM",EV(90),"Mixed beds(furniture)+futons/bedding(textile) naming"),
 row("Textile","Kids Rugs & Play Mats",31,"https://www.nitori-net.jp/ec/cat/Baby/m1KidsRug/1/","MEDIUM",EV(31)),
 row("Textile","Kids Beds & Futons",25,"https://www.nitori-net.jp/ec/cat/Baby/m2KidsShingu/1/","MEDIUM",EV(25),"Mixed beds(furniture)+futons(textile) naming"),
]

storage_rows = []

# Group: Bath & Washroom Goods (storage)
storage_rows.append(grow("Bath & Washroom Goods", "Storage"))
storage_rows += [
 row("Storage","Washstand Racks & Washroom Storage",56,"https://www.nitori-net.jp/ec/cat/BathToiletLaundry/LaundryToiletArticleStorage/1/","HIGH",EV(56)),
 row("Storage","Magnetic Bathroom & Washroom Storage",90,"https://www.nitori-net.jp/ec/cat/BathToiletLaundry/MagnetBathLaundry/1/","HIGH",EV(90)),
 row("Storage","Bathroom Racks & Bathroom Storage",109,"https://www.nitori-net.jp/ec/cat/BathToiletLaundry/BathArticleStorage/1/","HIGH",EV(109)),
 row("Storage","Tension Rods & Shelves",18,"https://www.nitori-net.jp/ec/cat/BathToiletLaundry/m1ShelfStrutRack_Strut/1/","HIGH",EV(18)),
]

# Group: Laundry Goods (storage)
storage_rows.append(grow("Laundry Goods", "Storage"))
storage_rows += [
 row("Storage","Laundry Racks & Washing Machine Racks",67,"https://www.nitori-net.jp/ec/cat/Laundry/ShelfStrutRackRack/1/","HIGH",EV(67)),
 row("Storage","Laundry Storage",107,"https://www.nitori-net.jp/ec/cat/Laundry/CreviceStorage/1/","HIGH",EV(107)),
 row("Storage","Laundry Baskets",76,"https://www.nitori-net.jp/ec/cat/Laundry/LaundryBasket/1/","HIGH",EV(76)),
]

# Group: Storage Furniture
storage_rows.append(grow("Storage Furniture", "Storage"))
storage_rows += [
 row("Storage","Chests & Drawers",275,"https://www.nitori-net.jp/ec/cat/Storage-Furniture/Chest/1/","MEDIUM",EV(275)),
 row("Storage","Closets & Wardrobes",162,"https://www.nitori-net.jp/ec/cat/Storage-Furniture/WardrobeLocker/1/","HIGH",EV(162)),
 row("Storage","Hanger Racks & Pole Hangers",94,"https://www.nitori-net.jp/ec/cat/Storage-Furniture/HangarRack/1/","HIGH",EV(94)),
 row("Storage","Dressers & Vanities",49,"https://www.nitori-net.jp/ec/cat/Storage-Furniture/Dresser/1/","MEDIUM",EV(49)),
 row("Storage","Entryway Storage",71,"https://www.nitori-net.jp/ec/cat/Storage-Furniture/EntranceStorage/1/","HIGH",EV(71)),
 row("Storage","Made-to-Order Storage",None,"https://www.nitori-net.jp/ec/cat/Storage-Furniture/f2Orderstorage/1/","LOW",None,"MANUAL REVIEW: page loaded (h1 matches) but no product-search pagination state present - appears to be a made-to-order configurator page without a standard listing count"),
 row("Storage","Living Room Chests",59,"https://www.nitori-net.jp/ec/cat/Storage-Furniture/m1LivingStorageCabinet/1/","MEDIUM",EV(59)),
 row("Storage","Kids Storage Furniture",93,"https://www.nitori-net.jp/ec/cat/Storage-Furniture/m1KidsStorageFurniture/1/","MEDIUM",EV(93)),
]

# Group: Storage Cases & Clothing Organizers
storage_rows.append(grow("Storage Cases & Clothing Organizers", "Storage"))
storage_rows += [
 row("Storage","Clothing Storage Cases",79,"https://www.nitori-net.jp/ec/cat/StorageRackDresser/ClothingCase/1/","HIGH",EV(79)),
 row("Storage","Plastic Chests",24,"https://www.nitori-net.jp/ec/cat/StorageRackDresser/ClothingCaseLiving/1/","HIGH",EV(24)),
 row("Storage","Storage Boxes, Baskets & Bins",175,"https://www.nitori-net.jp/ec/cat/StorageRackDresser/StorageBasket/1/","HIGH",EV(175)),
 row("Storage","Storage Bags & Compression Bags",84,"https://www.nitori-net.jp/ec/cat/StorageRackDresser/StorageBag/1/","HIGH",EV(84)),
 row("Storage","Slatted Boards & Closet Shelves",35,"https://www.nitori-net.jp/ec/cat/StorageRackDresser/Futondaiosiiresunoko/1/","MEDIUM",EV(35)),
 row("Storage","Storage Dividers & Small Item Storage",68,"https://www.nitori-net.jp/ec/cat/StorageRackDresser/StorageStorage/1/","HIGH",EV(68)),
 row("Storage","Collection Cases, Makeup & Jewelry Boxes",159,"https://www.nitori-net.jp/ec/cat/StorageRackDresser/Accessorybox/1/","HIGH",EV(159)),
 row("Storage","Tension Rods & Shelves",19,"https://www.nitori-net.jp/ec/cat/StorageRackDresser/ShelfStrutRackStrut/1/","HIGH",EV(19)),
]

# Group: Bookshelves, Racks & Shelves
storage_rows.append(grow("Bookshelves, Racks & Shelves", "Storage"))
storage_rows += [
 row("Storage","N-Polder Storage Shelving",111,"https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/Npolder/1/","HIGH",EV(111)),
 row("Storage","Cube Storage Boxes",62,"https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/ColorBox/1/","HIGH",EV(62)),
 row("Storage","Steel Racks & Steel Shelves",127,"https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/RackShelfMetal/1/","HIGH",EV(127)),
 row("Storage","Wood Shelves & Wood Racks",139,"https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/RackShelfWood/1/","MEDIUM",EV(139)),
 row("Storage","Storage Boxes",161,"https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/m1Storagebasket/1/","HIGH",EV(161)),
 row("Storage","Tension Pole Storage",41,"https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/tensionWallStorage/1/","HIGH",EV(41)),
 row("Storage","Collection Cases",38,"https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/InteriorArticleDisplaybox/1/","MEDIUM",EV(38)),
 row("Storage","Made-to-Order Storage",None,"https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/f1Orderstorage/1/","LOW",None,"MANUAL REVIEW: page loaded (h1 matches) but no product-search pagination state present - appears to be a made-to-order configurator page without a standard listing count"),
 row("Storage","Semi-Custom Racks",72,"https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/SemiOrderrack/1/","HIGH",EV(72)),
]

# Group: Kitchen Organization & Storage
storage_rows.append(grow("Kitchen Organization & Storage", "Storage"))
storage_rows += [
 row("Storage","Kitchen Wagons & Gap Storage",79,"https://www.nitori-net.jp/ec/cat/KitchenStorage/KDKitchenStorageWagon/1/","HIGH",EV(79)),
 row("Storage","Under-Sink & Under-Stove Storage",72,"https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenSink/1/","HIGH",EV(72)),
 row("Storage","Drawer Organizers & Cutlery Storage",47,"https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenAccessorie/1/","HIGH",EV(47)),
 row("Storage","Refrigerator Storage",64,"https://www.nitori-net.jp/ec/cat/KitchenStorage/RefrigeratorStorage/1/","HIGH",EV(64)),
 row("Storage","Dish Drainer Baskets, Racks & Mats",115,"https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenBucket/1/","MEDIUM",EV(115)),
 row("Storage","Magnetic Storage & Wall Organization",75,"https://www.nitori-net.jp/ec/cat/KitchenStorage/MagnetKitchenStorage/1/","HIGH",EV(75)),
 row("Storage","Kitchen Racks & Storage Shelves",66,"https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenRack/1/","HIGH",EV(66)),
 row("Storage","Hanging Cabinet Storage & Other",79,"https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenStorageOther/1/","HIGH",EV(79)),
]

# Group: TV Stands & Living Room Storage
storage_rows.append(grow("TV Stands & Living Room Storage", "Storage"))
storage_rows += [
 row("Storage","Living Room Sideboards & Cabinets",203,"https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/LivingStorageSideboard/1/","MEDIUM",EV(203)),
 row("Storage","Living Room Chests",74,"https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/LivingStorageCabinet/1/","MEDIUM",EV(74)),
 row("Storage","Display Racks",51,"https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/LivingStorageDisplayrac/1/","MEDIUM",EV(51)),
 row("Storage","CD & DVD Racks",8,"https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/LivingStorageCddvd/1/","HIGH",EV(8)),
 row("Storage","Magazine Racks",12,"https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/StorageMagazinera/1/","HIGH",EV(12)),
 row("Storage","Remote Control Cases",7,"https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/StorageRemote/1/","MEDIUM",EV(7)),
]

# Group: Desks & Office Chairs
storage_rows.append(grow("Desks & Office Chairs", "Storage"))
storage_rows += [
 row("Storage","Desk-Side Storage Wagons",131,"https://www.nitori-net.jp/ec/cat/Desk-Officechair/WagonRack/1/","MEDIUM",EV(131)),
]

notes = (
 "ACCESS: tier(a) direct HTTP fetch (requests) worked for the SSR shell but the homepage mega-menu is "
 "client-rendered (Angular/SAP Commerce Spartacus storefront) with no links in the raw HTML, so the top-level "
 "category list+hrefs were read from the live DOM via Claude-in-Chrome (tier c) after tier(b) Playwright failed "
 "at the network level (ERR_HTTP2_PROTOCOL_ERROR / connection hangs on every attempt, both default and with "
 "--disable-http2, while plain HTTP/1.1 requests to the same host succeeded every time - a host-specific "
 "HTTP/2 negotiation failure in this machine's Chromium network stack, not an anti-bot block). All subsequent "
 "category/subcategory tree traversal and quantity extraction used tier(a) direct HTTP fetch: individual "
 "category pages ARE server-side rendered by the storefront and embed a JSON state blob "
 "(script#nitoristore-state) containing cx-state.product.search.results.pagination.totalResults - this is the "
 "site's own authoritative product count for that exact category node, confirmed against the page's own h1 for "
 "every leaf recorded. "
 "TREE: built from the live homepage category flyout (36 top-level nodes) + each relevant top-level category "
 "page's own sub-category chip strip (a.categories-link), stopping at this 2nd level, which corresponds 1:1 to "
 "distinct product-type categories (e.g. Duvet Covers, Curtains variants, Storage Boxes); deeper chip levels "
 "seen on a few pages (e.g. under Duvet Covers: Cool-material/Plain/Patterned/Warm-material) are material/pattern "
 "filter facets on the same product type, not distinct categories, and were not descended into. "
 "QTY: site's own pagination.totalResults per leaf category page, evidence string records the exact JSON path. "
 "EXCLUDED: hardware (curtain rails/rods, blinds, curtain accessories/hooks), bathroom fixtures (soap "
 "dispensers, wash basins, shower heads, bath chairs, weight scales, towel rails), trash bins/dust boxes, "
 "cleaning tools (mops/brooms/buckets/sponges - entire 掃除道具 top category), pure decorative/interior goods "
 "(vases, candles, mirrors, photo frames, artificial plants - entire インテリア雑貨 top category incl. its "
 "WallInterior sub-branch, which was checked and contains only posters/mirrors/wallpaper/hooks, no textile wall "
 "hangings), pure furniture (beds, sofas, tables, chairs, desks, TV stands, bookcases, Buddhist "
 "altars/butsudan), apparel/toys/pet items, laundry equipment (drying racks/poles/clothespins/ironing boards), "
 "and two URLs (Storage-Furniture/f2wallstorage and TvStandLivingStorage/f1wallstorage) that silently resolved "
 "to a promotional 'Wall Storage Feature' campaign page instead of a real category listing (h1 mismatch, no "
 "product-search state) - dropped per the no-View-All/no-promotional-page rule. "
 "TvStandLivingStorage/f1middleboardporte ('Modular Cabinets' chip) silently resolved to a single product detail "
 "page (h1 = a specific product model name) - dropped as a bad slug per the brief's warning. "
 "DUPLICATES: Cushion/JumboCushion vs Shingu/m1JumboCushion, and Cushion/SofaMultiCoverMulti vs "
 "Shingu/m1SofaMultiCoverMulti, each resolved to identical totals under two different nav paths - kept once "
 "under the Cushions & Covers group, dropped from Futon & Bedding. CurtainRailBlind/m1BathArticleShowercurt vs "
 "BathToiletLaundry/BathArticleShowercurt both resolved to identical h1='Shower Curtains' and total=4 - kept "
 "once under Curtains, dropped the Bath duplicate. The two 'Towels' nodes (BathToiletLaundry/m1Towel=258 and "
 "LifeSuppliesDailyNecessities/Towel=279) and the two 'Kids Beds & Futons' nodes (Shingu=27, Baby=25) have "
 "different URLs AND different totals, so both were kept as genuinely distinct listing pages per the "
 "duplicate rule's carve-out. Two 'Made-to-Order Storage' nodes (under Storage Furniture and under Bookshelves/"
 "Racks/Shelves) loaded successfully (h1 matched) but returned no product-search pagination state, consistent "
 "with a made-to-order configurator rather than a standard listing - recorded with qty=null and a MANUAL REVIEW "
 "flag per the brief rather than fabricating a number. "
 "AMBIGUOUS/MEDIUM-confidence inclusions (kept per closest rule analogy, flagged MEDIUM): sleep pillows (not "
 "explicitly named in textile.md's bedding list but directly analogous to included Duvets/Comforters), "
 "shikibuton/folding-mattress (Japanese padded floor futon vs a rigid Western mattress), several "
 "'Kids Bed & Futon' and 'Baby Bed, Futon & Bedding' nodes that mix a furniture noun (bed) with a textile noun "
 "(futon/bedding) in one site category name, storage furniture pieces (chests, dressers, living-room "
 "sideboards/chests, display racks) that sit under an explicitly storage-labeled top-level nav item but are "
 "furniture-adjacent per storage.md's own boundary guidance."
)

data = {
 "sr": 177,
 "company": "Nitori Japan",
 "brand_site": "nitori-net.jp",
 "country": "Japan",
 "site_url": "https://www.nitori-net.jp/ec/",
 "status": "ok",
 "failure_reason": None,
 "notes": notes,
 "textile_rows": textile_rows,
 "storage_rows": storage_rows,
}

with open("ts177.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print("textile rows:", len(textile_rows), "storage rows:", len(storage_rows))
