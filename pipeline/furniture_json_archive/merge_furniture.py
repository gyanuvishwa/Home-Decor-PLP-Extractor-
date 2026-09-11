#!/usr/bin/env python3
"""Build Furniture.xlsx from the furniture worker JSON (f<SR>.json).

Writes a BRAND NEW workbook. Never opens, reads or touches:
  Kitchen_and_Dining.xlsx / Lighting.xlsx / Wall_Decor.xlsx /
  Decorative_Home_Accessories.xlsx / Final_Company_List (1).xlsx  (read-only for scope)

Sheets written:
  Output            - same 10-column layout/format as the four validated files
  Processing Ledger - one row per company in scope (must be exactly 286)
  Review            - leaf rows with null qty or a MANUAL REVIEW flag

Idempotent: rebuilds everything from whatever f*.json is on disk.

Usage:  python merge_furniture.py
"""
import io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

SCRATCH = os.path.dirname(os.path.abspath(__file__))
PROJ = r"C:\Users\GyanendraVishwakarma\Web Research Agent"
BOOK = os.path.join(PROJ, "Furniture.xlsx")
SRC = os.path.join(PROJ, "Final_Company_List (1).xlsx")

HDR = ["Maisons", "Company name", "Brand Site", "Country", "site URL",
       "Category", "Sub-Category", "Type", "qty", "link"]

HDR_FONT = Font(name="Calibri", sz=10, bold=True)
HDR_FILL = PatternFill("solid", fgColor="FFD9E1F2")
PARENT_FILL = PatternFill("solid", fgColor="FFFFF2CC")
PARENT_FONT = Font(name="Calibri", sz=10, bold=True)
BODY_FONT = Font(name="Calibri", sz=10)
THIN = Side(style="thin", color="FFBFBFBF")
CELL_BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# Navigation / marketing nodes that are never a product category (spec §3/§16).
BANNED = re.compile(
    r'^\s*(shop\s?all|view\s?all|browse\s?all|explore\s?all|see\s?all|all\s+products?|'
    r'all\s+furniture|shop\s+the\s+collection|discover|collections?|featured|'
    r'new\s?arrivals?|new\s?in|best\s?sellers?|sale|offers?|clearance|outlet|'
    r'gift\s?guide|gift\s?cards?|lookbook|blog|journal|magazine|inspiration|ideas|'
    r'stories|designers?|brands?|trending|recently\s?viewed|search\s+results?)\s*$', re.I)

# Categories that are NOT furniture (spec §12). Applied to sub_category text as a
# safety net on top of the worker's own judgement -- anything matching is dropped and
# reported, so a wrongly-dropped row is visible rather than silent.
NOT_FURNITURE = re.compile(
    r'\b('
    r'lamps?|lighting|chandeliers?|sconces?|pendants?|lanterns?|light\s?bulbs?|'
    r'mirrors?|clocks?|wall\s?art|wall\s?decor|wall\s?d[ée]cor|artwork|paintings?|'
    r'prints?|posters?|tapestr(y|ies)|wall\s?decals?|'
    r'vases?|candle\s?holders?|candles?|candlesticks?|home\s?fragrance|diffusers?|'
    r'photo\s?frames?|picture\s?frames?|sculptures?|figurines?|ornaments?|'
    r'planters?|artificial\s+(plants?|flowers?|trees?)|faux\s+(plants?|flowers?)|'
    r'wreaths?|garlands?|'
    r'glassware|dinnerware|tableware|serveware|flatware|cutlery|crockery|'
    r'plates?|bowls?|mugs?|cups?|tumblers?|wine\s?glasses?|drinking\s?glasses?|'
    r'cookware|bakeware|utensils?|knives|pans?|'
    r'rugs?|carpets?|cushions?|pillows?|throws?|curtains?|blinds?|bedding|'
    r'duvets?|quilts?|sheets?|towels?|table\s?linen|tablecloths?|placemats?|'
    r'mattress(es)?|mattress\s?toppers?|'
    r'storage\s?(baskets?|boxes|bins?|containers?|jars?|tins?)|baskets?|'
    r'organi[sz]ers?|'
    r'sinks?|toilets?|bathtubs?|showers?|taps?|faucets?|shower\s?heads?|'
    r'bathroom\s?accessor(y|ies)|'
    r'furniture\s?(legs?|knobs?|castors?|polish|care)|'
    r'covers?|protectors?|cushion\s?covers?'
    r')\b', re.I)

