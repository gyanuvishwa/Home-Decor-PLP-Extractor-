"""Parse the Output sheet into companies -> category sections -> groups/leaves."""
import openpyxl, json, sys

SRC = r'C:\Users\GyanendraVishwakarma\Web Research Agent\Final_Company_List (1).xlsx'
HL = 'FFFFF2CC'


def load():
    wb = openpyxl.load_workbook(SRC)
    ws = wb['Output']
    n = ws.max_row
    rows = []
    for r in range(1, n + 1):
        vals = [ws.cell(r, c).value for c in range(1, 11)]
        f = ws.cell(r, 7).fill
        hl = (f.fgColor.rgb == HL) if (f and f.fill_type) else False
        rows.append({'r': r, 'v': vals, 'hl': hl})
    return wb, ws, rows


def parse(rows):
    """Return list of companies. Each: {hdr_row, ident:[A..E], sections:[{cat, rows:[rowidx]}]}"""
    companies = []
    cur = None
    cursec = None
    blanks = []
    for row in rows[1:]:
        v = row['v']
        if all(x in (None, '') for x in v):
            blanks.append(row['r'])
            continue
        if v[0] not in (None, ''):  # new company
            cur = {'hdr': row['r'], 'ident': v[0:5], 'sections': []}
            companies.append(cur)
            cursec = None
        if cur is None:
            raise RuntimeError('orphan row %d' % row['r'])
        if v[5] not in (None, ''):  # new category section
            cursec = {'cat': str(v[5]).strip(), 'rows': []}
            cur['sections'].append(cursec)
        if cursec is None:
            raise RuntimeError('row %d before any category' % row['r'])
        cursec['rows'].append(row['r'])
    return companies, blanks


if __name__ == '__main__':
    wb, ws, rows = load()
    comps, blanks = parse(rows)
    print('companies', len(comps))
    print('sections', sum(len(c['sections']) for c in comps))
    print('blank rows', len(blanks))
    assigned = sum(len(s['rows']) for c in comps for s in c['sections'])
    print('rows in sections', assigned, 'of data rows', len(rows) - 1 - len(blanks))
