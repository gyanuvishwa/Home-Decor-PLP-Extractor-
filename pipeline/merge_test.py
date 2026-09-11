#!/usr/bin/env python3
"""Merge test-performance worker JSON (t*.json) into 'Test Performance.xlsx'.

Sheet 1 "Test Performance" uses the exact Sheet3/work column order:
  SR No. | Company Name | Brand Site | Country | Site URL | Category |
  Sub-Category | Type | Qty | Link

Sheet 2 "Comparison" benchmarks this run against the existing `work` sheet in
`new companies list77.xlsm` (the prior extraction of the same 10 companies).
Sheet 3 "Manual Review" lists every row whose qty could not be verified.

Idempotent: rebuilds the whole file from the t*.json files every run.
"""
import io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

PROJ = r"C:\Users\GyanendraVishwakarma\Web Research Agent"
DST = os.path.join(PROJ, "Test Performance.xlsx")
REF = os.path.join(PROJ, "new companies list77.xlsm")
HERE = os.path.dirname(os.path.abspath(__file__))

# The 10 companies taken from the "test" sheet (SR 1-10), in sheet order.
ROSTER = [
    (1,  "Quince Home",    "quince.com",       "USA"),
    (2,  "Simons Maison",  "simons.ca",        "Canada"),
    (3,  "JCPenney Home",  "jcpenney.com",     "USA"),
    (4,  "Kohl's Home",    "kohls.com",        "USA"),
    (5,  "Sur La Table",   "surlatable.com",   "USA"),
    (6,  "Etsy US",        "etsy.com",         "USA"),
    (7,  "Indigo Home",    "indigo.ca",        "Canada"),
    (8,  "AllModern",      "allmodern.com",    "USA"),
    (9,  "Birch Lane",     "birchlane.com",    "USA"),
    (10, "Joss & Main",    "jossandmain.com",  "USA"),
    (11, "Lamps Plus",             "lampsplus.com",       "USA"),
    (12, "Bouclair",               "bouclair.com",        "Canada"),
    (13, "Saks Home",              "saksfifthavenue.com", "USA"),
    (14, "Lumens",                 "lumens.com",          "USA"),
    (15, "Shades of Light",        "shadesoflight.com",   "USA"),
    (16, "Grandin Road",           "grandinroad.com",     "USA"),
    (17, "Muuto US",               "muuto.com",           "USA"),
    (18, "2Modern",                "2modern.com",         "USA"),
    (19, "Design Public",          "designpublic.com",    "USA"),
    (20, "Lightology",             "lightology.com",      "USA"),
    (21, "Terrain",                "shopterrain.com",     "USA"),
    (22, "Design Within Reach",    "dwr.com",             "USA"),
    (23, "Hudson Valley Lighting", "hvlgroup.com",        "USA"),
    (24, "Visual Comfort",         "visualcomfort.com",   "USA"),
    (25, "Cello World",            "celloworld.com",      "India"),
    (26, "Milton",                 "milton.in",           "India"),
    (27, "Pepperfry",              "pepperfry.com",       "India"),
    (28, "Myntra Home",            "myntra.com",          "India"),
    (29, "AJIO Home",              "ajio.com",            "India"),
    (30, "FOS Lighting",           "foslighting.in",      "India"),
]

HDR = ["SR No.", "Company Name", "Brand Site", "Country", "Site URL",
       "Category", "Sub-Category", "Type", "Qty", "Link"]

BODY_FONT = Font(name="Calibri", sz=10)
HDR_FONT = Font(name="Calibri", sz=10, bold=True)
HDR_FILL = PatternFill("solid", fgColor="DDEBF7")
BODY_ALIGN = Alignment(vertical="center")

BANNED = re.compile(
    r'^\s*(shop\s?all|view\s?all|browse\s?all|explore\s?all|see\s?all|all\s+products?|'
    r'discover|collections?|featured|new\s?arrivals?|new\s?in|best\s?sellers?|'
    r'sale|offers?|clearance|outlet|gift\s?guide|lookbook|blog|inspiration)\s*$', re.I)
PURE_CLOCK = re.compile(
    r'^\s*(wall|desk|table|alarm|floor|mantel|cuckoo)?\s*clocks?'
    r'(\s*(collections?|&\s*accessories))?\s*$', re.I)
MIXED_CLOCK = re.compile(r'clocks?', re.I)


def load_blocks():
    blocks, problems = [], []
    for sr, name, site, country in ROSTER:
        p = os.path.join(HERE, f"t{sr}.json")
        if not os.path.exists(p):
            problems.append(f"SR {sr} {name}: NO FILE (t{sr}.json missing)")
            blocks.append({"sr": sr, "company": name, "brand_site": site,
                           "country": country, "site_url": "", "status": "missing",
                           "failure_reason": "worker produced no output file",
                           "notes": None, "rows": []})
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
            for fld, val in (("category", cat), ("sub_category", sub)):
                bad = [ch for ch in val if ord(ch) > 127]
                if bad:
                    problems.append(f"SR {sr}: NON-ENGLISH chars {bad!r} in {fld} '{val}'")
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