# ...but these furniture nodes legitimately contain a banned word, so whitelist first.
FURNITURE_OVERRIDE = re.compile(
    r'\b('
    r'(bedside|side|end|console|coffee|dining|dressing|nesting|accent|bar|sofa|'
    r'lamp|writing|computer|office|work|meeting|patio|garden|outdoor|nest\s+of)\s+tables?|'
    r'tables?\s*(&|and)\s*chairs?|'
    r'lamp\s?tables?|'
    r'bed\s?frames?|beds?\b|headboards?|daybeds?|bunk\s?beds?|sofa\s?beds?|'
    r'cabinets?|sideboards?|cupboards?|dressers?|wardrobes?|armoires?|'
    r'chest(s)?\s+of\s+drawers?|drawer\s?units?|'
    r'bookcases?|bookshel(f|ves)|shelving\s?units?|display\s?units?|'
    r'tv\s?(units?|stands?|cabinets?)|media\s?units?|'
    r'sofas?|couches|sectionals?|loveseats?|chaise|settees?|'
    r'chairs?|armchairs?|recliners?|stools?|benches?|ottomans?|footstools?|poufs?|'
    r'desks?|vanit(y|ies)|'          # bare 'Vanity' is furniture per spec §6
    r'coat\s?(stands?|racks?)|hall\s?stands?|hat\s?stands?|'
    r'cribs?|cots?|cotbeds?|cot\s?beds?|changing\s?tables?|'   # nursery furniture, spec §1

    r'nightstands?|bedside\s?tables?|credenzas?|buffets?|trolle(y|ies)|carts?|'
    r'furniture'
    r')\b', re.I)


# ---- orchestrator adjudications (spec §11 ambiguous-shelving review) ------------
# Rows the worker emitted with an ambiguous-shelving flag AND whose own tile inspection
# showed the contents contradict the site's Furniture filing. §10 says preserve the site's
# classification "unless the product clearly contradicts it" -- these do.
# (sr, link) pairs. Anything ambiguous but NOT proven contradictory stays in, flagged,
# and appears on the Review sheet for manual adjudication.
ADJUDICATED_DROPS = {
    (15, "https://www.homecentre.com/ae/en/c/furniture-livingroom-wallshelves"),
        # worker: "all 34 tiles are wall/floating shelves and brackets despite the Furniture filing"
}


def load_scope():
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    ws = wb["Output"]
    scope = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is not None:
            scope.append({"sr": row[0], "company": row[1], "brand_site": row[2],
                          "country": row[3], "site_url": row[4]})
    wb.close()
    return scope


