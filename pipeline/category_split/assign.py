"""Assign every source row to KD / LIGHT / WALL / None, preserving group context."""
from parse import load, parse
from classify import (name_class, cat_class, decor_fallback, future_class,
                      KD, LIGHT, WALL, DECOR)

FILE_CLASSES = (KD, LIGHT, WALL, DECOR)


def is_group(row):
    v = row['v']
    return row['hl'] and v[8] in (None, '') and v[9] in (None, '')


def build():
    wb, ws, rows = load()
    comps, blanks = parse(rows)
    R = {r['r']: r for r in rows}

    # units: every row gets .cls (own assignment) and .ctx (files it must appear in as parent)
    info = {}
    for c in comps:
        for s in c['sections']:
            sec = cat_class(s['cat'])
            cur_grp = None          # row index of the open group row
            for ri in s['rows']:
                row = R[ri]
                nm = row['v'][6]
                own = name_class(nm)
                isg = is_group(row)
                parent = (info[cur_grp]['cls']
                          if (not isg and cur_grp is not None) else None)
                pname = R[cur_grp]['v'][6] if (not isg and cur_grp is not None) else None
                fut = None
                # Inside an umbrella Category the row has no decisive parent
                # scope, so a clear next-task record must not be dragged into a
                # file by an unrelated neighbouring group. Inside a decisive
                # section (Lighting/K&D/Wall Decor) we never do this - a "Bath"
                # group under Lighting is bath *lighting*.
                if sec is None and own is None:
                    fut = future_class(nm, s['cat'])
                cls = None if fut else (own or parent or sec)

                # Nothing in the four-file scheme claimed it. Decide whether it
                # is a NEXT-task record (leave unassigned) or a broad
                # decorative-accessory record (goes to the 4th file).
                if cls is None and fut is None:
                    fut = future_class(nm, s['cat']) or future_class(pname)
                    if fut is None:
                        cls = decor_fallback(nm) or decor_fallback(pname)

                if isg:
                    cur_grp = ri
                info[ri] = {'cls': cls, 'grp': None if isg else cur_grp,
                            'sec': s['cat'], 'seccls': sec, 'own': own,
                            'isgrp': isg, 'fut': fut,
                            'comp': c['hdr'], 'secid': id(s)}

    # propagate: a group row must appear in every file where one of its children lands
    for ri, d in info.items():
        if d['isgrp']:
            d['files'] = {d['cls']} if d['cls'] else set()
        else:
            d['files'] = {d['cls']} if d['cls'] else set()
    for ri, d in info.items():
        if not d['isgrp'] and d['grp'] is not None and d['cls']:
            info[d['grp']]['files'].add(d['cls'])

    return wb, ws, rows, comps, blanks, R, info


if __name__ == '__main__':
    from collections import Counter, defaultdict
    wb, ws, rows, comps, blanks, R, info = build()
    c = Counter(d['cls'] for d in info.values())
    print('row classes:', dict(c))
    qty = Counter()
    for ri, d in info.items():
        if R[ri]['v'][8] not in (None, ''):
            qty[d['cls']] += 1
    print('rows WITH qty by class:', dict(qty))

    # overrides: own class differs from section class
    ov = defaultdict(Counter)
    for ri, d in info.items():
        if d['own'] and d['seccls'] and d['own'] != d['seccls']:
            ov[(d['sec'], d['own'])][str(R[ri]['v'][6])] += 1
    print('\n=== OVERRIDES (sub-category beats major category) ===')
    for (sec, own), names in sorted(ov.items(), key=lambda x: -sum(x[1].values())):
        print('%s  ->  %s   (%d rows)' % (sec, own, sum(names.values())))
        print('    ' + ' | '.join('%s(%d)' % (k, v) for k, v in names.most_common(40)))
