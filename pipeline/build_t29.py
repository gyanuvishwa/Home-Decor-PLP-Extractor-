#!/usr/bin/env python3
"""Rebuild t29.json (AJIO Home) from the browser-verified category tree.

Every number here was read live from ajio.com in a real browser on 2026-08-06,
each one confirmed twice: the internal category API's
`pagination.totalResults`, and the listing page's own "N Items Found" header.
Style-type leaves additionally had their browsable filter URL loaded and the
rendered count checked against the API figure.
"""
import io, json, urllib.parse

BASE = "https://www.ajio.com"
WTD = "831203001"   # Decor & Gifting > Wall & Table Decor
LIG = "831203007"   # Decor & Gifting > Lighting


def style_url(slug, cid, style):
    q = ":relevance:brickstyletype:" + style
    return f"{BASE}/{slug}/c/{cid}?query={urllib.parse.quote(q, safe='')}"


def cat_url(slug, cid):
    return f"{BASE}/{slug}/c/{cid}"


API = "internal category API pagination.totalResults"
HDR = "listing header 'N Items Found'"


def ev(n, extra=""):
    return (f"{HDR} = {n:,} on the live page, cross-checked against the "
            f"{API} = {n}{extra}")


rows = []


def add(cat, sub, qty, link, evidence, flag=None):
    rows.append({"category": cat, "sub_category": sub, "qty": qty,
                 "link": link, "evidence": evidence, "flag": flag})


# ---- Lighting: style-type leaves of Decor & Gifting > Lighting (32,057) ----
# Light Bulbs (9) excluded per brief. The 13 kept leaves sum to 32,048, which is
# exactly the parent total 32,057 minus those 9 bulbs - so the split is complete
# and loses nothing.
for name, qty in [
    ("Hanging Lights", 8198), ("Wall Lamps", 20477), ("Table Lamps", 2114),
    ("Floor Lamps", 394), ("Decorative Lights", 390), ("Chandeliers", 267),
    ("Night Lamps", 103), ("Lamp Shades", 38), ("Picture Lights", 32),
    ("Gate Lights", 29), ("Flush Mount", 3), ("String Lights", 2),
    ("Work & Study Lamps", 1),
]:
    add("Lighting", name, qty, style_url("lighting", LIG, name),
        ev(qty, "; style-type leaf of Lighting (32,057), URL loaded and "
                "rendered count matched"))

# ---- Wall Decor & Mirrors ----
# Wall & Table Decor (59,024) is NOT used as a row: it contains 6,111 clocks,
# which the spec never extracts. Its qualifying style-type leaves are used
# instead. Leaves that duplicate a dedicated category (Lighting 6,629,
# Photo Frames 362, Mirror 12) are omitted to avoid double-counting, as are
# Key Holders (177), Wall Shelves (372), Gift Hampers (1) and Skater (1).
for name, qty in [("Wall Art", 31420), ("Wall Stickers & Posters", 12831)]:
    add("Wall Decor & Mirrors", name, qty,
        style_url("wall-table-decor", WTD, name),
        ev(qty, "; style-type leaf of Wall & Table Decor (59,024), URL loaded "
                "and rendered count matched"))

add("Wall Decor & Mirrors", "Mirrors", 34, cat_url("mirrors", "831203008"),
    ev(34, "; dedicated category node 831203008"))

# ---- Home Accessories ----
add("Home Accessories", "Showpieces & Figurines", 4089,
    cat_url("showpieces-figurines", "831203002"), ev(4089))
add("Home Accessories", "Photo Frames", 1680,
    cat_url("photo-frames", "831203009"), ev(1680))
add("Home Accessories", "Vases", 729, cat_url("vases", "831203010"), ev(729))
add("Home Accessories", "Table Accents", 122,
    cat_url("table-accents", "831203011"), ev(122))
add("Home Accessories", "Jharokhas", 36, style_url("wall-table-decor", WTD, "Jharokhas"),
    ev(36, "; style-type leaf of Wall & Table Decor (decorative wall panels)"))

# ---- Home Fragrance ----
add("Home Fragrance", "Home Fragrances", 1633,
    cat_url("home-fragrances", "831203006"), ev(1633))
