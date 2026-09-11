#!/usr/bin/env python3
"""Merge Batch 8 worker JSON into a new workbook preserving Sheet3 structure.

Reads Home_Decor_Extraction_Batch1-7.xlsx, APPENDS batch 8 companies, writes
Home_Decor_Extraction_Batch1-8.xlsx. Batch 1-7 rows are copied verbatim and are
never modified.

Usage:  python merge.py [sr ...]      # default: every roster sr with a c*.json
"""
import json, os, re, shutil, sys, io
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl
from openpyxl.styles import Font, Alignment
from copy import copy

PROJ = r"C:\Users\GyanendraVishwakarma\Web Research Agent"
SRC = os.path.join(PROJ, "Home_Decor_Extraction_Batch1-7.xlsx")
DST = os.path.join(PROJ, "Home_Decor_Extraction_Batch1-8.xlsx")
HERE = os.path.dirname(os.path.abspath(__file__))

# Batch 8 roster: the only Sheet1 companies never extracted in batches 1-7.
# (Sheet1 SR -> company). Order defines output order.
# SR 36 Made In Design is SKIPPED per user instruction (robots.txt opts Anthropic
# crawlers out + Cloudflare 403); it is recorded in the review file, not in Sheet3.
ROSTER = [
    (37, "BHV Marais Maison", "bhv.fr", "France"),
    (51, "Dille & Kamille", "dille-kamille.com", "Netherlands"),
]
SKIPPED = [(36, "Made In Design", "madeindesign.com", "France")]

FIRST_OUT_SR = 85   # continues from Myer Home (84) in Batch1-7

BODY_FONT = Font(name="Calibri", sz=10)
BODY_ALIGN = Alignment(vertical="center")

BANNED = re.compile(
    r'^\s*(shop\s?all|view\s?all|browse\s?all|explore\s?all|see\s?all|all\s+products?|'
    r'discover|collections?|featured|new\s?arrivals?|new\s?in|best\s?sellers?|'
    r'sale|offers?|clearance|outlet|gift\s?guide|lookbook|blog|inspiration)\s*$', re.I)

# A category that is *purely* clocks -> drop outright (spec: never extract clocks).
PURE_CLOCK = re.compile(
    r'^\s*(wall|desk|table|alarm|floor|mantel|cuckoo)?\s*clocks?'
    r'(\s*(collections?|&\s*accessories))?\s*$', re.I)

# A merged category that *contains* clocks alongside in-scope items. Keep the row,
# flag it, and let the user decide.
MIXED_CLOCK = re.compile(r'clocks?', re.I)


def load_rows():
    """Return (blocks, problems). blocks = list of dict per company in ROSTER order."""
    want = set(int(a) for a in sys.argv[1:]) or None
    blocks, problems = [], []
    for sr, name, site, country in ROSTER:
        if want and sr not in want:
            continue
        p = os.path.join(HERE, f"c{sr}.json")
        if not os.path.exists(p):
            problems.append(f"SR {sr} {name}: NO FILE (c{sr}.json missing)")
            continue
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except Exception as e:
            problems.append(f"SR {sr} {name}: BAD JSON: {e}")
            continue

        rows, seen_links, seen_names = [], set(), set()
        for r in d.get("rows") or []:
            sub = (r.get("sub_category") or "").strip()
            cat = (r.get("category") or "").strip()
            link = (r.get("link") or "").strip()
            qty = r.get("qty")
            if not sub:
                problems.append(f"SR {sr}: row with empty sub_category dropped")
                continue
            if BANNED.match(sub) or PURE_CLOCK.match(sub):
                problems.append(f"SR {sr}: dropped banned sub-category '{sub}'")
                continue
            if MIXED_CLOCK.search(sub) and not r.get("flag"):
                r["flag"] = ("MANUAL REVIEW: site merges clocks into this category, "
                             "so the total includes clocks (spec excludes clocks)")
            if link and link in seen_links:
                problems.append(f"SR {sr}: dropped duplicate link for '{sub}'")
                continue
            key = (cat.lower(), sub.lower())
            if key in seen_names:
                problems.append(f"SR {sr}: dropped duplicate '{cat}/{sub}'")
                continue
            if qty == 0:
                problems.append(f"SR {sr}: dropped empty (0-product) category '{sub}'")
                continue
            # English-only guard for batch 8 output.
            for fld, val in (("category", cat), ("sub_category", sub)):
                offenders = [ch for ch in val if ord(ch) > 127]
                if offenders:
                    problems.append(
                        f"SR {sr}: NON-ENGLISH characters {offenders!r} in {fld} "
                        f"'{val}' -> must be translated before merge")
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
            rows.append({"category": cat, "sub_category": sub, "qty": qty,
                         "link": link, "flag": r.get("flag"),
                         "evidence": r.get("evidence")})

        blocks.append({"sr": sr, "company": name, "brand_site": site,
                       "country": country,
                       "site_url": (d.get("site_url") or "").strip(),
                       "status": d.get("status") or "unknown",
                       "failure_reason": d.get("failure_reason"),
                       "notes": d.get("notes"), "rows": rows})
    return blocks, problems