def load_blocks(scope):
    blocks, problems = [], []
    for c in scope:
        sr = c["sr"]
        p = os.path.join(SCRATCH, f"f{sr}.json")
        if not os.path.exists(p):
            blocks.append({**c, "status": "MISSING", "failure_reason":
                           f"no f{sr}.json produced", "notes": None, "rows": []})
            problems.append(f"SR {sr}: NO FILE (f{sr}.json missing)")
            continue
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except Exception as e:
            blocks.append({**c, "status": "error", "failure_reason":
                           f"worker JSON did not parse: {e}", "notes": None, "rows": []})
            problems.append(f"SR {sr}: BAD JSON: {e}")
            continue

        rows, seen_links, seen_names = [], set(), set()
        for r in d.get("rows") or []:
            sub = (r.get("sub_category") or "").strip()
            cat = (r.get("category") or "").strip() or "Furniture"
            link = (r.get("link") or "").strip()
            qty = r.get("qty")
            is_parent = bool(r.get("is_group") or r.get("parent"))

            if not sub:
                problems.append(f"SR {sr}: row with empty sub_category dropped")
                continue
            if BANNED.match(sub):
                problems.append(f"SR {sr}: dropped nav/marketing node '{sub}'")
                continue
            if NOT_FURNITURE.search(sub) and not FURNITURE_OVERRIDE.search(sub):
                problems.append(f"SR {sr}: DROPPED non-furniture '{cat} / {sub}'")
                continue
            if (sr, link) in ADJUDICATED_DROPS:
                problems.append(f"SR {sr}: ADJUDICATED DROP (wall shelving) '{sub}' -> {link}")
                continue

            if is_parent:
                if qty is not None or link:
                    problems.append(f"SR {sr}: grouping row '{sub}' had qty/link -> cleared")
                qty, link = None, ""
            else:
                # Spec §25: a record is a duplicate only when company + category/sub-category
                # + qty + URL all repeat. A repeated NAME at a different URL is a genuinely
                # different listing page (RH files Sofas under both Fabric Seating and
                # Leather Seating; they share no products) -- keep both.
                key = (cat.lower(), sub.lower(), link.lower())
                if key in seen_names:
                    problems.append(f"SR {sr}: dropped exact duplicate '{cat}/{sub}' -> {link}")
                    continue
                if link and link in seen_links:
                    problems.append(f"SR {sr}: '{sub}' shares a link with another row (kept, flagged)")
                    r = dict(r)
                    r["flag"] = ((r.get("flag") + " | ") if r.get("flag") else "") + \
                        "SAME LINK AS ANOTHER ROW IN THIS COMPANY - verify not an accidental duplicate"
                if qty == 0:
                    problems.append(f"SR {sr}: dropped empty (0-product) category '{sub}'")
                    continue
                if qty is not None:
                    if not isinstance(qty, int) or isinstance(qty, bool) or qty < 0:
                        problems.append(f"SR {sr}: non-integer qty {qty!r} for '{sub}' -> nulled")
                        qty = None
                    elif not (r.get("evidence") or "").strip():
                        problems.append(f"SR {sr}: qty {qty} for '{sub}' has NO evidence -> nulled")
                        qty = None
                if link:
                    if not re.match(r'^https?://', link):
                        problems.append(f"SR {sr}: non-absolute link for '{sub}' -> nulled: {link}")
                        link = ""
                    elif re.search(r'(r\.jina\.ai|translate\.goog|web\.archive\.org|webcache)', link):
                        problems.append(f"SR {sr}: PROXY URL in link for '{sub}' -> nulled: {link}")
                        link = ""
                    elif re.search(r'[?&](q|query|search|keyword)=', link) or '/search' in link.lower():
                        problems.append(f"SR {sr}: SEARCH URL in link for '{sub}' (kept, flagged): {link}")
                        r = dict(r)
                        r["flag"] = ((r.get("flag") + " | ") if r.get("flag") else "") + \
                            "LINK LOOKS LIKE A SEARCH PAGE - verify"
                if link:
                    seen_links.add(link)
                seen_names.add(key)

            for fld, val in (("category", cat), ("sub_category", sub)):
                bad = sorted({ch for ch in val if ord(ch) > 127})
                if bad:
                    problems.append(f"SR {sr}: NON-ENGLISH chars {bad!r} in {fld} '{val}'")

            rows.append({"category": cat, "sub_category": sub, "qty": qty,
                         "link": link, "parent": is_parent,
                         "flag": r.get("flag"), "evidence": r.get("evidence")})

        # Drop grouping rows left with no surviving children. Hierarchy is nested, so a
        # parent may be followed by further parents before the first leaf -- scan forward
        # over consecutive parents and require a leaf before the block ends.
        pruned = []
        for i, row in enumerate(rows):
            if row["parent"]:
                j = i + 1
                while j < len(rows) and rows[j]["parent"]:
                    j += 1
                if j >= len(rows):
                    problems.append(f"SR {sr}: grouping row '{row['sub_category']}' "
                                    f"has no surviving children -> dropped")
                    continue
            pruned.append(row)

        blocks.append({**c,
                       "status": d.get("status") or "unknown",
                       "failure_reason": d.get("failure_reason"),
                       "notes": d.get("notes"),
                       "rows": pruned})
    return blocks, problems


def style(ws, r, ncols=10, parent=False):
    for c in range(1, ncols + 1):
        cell = ws.cell(r, c)
        cell.font = PARENT_FONT if parent else BODY_FONT
        cell.alignment = Alignment(vertical="center")
        cell.border = CELL_BORDER
        if parent:
            cell.fill = PARENT_FILL


def ledger_status(b):
    """Exactly one of the four spec §3 outcomes."""
    st = (b["status"] or "").lower()
    if st in ("blocked", "failed"):
        return "BLOCKED / ACCESS FAILURE"
    if st in ("error", "missing", "unknown"):
        return "PROCESSING ERROR"
    # ok / partial
    return "FURNITURE FOUND" if b["rows"] else "NO FURNITURE FOUND"


