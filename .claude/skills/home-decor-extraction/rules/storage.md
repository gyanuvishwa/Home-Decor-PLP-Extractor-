############################################################
# CATEGORY RULES: STORAGE EXTRACTION
############################################################

This file defines ONLY the category-specific rules for STORAGE.

The master Home Decor Extraction Skill controls:

- company manifest
- company processing
- batching
- progress tracking
- category-specific cache
- continuation/resume
- duplicate prevention
- Excel generation
- formatting
- reconciliation
- validation framework
- blocked website handling
- token optimization

When the user says:

"Extract Storage"

load and apply THESE rules.

Do not apply Furniture, Lighting, Kitchen & Dining, Textile,
Wall Decor, Decorative Home Accessories, or Bathroom rules unless
required to resolve an ambiguity.

============================================================
1. OBJECTIVE
============================================================

Extract genuine STORAGE products and storage-related categories from
the websites of all companies in the active company manifest.

For every valid Storage category/subcategory, capture:

- Company Name
- Brand Site
- Country
- Site URL
- Category
- Sub-Category
- Type
- Qty
- Link

Create:

Storage.xlsx

The output must follow the established workbook structure.

============================================================
2. CORE CLASSIFICATION PRINCIPLE
============================================================

Use:

PRIMARY PRODUCT TYPE
        >
PRIMARY FUNCTION
        >
WEBSITE CATEGORY HIERARCHY
        >
ROOM / LOCATION

The product's primary purpose must be STORAGE.

Do not classify something as Storage simply because it is located in a
"Storage", "Utility", "Bedroom", "Kitchen", "Bathroom", "Office", or
"Home Organization" section.

The actual product must primarily provide storage, containment,
organization, shelving, or storage-related utility.

============================================================
3. MAIN STORAGE GROUPS
============================================================

Include genuine storage categories such as:

- Storage
- Home Storage
- Storage Solutions
- Home Organization
- Organization
- Storage & Organization
- Storage Furniture
- Storage Accessories
- Organizers

Only include the category when the products underneath genuinely
serve a storage/organization purpose.

============================================================
4. STORAGE BOXES & CONTAINERS
============================================================

Include:

- Storage Boxes
- Storage Bins
- Storage Containers
- Storage Tubs
- Storage Crates
- Storage Cases
- Storage Trunks
- Storage Chests
- Decorative Storage Boxes
- Fabric Storage Boxes
- Folding Storage Boxes
- Stackable Storage Boxes
- Under-Bed Storage Boxes
- Under-Bed Storage Containers
- Toy Storage Boxes
- Toy Storage Containers
- Document Storage Boxes
- Shoe Storage Boxes
- Clothes Storage Boxes

Also include clearly identified variations such as:

- Lidded Storage Boxes
- Clear Storage Boxes
- Plastic Storage Boxes
- Wooden Storage Boxes
- Woven Storage Boxes

provided that the primary purpose is storage.

============================================================
5. STORAGE BASKETS
============================================================

Include:

- Storage Baskets
- Woven Storage Baskets
- Rattan Storage Baskets
- Cane Storage Baskets
- Bamboo Storage Baskets
- Seagrass Storage Baskets
- Fabric Storage Baskets
- Wire Storage Baskets
- Decorative Storage Baskets
- Laundry Baskets
- Toy Baskets
- Blanket Baskets
- Clothes Baskets
- Bathroom Storage Baskets
- Kitchen Storage Baskets

IMPORTANT:

A decorative basket with no meaningful storage function should be
classified according to its actual website category.

Do not automatically classify every basket as Storage.

Primary purpose and website hierarchy decide.

============================================================
6. STORAGE BAGS & POUCHES
============================================================

Include home-use storage products such as:

- Storage Bags
- Clothes Storage Bags
- Bedding Storage Bags
- Blanket Storage Bags
- Shoe Storage Bags
- Under-Bed Storage Bags
- Vacuum Storage Bags
- Fabric Storage Bags
- Laundry Bags
- Garment Storage Bags
- Toy Storage Bags

Exclude fashion/lifestyle bags whose primary purpose is personal
carrying rather than home storage.

