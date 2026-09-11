#!/usr/bin/env python3
"""One-time reconstruction: Bathroom.xlsx (Output/Processing Ledger/Review) -> b<SR>.json.

The Bathroom run (SR 1-196) was done on another machine which delivered only
the merged workbook, not the per-company worker JSON the rest of this
pipeline's tooling expects (f<SR>.json / pc<SR>.json / se<SR>.json). This
script rebuilds that missing archive layer from the workbook so future
merges/re-merges of the Bathroom run can work the same way every other
category does.

Row schema matches pc<SR>.json: {category, sub_category, qty, link, is_group,
evidence, flag}. `evidence` and `flag` are not separable from the ledger's
free-text Notes column, so evidence is left null on reconstructed rows and
the full Notes text is preserved verbatim in the JSON's top-level `notes`
field (same place merge scripts read from) - nothing is lost, it is just not
re-split per-row.
"""
import json
import sys
import openpyxl

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\GyanendraVishwakarma\Downloads\Bathroom.xlsx"
OUT_DIR = "pipeline/bathroom_json_archive"

wb = openpyxl.load_workbook(SRC, data_only=True)
ws_out = wb["Output"]
ws_ledger = wb["Processing Ledger"]
ws_review = wb["Review"]

# ---- Ledger: sr -> {company, country, website, found, count, status, notes}
ledger = {}
for r in range(2, ws_ledger.max_row + 1):
    sr = ws_ledger.cell(r, 1).value
    if sr is None:
        continue
    ledger[sr] = {
        "company": ws_ledger.cell(r, 2).value,
        "country": ws_ledger.cell(r, 3).value,
        "website": ws_ledger.cell(r, 4).value,
        "found": ws_ledger.cell(r, 5).value,
        "count": ws_ledger.cell(r, 6).value,
        "status": ws_ledger.cell(r, 7).value,
        "notes": ws_ledger.cell(r, 8).value,
    }

# ---- Output: walk blocks. A row with col A (Maisons) set starts a new
# company block and is itself the first category-section row.
blocks = {}  # sr -> list of row dicts (category, sub_category, qty, link, is_group)
cur_sr = None
cur_category = None
for r in range(2, ws_out.max_row + 1):
    maisons = ws_out.cell(r, 1).value
    category = ws_out.cell(r, 6).value
    sub_category = ws_out.cell(r, 7).value
    qty = ws_out.cell(r, 9).value
    link = ws_out.cell(r, 10).value

    if maisons is not None:
        cur_sr = maisons
        blocks.setdefault(cur_sr, [])

    if category is not None:
        cur_category = category

    if cur_sr is None:
        continue
    if sub_category is None and category is None:
        continue  # blank separator row

    is_group = qty is None and link is None
    blocks[cur_sr].append(
        {
            "category": cur_category or category,
            "sub_category": sub_category if sub_category is not None else category,
            "qty": qty,
            "link": link,
            "is_group": is_group,
            "evidence": None,
            "flag": None,
        }
    )

# The block's own banner row (category==sub_category=="Bathroom", qty/link
# blank) duplicates the top-level grouping and is not a row in the pc<SR>.json
# sense for other categories - keep it anyway as a grouping row; merge script
# dedup on (category, sub_category, link) will collapse true duplicates.

# ---- Review: sr -> list of review rows (kept in notes as a rendered block,
# since the pc<SR>.json contract has no separate review[] field - merge
# scripts build Review purely from rows flagged in notes/flag today, so we
# preserve these as an appendix in notes text instead of silently dropping
# them).
review_by_sr = {}
for r in range(2, ws_review.max_row + 1):
    sr = ws_review.cell(r, 1).value
    if sr is None:
        continue
    review_by_sr.setdefault(sr, []).append(
        {
            "category": ws_review.cell(r, 3).value,
            "sub_category": ws_review.cell(r, 4).value,
            "qty": ws_review.cell(r, 5).value,
            "issue": ws_review.cell(r, 6).value,
            "link": ws_review.cell(r, 7).value,
        }
    )

written = 0
for sr, led in ledger.items():
    status = (led["status"] or "").upper()
    if status == "PENDING":
        continue  # nothing to reconstruct - not yet processed

    if status == "BATHROOM FOUND":
        py_status = "ok"
        failure_reason = None
    elif status == "NO BATHROOM FOUND":
        py_status = "ok"
        failure_reason = None
    elif "BLOCKED" in status:
        py_status = "blocked"
        failure_reason = "ACCESS FAILURE (see notes)"
    else:
        py_status = "unknown"
        failure_reason = f"unrecognised ledger status: {led['status']!r}"

    rows = blocks.get(sr, [])
    review_rows = review_by_sr.get(sr, [])

    record = {
        "status": py_status,
        "failure_reason": failure_reason,
        "notes": led["notes"] or "",
        "rows": rows,
        "review": review_rows,  # extra field vs. the pc<SR>.json contract -
                                 # kept for lossless reconstruction; merge
                                 # script should read it explicitly.
        "_reconstructed_from": "Bathroom.xlsx delivered 2026-09-01 (checkpoint), not original worker JSON",
    }

    with open(f"{OUT_DIR}/b{sr}.json", "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1, ensure_ascii=False)
    written += 1

print(f"Reconstructed {written} b<SR>.json files (of {len(ledger)} roster entries).")
pending = [sr for sr, led in ledger.items() if (led["status"] or "").upper() == "PENDING"]
print(f"Pending (no file written, still to extract): {len(pending)} -> {sorted(pending)[:10]}...")
