############################################################
# CATEGORY RULES: TEXTILE EXTRACTION
############################################################

This file defines ONLY the category-specific rules for TEXTILE.

The master Home Decor Extraction Skill controls:

- company processing
- batching
- caching
- progress tracking
- website access
- output generation
- duplicate prevention
- validation
- continuation/resume behavior

Do NOT redefine those common workflow rules here.

When the user says:

"Extract Textile"

load and apply THESE rules.

Do not apply Furniture, Lighting, Kitchen & Dining, Wall Decor,
Decorative Home Accessories, Storage, or Bathroom classification rules
unless explicitly required for resolving an ambiguity.

============================================================
1. OBJECTIVE
============================================================

Extract textile-related product categories and subcategories from the
websites of all companies in the active company manifest.

For each valid Textile category/subcategory, capture:

- Company
- Country
- Website
- Category
- Sub-Category
- Type
- Quantity
- URL

The objective is to identify products whose PRIMARY PRODUCT TYPE is
textile/home textile/fabric-based home furnishing.

Process every company in the active company scope.

Do not assume that a company has no Textile products merely because
it had no Textile records in a previous extraction.

============================================================
2. CORE CLASSIFICATION PRINCIPLE
============================================================

Use:

PRIMARY PRODUCT TYPE
        >
PRODUCT PURPOSE
        >
WEBSITE CATEGORY HIERARCHY
        >
ROOM NAME

The room name alone must NEVER determine whether something is Textile.

Examples:

Bedroom
    → Bedding
        → Duvet Covers

→ Textile

Living Room
    → Curtains

→ Textile

Bathroom
    → Towels

→ Textile

Dining
    → Table Linens

→ Textile

Do not classify an item as Textile merely because it is located under
a room category.

============================================================
3. MAIN TEXTILE GROUPS
============================================================

Include clearly identified textile/home-textile categories such as:

BEDDING
- Bedding
- Bed Linen
- Bed Linens
- Bed Sheets
- Fitted Sheets
- Flat Sheets
- Sheet Sets
- Duvet Covers
- Quilt Covers
- Comforter Covers
- Quilts
- Duvets
- Comforters
- Bedspreads
- Coverlets
- Blankets
- Throws
- Bed Throws
- Bed Runners
- Mattress Protectors
- Mattress Toppers
- Pillowcases
- Pillow Shams
- Bolster Covers
- Pillow Covers

============================================================
4. PILLOWS & CUSHIONS
============================================================

Include textile-based:

- Cushions
- Cushion Covers
- Decorative Cushions
- Throw Pillows
- Pillow Covers
- Bolster Cushions
- Bolster Covers
- Floor Cushions
- Seat Cushions
- Chair Cushions
- Bench Cushions
- Outdoor Cushions when clearly textile/fabric products

If the website clearly classifies the item as a textile/fabric home
furnishing product, include it.

Do NOT include furniture simply because it contains cushions.

Example:

Sofa
→ NOT Textile

Sofa Cushion
→ Textile

Cushion Cover
→ Textile

============================================================
5. CURTAINS & WINDOW TEXTILES
============================================================

Include:

- Curtains
- Curtain Panels
- Ready Made Curtains
- Sheer Curtains
- Blackout Curtains
- Voile Curtains
- Eyelet Curtains
- Pencil Pleat Curtains
- Tab Top Curtains
- Net Curtains
- Door Curtains
- Window Curtains
- Curtain Liners
- Curtain Valances
- Drapes
- Drapery
- Fabric Blinds
- Roman Blinds
- Roller Blinds when clearly textile/fabric
- Window Textiles

Also include relevant curtain-related textile categories when the
actual product is fabric/textile.

Do NOT include hardware:

- Curtain Rods
- Curtain Rails
- Curtain Poles
- Curtain Tracks
- Curtain Rings
- Curtain Hooks
- Finials
- Brackets

Those are NOT Textile.