Examples:

Handbag
→ NOT Storage

Tote Bag
→ NOT Storage

Travel Bag
→ NOT Storage

Clothes Storage Bag
→ Storage

Bedding Storage Bag
→ Storage

============================================================
7. ORGANIZERS
============================================================

Include genuine home organizers:

- Home Organizers
- Storage Organizers
- Drawer Organizers
- Closet Organizers
- Wardrobe Organizers
- Shelf Organizers
- Cabinet Organizers
- Desk Organizers
- Makeup Organizers
- Jewellery Organizers
- Jewelry Organizers
- Shoe Organizers
- Clothes Organizers
- Toy Organizers
- Bathroom Organizers
- Kitchen Organizers
- Pantry Organizers
- Office Organizers
- File Organizers
- Document Organizers

The product must primarily provide organization/storage.

============================================================
8. DRAWER STORAGE
============================================================

Include:

- Drawer Organizers
- Drawer Dividers
- Drawer Storage
- Drawer Trays
- Drawer Inserts
- Cutlery Organizers
- Clothing Drawer Organizers
- Jewellery Drawer Organizers
- Makeup Drawer Organizers

Do NOT automatically include decorative trays.

Example:

Decorative Serving Tray
→ Kitchen & Dining / Decorative Home Accessories

Drawer Organizer
→ Storage

============================================================
9. CLOSET & WARDROBE STORAGE
============================================================

Include:

- Closet Storage
- Wardrobe Storage
- Closet Organizers
- Wardrobe Organizers
- Hanging Organizers
- Clothes Organizers
- Shoe Organizers
- Garment Organizers
- Closet Baskets
- Closet Boxes
- Wardrobe Boxes
- Hanging Storage
- Clothing Storage

Include modular organization systems when their primary purpose is
storage.

============================================================
10. SHOE STORAGE
============================================================

Include:

- Shoe Storage
- Shoe Racks
- Shoe Organizers
- Shoe Cabinets
- Shoe Shelves
- Shoe Storage Benches when primarily sold as storage furniture
- Shoe Boxes
- Shoe Storage Boxes
- Shoe Cubbies

Important:

A shoe rack/cabinet is Storage when its primary purpose is storing
shoes.

============================================================
11. LAUNDRY STORAGE
============================================================

Include:

- Laundry Baskets
- Laundry Hampers
- Laundry Bags
- Laundry Sorters
- Laundry Storage
- Clothes Hampers
- Clothes Baskets
- Laundry Organizers
- Laundry Cabinets when primarily storage

Do not include:

- Washing Machines
- Dryers
- Irons
- Ironing Boards

unless the actual category is specifically a storage product.

============================================================
12. TOY STORAGE
============================================================

Include:

- Toy Storage
- Toy Boxes
- Toy Bins
- Toy Baskets
- Toy Organizers
- Toy Storage Units
- Children's Storage
- Playroom Storage
- Kids' Storage

Do not include toys themselves.

============================================================
13. KITCHEN / PANTRY STORAGE
============================================================

Include storage products whose primary purpose is kitchen/pantry
organization:

- Pantry Storage
- Pantry Organizers
- Food Storage Containers
- Kitchen Storage Containers
- Kitchen Storage Baskets
- Kitchen Organizers
- Spice Organizers
- Cabinet Organizers
- Drawer Organizers
- Shelf Organizers
- Food Storage Jars when primarily marketed as storage
- Container Sets when primarily storage-oriented

IMPORTANT BOUNDARY:

Kitchen & Dining products are NOT automatically Storage.

Examples:

Plate
→ Kitchen & Dining

Bowl
→ Kitchen & Dining

Glass
→ Kitchen & Dining

Serving Tray
→ Kitchen & Dining / Decorative Home Accessories

Food Storage Container
→ Storage

Pantry Organizer
→ Storage

Kitchen Drawer Organizer
→ Storage

============================================================
14. BATHROOM STORAGE
============================================================

Include genuine bathroom storage products:

