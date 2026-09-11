#!/usr/bin/env python3
"""Post-merge validation of Seasonal.xlsx + protected-file check.

Run after EVERY merge_seasonal.py, no exceptions (SKILL.md SS7). Two checks
are hard failures (asserted, not just printed):
  1. STRICT whole-file duplicate-URL check -- a link used by more than one
     DIFFERENT company is always a bug.
  2. JUNK/non-canonical URL check -- a category link that is actually a
     PDP/search/tracking/campaign/blog/editorial/image/pagination URL.
"""
import os, re, sys, json, hashlib, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl

SCRATCH = os.path.dirname(os.path.abspath(__file__))
PROJ = r"C:\Users\GyanendraVishwakarma\Web Research Agent"
BOOK = os.path.join(PROJ, "Seasonal.xlsx")
PROTECTED = ["Kitchen_and_Dining.xlsx", "Lighting.xlsx", "Wall_Decor.xlsx",
             "Decorative_Home_Accessories.xlsx", "Furniture.xlsx", "Textile.xlsx",
             "Storage.xlsx", "Pet_Care.xlsx", "Final_Company_List (1).xlsx"]

# Same duplicate roster entry already resolved in Furniture/Pet Care -- SR 286
# = SR 165 "Noon UAE", same company. Dropped entirely by merge_seasonal.py.
# Ledger is intentionally 286 - len(this set), not 286.
KNOWN_ROSTER_DUPLICATES = {286}

# Mirrors merge_seasonal.py's JUNK_URL / SEARCH_URL -- kept in sync manually,
# this is an independent cross-check, not a re-import, on purpose (catches a
# merge-script regression rather than trusting the same regex against itself).
JUNK_URL = re.compile(
    r'(?:r\.jina\.ai|translate\.goog|web\.archive\.org|webcache|'
    r'/blog/|/blogs/|/editorial/|/journal/|/magazine/|/inspiration/|/lookbook/|'
    r'/product/|/products/[^/?]+-p-|/p/\d+|/dp/\d+|/pd/|'
    r'\.(?:jpg|jpeg|png|gif|webp|svg)(?:\?|$)|'
    r'/cart|/checkout|/account|/wishlist|'
    r'utm_[a-z]+=|[?&]campaign=|[?&]affiliate=|'
    r'[?&]page=\d+$)', re.I)