============================================================
6. RUGS & FLOOR TEXTILES
============================================================

Include:

- Rugs
- Area Rugs
- Floor Rugs
- Runner Rugs
- Hallway Runners
- Doormats
- Mats
- Bath Mats
- Kitchen Mats
- Shag Rugs
- Woven Rugs
- Handwoven Rugs
- Flatweave Rugs
- Outdoor Rugs
- Indoor/Outdoor Rugs
- Sheepskin Rugs
- Faux Fur Rugs
- Kilims
- Tapestries used as floor textiles

The primary product must be a textile/fabric/floor-covering product.

Do NOT include:

- Flooring
- Tiles
- Hardwood Flooring
- Vinyl Flooring
- Laminate Flooring
- Construction materials

============================================================
7. TABLE TEXTILES
============================================================

Include:

- Tablecloths
- Table Covers
- Table Runners
- Placemats
- Fabric Placemats
- Napkins
- Cloth Napkins
- Table Linens
- Dining Linens
- Fabric Table Mats

Do NOT include the underlying table/furniture.

Example:

Dining Table
→ Furniture

Tablecloth
→ Textile

Table Runner
→ Textile

Cloth Napkin
→ Textile

============================================================
8. KITCHEN TEXTILES
============================================================

Include textile-based kitchen products such as:

- Kitchen Towels
- Tea Towels
- Dish Towels
- Oven Gloves
- Oven Mitts
- Pot Holders
- Aprons
- Kitchen Aprons
- Kitchen Cloths
- Kitchen Textiles
- Fabric Bread Bags
- Fabric Kitchen Storage where the primary product is textile

Do NOT include:

- Cookware
- Plates
- Bowls
- Glassware
- Mugs
- Cups
- Cutlery
- Appliances
- Kitchen Furniture

============================================================
9. BATHROOM TEXTILES
============================================================

IMPORTANT:

Bathroom is a room designation.

It does NOT mean all bathroom products belong to the Bathroom
category for this extraction.

Include genuine bathroom textiles:

- Bath Towels
- Hand Towels
- Face Towels
- Washcloths
- Bath Sheets
- Bath Mats
- Bath Rugs
- Shower Curtains
- Fabric Shower Curtains
- Bathroom Towels
- Bathroom Linen
- Bathroom Textiles
- Robes
- Bathrobes

Do NOT include:

- Bathroom Furniture
- Bathroom Cabinets
- Bathroom Vanity Units
- Bathroom Mirrors
- Bathroom Lighting
- Sinks
- Toilets
- Baths
- Showers
- Faucets
- Bathroom Hardware

Those belong to their appropriate categories/future tasks.

============================================================
10. BEDROOM TEXTILES
============================================================

Include:

- Bedding
- Bed Linen
- Sheets
- Duvet Covers
- Duvets
- Quilts
- Blankets
- Bedspreads
- Coverlets
- Pillowcases
- Pillow Covers
- Bed Runners
- Bed Throws
- Mattress Protectors
- Bedroom Curtains
- Bedroom Rugs

Do NOT include:

- Beds
- Bed Frames
- Headboards
- Wardrobes
- Dressers
- Nightstands
- Bedside Tables
- Bedroom Furniture

Those are Furniture.

============================================================
11. LIVING ROOM TEXTILES
============================================================

Include:

- Curtains
- Drapes
- Throws
- Blankets
- Cushions
- Cushion Covers
- Decorative Pillows
- Rugs
- Floor Textiles
- Upholstery fabrics when sold as textile products

Do NOT include:

- Sofas
- Chairs
- Armchairs
- Ottomans
- Benches
- Tables

Those are Furniture unless the actual extracted product is a textile
component such as a cushion or cover.

============================================================
12. OUTDOOR TEXTILES
============================================================

Include genuine outdoor textile products:

