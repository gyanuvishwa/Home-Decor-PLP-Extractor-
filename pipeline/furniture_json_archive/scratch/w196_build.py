import json
from urllib.parse import quote

BASE = "https://www.kohls.com"

def cn_url(path, product, category):
    parts = []
    if product:
        parts.append("Product:" + quote(product, safe=""))
    parts.append("Category:" + quote(category, safe=""))
    parts.append("Department:" + quote("Furniture", safe=""))
    cn = "+".join(parts)
    return f"{BASE}{path}?CN={cn}"

BLOCK_FLAG = "MANUAL REVIEW: qty unverifiable - every catalog.jsp listing page on kohls.com (incl. same-origin fetch from within an already-loaded page) returns Akamai/HUMAN Bot Manager's static block page ('Powered and protected by ... Privacy', ~2.4KB, HTTP 200) instead of the real listing; confirmed on 3 independent requests (2 navigations + 1 same-origin fetch) to 2 different catalog URLs. Homepage and /sitemap*.xml load normally, so this is a target-side block scoped to catalog/product listing pages, consistent with the prior Home-Decor pass's documented Akamai finding for this same site."

# category -> list of (Category, Product, path, extra_flag or None)
tree = [
 ("Bars & Wine Cabinets", [
    ("Bars & Bar Sets", "/catalog/bars-bar-sets-bars-wine-cabinets-furniture.jsp", None),
    ("Wine Cabinets", "/catalog/wine-cabinets-bars-wine-cabinets-furniture.jsp", None),
 ]),
 ("Beds & Headboards", [
    ("Beds", "/catalog/beds-beds-headboards-furniture.jsp", None),
    ("Headboards", "/catalog/bedroom-headboards-beds-headboards-furniture.jsp", None),
 ]),
 ("Bookcases & Shelving", [
    ("Bakers Racks", "/catalog/bakers-racks-bookcases-shelving-furniture.jsp", None),
    ("Bookshelves", "/catalog/bookshelves-bookcases-shelving-furniture.jsp", None),
    ("Cubbies & Cube Storage", "/catalog/cubbies-cube-storage-bookcases-shelving-furniture.jsp", None),
 ]),
 ("Cabinets", [
    ("Bath Cabinets", "/catalog/bath-cabinets-cabinets-furniture.jsp", None),
    ("File Cabinets", "/catalog/file-cabinets-cabinets-furniture.jsp", None),
    ("Medicine Cabinets", "/catalog/medicine-cabinets-cabinets-furniture.jsp", None),
    ("Office Cabinets", "/catalog/office-cabinets-cabinets-furniture.jsp", None),
    ("Other Cabinets", "/catalog/other-cabinets-cabinets-furniture.jsp", None),
    ("Sideboards", "/catalog/sideboards-cabinets-furniture.jsp", None),
 ]),
 ("Carts & Islands", [
    ("Carts", "/catalog/carts-carts-islands-furniture.jsp", None),
    ("Islands", "/catalog/islands-carts-islands-furniture.jsp", None),
    ("Microwave Carts", "/catalog/microwave-carts-carts-islands-furniture.jsp", None),
    ("Serving Carts", "/catalog/serving-carts-carts-islands-furniture.jsp", None),
 ]),
 ("Chairs", [
    ("Accent Chairs", "/catalog/accent-chairs-chairs-furniture.jsp", None),
    ("Adirondack Chairs", "/catalog/adirondack-chairs-chairs-furniture.jsp", None),
    ("Beanbag Chairs", "/catalog/beanbag-chairs-chairs-furniture.jsp", None),
    ("Benches", "/catalog/benches-chairs-furniture.jsp", None),
    ("Chaises", "/catalog/chaises-chairs-furniture.jsp", None),
    ("Folding Chairs", "/catalog/folding-chairs-chairs-furniture.jsp", None),
    ("Lawn Chairs", "/catalog/lawn-chairs-chairs-furniture.jsp", None),
    ("Other", "/catalog/other-chairs-furniture.jsp", "MANUAL REVIEW: site's own catch-all 'Other' node under Chairs - contents not inspectable (catalog page blocked)"),
    ("Rocking Chairs & Gliders", "/catalog/rocking-chairs-gliders-chairs-furniture.jsp", None),
    ("Stools", "/catalog/stools-chairs-furniture.jsp", None),
 ]),
 ("Desks", [
    ("Computer Desks", "/catalog/computer-desks-desks-furniture.jsp", None),
    ("Executive Desks", "/catalog/executive-desks-desks-furniture.jsp", None),
    ("Writing Desks", "/catalog/writing-desks-desks-furniture.jsp", None),
 ]),
 ("Dressers & Chests", [
    ("Armoires", "/catalog/armoires-dressers-chests-furniture.jsp", None),
    ("Chests", "/catalog/chests-dressers-chests-furniture.jsp", None),
    ("Dressers", "/catalog/dressers-dressers-chests-furniture.jsp", None),
    ("Jewelry Armoires", "/catalog/jewelry-armoires-dressers-chests-furniture.jsp", None),
    ("Nightstands", "/catalog/bedroom-nightstands-dressers-chests-furniture.jsp", None),
 ]),
 ("Furniture Collections & Sets", [
    ("Furniture Collections", "/catalog/furniture-collections-furniture-collections-sets-furniture.jsp", "MANUAL REVIEW: 'Furniture Collections' is the site's own Product facet (distinct from 'Furniture Sets') under Department:Furniture - could not open the page to confirm it lists real furniture-collection products rather than a marketing/editorial collections hub, since all catalog pages are blocked"),
    ("Furniture Sets", "/catalog/furniture-sets-furniture-collections-sets-furniture.jsp", None),
 ]),
 ("Other Furniture", [
    ("Coat Racks", "/catalog/coat-racks-other-furniture-furniture.jsp", None),
    ("Hammocks", "/catalog/hammocks-other-furniture-furniture.jsp", None),
    ("Step Stools", "/catalog/step-stools-other-furniture-furniture.jsp", None),
 ]),
 ("Ottomans & Poufs", [
    ("Ottomans", "/catalog/ottomans-ottomans-poufs-furniture.jsp", None),
    ("Poufs", "/catalog/poufs-ottomans-poufs-furniture.jsp", None),
    ("Trunks", "/catalog/trunks-ottomans-poufs-furniture.jsp", None),
 ]),
 ("Sofas & Sectionals", [
    ("Couches", "/catalog/couches-sofas-sectionals-furniture.jsp", None),
    ("Loveseats", "/catalog/loveseats-sofas-sectionals-furniture.jsp", None),
 ]),
 ("Tables", [
    ("Accent Tables", "/catalog/living-room-accent-tables-tables-furniture.jsp", None),
    ("Bar Tables", "/catalog/bar-tables-tables-furniture.jsp", None),
    ("Coffee Tables", "/catalog/coffee-tables-tables-furniture.jsp", None),
    ("Console Tables", "/catalog/console-tables-tables-furniture.jsp", None),
    ("Dining Sets", "/catalog/dining-sets-tables-furniture.jsp", None),
    ("Dining Tables", "/catalog/dining-tables-tables-furniture.jsp", None),
    ("End Tables", "/catalog/end-tables-tables-furniture.jsp", None),
    ("Folding Tables", "/catalog/folding-tables-tables-furniture.jsp", None),
    ("Other Tables", "/catalog/other-tables-tables-furniture.jsp", None),
    ("TV Tray Tables", "/catalog/tv-tray-tables-tables-furniture.jsp", None),
 ]),
 ("TV Stands & Entertainment Centers", [
    ("Entertainment Centers", "/catalog/entertainment-centers-tv-stands-entertainment-centers-furniture.jsp", None),
    ("Media Storage", "/catalog/media-storage-tv-stands-entertainment-centers-furniture.jsp", None),
 ]),
]

