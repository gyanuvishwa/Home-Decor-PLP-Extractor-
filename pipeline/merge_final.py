#!/usr/bin/env python3
"""Merge worker JSON (c<SR>.json) into 'Final_Company_List (1).xlsx'.

Adds/replaces an 'Output' sheet in Sheet3 format and stamps the Status column on
'Master Company List'. The Master Company List rows themselves are never otherwise
modified. Idempotent: rebuilds the Output sheet from scratch on every run.

Usage:  python merge_final.py [sr ...]      # default: every roster sr with a c*.json
"""
import io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

PROJ = r"C:\Users\GyanendraVishwakarma\Web Research Agent"
BOOK = os.path.join(PROJ, "Final_Company_List (1).xlsx")
SCRATCH = (r"C:\Users\GYANEN~1\AppData\Local\Temp\claude"
           r"\C--Users-GyanendraVishwakarma-Web-Research-Agent"
           r"\be91bad7-b37a-4694-bdbe-c47fea1bb5d9\scratchpad")

MASTER = "Master Company List"
OUT = "Output"
# Every S.N. extracted so far. The Output sheet is rebuilt from scratch on each run,
# so this must list ALL completed companies, not just the newest batch — otherwise
# earlier companies would be silently dropped from the sheet.
BATCH = list(range(1, 328))         # S.N. 1-327 = the full roster (rolling pool; SR whose
                                     # still be missing c<SR>.json mid-flight, tolerated)

HDR = ["SR N0.", "Company name", "Brand Site", "Country", "site URL",
       "Category", "Sub-Category", "Type", "qty", "link"]

# ---- final-cleanup classification (2026-08-13) ----------------------------------
# Companies that could not be extracted at all (robots.txt Claude-specific block,
# or an access wall nobody could get through). Master List Status -> blank.
FAILED_SRS = {113, 129, 159, 161, 187, 189, 229, 264, 316}

# Companies confirmed to be the SAME catalogue as another already-completed roster
# S.N. (rows intentionally left empty per the project's duplicate-company convention).
# Master List Status -> "Duplicate". Manually verified against each c<SR>.json's own
# notes field (a naive "duplicate" keyword search over-matches rows that discuss and
# then rule OUT duplication, e.g. S.N. 193/198's UAE-closure notes) -- do not regenerate
# this list from a regex without re-reading the notes.
DUPLICATE_SRS = {
    39, 82, 85, 88, 137, 142, 151, 153, 156, 164, 165, 166, 168, 179, 182, 194,
    219, 221, 225, 231, 233, 242, 244, 247, 250, 256, 257, 320, 325,
}

# Companies that were genuinely, successfully researched and the correct answer is
# zero in-scope products (no online catalogue at all, a real store closure, an
# offline/paused shop, or a scam/impersonation domain that isn't the real company).
# NOT a duplicate of another roster row. Master List Status stays the normal Done/
# Partial stamp; these just contribute no rows to Output (nothing to show).
LEGIT_ZERO_SRS = {24, 26, 70, 71, 109, 193, 198, 249, 261}

HDR_FONT = Font(name="Calibri", sz=10, bold=True)
HDR_FILL = PatternFill("solid", fgColor="FFD9E1F2")      # header band
PARENT_FILL = PatternFill("solid", fgColor="FFFFF2CC")   # grouping-row highlight -- light yellow, the only fill color used
PARENT_FONT = Font(name="Calibri", sz=10, bold=True)
BODY_FONT = Font(name="Calibri", sz=10)
BODY_ALIGN = Alignment(vertical="center")
THIN = Side(style="thin", color="FFBFBFBF")
CELL_BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

BANNED = re.compile(
    r'^\s*(shop\s?all|view\s?all|browse\s?all|explore\s?all|see\s?all|all\s+products?|'
    r'discover|collections?|collection|featured|new\s?arrivals?|new\s?in|'
    r'best\s?sellers?|sale|offers?|clearance|outlet|gift\s?guide|gifts?|gift\s?sets?|'
    r'gift\s?cards?|lookbook|blog|journal|magazine|inspiration|ideas|stories|'
    r'designers?|brands?|trending|recently\s?viewed)\s*$', re.I)

# Scope exclusions added this batch (spec change vs earlier batches).
OUT_OF_SCOPE = re.compile(
    r'(home\s?fragrance|reed\s?diffuser|diffusers?|room\s?spray|essential\s?oils?|'
    r'aroma\s?oils?|wax\s?melts?|potpourri|incense|'
    r'artificial\s+(plants?|flowers?|trees?|greenery)|'
    r'faux\s+(plants?|flowers?|trees?|greenery|stems?|florals?)|'
    r'wreaths?|garlands?|botanical\s?decor|'
    r'christmas|holiday\s?(collection|arrivals?|decor))', re.I)


def load_roster():
    wb = openpyxl.load_workbook(BOOK, data_only=True)
    ws = wb[MASTER]
    roster = {}
    for r in range(2, ws.max_row + 1):
        sn = ws.cell(r, 1).value
        if isinstance(sn, int):
            roster[sn] = {"row": r, "company": ws.cell(r, 2).value,
                          "domain": ws.cell(r, 3).value,
                          "country": ws.cell(r, 4).value}
    return roster