- Outdoor Cushions
- Outdoor Cushion Covers
- Outdoor Rugs
- Outdoor Throws
- Outdoor Blankets
- Outdoor Curtains
- Outdoor Fabric
- Garden Furniture Covers
- Patio Furniture Covers

The product must itself be textile/fabric.

Do NOT include:

- Outdoor Tables
- Outdoor Chairs
- Outdoor Sofas
- Garden Furniture
- Outdoor Furniture

Those are Furniture.

============================================================
13. FABRIC & UPHOLSTERY
============================================================

Include when the website sells them as home-textile products:

- Upholstery Fabric
- Curtain Fabric
- Furnishing Fabric
- Decorative Fabric
- Home Decor Fabric
- Fabric by the Meter
- Fabric by the Yard
- Textile Fabric

Only include these when they are clearly intended for home/furnishing
use.

Do NOT include general fashion/apparel fabric unless the website's
category clearly places it under home/furnishing textiles.

============================================================
14. WALL TEXTILES
============================================================

Include textile wall products when they are genuinely textile-based:

- Tapestries
- Fabric Wall Hangings
- Textile Wall Art
- Woven Wall Hangings
- Macramé Wall Hangings
- Fabric Wall Decor

However, preserve the actual website hierarchy.

If the product is clearly a textile product:

→ Textile

If it is a non-textile decorative wall product:

→ Wall Decor

Do not classify all Wall Decor as Textile.

============================================================
15. SEASONAL / DECORATIVE TEXTILES
============================================================

Include textile-based seasonal or decorative home products only when
they are genuinely textile products.

Examples:

- Fabric Christmas Stockings
- Fabric Table Runners
- Fabric Christmas Decorations
- Textile Decorative Throws
- Fabric Decorative Cushions

However:

Do NOT automatically include:

- Gifts
- Gift Collections
- Holiday Collections
- Collections
- Seasonal Landing Pages

A collection URL is not a valid product-category URL unless it is
actually a standard category/subcategory under the website's
navigation and meets the URL rules.

============================================================
16. MATERIAL RULE
============================================================

The material must support textile classification.

Common textile materials include:

- Cotton
- Linen
- Wool
- Silk
- Velvet
- Polyester
- Acrylic
- Microfiber
- Fleece
- Chenille
- Jute
- Hemp
- Canvas
- Fabric
- Woven Textile
- Knitted Textile
- Natural Fibres
- Synthetic Fibres
- Blended Fabrics

Material alone is NOT sufficient.

Example:

Cotton Chair
→ Furniture

Cotton Cushion
→ Textile

Wooden Table
→ Furniture

Linen Tablecloth
→ Textile

============================================================
17. DO NOT CLASSIFY BY MATERIAL ALONE
============================================================

Never use:

"made of fabric"

as the sole reason for classification.

The actual product type must be textile/home furnishing textile.

Examples:

Fabric Sofa
→ Furniture

Fabric Armchair
→ Furniture

Fabric Ottoman
→ Furniture

Cushion Cover
→ Textile

Curtain
→ Textile

Blanket
→ Textile

============================================================
18. PET / NON-HOME TEXTILES
============================================================

Do not automatically include textile products intended primarily for
pets unless the website clearly classifies them as home textiles.

Examples generally excluded:

- Dog Beds
- Cat Beds
- Pet Blankets
- Pet Clothing
- Pet Towels

Do not infer inclusion from material alone.

============================================================
19. APPAREL / FASHION
============================================================

Do NOT include:

- Clothing
- Dresses
- Shirts
- Trousers
- Jackets
- Shoes
- Bags
- Fashion Accessories
- Apparel Textiles

unless the website explicitly identifies them as home/furnishing
textiles relevant to the extraction.

This task is HOME TEXTILE, not fashion-textile extraction.

============================================================
20. BABY / CHILDREN'S TEXTILES
============================================================

Include only when they are genuine home textiles:

- Baby Bedding
- Children's Bedding
- Children's Curtains
- Children's Rugs
- Children's Blankets
- Children's Cushions