def main():
    for f in ("Furniture.xlsx",):
        lock = os.path.join(PROJ, "~$" + f)
        if os.path.exists(lock):
            sys.exit(f"ABORT: {f} is open in Excel (lock {lock}). Close it first.")

    scope = load_scope()
    assert len(scope) == 286, f"scope is {len(scope)}, expected 286"
    blocks, problems = load_blocks(scope)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Output"

    ws.append(HDR)
    for c in range(1, 11):
        cell = ws.cell(1, c)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.border = CELL_BORDER
        cell.alignment = Alignment(vertical="center", horizontal="center")
    ws.row_dimensions[1].height = 20

    r = 2
    leaf_total = parent_total = 0
    review = []
    for b in blocks:
        if not b["rows"]:
            continue
        rows = b["rows"]
        prev_cat = None
        for i, row in enumerate(rows):
            if i == 0:
                ws.cell(r, 1, b["sr"]); ws.cell(r, 2, b["company"])
                ws.cell(r, 3, b["brand_site"]); ws.cell(r, 4, b["country"])
                ws.cell(r, 5, b["site_url"]); ws.cell(r, 8, "category")
            if row["category"] and row["category"] != prev_cat:
                ws.cell(r, 6, row["category"])
                prev_cat = row["category"]
            ws.cell(r, 7, row["sub_category"])
            if row["parent"]:
                parent_total += 1
            else:
                leaf_total += 1
                if row["qty"] is not None:
                    ws.cell(r, 9, row["qty"])
                if row["link"]:
                    ws.cell(r, 10, row["link"])
                if row["qty"] is None or row.get("flag"):
                    review.append((b["sr"], b["company"], row["category"],
                                   row["sub_category"], row["qty"],
                                   row.get("flag") or "qty could not be verified",
                                   row["link"]))
            style(ws, r, parent=row["parent"])
            r += 1
        ws.cell(r, 1, None); style(ws, r); r += 1        # blank separator row

    for col, w in zip("ABCDEFGHIJ", (8, 24, 20, 10, 34, 20, 34, 10, 8, 78)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"

    # ---------------- Processing Ledger (all 286) ----------------
    lw = wb.create_sheet("Processing Ledger")
    LHDR = ["Maisons", "Company", "Country", "Website", "Furniture Found",
            "Furniture Record Count", "Status", "Notes"]
    lw.append(LHDR)
    for c in range(1, len(LHDR) + 1):
        cell = lw.cell(1, c)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.border = CELL_BORDER
        cell.alignment = Alignment(vertical="center", horizontal="center")
    counts = {"FURNITURE FOUND": 0, "NO FURNITURE FOUND": 0,
              "BLOCKED / ACCESS FAILURE": 0, "PROCESSING ERROR": 0}
    lr = 2
    for b in blocks:
        st = ledger_status(b)
        counts[st] += 1
        leaves = [x for x in b["rows"] if not x["parent"]]
        note = b.get("failure_reason") or b.get("notes") or ""
        lw.cell(lr, 1, b["sr"]); lw.cell(lr, 2, b["company"])
        lw.cell(lr, 3, b["country"]); lw.cell(lr, 4, b["site_url"])
        lw.cell(lr, 5, "YES" if b["rows"] else "NO")
        lw.cell(lr, 6, len(leaves))
        lw.cell(lr, 7, st)
        lw.cell(lr, 8, str(note)[:2000])
        style(lw, lr, ncols=len(LHDR))
        lw.cell(lr, 8).alignment = Alignment(vertical="top", wrap_text=True)
        lr += 1
    for col, w in zip("ABCDEFGH", (8, 28, 12, 40, 15, 10, 26, 100)):
        lw.column_dimensions[col].width = w
    lw.freeze_panes = "A2"

    # ---------------- Review sheet ----------------
    rw = wb.create_sheet("Review")
    RHDR = ["Maisons", "Company", "Category", "Sub-Category", "qty", "Issue", "link"]
    rw.append(RHDR)
    for c in range(1, len(RHDR) + 1):
        cell = rw.cell(1, c)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.border = CELL_BORDER
        cell.alignment = Alignment(vertical="center", horizontal="center")
    for i, rec in enumerate(review, start=2):
        for j, v in enumerate(rec, start=1):
            rw.cell(i, j, v)
        style(rw, i, ncols=len(RHDR))
    for col, w in zip("ABCDEFG", (8, 26, 20, 32, 8, 60, 70)):
        rw.column_dimensions[col].width = w
    rw.freeze_panes = "A2"

    wb.save(BOOK)

    # ---------------- report ----------------
    print(f"WROTE -> {BOOK}")
    print(f"  Output sheet: {r-1} rows | leaf rows {leaf_total} | grouping rows {parent_total}")
    print(f"  companies with rows: {sum(1 for b in blocks if b['rows'])}")
    print(f"  ledger rows: {lr-2}  (must be 286)")
    print(f"  review rows: {len(review)}")
    print()
    for k, v in counts.items():
        print(f"  {k:<26} {v}")
    print(f"  {'TOTAL':<26} {sum(counts.values())}")
    if problems:
        print(f"\nDATA-HYGIENE MESSAGES ({len(problems)}):")
        for p in problems:
            print("  " + p)


if __name__ == "__main__":
    main()