def load_blocks(want):
    blocks, problems = [], []
    for sr in sorted(want):
        p = os.path.join(SCRATCH, f"c{sr}.json")
        if not os.path.exists(p):
            problems.append(f"SR {sr}: NO FILE (c{sr}.json missing)")
            continue
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except Exception as e:
            problems.append(f"SR {sr}: BAD JSON: {e}")
            continue

        rows, seen_links, seen_names = [], set(), set()
        for r in d.get("rows") or []:
            sub = (r.get("sub_category") or "").strip()
            cat = (r.get("category") or "").strip()
            link = (r.get("link") or "").strip()
            qty = r.get("qty")
            is_parent = bool(r.get("parent"))
            if not sub:
                problems.append(f"SR {sr}: row with empty sub_category dropped")
                continue
            if BANNED.match(sub):
                problems.append(f"SR {sr}: dropped nav/marketing sub-category '{sub}'")
                continue
            if OUT_OF_SCOPE.search(sub) or OUT_OF_SCOPE.search(cat):
                problems.append(f"SR {sr}: dropped out-of-scope '{cat}/{sub}'")
                continue

            if is_parent:
                # Grouping row: never carries qty or link.
                if qty is not None or link:
                    problems.append(f"SR {sr}: parent '{sub}' had qty/link -> cleared")
                qty, link = None, ""
            else:
                if link and link in seen_links:
                    # Same URL can legitimately host more than one row when a worker
                    # splits a page's own products by type (e.g. a "Bathroom Accessories"
                    # page containing both mirrors and decorative accessories, each pulled
                    # out as its own row per Rule 0.3/0.4). That's a documented overlap,
                    # not an accidental duplicate -- keep the row, just flag it for review.
                    problems.append(f"SR {sr}: '{sub}' shares a link with another row (kept, flagged)")
                    r = dict(r)
                    r["flag"] = (r.get("flag") + " | " if r.get("flag") else "") + \
                        "SAME LINK AS ANOTHER ROW IN THIS COMPANY - verify not an accidental duplicate"
                key = (cat.lower(), sub.lower())
                if key in seen_names:
                    problems.append(f"SR {sr}: dropped duplicate '{cat}/{sub}'")
                    continue
                if qty == 0:
                    problems.append(f"SR {sr}: dropped empty (0-product) category '{sub}'")
                    continue
                if qty is not None:
                    if not isinstance(qty, int) or qty < 0:
                        problems.append(f"SR {sr}: non-integer qty {qty!r} for '{sub}' -> nulled")
                        qty = None
                    elif not (r.get("evidence") or "").strip():
                        problems.append(f"SR {sr}: qty {qty} for '{sub}' has NO evidence -> nulled")
                        qty = None
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

        # Drop parent rows that ended up with no surviving children.
        # Hierarchy is nested: a top-level parent is legitimately followed by a
        # sub-parent before any leaf appears (Lighting > Ceiling Lights > Chandeliers).
        # So scan forward over consecutive parent rows and require a leaf to follow;
        # only a parent whose block ends without one is genuinely orphaned.
        pruned = []
        for i, row in enumerate(rows):
            if row["parent"]:
                j = i + 1
                while j < len(rows) and rows[j]["parent"]:
                    j += 1
                if j >= len(rows):
                    problems.append(f"SR {sr}: parent '{row['sub_category']}' has no "
                                    f"surviving children -> dropped")
                    continue
            pruned.append(row)

        blocks.append({"sr": sr, "company": d.get("company"),
                       "brand_site": d.get("brand_site"),
                       "country": d.get("country"),
                       "site_url": (d.get("site_url") or "").strip(),
                       "status": d.get("status") or "unknown",
                       "failure_reason": d.get("failure_reason"),
                       "notes": d.get("notes"), "rows": pruned})
    return blocks, problems


def style(ws, r, parent=False):
    for c in range(1, 11):
        cell = ws.cell(r, c)
        cell.font = PARENT_FONT if parent else BODY_FONT
        cell.alignment = Alignment(vertical="center")
        cell.border = CELL_BORDER
        if parent:
            cell.fill = PARENT_FILL