Do NOT include:

- Baby Clothing
- Children's Clothing
- Toys
- General children's products

============================================================
21. FURNITURE BOUNDARY
============================================================

Do not classify furniture as Textile.

Examples:

Sofa
→ Furniture

Dining Chair
→ Furniture

Bed
→ Furniture

Ottoman
→ Furniture when the website treats it as seating/furniture

Cushion
→ Textile

Cushion Cover
→ Textile

Furniture Cover
→ Textile

Bedspread
→ Textile

============================================================
22. STORAGE BOUNDARY
============================================================

Textile storage products can be ambiguous.

Include if the primary product is a textile/fabric storage item and the
website presents it as home textile.

Examples potentially Textile:

- Fabric Storage Basket
- Fabric Storage Bag
- Textile Laundry Bag

However, standalone storage products belong to the Storage task when
the website primarily classifies them as Storage.

Do not force ambiguous products into Textile.

Use:

PRIMARY PRODUCT TYPE
+
WEBSITE CATEGORY HIERARCHY
+
PRODUCT PURPOSE

If unresolved:

confidence = LOW

============================================================
23. HOME FRAGRANCE / PLANTS / DECORATIVE ACCESSORIES
============================================================

Do NOT include:

- Candles
- Diffusers
- Room Fragrance
- Incense
- Artificial Plants
- Flowers
- Trees
- Vases
- Sculptures
- Figurines
- Decorative Objects
- Decorative Accessories

unless the actual product is a textile product.

Example:

Fabric Flower
→ Textile only if genuinely sold as a textile/fabric home product.

Artificial Flower
→ NOT Textile.

============================================================
24. CATEGORY HIERARCHY
============================================================

Follow the actual website navigation.

Example:

Home
 → Textiles
    → Bedding
       → Bed Linen
          → Duvet Covers

Record the relevant deepest valid category/subcategory URL according
to the common URL rules.

Do not flatten the hierarchy unnecessarily.

============================================================
25. PARENT CATEGORY URL RULE
============================================================

Do NOT add the URL of a parent category when valid subcategories exist.

Example:

Textiles
    Bedding
        Bed Linen
            Duvet Covers

Do NOT record:

Textiles → URL

if valid subcategories are available.

Instead record the relevant deepest valid subcategory:

Duvet Covers → URL

However, if:

Textiles
    → No subcategories

then the Textiles category URL may be recorded.

============================================================
26. GROUPING ROWS
============================================================

Preserve the established workbook grouping convention.

Example:

Textiles
    blank quantity
    blank URL

Bedding
    blank quantity
    blank URL

Duvet Covers
    124
    URL

Do not place quantity or URL on grouping rows.

============================================================
27. VIEW ALL / COLLECTIONS
============================================================

DO NOT extract:

- View All
- Shop All
- All Products
- Collections
- Seasonal Collections
- Gift Collections
- Promotional Landing Pages

Only extract actual category/subcategory listing pages.

============================================================
28. QUANTITY
============================================================

Extract the quantity exactly as displayed on the relevant listing page.

Do NOT:

- estimate
- calculate
- infer
- combine
- aggregate

Example:

Duvet Covers | 83 | URL A
Bed Sheets | 126 | URL B
Curtains | 94 | URL C

Keep separate rows.

============================================================
29. URL
============================================================

Use the relevant category/product-listing page URL.

Do NOT use:

- Product-detail URLs
- Search-result URLs
- Homepage URLs
- View All URLs
- Collection URLs
- Promotional URLs

Do not invent URLs.

Use the actual URL observed from the website.

============================================================
30. DUPLICATES
============================================================

If the same company + category + subcategory + URL appears multiple
times through different navigation paths:

retain only one record unless the website genuinely provides different
listing pages.

Do not duplicate records simply because the same category is linked
from multiple locations.