- Bathroom Storage
- Bathroom Organizers
- Bathroom Storage Baskets
- Bathroom Storage Boxes
- Bathroom Storage Cabinets
- Bathroom Shelving Units
- Bathroom Storage Units
- Under-Sink Storage
- Toilet Storage Cabinets
- Bathroom Caddies
- Shower Caddies
- Bathroom Organizers
- Vanity Organizers
- Bathroom Drawer Organizers

IMPORTANT:

Bathroom is a location, not the classification itself.

Include only products whose primary purpose is storage/organization.

Do NOT include:

- Bathroom Mirrors
- Bathroom Lighting
- Toilets
- Sinks
- Bathtubs
- Showers
- Faucets
- Bathroom Fixtures

Bathroom Furniture must be handled according to the Furniture task
when the product is genuinely furniture.

============================================================
15. OFFICE STORAGE
============================================================

Include:

- Office Storage
- Filing Cabinets
- File Storage
- Document Storage
- Office Organizers
- Desk Organizers
- File Organizers
- Storage Cabinets
- Office Shelving
- Office Storage Boxes
- Document Boxes

IMPORTANT:

If the product is primarily an office furniture product, use the
Furniture rules.

Example:

Office Filing Cabinet
→ Storage or Furniture depending on the website's primary category
and product purpose.

If the site explicitly places it under Office Furniture, prefer
Furniture.

If explicitly placed under Office Storage/Organization, use Storage.

============================================================
16. LIVING ROOM STORAGE
============================================================

Include:

- Living Room Storage
- Storage Baskets
- Storage Boxes
- Media Storage
- Storage Cabinets
- Storage Units
- Toy Storage
- Blanket Storage
- Magazine Storage
- Book Storage

Furniture boundary:

TV Unit
Console Cabinet
Sideboard
Bookcase

may be Furniture when clearly sold as furniture.

Do NOT automatically classify every cabinet, shelf, or unit as Storage.

Use the website hierarchy and primary product purpose.

============================================================
17. BEDROOM STORAGE
============================================================

Include:

- Bedroom Storage
- Under-Bed Storage
- Wardrobe Organizers
- Clothes Storage
- Shoe Storage
- Bedding Storage
- Blanket Storage
- Storage Boxes
- Storage Baskets
- Closet Organizers
- Drawer Organizers

Furniture examples such as:

- Wardrobe
- Dresser
- Chest of Drawers
- Bedside Cabinet

require careful classification.

If the website explicitly categorizes them as Furniture/Bedroom
Furniture, they belong to Furniture.

If they are explicitly presented as Storage products, they may be
included in Storage.

============================================================
18. SHELVING
============================================================

Shelving is a major ambiguity.

Do NOT automatically classify every shelf as Storage.

INCLUDE when clearly intended as storage/organization:

- Storage Shelves
- Storage Shelving
- Freestanding Storage Shelves
- Utility Shelving
- Garage Storage Shelving
- Closet Shelving
- Pantry Shelving
- Storage Racks
- Storage Shelf Units

Furniture boundary:

Bookcase
Bookshelf
Display Cabinet
Display Shelving

may belong to Furniture depending on the website hierarchy and product
presentation.

Wall Decor boundary:

Decorative Wall Shelf
Floating Decorative Shelf
Wall Decor Shelf
Wall Ledge

may belong to Wall Decor.

Use:

WEBSITE CATEGORY
+
PRODUCT PURPOSE
+
PRODUCT PRESENTATION

Do not classify by the word "shelf" alone.

============================================================
19. RACKS
============================================================

Include racks whose primary purpose is storage/organization:

- Storage Racks
- Shoe Racks
- Clothes Racks
- Kitchen Storage Racks
- Bathroom Storage Racks
- Pantry Racks
- Utility Racks
- Towel Storage Racks
- Magazine Racks
- Storage Carts/Racks

Do NOT include decorative wall racks simply because they can hold
objects.

If primarily decorative:

→ Decorative Home Accessories / Wall Decor

If primarily storage:

→ Storage

============================================================
20. STORAGE CARTS & TROLLEYS
============================================================

Include:

- Storage Carts
- Utility Carts
- Storage Trolleys
- Rolling Storage
- Rolling Carts
- Kitchen Storage Carts
- Bathroom Storage Carts
- Office Storage Carts