rows = []
for category, children in tree:
    rows.append({
        "category": "Furniture",
        "sub_category": category,
        "qty": None,
        "link": None,
        "is_group": True,
        "evidence": None,
        "flag": None,
    })
    for product, path, extra_flag in children:
        flag = BLOCK_FLAG if not extra_flag else BLOCK_FLAG + " | " + extra_flag
        rows.append({
            "category": "Furniture",
            "sub_category": product,
            "qty": None,
            "link": cn_url(path, product, category),
            "is_group": False,
            "evidence": None,
            "flag": flag,
        })

# Futons: leaf itself (no children found in sitemap taxonomy)
rows.append({
    "category": "Furniture",
    "sub_category": "Futons",
    "qty": None,
    "link": cn_url("/catalog/futons-furniture.jsp", None, "Futons"),
    "is_group": False,
    "evidence": None,
    "flag": BLOCK_FLAG,
})

notes = (
    "ACCESS: robots.txt has no Claude/anthropic-specific disallow (generic User-agent:* rules only, "
    "plus a full-site Disallow for meta-externalagent/meta-webindexer/Baiduspider - not applicable). "
    "Homepage (https://www.kohls.com/) and /sitemap*.xml load normally in Chrome. Every catalog.jsp "
    "listing page - reached by direct navigation to a guessed Department:Furniture URL, by clicking "
    "through from the real 'Home & Pet' nav link, AND by same-origin fetch() from within the already-"
    "loaded homepage - returns HTTP 200 but the response body is Akamai/HUMAN Bot Manager's static "
    "'Powered and protected by ... Privacy' block page (~2.4KB), not the real listing. This matches the "
    "prior Home-Decor pass's independently-documented finding that kohls.com sits behind Akamai Bot "
    "Manager with a behavioral JS sensor challenge on every catalog/product page. Per the hard-block "
    "rule this was treated as a confirmed target-side block after 3 requests across 2 URLs and no "
    "further catalog-page requests were attempted. "
    "TREE SOURCE: the mega-menu has no standalone 'Furniture' top-level item (furniture lives inside "
    "the 'Home & Pet' department, itself catalog.jsp-blocked), so the full category tree was built from "
    "kohls.com's own /sitemap_catalog_1..6.xml files (fetched via same-origin fetch(), which are NOT "
    "Akamai-protected - confirmed working, ~37,953 total catalog URLs). Filtered every URL whose CN "
    "query carries Department:Furniture, dropped color/material/brand/size/sports-team/trend/etc. "
    "filter-facet URLs (per brief's never-extract-filter-pages rule), and grouped by the Category+Product "
    "taxonomy facets to reconstruct the site's own Furniture > Category > Product hierarchy (16 top "
    "Category nodes, 58 Category+Product leaves incl. Futons which has no Product children and is "
    "recorded as its own leaf). Cross-checked the Room-tagged URLs too (Room:Bedroom+Category:X+Product:Y "
    "etc.) - this surfaced 2 leaves (Headboards under Beds & Headboards, Nightstands under Dressers & "
    "Chests) that exist ONLY as Room-qualified sitemap entries, confirming the brief's warning that the "
    "product facet alone under-reports vs. the union of facet combinations; the Room facet itself was "
    "dropped from the final Category>Product link since it is a cross-cutting view, not part of the "
    "hierarchy. "
    "EXCLUDED: the entire 'Mattresses & Accessories' category (Air Mattresses, Mattresses - bedding per "
    "brief, not furniture); 'Other Furniture > Furniture Protectors' (furniture care/cover product, "
    "explicitly excluded). Kept Carts & Islands (kitchen carts/islands filed by the site under the "
    "Furniture department), Bath/Medicine/Office/File/Other Cabinets and Sideboards (site-classified "
    "furniture cabinets), Hammocks/Coat Racks/Step Stools (Other Furniture leaves), and Trunks/Poufs/"
    "Ottomans - all per the 'if the site itself files a node under Furniture, keep it' rule. Flagged "
    "'Other' under Chairs (site's own ambiguous catch-all) and 'Furniture Collections' under Furniture "
    "Collections & Sets (facet name similar to a marketing collections hub, but is the site's own Product "
    "facet value, not a nav 'Shop the Collection' link) for manual review since the pages could not be "
    "opened to inspect actual product tiles. "
    "QTY: could not be obtained for ANY leaf - every listing page (SSR HTML, and the equivalent "
    "same-origin fetch that worked for CB2/Maisons du Monde on other companies) is blocked by Akamai on "
    "this site, exactly as the prior Home-Decor pass found. All qty are null with a flag naming the "
    "block mechanism and the 3 independent confirmations. Links are the canonical CN=Product:...+"
    "Category:...+Department:Furniture URLs reconstructed from the real sitemap-derived slug and facet "
    "values (same construction pattern the site's own sitemap uses, and the same pattern the prior "
    "Home-Decor pass's verified-working URLs for this company follow), but the pages themselves were not "
    "verified live because of the block."
)

out = {
    "sr": 196,
    "company": "Kohl's Home",
    "brand_site": "kohls.com",
    "country": "USA",
    "site_url": "https://www.kohls.com/",
    "status": "partial",
    "failure_reason": "Akamai/HUMAN Bot Manager blocks every catalog.jsp listing page (SSR navigation and same-origin fetch alike) with a static interstitial instead of the real listing, so no product qty could be verified for any Furniture leaf; only the homepage and static sitemap XML files are reachable. Category/sub-category tree and canonical URLs were reconstructed from the site's own sitemap taxonomy instead.",
    "notes": notes,
    "rows": rows,
}

path = r"C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\furniture_json_archive\f196.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

leaf = sum(1 for r in rows if not r["is_group"])
grp = sum(1 for r in rows if r["is_group"])
nullq = sum(1 for r in rows if not r["is_group"] and r["qty"] is None)
flagged = sum(1 for r in rows if r["flag"])
print(f"rows={len(rows)} leaf={leaf} group={grp} null_qty={nullq} flagged={flagged}")