============================================================
31. MULTI-LEVEL TEXTILE CATEGORIES
============================================================

If a website contains:

Textiles
    Bedding
        Bed Linen
            Sheets
            Duvet Covers
            Pillowcases

preserve the hierarchy.

Do not unnecessarily collapse:

Sheets
Duvet Covers
Pillowcases

into one Bedding record.

============================================================
32. COMPANY PROCESSING
============================================================

Every company in the active manifest must be checked independently.

Do not assume:

"Company had no Furniture"

means:

"Company has no Textile."

Each extraction category is independent.

============================================================
33. BLOCKED WEBSITE
============================================================

If the website cannot be accessed:

status = BLOCKED / FAILED

Record:

- Company
- Country
- Website
- Reason
- Attempted method

Do not fabricate Textile records.

Continue with the next company.

============================================================
34. NO TEXTILE
============================================================

If reasonable navigation inspection finds no valid Textile category:

status = NO_CATEGORY

Do not create empty category records.

============================================================
35. CONFIDENCE
============================================================

Use:

HIGH
MEDIUM
LOW

HIGH:

Clearly textile category.

Example:

Duvet Covers

MEDIUM:

Textile classification is likely but hierarchy is somewhat unclear.

LOW:

Product could reasonably belong to another category such as Storage,
Furniture, or Wall Decor.

Low-confidence records should enter the review queue.

============================================================
36. OUTPUT
============================================================

Output filename:

Textile.xlsx

Use the established workbook structure:

Maisons
Company name
Brand Site
Country
site URL
Category
Sub-Category
Type
qty
link

Preserve existing formatting conventions.

Do not invent a new schema unless the common extraction engine requires
it.

============================================================
37. VALIDATION CHECKLIST
============================================================

Before completing Textile extraction, verify:

✓ Every company in the active scope was processed.

✓ No company was silently skipped.

✓ Only Textile/home-textile products are included.

✓ Furniture was not incorrectly included.

✓ Lighting was not included.

✓ Kitchen & Dining products were not incorrectly included.

✓ Decorative accessories were not included.

✓ Bathroom fixtures were not included.

✓ Bathroom textiles were included where valid.

✓ Bedding was included.

✓ Curtains were included.

✓ Rugs were included.

✓ Cushions were included.

✓ Table textiles were included.

✓ Kitchen textiles were included.

✓ Textile wall hangings were included where valid.

✓ Outdoor textiles were included where valid.

✓ Apparel/fashion products were excluded.

✓ Pet products were not incorrectly included.

✓ View All links were excluded.

✓ Collection links were excluded.

✓ Product-detail URLs were excluded.

✓ Quantities were not estimated.

✓ Quantities were not aggregated.

✓ URLs were not invented.

✓ Duplicate records were prevented.

✓ Category hierarchy was preserved.

✓ Parent URLs were not unnecessarily added when subcategories exist.

✓ Existing validated category files were not modified.

============================================================
38. FINAL REPORT
============================================================

Report:

Total companies in active manifest:
Companies checked:
Textile found:
No Textile:
Blocked:
Failed:

Total Textile records:
Total grouping rows:
Low-confidence records:
Duplicates prevented:

Also provide:

Company | Country | Textile Records | Status

for the processed companies.

============================================================
FINAL PRINCIPLE
============================================================

TEXTILE EXTRACTION IS BASED ON:

PRIMARY PRODUCT TYPE
+
PRODUCT PURPOSE
+
WEBSITE CATEGORY HIERARCHY

NOT ROOM NAME ALONE.

NOT MATERIAL ALONE.

NOT KEYWORD MATCHING ALONE.

When uncertain, preserve the website hierarchy and use the review queue
instead of guessing.

NO FABRICATION.
NO DUPLICATE RESEARCH.
NO DUPLICATE RECORDS.
NO QUANTITY AGGREGATION.
NO URL INVENTION.
NO UNAUTHORIZED CATEGORY MIXING.