Do not include serving carts if their primary purpose is serving/dining
rather than storage.

============================================================
21. STORAGE FURNITURE BOUNDARY
============================================================

Storage furniture requires careful classification.

Potential Furniture:

- Wardrobes
- Dressers
- Chests of Drawers
- Sideboards
- Cabinets
- Bookcases
- TV Units
- Console Units
- Display Cabinets

Potential Storage:

- Storage Cabinets
- Storage Units
- Storage Shelves
- Storage Racks
- Storage Organizers

RULE:

If the website explicitly places the product inside a Furniture
category, prefer Furniture.

If explicitly placed inside a Storage/Organization category, prefer
Storage.

Do not override a clear website category hierarchy without strong
evidence.

============================================================
22. MATERIAL RULE
============================================================

Storage can be made from any material.

Include:

- Wood
- Metal
- Steel
- Iron
- Aluminium
- Plastic
- Acrylic
- Glass
- Rattan
- Cane
- Bamboo
- Fabric
- Cotton
- Wicker
- Seagrass
- Jute
- Resin
- Composite materials

Material does NOT determine whether the product is Storage.

Example:

Wooden Storage Box
→ Storage

Metal Storage Rack
→ Storage

Rattan Storage Basket
→ Storage

Plastic Storage Bin
→ Storage

============================================================
23. DECORATIVE VS STORAGE
============================================================

Do not classify a product as Storage merely because it can technically
hold something.

Primary purpose matters.

Examples:

Decorative Bowl
→ NOT Storage

Decorative Tray
→ NOT Storage

Vase
→ NOT Storage

Sculpture
→ NOT Storage

Decorative Basket
→ depends on website classification and primary purpose

Storage Basket
→ Storage

Storage Box
→ Storage

Organizer
→ Storage

============================================================
24. HOME ACCESSORIES BOUNDARY
============================================================

Exclude purely decorative products:

- Vases
- Sculptures
- Figurines
- Candle Holders
- Decorative Objects
- Decorative Bowls
- Decorative Trays
- Photo Frames
- Ornaments
- Planters
- Decorative Accessories

Even if these products can technically contain or hold objects, they
are NOT Storage unless their primary purpose is explicitly storage.

============================================================
25. TEXTILE BOUNDARY
============================================================

Do not automatically classify textile products as Storage.

Examples:

Blanket
→ Textile

Curtain
→ Textile

Cushion
→ Textile

Fabric Storage Basket
→ Storage

Fabric Storage Box
→ Storage

Laundry Bag
→ Storage

Clothes Storage Bag
→ Storage

The primary function decides.

============================================================
26. KITCHEN & DINING BOUNDARY
============================================================

Exclude:

- Plates
- Bowls
- Cups
- Mugs
- Glassware
- Serveware
- Cutlery
- Cookware
- Serving Trays

unless the website explicitly classifies the product as a storage/
organization product.

Examples:

Glass Storage Jar
→ Storage

Food Storage Container
→ Storage

Decorative Glass Bowl
→ Kitchen & Dining / Decorative Home Accessories

============================================================
27. FURNITURE BOUNDARY
============================================================

Do NOT include obvious furniture merely because it provides storage.

Examples:

Dining Table
→ Furniture

Coffee Table
→ Furniture

Sofa
→ Furniture

Bed
→ Furniture

Dining Chair
→ Furniture

Wardrobe
→ carefully classify according to explicit website hierarchy

Storage Cabinet
→ Storage if explicitly categorized as storage

Storage Unit
→ Storage if explicitly categorized as storage

============================================================
28. BATHROOM BOUNDARY
============================================================

Do not include bathroom fixtures.

Exclude:

- Toilets
- Sinks
- Bathtubs
- Showers
- Faucets
- Taps
- Bathroom Mirrors
- Bathroom Lighting

Include only bathroom storage products.

============================================================
29. OUTDOOR / GARDEN STORAGE
============================================================

Include genuine outdoor storage:

- Garden Storage
- Outdoor Storage
- Garden Storage Boxes
- Deck Boxes
- Patio Storage Boxes
- Outdoor Storage Cabinets
- Garden Sheds when appropriate to the website's home-storage
  category
