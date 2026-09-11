"""Fix SR200 Indigo Home: the block had 9 sub-category rows sharing only 3 links
(collections/home-decor x4, collections/entertain-serve x4, collections/mugs).
Those sub-category names do not exist on indigo.ca.

Verified 2026-08-17 against indigo.ca's own Constructor.io discovery layer
(browse/group_id/<handle>, key_Al6HhP1ovMAKoxK5). total_num_results was confirmed
equal to the rendered "Search Results: N items" header for home-decor (74), mugs
(156) and entertain-serve (116) in a real browser.

Indigo's Home & Entertaining tree bottoms out at 6 leaf collections -- there are no
deeper sub-categories, which is why the original extraction invented names and
reused the parent link.

/collections/lighting is dropped: it is a BOOKS subject page (parents: books >
home-garden), 32 titles about lighting design, not lamps. Indigo has no lighting
product category.
"""
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill

ROOT = r"C:\Users\GyanendraVishwakarma\Web Research Agent"

GROUP_FILL = PatternFill("solid", fgColor="FFFFF2CC")

SITE = ("Indigo Home", "indigo.ca", "Canada", "https://www.indigo.ca/")
B = "https://www.indigo.ca/collections/"

# (sub_category, qty, link) verified 2026-08-17
KD = [
    ("Mugs", 156, B + "mugs"),
    ("Entertain & Serve", 116, B + "entertain-serve"),
    ("Water Bottles", 49, B + "water-bottles"),
]
HA = [
    ("Home Decor", 74, B + "home-decor"),
    ("Candles & Home Fragrance", 146, B + "candles-home-fragrance"),
    ("Seasonal Decor", 14, B + "seasonal-decor"),
]


def clear(ws, r):
    for c in range(1, 11):
        cell = ws.cell(r, c)
        cell.value = None
        cell.fill = PatternFill()
        cell.font = Font()


def banner(ws, r, category):
    clear(ws, r)
    vals = [200, SITE[0], SITE[1], SITE[2], SITE[3], category, category, "category", None, None]
    for c, v in enumerate(vals, 1):
        ws.cell(r, c).value = v


def group(ws, r, category):
    clear(ws, r)
    ws.cell(r, 6).value = category
    ws.cell(r, 7).value = category
    for c in range(1, 11):
        ws.cell(r, c).fill = GROUP_FILL
        ws.cell(r, c).font = Font(bold=True)


def leaf(ws, r, sub, qty, link):
    clear(ws, r)
    ws.cell(r, 7).value = sub
    ws.cell(r, 9).value = qty
    ws.cell(r, 10).value = link


def write_block(ws, start, sections):
    """sections = [(category, rows, is_banner)] -> returns number of rows written."""
    r = start
    for idx, (cat, rows) in enumerate(sections):
        if idx == 0:
            banner(ws, r, cat)
        else:
            group(ws, r, cat)
        r += 1
        for sub, qty, link in rows:
            leaf(ws, r, sub, qty, link)
            r += 1
    return r - start


def do(path, sheet, start, old_len, sections):
    wb = openpyxl.load_workbook(path)
    ws = wb[sheet]
    assert ws.cell(start, 2).value == "Indigo Home", (path, ws.cell(start, 2).value)
    new_len = write_block(ws, start, sections)
    if new_len < old_len:
        ws.delete_rows(start + new_len, old_len - new_len)
    wb.save(path)
    print(f"{path}: rows {old_len} -> {new_len}")


def drop(path, sheet, start, n):
    """Delete the whole Indigo block (used for Lighting.xlsx)."""
    wb = openpyxl.load_workbook(path)
    ws = wb[sheet]
    assert ws.cell(start, 2).value == "Indigo Home", (path, ws.cell(start, 2).value)
    ws.delete_rows(start, n)
    wb.save(path)
    print(f"{path}: deleted {n} row(s) at {start}")


if __name__ == "__main__":
    do(ROOT + r"\Final_Company_List (1).xlsx", "Output", 7859, 11,
       [("Kitchen & Dining", KD), ("Home Accessories", HA)])
    do(ROOT + r"\Kitchen_and_Dining.xlsx", "Output", 2379, 6,
       [("Kitchen & Dining", KD)])
    do(ROOT + r"\Decorative_Home_Accessories.xlsx", "Output", 1964, 4,
       [("Home Accessories", HA)])
    # Lighting.xlsx: single bogus row + its trailing blank separator
    drop(ROOT + r"\Lighting.xlsx", "Output", 2505, 2)