def read_reference():
    """Prior extraction of the same companies, from the `work` sheet."""
    if not os.path.exists(REF):
        return {}
    ws = openpyxl.load_workbook(REF, data_only=True, read_only=True)["work"]
    out, cur = {}, None
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[1]:
            cur = str(r[1]).strip()
            out.setdefault(cur, [])
        if cur and (r[6] or r[9]):
            q = r[8]
            try:
                q = int(str(q).strip()) if q not in (None, "") else None
            except ValueError:
                q = None
            out[cur].append({"sub": str(r[6] or "").strip(), "qty": q,
                             "link": str(r[9] or "").strip()})
    return out


def norm(s):
    s = re.sub(r'[^a-z0-9]+', ' ', (s or "").lower()).strip()
    s = re.sub(r'\b(and)\b', '', s).strip()
    # crude singularisation so "Vases" ~ "Vase", "Mirrors" ~ "Mirror"
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s") else w for w in s.split())


def style_row(ws, r, ncols=10):
    for c in range(1, ncols + 1):
        ws.cell(r, c).font = Font(name="Calibri", sz=10)
        ws.cell(r, c).alignment = Alignment(vertical="center")


def main():
    blocks, problems = load_blocks()
    ref = read_reference()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Performance"
    ws.append(HDR)
    for c in range(1, 11):
        ws.cell(1, c).font = HDR_FONT
        ws.cell(1, c).fill = HDR_FILL

    r = 2
    written = 0
    review = []
    for b in blocks:
        rows = b["rows"]
        if not rows:
            ws.cell(r, 1, b["sr"]); ws.cell(r, 2, b["company"])
            ws.cell(r, 3, b["brand_site"]); ws.cell(r, 4, b["country"])
            ws.cell(r, 5, b["site_url"])
            reason = str(b.get("failure_reason") or b["status"]).strip()
            short = re.split(r'(?<=[.!])\s', reason)[0]
            if len(short) > 150:
                short = short[:147].rstrip() + "..."
            ws.cell(r, 7, f"NOT EXTRACTED - {short}")
            style_row(ws, r)
            review.append([b["sr"], b["company"], "", "NOT EXTRACTED", None, reason, ""])
            r += 1
            continue

        prev_cat = None
        for i, row in enumerate(rows):
            if i == 0:
                ws.cell(r, 1, b["sr"]); ws.cell(r, 2, b["company"])
                ws.cell(r, 3, b["brand_site"]); ws.cell(r, 4, b["country"])
                ws.cell(r, 5, b["site_url"])
            if row["category"] and row["category"] != prev_cat:
                ws.cell(r, 6, row["category"])
                prev_cat = row["category"]
            ws.cell(r, 7, row["sub_category"])
            ws.cell(r, 8, "Category")
            if row["qty"] is not None:
                ws.cell(r, 9, row["qty"])
            if row["link"]:
                ws.cell(r, 10, row["link"])
            if row["qty"] is None or row.get("flag"):
                review.append([b["sr"], b["company"], row["category"], row["sub_category"],
                               row["qty"], row.get("flag") or "qty could not be verified",
                               row["link"]])
            style_row(ws, r)
            r += 1
            written += 1

    for col, w in zip("ABCDEFGHIJ", (8, 22, 20, 10, 34, 22, 34, 10, 8, 60)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"

    # ---------------- Comparison sheet ----------------
    cs = wb.create_sheet("Comparison")
    chdr = ["SR No.", "Company Name", "Status", "This run: rows",
            "Prior run: rows", "Sub-categories matched", "Only in this run",
            "Only in prior run", "Qty same", "Qty differs", "Qty new (prior blank)",
            "Qty lost (this blank)", "Notes"]
    cs.append(chdr)
    for c in range(1, len(chdr) + 1):
        cs.cell(1, c).font = HDR_FONT
        cs.cell(1, c).fill = HDR_FILL

    detail = []
    tot = dict(mine=0, theirs=0, match=0, same=0, diff=0, new=0, lost=0)
    for b in blocks:
        mine = {norm(x["sub_category"]): x for x in b["rows"]}
        theirs = {norm(x["sub"]): x for x in ref.get(b["company"], [])}
        keys = set(mine) & set(theirs)
        same = diff = newq = lostq = 0
        for k in sorted(keys):
            a, c = mine[k]["qty"], theirs[k]["qty"]
            if a is not None and c is not None:
                if a == c:
                    same += 1
                    verdict = "same"
                else:
                    diff += 1
                    verdict = "DIFFERS"
            elif a is not None and c is None:
                newq += 1; verdict = "new (prior had no qty)"
            elif a is None and c is not None:
                lostq += 1; verdict = "this run has no qty"
            else:
                verdict = "both blank"
            detail.append([b["sr"], b["company"], mine[k]["sub_category"],
                           theirs[k]["sub"], a, c, verdict,
                           (f"{abs(a-c)} ({abs(a-c)/c*100:.0f}%)" if a is not None
                            and c not in (None, 0) and a != c else ""),
                           mine[k]["link"]])
        only_mine = sorted(mine[k]["sub_category"] for k in set(mine) - set(theirs))
        only_theirs = sorted(theirs[k]["sub"] for k in set(theirs) - set(mine))
        cs.append([b["sr"], b["company"], b["status"], len(b["rows"]),
                   len(ref.get(b["company"], [])), len(keys),
                   "; ".join(only_mine)[:32000], "; ".join(only_theirs)[:32000],
                   same, diff, newq, lostq,
                   str(b.get("failure_reason") or b.get("notes") or "")[:500]])
        tot["mine"] += len(b["rows"]); tot["theirs"] += len(ref.get(b["company"], []))
        tot["match"] += len(keys); tot["same"] += same; tot["diff"] += diff
        tot["new"] += newq; tot["lost"] += lostq
    cs.append([])
    cs.append(["", "TOTAL", "", tot["mine"], tot["theirs"], tot["match"], "", "",
               tot["same"], tot["diff"], tot["new"], tot["lost"], ""])
    for c in range(1, len(chdr) + 1):
        cs.cell(cs.max_row, c).font = HDR_FONT
    for col, w in zip("ABCDEFGHIJKLM", (8, 20, 9, 13, 13, 13, 46, 46, 10, 11, 12, 12, 50)):
        cs.column_dimensions[col].width = w
    cs.freeze_panes = "A2"

    # ---------------- Qty detail sheet ----------------
    ds = wb.create_sheet("Qty Comparison")
    dhdr = ["SR No.", "Company Name", "Sub-Category (this run)",
            "Sub-Category (prior run)", "Qty this run", "Qty prior run",
            "Verdict", "Delta", "Link"]
    ds.append(dhdr)
    for c in range(1, len(dhdr) + 1):
        ds.cell(1, c).font = HDR_FONT
        ds.cell(1, c).fill = HDR_FILL
    for row in detail:
        ds.append(row)
    for col, w in zip("ABCDEFGHI", (8, 20, 34, 34, 12, 12, 22, 14, 60)):
        ds.column_dimensions[col].width = w
    ds.freeze_panes = "A2"

    # ---------------- Manual review sheet ----------------
    rs = wb.create_sheet("Manual Review")
    rhdr = ["SR No.", "Company Name", "Category", "Sub-Category",
            "Qty (blank = unverified)", "Reason", "Link"]
    rs.append(rhdr)
    for c in range(1, len(rhdr) + 1):
        rs.cell(1, c).font = HDR_FONT
        rs.cell(1, c).fill = HDR_FILL
    for item in review:
        rs.append(item)
    for col, w in zip("ABCDEFG", (8, 22, 22, 34, 22, 70, 60)):
        rs.column_dimensions[col].width = w
    rs.freeze_panes = "A2"

    if os.path.exists(DST):
        os.remove(DST)
    wb.save(DST)

    # ---------------- report ----------------
    print(f"WROTE -> {DST}")
    print(f"companies: {len(blocks)}   data rows: {written}\n")
    print(f'{"SR":>3} {"Company":<20} {"status":<8} {"rows":>5} {"noqty":>6} '
          f'{"prior":>6} {"match":>6} {"same":>5} {"diff":>5}')
    tr = tn = 0
    for b in blocks:
        n = len(b["rows"]); nn = sum(1 for x in b["rows"] if x["qty"] is None)
        tr += n; tn += nn
        mine = {norm(x["sub_category"]) for x in b["rows"]}
        th = {norm(x["sub"]): x for x in ref.get(b["company"], [])}
        k = mine & set(th)
        s = sum(1 for kk in k
                for a in [next(x["qty"] for x in b["rows"] if norm(x["sub_category"]) == kk)]
                if a is not None and th[kk]["qty"] is not None and a == th[kk]["qty"])
        d = sum(1 for kk in k
                for a in [next(x["qty"] for x in b["rows"] if norm(x["sub_category"]) == kk)]
                if a is not None and th[kk]["qty"] is not None and a != th[kk]["qty"])
        print(f'{b["sr"]:>3} {b["company"][:20]:<20} {b["status"]:<8} {n:>5} {nn:>6} '
              f'{len(th):>6} {len(k):>6} {s:>5} {d:>5}')
    print(f'\nTOTAL rows {tr} | qty verified {tr-tn} | needs review {tn}')
    print(f'qty agreement on matched sub-categories: same {tot["same"]}, '
          f'differs {tot["diff"]}, new {tot["new"]}, lost {tot["lost"]}')
    if problems:
        print(f"\nDATA-HYGIENE ACTIONS ({len(problems)}):")
        for p in problems:
            print("  -", p)


if __name__ == "__main__":
    main()