add("Home Fragrance", "Candles & Holders", 1036,
    style_url("wall-table-decor", WTD, "Candles & Holders"),
    ev(1036, "; style-type leaf of Wall & Table Decor"))

# ---- Garden ----
add("Garden", "Gardening & Planters", 1732,
    cat_url("gardening-planters", "831203005"), ev(1732),
    flag="MANUAL REVIEW: AJIO merges decorative planters with gardening "
         "supplies in this single node; it exposes no planters-only listing.")

# ---- Kitchen & Dining ----
# Serveware (1,674), Drinkware (6,592) and Serveware & Drinkware (4,970) were
# checked for overlap via each node's own Category facet: they are distinct
# nodes, with only 2 products appearing across two of them. Safe to keep all.
add("Kitchen & Dining", "Drinkware", 6592, cat_url("drinkware", "831202012"),
    ev(6592, "; Category facet confirms 6,592 in this node, distinct from "
             "Serveware and Serveware & Drinkware"))
add("Kitchen & Dining", "Serveware & Drinkware", 4970,
    cat_url("serveware-drinkware", "831202005"),
    ev(4970, "; Category facet confirms 4,970 in this node, distinct from "
             "Drinkware (2 products overlap)"))
add("Kitchen & Dining", "Tea & Coffee Serveware", 2970,
    cat_url("tea-coffee-serveware", "831202015"), ev(2970))
add("Kitchen & Dining", "Serveware", 1674, cat_url("serveware", "831202011"),
    ev(1674, "; Category facet confirms all 1,674 sit in this node alone"))
add("Kitchen & Dining", "Dinnerware", 468, cat_url("dinnerware", "831202013"),
    ev(468))
add("Kitchen & Dining", "Barware", 250, cat_url("barware", "831202014"), ev(250))
add("Kitchen & Dining", "Tableware", 95, cat_url("tableware", "831202016"), ev(95))

doc = {
    "sr": 29,
    "company": "AJIO Home",
    "brand_site": "ajio.com",
    "country": "India",
    "site_url": "https://www.ajio.com/",
    "status": "ok",
    "failure_reason": None,
    "notes": (
        "Completed in a real browser after the HTTP-layer worker was blocked by "
        "AJIO's Akamai edge. Full L3 taxonomy recovered by sweeping the category "
        "id space (831202001-016 Kitchen & Dining, 831203001-011 Decor & "
        "Gifting) through the site's own internal category API from within the "
        "page; note the parent listing's Category facet is INCOMPLETE (it omits "
        "Table Accents), so the id sweep is the reliable method. Every qty is "
        "double-sourced: API pagination.totalResults and the page's own "
        "'N Items Found' header. "
        "Wall & Table Decor (59,024) is deliberately NOT a row - it contains "
        "6,111 clocks, which the spec never extracts; its qualifying style-type "
        "leaves are used instead. Likewise Lighting (32,057) is represented by "
        "its 13 in-scope style-type leaves rather than the parent, so no parent "
        "and child are both present and nothing double-counts. Style-type URLs "
        "were each loaded in the browser and the rendered count matched the API. "
        "Excluded per brief: Clocks (6,111), Wall Shelves (372), Key Holders "
        "(177), Light Bulbs (9), Gift Hampers (1), Skater (1), Stationery & "
        "Organisers (1,573), Festive Gifts (1,504), Kitchen Linen (59,770), "
        "Table Covers/Runners/Slipcovers (32,887), Table Napkins/Coasters/"
        "Placemats (3,972), Kitchen Organisers (5,192), Cookware (1,455), "
        "Kitchen Tools (1,173), Cutlery (443), Bakeware (50), Kitchen "
        "Appliances (10), and all Furnishings and Bath & Laundry."
    ),
    "rows": rows,
}

p = "t29.json"
json.dump(doc, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {p}: {len(rows)} rows, "
      f"{sum(1 for r in rows if r['qty'] is None)} null, "
      f"{sum(1 for r in rows if r['flag'])} flagged")
print("lighting leaves sum:", sum(r["qty"] for r in rows if r["category"] == "Lighting"))
