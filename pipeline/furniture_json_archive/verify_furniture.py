#!/usr/bin/env python3
"""Post-merge validation of Furniture.xlsx (spec §30/§31) + protected-file check."""
import os, re, sys, json, hashlib, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl

SCRATCH = os.path.dirname(os.path.abspath(__file__))
PROJ = r"C:\Users\GyanendraVishwakarma\Web Research Agent"
BOOK = os.path.join(PROJ, "Furniture.xlsx")
PROTECTED = ["Kitchen_and_Dining.xlsx", "Lighting.xlsx", "Wall_Decor.xlsx",
             "Decorative_Home_Accessories.xlsx", "Final_Company_List (1).xlsx"]

BAD_CAT = re.compile(
    r'\b(lamps?|lighting|chandeliers?|sconces?|mirrors?|clocks?|wall\s?art|vases?|'
    r'candle\s?holders?|glassware|dinnerware|serveware|plates?|bowls?|mugs?|'
    r'rugs?|cushions?|curtains?|bedding|towels?|storage\s?(baskets?|boxes|bins?)|'
    r'sinks?|toilets?|bathtubs?|taps?|faucets?)\b', re.I)
OK_OVERRIDE = re.compile(
    r'\b(tables?|beds?|bed\s?frames?|cabinets?|sideboards?|wardrobes?|dressers?|'
    r'bookcases?|shelving|tv\s?units?|media\s?units?|sofas?|chairs?|armchairs?|'
    r'stools?|benches?|ottomans?|desks?|vanit(y|ies)|furniture|chest)\b', re.I)
BANNED_URL = re.compile(r'(r\.jina\.ai|translate\.goog|web\.archive\.org|/search|[?&]q=)', re.I)


def main():
    print("=== PROTECTED FILES ===")
    base = {}
    bl = os.path.join(SCRATCH, "protected_baseline.sha256")
    if os.path.exists(bl):
        for line in open(bl, encoding="utf-8"):
            h, _, name = line.strip().partition(" ")
            base[name.lstrip("*").strip()] = h
    for f in PROTECTED:
        p = os.path.join(PROJ, f)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        exp = base.get(f)
        state = "UNCHANGED" if exp == h else ("MODIFIED !!!" if exp else "(no baseline)")
        print(f"  {f:<38} {state}")

    print("\n=== Furniture.xlsx ===")
    wb = openpyxl.load_workbook(BOOK, read_only=True, data_only=True)
    print("  sheets:", wb.sheetnames)
    ws = wb["Output"]
    rows = list(ws.iter_rows(min_row=2, values_only=True))

    companies = [r for r in rows if r[0] is not None]
    leaves = [r for r in rows if (r[8] is not None or r[9])]
    groups = [r for r in rows if r[6] and r[8] is None and not r[9]]
    blanks = [r for r in rows if not any(v is not None for v in r)]
    print(f"  total rows          {len(rows)}")
    print(f"  companies           {len(companies)}")
    print(f"  leaf rows           {len(leaves)}")
    print(f"  grouping rows       {len(groups)}")
    print(f"  separator rows      {len(blanks)}")

    srs = [r[0] for r in companies]
    assert len(srs) == len(set(srs)), "DUPLICATE SR in Output"
    print(f"  SR unique           yes ({min(srs)}..{max(srs)})" if srs else "  (empty)")

    # duplicate (company, sub-category, qty, link)
    cur = None
    seen = collections.Counter()
    for r in rows:
        if r[0] is not None:
            cur = r[1]
        if r[9]:
            seen[(cur, r[6], r[8], r[9])] += 1
    dups = {k: v for k, v in seen.items() if v > 1}
    print(f"  duplicate records   {len(dups)}")
    for k, v in list(dups.items())[:20]:
        print("      ", v, k)

    # duplicate links within a company
    cur = None
    bycomp = collections.defaultdict(collections.Counter)
    for r in rows:
        if r[0] is not None:
            cur = r[1]
        if r[9]:
            bycomp[cur][r[9]] += 1
    dl = [(c, l, n) for c, cnt in bycomp.items() for l, n in cnt.items() if n > 1]
    print(f"  same link twice in one company: {len(dl)}")
    for x in dl[:20]:
        print("      ", x)

    # non-ASCII
    na = [(r[5], r[6]) for r in rows if any(ord(ch) > 127 for ch in str(r[5] or "") + str(r[6] or ""))]
    print(f"  non-ASCII cells     {len(na)}")
    for x in na[:20]:
        print("      ", x)

    # bad URLs
    bad = [(r[6], r[9]) for r in rows if r[9] and (BANNED_URL.search(str(r[9])) or not str(r[9]).startswith("http"))]
    print(f"  suspect URLs        {len(bad)}")
    for x in bad[:20]:
        print("      ", x)

    # grouping rows carrying qty/link
    bg = [r[6] for r in rows if r[6] and r[7] is None and r[0] is None and False]
    # non-furniture-looking sub-categories
    nf = [(r[5], r[6]) for r in rows if r[6] and BAD_CAT.search(str(r[6])) and not OK_OVERRIDE.search(str(r[6]))]
    print(f"  non-furniture-looking sub-categories: {len(nf)}")
    for x in nf[:40]:
        print("      ", x)

    # qty sanity
    q = [r[8] for r in leaves if isinstance(r[8], int)]
    print(f"  leaf rows with qty  {len(q)} / {len(leaves)}   (null qty {len(leaves)-len(q)})")

    lw = wb["Processing Ledger"]
    lrows = list(lw.iter_rows(min_row=2, values_only=True))
    lrows = [r for r in lrows if r[0] is not None]
    st = collections.Counter(r[6] for r in lrows)
    print("\n=== LEDGER ===")
    print(f"  ledger rows         {len(lrows)}  (must be 286)")
    lsrs = [r[0] for r in lrows]
    print(f"  unique SR           {len(set(lsrs))}")
    for k, v in st.items():
        print(f"  {k:<26} {v}")
    print(f"  {'SUM':<26} {sum(st.values())}")
    assert len(lrows) == 286, "LEDGER IS NOT 286 ROWS"
    print("\nOK" if sum(st.values()) == 286 else "\nRECONCILIATION FAILED")


if __name__ == "__main__":
    main()
