#!/usr/bin/env python3
"""Scan every b<SR>.json for non-ASCII text in category/sub_category fields
(rows[] and review[]). Exit code 1 and a listing if anything remains.

Usage:  python check_english_only.py
"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRATCH = os.path.dirname(os.path.abspath(__file__))


def has_nonascii(s):
    return any(ord(ch) > 127 for ch in (s or ""))


def main():
    bad = []
    for f in sorted(glob.glob(os.path.join(SCRATCH, "b*.json")),
                     key=lambda p: int(re.search(r"b(\d+)\.json", p).group(1))):
        sr = int(re.search(r"b(\d+)\.json", f).group(1))
        d = json.load(open(f, encoding="utf-8"))
        for section in ("rows", "review"):
            for r in d.get(section) or []:
                for fld in ("category", "sub_category"):
                    v = r.get(fld)
                    if has_nonascii(v):
                        bad.append((sr, section, fld, v))

    if bad:
        print(f"FAIL: {len(bad)} non-ASCII category/sub_category values remain\n")
        for sr, section, fld, v in bad:
            print(f"  SR {sr} [{section}.{fld}]: {v!r}")
        sys.exit(1)
    print("PASS: no non-ASCII category/sub_category values in any b<SR>.json")


if __name__ == "__main__":
    main()