def main():
    lock = os.path.join(PROJ, "~$Final_Company_List (1).xlsx")
    if os.path.exists(lock):
        sys.exit(f"ABORT: workbook is open in Excel (lock file {lock}). Close it first.")

    want = set(int(a) for a in sys.argv[1:]) or set(BATCH)
    roster = load_roster()
    blocks, problems = load_blocks(want)

    wb = openpyxl.load_workbook(BOOK)
    if OUT in wb.sheetnames:
        del wb[OUT]
    ws = wb.create_sheet(OUT)

    ws.append(HDR)
    for c in range(1, 11):
        cell = ws.cell(1, c)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.border = CELL_BORDER
        cell.alignment = Alignment(vertical="center", horizontal="center")
    ws.row_dimensions[1].height = 20

    def classify(b):
        if b["status"] == "failed":
            return "failed"
        if b["sr"] in DUPLICATE_SRS:
            return "duplicate"
        if b["sr"] in LEGIT_ZERO_SRS:
            return "legit_zero"
        if not b["rows"]:
            return "legit_zero"   # safety net: unclassified zero-row block
        return "has_data"

    r = 2
    leaf_total = parent_total = 0
    review = []
    sr_map = []          # (original_sr, company, new_sr) for has_data companies
    excluded = []        # (original_sr, company, category) skipped from Output entirely
    new_sr = 0
    for b in blocks:
        cat = classify(b)
        if cat != "has_data":
            excluded.append((b["sr"], b["company"], cat))
            continue     # no placeholder row -- failed/duplicate/legit_zero don't appear in Output

        new_sr += 1
        sr_map.append((b["sr"], b["company"], new_sr))
        rows = b["rows"]
        prev_cat = None
        for i, row in enumerate(rows):
            if i == 0:
                ws.cell(r, 1, new_sr); ws.cell(r, 2, b["company"])
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
                    review.append((r, b["company"], row["category"], row["sub_category"],
                                   row["qty"],
                                   row.get("flag") or "qty could not be verified",
                                   row["link"]))
            style(ws, r, parent=row["parent"])
            r += 1
        ws.cell(r, 1, None); style(ws, r); r += 1         # separator

    for col, w in zip("ABCDEFGHIJ", (8, 24, 20, 10, 34, 20, 34, 10, 8, 78)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"

    # ---- stamp Status on the Master Company List ----
    mws = wb[MASTER]
    stamped = []
    for b in blocks:
        info = roster.get(b["sr"])
        if not info:
            problems.append(f"SR {b['sr']}: not found in {MASTER}, Status not stamped")
            continue
        cat = classify(b)
        if cat == "duplicate":
            val = "Duplicate"
        elif cat == "failed":
            val = None                                             # blank
        else:                                                       # legit_zero or has_data
            val = {"ok": "Done", "partial": "Partial"}.get(b["status"])
        mws.cell(info["row"], 5, val)
        stamped.append((b["sr"], info["company"], val or "(blank)"))

    wb.save(BOOK)

    # ---- report ----
    print(f"WROTE -> {BOOK}")
    print(f"  sheet '{OUT}': {r-1} rows  |  leaf rows {leaf_total}  parent rows {parent_total}")
    print(f"  companies written: {len(blocks)}\n")
    print(f'{"SR":>3} {"Company":<24} {"status":<8} {"leaf":>5} {"par":>4} {"noqty":>6}  note')
    tot_null = 0
    for b in blocks:
        leaf = [x for x in b["rows"] if not x["parent"]]
        par = len(b["rows"]) - len(leaf)
        nn = sum(1 for x in leaf if x["qty"] is None)
        tot_null += nn
        note = b.get("failure_reason") or b.get("notes") or ""
        print(f'{b["sr"]:>3} {str(b["company"])[:24]:<24} {b["status"]:<8} '
              f'{len(leaf):>5} {par:>4} {nn:>6}  {str(note)[:56]}')
    print(f'\nTOTAL leaf rows {leaf_total} | qty verified {leaf_total-tot_null} '
          f'| needs review {tot_null}')

    print(f"\nSTATUS stamped on '{MASTER}':")
    for sr, name, val in stamped:
        print(f"  S.N. {sr:>3}  {str(name)[:30]:<30} -> {val}")

    print(f"\nOutput sheet SR renumbered 1..{new_sr} ({new_sr} companies with real data); "
          f"master-list S.N. is NOT written to Output. Mapping (master S.N. -> Output SR):")
    for orig_sr, name, out_sr in sr_map:
        print(f"  {orig_sr:>3} -> {out_sr:>3}  {str(name)[:40]}")

    print(f"\nEXCLUDED from Output entirely ({len(excluded)}): "
          f"{sum(1 for _,_,c in excluded if c=='failed')} failed, "
          f"{sum(1 for _,_,c in excluded if c=='duplicate')} duplicate, "
          f"{sum(1 for _,_,c in excluded if c=='legit_zero')} legit_zero")
    for orig_sr, name, cat in excluded:
        print(f"  S.N. {orig_sr:>3}  {str(name)[:35]:<35} [{cat}]")

    missing = sorted(want - {b["sr"] for b in blocks})
    if missing:
        print(f"\nMISSING worker files for SR: {missing}")
    if problems:
        print(f"\nDATA-HYGIENE ACTIONS ({len(problems)}):")
        for p in problems:
            print("  -", p)

    json.dump([{"row": x[0], "company": x[1], "category": x[2], "sub_category": x[3],
                "qty": x[4], "reason": x[5], "link": x[6]} for x in review],
              io.open(os.path.join(SCRATCH, "review.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\nreview rows (qty null or flagged): {len(review)} -> review.json")


if __name__ == "__main__":
    main()