- Outdoor Storage Benches when primarily classified as storage

Do NOT include:

- Garden Furniture
- Outdoor Tables
- Outdoor Chairs
- Garden Decor
- Planters
- Garden Tools

unless the actual product is a storage product.

============================================================
30. UTILITY / LAUNDRY / CLEANING STORAGE
============================================================

Include:

- Utility Storage
- Cleaning Storage
- Laundry Storage
- Mop Storage
- Cleaning Organizers
- Utility Cabinets
- Utility Shelves
- Utility Baskets
- Cleaning Product Organizers

Do not include the cleaning products/tools themselves.

Example:

Mop
→ NOT Storage

Mop Holder/Storage Rack
→ Storage

Cleaning Basket
→ Storage

============================================================
31. PET STORAGE
============================================================

Generally exclude pet-specific products unless they are clearly
home-storage/organization products.

Example:

Pet Bed
→ NOT Storage

Pet Toy
→ NOT Storage

Pet Food Storage Container
→ Storage

Pet Toy Storage Box
→ Storage

============================================================
32. BABY / CHILDREN STORAGE
============================================================

Include:

- Kids Storage
- Children's Storage
- Toy Storage
- Nursery Storage
- Baby Storage
- Children's Storage Baskets
- Toy Boxes
- Toy Organizers
- Kids Storage Units

Do NOT include:

- Toys
- Baby Clothing
- Children's Clothing
- Decorative Children's Accessories

============================================================
33. CATEGORY HIERARCHY
============================================================

Follow the actual website navigation hierarchy.

Example:

Storage
    → Home Storage
        → Storage Boxes
            → Decorative Storage Boxes
            → Fabric Storage Boxes
        → Storage Baskets
            → Woven Baskets
            → Laundry Baskets

Preserve the actual hierarchy.

Do not flatten all categories into one generic "Storage" row.

============================================================
34. PARENT CATEGORY URL RULE
============================================================

Do NOT add the main Storage URL when valid subcategories exist.

Example:

Storage
    → Boxes
        → Storage Boxes
        → Under-Bed Storage
        → Toy Storage

Do NOT record:

Storage → URL

if valid subcategories are available.

Record the appropriate valid subcategory URLs.

If a category has NO subcategories, the category URL itself may be
recorded.

============================================================
35. VIEW ALL / COLLECTIONS
============================================================

Do NOT include:

- View All
- Shop All
- All Products
- Collections
- Gift Collections
- Seasonal Collections
- Promotional pages
- Search-result pages

Only use genuine category/subcategory listing pages.

============================================================
36. QUANTITY
============================================================

Extract the exact number of products shown for the category page.

Preferred order:

1. Explicit total:

"186 Products"
→ 186

2. Pagination total:

"Showing 1–24 of 186"
→ 186

3. If no total exists:

paginate through the category and count unique product cards.

Never estimate.

Never invent.

Never combine quantities from unrelated URLs.

============================================================
37. URL RULE
============================================================

Use the actual category/subcategory listing URL.

Do NOT use:

- Product detail URLs
- Search URLs
- Homepage URLs
- View All URLs
- Collection URLs
- Promotional URLs

Never invent or manually construct a URL unless it is directly
verified from the website.

============================================================
38. DUPLICATE RULE
============================================================

A record should normally be unique by:

Company
+
Category
+
Sub-Category
+
URL

If the same category is reachable through multiple navigation paths
but points to the same listing URL:

keep one record.

If genuinely different listing URLs contain different products:

keep them separately.

Do not duplicate a record simply because the website links to it from
multiple locations.

============================================================
39. ZERO-PRODUCT CATEGORY
============================================================

If a valid Storage category exists but contains zero products:

Qty = 0

provided the website explicitly shows zero products.

Do not assume zero.

============================================================
40. BLOCKED / FAILED WEBSITE
============================================================

If the website cannot be accessed:

do not fabricate Storage records.

Record:

Company
Country
Website
Status = BLOCKED / FAILED
Reason

Continue to the next company.

Do not repeatedly retry indefinitely.

