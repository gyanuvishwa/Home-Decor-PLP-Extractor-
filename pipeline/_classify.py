#!/usr/bin/env python3
"""Classify every archived worker JSON into: failed / duplicate / legit_zero / has_data.

failed       -> status == "failed" (blocked/inaccessible, no data obtained)
duplicate    -> status == "ok", rows == [], notes mention it's the same catalogue as
                another already-completed S.N.
legit_zero   -> status == "ok"/"partial", rows == [], but NOT a duplicate (a genuine
                researched finding of zero in-scope products)
has_data     -> rows non-empty (regardless of status)

Prints a full report so borderline "duplicate vs legit_zero" calls can be eyeballed
before anything is written back to the workbook.
"""
import json, glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ARCHIVE = r"C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\json_archive"

DUP_RE = re.compile(
    r"duplicat|same catalog|same domain|identical domain|same as s\.?n\.?\s*\d+|"
    r"already[- ]completed|already completed|confirms? .{0,40}same|"
    r"confirmed duplicate|treat as duplicate|reference to s\.?n\.?\s*\d+|"
    r"redirect(s|ed)? into|301[- ]redirect",
    re.I,
)

def sr_of(path):
    m = re.search(r"c(\d+)\.json$", os.path.basename(path))
    return int(m.group(1)) if m else -1

results = {"failed": [], "duplicate": [], "legit_zero": [], "has_data": [], "load_error": []}

paths = sorted(glob.glob(os.path.join(ARCHIVE, "c*.json")), key=sr_of)
for path in paths:
    sr = sr_of(path)
    try:
        d = json.load(open(path, encoding="utf-8"))
        if not isinstance(d, dict):
            raise ValueError(f"top-level JSON is {type(d).__name__}, not an object")
    except Exception as e:
        results["load_error"].append((sr, path, str(e)))
        continue
    status = d.get("status")
    rows = d.get("rows") or []
    company = d.get("company")
    notes = (d.get("notes") or "") + " " + (d.get("failure_reason") or "")
    if status == "failed":
        results["failed"].append((sr, company, (d.get("failure_reason") or "")[:160]))
    elif len(rows) == 0:
        if DUP_RE.search(notes):
            results["duplicate"].append((sr, company, notes[:220]))
        else:
            results["legit_zero"].append((sr, company, notes[:220]))
    else:
        results["has_data"].append((sr, company, len(rows)))

print(f"Total archived files scanned: {len(paths)}\n")

for cat in ["failed", "duplicate", "legit_zero", "load_error"]:
    print(f"=== {cat.upper()} ({len(results[cat])}) ===")
    for item in results[cat]:
        print(" ", item)
    print()

print(f"HAS_DATA: {len(results['has_data'])} companies will populate the Output sheet")
print(f"failed + duplicate + legit_zero = {len(results['failed'])+len(results['duplicate'])+len(results['legit_zero'])}")
print(f"Grand total classified = {sum(len(v) for v in results.values())}")

json.dump(
    {k: v for k, v in results.items()},
    open(os.path.join(ARCHIVE, "..", "_classify_report.json"), "w", encoding="utf-8"),
    indent=1, ensure_ascii=False,
)