# Mirrors merge_seasonal.py's JUNK_URL_VERIFIED_EXCEPTIONS -- kept in sync
# manually, same reasoning: these 9 AmbienteDirect (SR 157) URLs were
# individually confirmed (orchestrator verify pass, 2026-09-04) via a live
# re-fetch showing genuine schema.org ItemList product-grid markup
# (numberOfItems present), not editorial/lookbook content. The site files
# real holiday PLPs under /inspiration/design-special/<slug>, which the
# general JUNK_URL /inspiration/ heuristic correctly rejects for every other
# site but false-positives on here.
JUNK_URL_VERIFIED_EXCEPTIONS = {
    "https://www.ambientedirect.com/inspiration/design-special/weihnachtsdeko",
    "https://www.ambientedirect.com/inspiration/design-special/advent",
    "https://www.ambientedirect.com/inspiration/design-special/christbaumschmuck",
    "https://www.ambientedirect.com/inspiration/design-special/alessi-xmas",
    "https://www.ambientedirect.com/inspiration/design-special/valentinstag",
    "https://www.ambientedirect.com/inspiration/design-special/happy-ostern",
    "https://www.ambientedirect.com/inspiration/design-special/silvester-glamour",
    "https://www.ambientedirect.com/inspiration/design-special/geschenke-zum-vatertag",
    "https://www.ambientedirect.com/inspiration/design-special/geschenke-zum-muttertag",
}
SEARCH_URL = re.compile(r'[?&](q|query|search|keyword)=|/search(/|\?|$)', re.I)


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
        if not os.path.exists(p):
            print(f"  {f:<38} (not found)")
            continue
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        exp = base.get(f)
        state = "UNCHANGED" if exp == h else ("MODIFIED !!!" if exp else "(no baseline)")
        print(f"  {f:<38} {state}")

    print("\n=== Seasonal.xlsx ===")
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

    # duplicate (company, category, sub-category, qty, link)
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

    # STRICT whole-file duplicate URL check -- a link must never repeat across
    # DIFFERENT companies (each URL belongs to exactly one company's domain;
    # a cross-company repeat means a copy-paste/wrong-company-assigned bug).
    # MANDATORY on every merge (SKILL.md SS7 item 4) -- hard assert below, not
    # a warning.
    cur = None
    link_owners = collections.defaultdict(set)
    link_rows = collections.defaultdict(list)
    for r in rows:
        if r[0] is not None:
            cur = (r[0], r[1])
        if r[9]:
            link_owners[r[9]].add(cur)
            link_rows[r[9]].append((cur, r[6]))
    cross_company_dupes = {link: owners for link, owners in link_owners.items() if len(owners) > 1}
    print(f"  STRICT: same URL used by >1 company: {len(cross_company_dupes)}")
    for link, owners in list(cross_company_dupes.items())[:20]:
        print("      ", link)
        for (sr, comp), sub in link_rows[link]:
            if (sr, comp) in owners:
                print("          ->", sr, comp, "/", sub)

    # non-ASCII
    na = [(r[5], r[6]) for r in rows if any(ord(ch) > 127 for ch in str(r[5] or "") + str(r[6] or ""))]
    print(f"  non-ASCII cells     {len(na)}")
    for x in na[:20]:
        print("      ", x)

    # JUNK / non-canonical URLs (PDP, search, tracking/campaign, blog/editorial,
    # image, pagination) -- explicit user requirement, checked on every merge.
    junk = [(r[5], r[6], r[9]) for r in rows if r[9] and JUNK_URL.search(str(r[9]))
            and str(r[9]) not in JUNK_URL_VERIFIED_EXCEPTIONS]
    search_like = [(r[5], r[6], r[9]) for r in rows if r[9] and SEARCH_URL.search(str(r[9]))
                   and not JUNK_URL.search(str(r[9]))]
    not_http = [(r[5], r[6], r[9]) for r in rows if r[9] and not str(r[9]).startswith("http")]
    print(f"  JUNK URLs (PDP/blog/tracking/image/etc): {len(junk)}")
    for x in junk[:30]:
        print("      ", x)
    print(f"  search-like URLs (kept, must be flagged): {len(search_like)}")
    for x in search_like[:20]:
        print("      ", x)
    print(f"  non-http(s) / relative URLs: {len(not_http)}")
    for x in not_http[:20]:
        print("      ", x)

    # qty sanity
    q = [r[8] for r in leaves if isinstance(r[8], int)]
    print(f"  leaf rows with qty  {len(q)} / {len(leaves)}   (null qty {len(leaves)-len(q)})")

    # category = holiday name sanity: every leaf must carry a category
    cur_cat = None
    no_cat = 0
    for r in rows:
        if r[0] is not None:
            cur_cat = None
        if r[6]:
            cur_cat = r[6]
        if r[9] and not cur_cat:
            no_cat += 1
    print(f"  leaf rows missing a category (holiday) name: {no_cat}")

    expected_ledger_rows = 286 - len(KNOWN_ROSTER_DUPLICATES)
    lw = wb["Processing Ledger"]
    lrows = list(lw.iter_rows(min_row=2, values_only=True))
    lrows = [r for r in lrows if r[0] is not None]
    st = collections.Counter(r[6] for r in lrows)
    print("\n=== LEDGER ===")
    print(f"  ledger rows         {len(lrows)}  (must be {expected_ledger_rows}: "
          f"286 roster entries minus {len(KNOWN_ROSTER_DUPLICATES)} known "
          f"roster duplicate(s) {sorted(KNOWN_ROSTER_DUPLICATES)})")
    lsrs = [r[0] for r in lrows]
    print(f"  unique SR           {len(set(lsrs))}")
    dup_srs_present = KNOWN_ROSTER_DUPLICATES & set(lsrs)
    print(f"  known duplicates still in ledger: {sorted(dup_srs_present) or 'none'}")
    for k, v in st.items():
        print(f"  {k:<26} {v}")
    print(f"  {'SUM':<26} {sum(st.values())}")

    rw = wb["Review"]
    rrows = [r for r in rw.iter_rows(min_row=2, values_only=True) if r[0] is not None]
    print(f"\n  review rows         {len(rrows)}")

    ok = (sum(st.values()) == len(lrows) and not cross_company_dupes and not junk)
    print("\nOK" if ok else "\nRECONCILIATION FAILED")

    assert len(lrows) <= expected_ledger_rows, (
        f"LEDGER HAS MORE ROWS THAN EXPECTED (got {len(lrows)}, max {expected_ledger_rows}) "
        "-- partial batches are fine as long as this doesn't exceed the full roster")
    assert not dup_srs_present, (
        f"KNOWN ROSTER DUPLICATE(S) STILL IN LEDGER: {sorted(dup_srs_present)}")
    assert not cross_company_dupes, (
        f"STRICT DUPLICATE URL CHECK FAILED -- {len(cross_company_dupes)} link(s) "
        "assigned to more than one company (see list above)"
    )
    assert not junk, (
        f"JUNK URL CHECK FAILED -- {len(junk)} category link(s) look like PDP/search/"
        "tracking/blog/image/pagination URLs, not category PLPs (see list above). "
        "merge_seasonal.py should have flagged these to Review instead of leaving "
        "them silently in the Output link column -- treat this as a merge-script bug."
    )


if __name__ == "__main__":
    main()
