"""Write the three category workbooks from the assigned rows, preserving
values, hierarchy and formatting exactly as they appear in the source."""
import os
from copy import copy
import openpyxl
from openpyxl.utils import get_column_letter

from assign import build
from classify import KD, LIGHT, WALL, DECOR

OUTDIR = r'C:\Users\GyanendraVishwakarma\Web Research Agent'
TARGETS = [(KD, 'Kitchen_and_Dining.xlsx'),
           (LIGHT, 'Lighting.xlsx'),
           (WALL, 'Wall_Decor.xlsx'),
           (DECOR, 'Decorative_Home_Accessories.xlsx')]


def apply_style(src, dst):
    dst.font = copy(src.font)
    dst.fill = copy(src.fill)
    dst.border = copy(src.border)
    dst.alignment = copy(src.alignment)
    dst.number_format = src.number_format
    dst.protection = copy(src.protection)


def copy_cell(src, dst):
    dst.value = src.value
    apply_style(src, dst)
    if src.hyperlink is not None:
        dst.hyperlink = copy(src.hyperlink)


def main():
    wb, ws, rows, comps, blanks, R, info = build()
    stats = {}

    for cls, fname in TARGETS:
        out = openpyxl.Workbook()
        os_ = out.active
        os_.title = 'Output'

        # column widths + header row
        for c in range(1, 11):
            L = get_column_letter(c)
            if L in ws.column_dimensions and ws.column_dimensions[L].width:
                os_.column_dimensions[L].width = ws.column_dimensions[L].width
            copy_cell(ws.cell(1, c), os_.cell(1, c))

        w = 2
        n_rows = n_qty = 0
        companies = 0
        for comp in comps:
            emit = []           # (source_row, section_cat, is_section_first)
            for s in comp['sections']:
                sec_rows = [ri for ri in s['rows'] if cls in info[ri]['files']]
                for i, ri in enumerate(sec_rows):
                    emit.append((ri, s['cat'], i == 0))
            if not emit:
                continue
            companies += 1
            hdr = comp['hdr']

            for k, (ri, cat, first_of_sec) in enumerate(emit):
                src_row = hdr if k == 0 else ri
                for c in range(1, 11):
                    # style: the company banner row takes the source banner's
                    # look (bold + highlight), as in the source workbook
                    style_src = ws.cell(hdr if k == 0 else ri, c)
                    copy_cell(ws.cell(ri, c), os_.cell(w, c))
                    if k == 0:
                        apply_style(style_src, os_.cell(w, c))
                if k == 0:
                    # company identity + Type from the source banner row
                    for c in (1, 2, 3, 4, 5, 8):
                        os_.cell(w, c).value = ws.cell(hdr, c).value
                if first_of_sec:
                    os_.cell(w, 6).value = cat
                elif os_.cell(w, 6).value is not None and k != 0:
                    os_.cell(w, 6).value = None
                n_rows += 1
                if os_.cell(w, 9).value not in (None, ''):
                    n_qty += 1
                w += 1
            w += 1      # blank separator row between companies

        path = os.path.join(OUTDIR, fname)
        out.save(path)
        stats[cls] = {'file': fname, 'rows': n_rows, 'qty_rows': n_qty,
                      'companies': companies}
        print('%-26s rows=%-6d qty-records=%-6d companies=%d'
              % (fname, n_rows, n_qty, companies))
    return stats


if __name__ == '__main__':
    main()
