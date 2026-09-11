"""Reconcile the three output workbooks against the source Output sheet.

Company identity is forward-filled on both sides: in the source it appears only
on a company's banner row, and the banner row is not the same physical row once
the data is split, so the raw cell value cannot be compared directly.
"""
import os
from collections import Counter
import openpyxl

from assign import build
from classify import KD, LIGHT, WALL, DECOR

OUTDIR = r'C:\Users\GyanendraVishwakarma\Web Research Agent'
FILES = [(KD, 'Kitchen_and_Dining.xlsx'), (LIGHT, 'Lighting.xlsx'),
         (WALL, 'Wall_Decor.xlsx'),
         (DECOR, 'Decorative_Home_Accessories.xlsx')]


def qty_key(comp_id, v):
    """Identity of a quantity record: company + sub-category + qty + link."""
    return (comp_id, str(v[6] or ''), str(v[8] or ''), str(v[9] or ''))


def scan(vals):
    """Forward-fill company identity; yield (comp_id, row) and banner rows."""
    cur = None
    banners = 0
    out = []
    for v in vals:
        if v[0] not in (None, '') or v[1] not in (None, ''):
            cur = (str(v[0]), str(v[1]), str(v[2]), str(v[3]))
            banners += 1
        out.append((cur, v))
    return out, banners


def main():
    wb, ws, rows, comps, blanks, R, info = build()

    src_vals = [r['v'] for r in rows[1:]
                if any(x not in (None, '') for x in r['v'])]
    src_scan, src_banners = scan(src_vals)
    src_qty = [(cid, v) for cid, v in src_scan if v[8] not in (None, '')]

    exp = Counter()
    rowmap = {}
    i = 0
    for r in rows[1:]:
        if not any(x not in (None, '') for x in r['v']):
            continue
        if r['v'][8] not in (None, ''):
            rowmap[i] = info[r['r']]['cls']
            i += 1
    for n, (cid, v) in enumerate(src_qty):
        exp[rowmap[n]] += 1

    print('SOURCE  (Final_Company_List (1).xlsx  ->  sheet "Output")')
    print('  data rows (non-blank)      :', len(src_vals))
    print('  quantity records (qty set) :', len(src_qty))
    print('  grouping / parent rows     :', len(src_vals) - len(src_qty))
    print('  companies (banner rows)    :', src_banners)
    print('  qty records by class       :', dict(exp))

    src_keys = Counter(qty_key(cid, v) for cid, v in src_qty)
    src_assigned = set()
    for n, (cid, v) in enumerate(src_qty):
        if rowmap[n] is not None:
            src_assigned.add(qty_key(cid, v))

    total_out = 0
    out_keys = set()
    results = {}
    for cls, fname in FILES:
        p = os.path.join(OUTDIR, fname)
        w2 = openpyxl.load_workbook(p, read_only=True)
        s2 = w2['Output']
        vals = [list(r) for r in s2.values][1:]
        vals = [v for v in vals if any(x not in (None, '') for x in v)]
        sc, banners = scan(vals)
        qty = [(cid, v) for cid, v in sc if v[8] not in (None, '')]
        ks = [qty_key(cid, v) for cid, v in qty]
        dup = sum(c - 1 for c in Counter(ks).values() if c > 1)
        print('\n%s' % fname)
        print('  total rows written    :', len(vals))
        print('  quantity records      :', len(qty))
        print('  grouping/parent rows  :', len(vals) - len(qty))
        print('  companies             :', banners)
        print('  expected qty records  :', exp[cls],
              '->', 'MATCH' if len(qty) == exp[cls] else 'MISMATCH')
        print('  duplicate qty records :', dup)
        out_keys |= set(ks)
        total_out += len(qty)
        results[cls] = (fname, len(qty), banners, len(vals))
        w2.close()

    fut = Counter()
    for r in rows[1:]:
        if r['v'][8] not in (None, '') and info[r['r']].get('fut'):
            fut[info[r['r']]['fut']] += 1

    missing = src_assigned - out_keys
    print('\nRECONCILIATION')
    print('  source qty records            :', len(src_qty))
    print('  distributed to the 4 files    :', total_out)
    print('  still unassigned              :', len(src_qty) - total_out)
    print('  of which next-task records    :', dict(fut), '=', sum(fut.values()))
    print('  of which other/out-of-scope   :',
          len(src_qty) - total_out - sum(fut.values()))
    print('  assigned records missing      :', len(missing))
    print('  exact duplicate rows in source:',
          sum(c - 1 for c in src_keys.values() if c > 1))
    print('  DATA-LOSS CHECK               :', 'PASS' if not missing else 'FAIL')
    for m in list(missing)[:20]:
        print('   MISSING', m)
    return results


if __name__ == '__main__':
    main()
