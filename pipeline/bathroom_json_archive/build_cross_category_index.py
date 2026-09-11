#!/usr/bin/env python3
"""Build cross_category_url_index.json: normalized leaf URL -> [owning workbook(s)].

Read-only against every OTHER category's Output sheet. Used by
merge_bathroom.py to enforce the run's own already-declared OPTION 1 dedup
policy ("a leaf URL already recorded in another category workbook goes to
review[], never rows[]") against the FULL set of protected workbooks, not
just Furniture.xlsx as the original run did.

Re-run this whenever another category workbook is rebuilt, before the next
Bathroom merge.

Usage:  python build_cross_category_index.py
"""
import json, os
import openpyxl

PROJ = r"C:\Users\GyanendraVishwakarma\Web Research Agent"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cross_category_url_index.json")

FILES = ["Furniture.xlsx", "Textile.xlsx", "Storage.xlsx", "Lighting.xlsx",
         "Wall_Decor.xlsx", "Kitchen_and_Dining.xlsx",
         "Decorative_Home_Accessories.xlsx", "Pet_Care.xlsx"]
# Seasonal is deliberately excluded: it is the one category that overlaps
# every other on purpose (home-decor-extraction/SKILL.md's sibling skill
# notes), so a Seasonal leaf must never suppress a genuine Bathroom leaf.


def get_leaf_urls(path):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb["Output"]
    urls = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        link = row[9] if len(row) > 9 else None
        if link:
            urls.add(link.strip().rstrip("/"))
    wb.close()
    return urls


def main():
    index = {}
    for f in FILES:
        path = os.path.join(PROJ, f)
        if not os.path.exists(path):
            print(f"skip (not found): {f}")
            continue
        urls = get_leaf_urls(path)
        for u in urls:
            index.setdefault(u, []).append(f)
        print(f"{f}: {len(urls)} leaf URLs")

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False)
    print(f"\nWROTE -> {OUT}  ({len(index)} distinct URLs)")


if __name__ == "__main__":
    main()