============================================================
41. NO STORAGE CATEGORY
============================================================

If reasonable website navigation confirms that no Storage category or
valid Storage products exist:

Status = NO_CATEGORY

Do not create fake rows.

Do not add a blank Storage row.

============================================================
42. AMBIGUITY HANDLING
============================================================

If classification is obvious:

process normally.

If ambiguous:

check, in order:

1. Website navigation hierarchy
2. Parent category
3. Subcategory
4. Product title
5. Product description
6. Product purpose
7. Website's own classification

Do NOT make a decision based only on a keyword.

Examples:

"Basket"
→ inspect whether it is decorative or storage.

"Shelf"
→ inspect whether it is wall decor, furniture, or storage.

"Cabinet"
→ inspect whether it is furniture, bathroom, or storage.

"Rack"
→ inspect whether it is decorative, furniture, or storage.

If ambiguity remains:

mark:

confidence = LOW

and place the record into the review queue rather than guessing.

============================================================
43. OUTPUT
============================================================

Create:

Storage.xlsx

Use the established schema:

SR No.
Company Name
Brand Site
Country
Site URL
Category
Sub-Category
Type
Qty
Link

Type should follow the established output convention.

Preserve the existing workbook formatting and column order.

============================================================
44. GROUPING ROWS
============================================================

Preserve the established grouping-row convention.

Example:

Storage
    blank Qty
    blank Link

Storage Boxes
    blank Qty
    blank Link

Under-Bed Storage
    86
    URL

Storage Baskets
    142
    URL

Do not place quantities or URLs on grouping rows.

============================================================
45. VALIDATION CHECKLIST
============================================================

Before finalizing Storage.xlsx:

✓ Every company in the active manifest was processed.

✓ No company was silently skipped.

✓ Only genuine Storage products/categories are included.

✓ Furniture was not incorrectly included.

✓ Textile was not incorrectly included.

✓ Kitchen & Dining was not incorrectly included.

✓ Decorative Home Accessories were not incorrectly included.

✓ Wall Decor was not incorrectly included.

✓ Lighting was not included.

✓ Bathroom fixtures were excluded.

✓ Bathroom storage was included.

✓ Outdoor storage was included.

✓ Kitchen/pantry storage was included.

✓ Closet/wardrobe storage was included.

✓ Shoe storage was included.

✓ Laundry storage was included.

✓ Toy storage was included.

✓ Office storage was included where appropriate.

✓ Storage boxes were included.

✓ Storage baskets were included.

✓ Organizers were included.

✓ Storage racks were included where appropriate.

✓ Decorative-only products were excluded.

✓ Product-detail URLs were excluded.

✓ View All links were excluded.

✓ Collection links were excluded.

✓ Search-result URLs were excluded.

✓ Quantities were not estimated.

✓ Quantities were not aggregated.

✓ URLs were verified.

✓ Duplicate records were prevented.

✓ Category hierarchy was preserved.

✓ Parent category URLs were not unnecessarily added when valid
  subcategories exist.

✓ No existing validated category file was modified.

============================================================
46. FINAL REPORT
============================================================

Report:

Total companies in active manifest:
Companies checked:
Storage found:
No Storage:
Blocked:
Failed:

Total Storage records:
Total grouping rows:
Low-confidence records:
Duplicates prevented:

Also provide:

Company | Country | Storage Records | Status

============================================================
FINAL PRINCIPLE
============================================================

STORAGE CLASSIFICATION IS BASED ON:

PRIMARY PRODUCT TYPE
+
PRIMARY FUNCTION
+
WEBSITE CATEGORY HIERARCHY
+
PRODUCT PURPOSE

NOT:

- keyword alone
- room name alone
- material alone
- ability to technically hold something

The strongest evidence is the website's own category hierarchy and
the product's primary purpose.

QUALITY > SPEED.

NO FABRICATION.
NO DUPLICATE RESEARCH.
NO DUPLICATE RECORDS.
NO QUANTITY AGGREGATION.
NO URL INVENTION.
NO UNAUTHORIZED CATEGORY MIXING.
NO RECLASSIFICATION WITHOUT EVIDENCE.