def style(ws, r):
    for c in range(1, 11):
        cell = ws.cell(r, c)
        cell.font = copy(BODY_FONT)
        cell.alignment = copy(BODY_ALIGN)


def main():
    blocks, problems = load_rows()

    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy2(SRC, DST)
    wb = openpyxl.load_workbook(DST)
    ws = wb["Sheet3"]

    # find true last used row
    last = ws.max_row
    while last > 1 and all(ws.cell(last, c).value in (None, "") for c in range(1, 11)):
        last -= 1
    baseline = last
    print(f"batch 1-7 last used Sheet3 row: {baseline} (untouched)")

    out_sr = FIRST_OUT_SR
    r = last + 1
    written = 0
    review = []  # (excel_row, company, category, sub, qty, reason, link)
    for b in blocks:
        ws.cell(r, 1, None)  # blank separator row
        style(ws, r)
        r += 1

        rows = b["rows"]
        if not rows:
            ws.cell(r, 1, out_sr); ws.cell(r, 2, b["company"])
            ws.cell(r, 3, b["brand_site"]); ws.cell(r, 4, b["country"])
            ws.cell(r, 5, b["site_url"])
            reason = (b.get("failure_reason") or b["status"]).strip()
            short = re.split(r'(?<=[.!])\s', reason)[0]
            if len(short) > 150:
                short = short[:147].rstrip() + "..."
            ws.cell(r, 7, f"NOT EXTRACTED — {short}")
            style(ws, r)
            review.append((r, b["company"], "", "NOT EXTRACTED", None, reason, ""))
            r += 1
            out_sr += 1
            continue

        prev_cat = None
        for i, row in enumerate(rows):
            if i == 0:
                ws.cell(r, 1, out_sr); ws.cell(r, 2, b["company"])
                ws.cell(r, 3, b["brand_site"]); ws.cell(r, 4, b["country"])
                ws.cell(r, 5, b["site_url"]); ws.cell(r, 8, "category")
            if row["category"] and row["category"] != prev_cat:
                ws.cell(r, 6, row["category"])
                prev_cat = row["category"]
            ws.cell(r, 7, row["sub_category"])
            if row["qty"] is not None:
                ws.cell(r, 9, row["qty"])
            if row["link"]:
                ws.cell(r, 10, row["link"])
            if row["qty"] is None or row.get("flag"):
                review.append((r, b["company"], row["category"], row["sub_category"],
                               row["qty"],
                               row.get("flag") or "qty could not be verified",
                               row["link"]))
            style(ws, r)
            r += 1
            written += 1
        out_sr += 1

    wb.save(DST)

    # ---- integrity check: batch 1-7 region must be byte-identical in content ----
    a = openpyxl.load_workbook(SRC, data_only=True)["Sheet3"]
    bsh = openpyxl.load_workbook(DST, data_only=True)["Sheet3"]
    diffs = 0
    for rr in range(1, baseline + 1):
        for cc in range(1, 11):
            if a.cell(rr, cc).value != bsh.cell(rr, cc).value:
                diffs += 1
                if diffs <= 5:
                    print(f"  !! row {rr} col {cc}: {a.cell(rr,cc).value!r} -> {bsh.cell(rr,cc).value!r}")
    print(f"batch 1-7 integrity: {'OK - 0 cells changed' if diffs == 0 else f'FAIL - {diffs} cells changed'}")

    # ---- language audit over the ENTIRE output file (read-only, reports only) ----
    audit = []
    for rr in range(2, bsh.max_row + 1):
        for cc in (6, 7):  # Category, Sub-Category
            v = bsh.cell(rr, cc).value
            if isinstance(v, str) and any(ord(ch) > 127 for ch in v):
                who = None
                for back in range(rr, 1, -1):
                    if bsh.cell(back, 2).value:
                        who = bsh.cell(back, 2).value
                        break
                audit.append((rr, who, "Category" if cc == 6 else "Sub-Category", v))
    b8_audit = [a for a in audit if a[0] > baseline]
    print(f"\nLANGUAGE AUDIT: {len(audit)} cells contain non-ASCII characters "
          f"({len(b8_audit)} of them in batch 8)")
    if b8_audit:
        print("  BATCH 8 OFFENDERS (must be fixed):")
        for a in b8_audit:
            print("   ", a)
    if audit:
        by_co = {}
        for rr, who, fld, v in audit:
            by_co.setdefault(who, 0)
            by_co[who] += 1
        print("  pre-existing (batch 1-7, NOT modified) by company:")
        for who, n in sorted(by_co.items(), key=lambda x: -x[1]):
            print(f"    {n:>4}  {who}")
    json.dump([{"row": a[0], "company": a[1], "field": a[2], "value": a[3]} for a in audit],
              io.open(os.path.join(HERE, "language_audit.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # Companion review sheet (separate file so Sheet3 structure is untouched).
    rv = os.path.join(PROJ, "Batch8_Manual_Review.xlsx")
    rwb = openpyxl.Workbook()
    rws = rwb.active
    rws.title = "Manual Review"
    hdr = ["Sheet3 Row", "Company name", "Category", "Sub-Category",
           "qty (blank = unverified)", "Reason", "link"]
    rws.append(hdr)
    for c in range(1, len(hdr) + 1):
        rws.cell(1, c).font = Font(name="Calibri", sz=10, bold=True)
    for sr, name, site, country in SKIPPED:
        rws.append(["(not in Sheet3)", name, "", "SKIPPED BY INSTRUCTION", None,
                    "Made In Design was skipped on user instruction. "
                    "madeindesign.com/robots.txt disallows anthropic-ai, ClaudeBot and "
                    "Claude-Web (Disallow: /), and all HTML requests return HTTP 403 "
                    "behind a Cloudflare 'Just a moment...' challenge. Not extractable "
                    "at the HTTP layer without circumventing an access control; needs a "
                    "real browser session or a licensed data feed.",
                    "https://www.madeindesign.com/"])
    for item in review:
        rws.append(list(item))
    for col, w in zip("ABCDEFG", (11, 24, 24, 34, 22, 62, 72)):
        rws.column_dimensions[col].width = w
    rwb.save(rv)
    print(f"REVIEW -> {rv}  ({len(review)} rows)")

    # ---- report ----
    print(f"WROTE -> {DST}")
    print(f"companies appended: {len(blocks)}   data rows written: {written}\n")
    tot_rows = tot_null = 0
    print(f'{"SR":>4} {"Company":<24} {"status":<8} {"rows":>5} {"noqty":>6}  note')
    for b in blocks:
        n = len(b["rows"])
        nn = sum(1 for x in b["rows"] if x["qty"] is None)
        tot_rows += n; tot_null += nn
        note = b.get("failure_reason") or b.get("notes") or ""
        print(f'{b["sr"]:>4} {b["company"][:24]:<24} {b["status"]:<8} {n:>5} {nn:>6}  {str(note)[:60]}')
    print(f'\nTOTAL rows {tot_rows} | qty verified {tot_rows-tot_null} | needs review {tot_null}')
    if problems:
        print(f"\nDATA-HYGIENE ACTIONS ({len(problems)}):")
        for p in problems:
            print("  -", p)


if __name__ == "__main__":
    main()
