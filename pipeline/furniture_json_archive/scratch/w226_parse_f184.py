import json, re

d = json.load(open('f184.json', encoding='utf-8'))
rows = d['rows']
out = []
for r in rows:
    if r['is_group']:
        out.append(('GROUP', r['category'], r['sub_category'], None, None))
    else:
        last = r['link'].rstrip('/').split('/')[-1]
        m = re.search(r'-([0-9a-z]+)$', last)
        cid = m.group(1) if m else last
        out.append(('LEAF', r['category'], r['sub_category'], cid, r['link']))

with open('scratch/w226_f184_parsed.txt', 'w', encoding='utf-8') as f:
    for o in out:
        f.write(repr(o) + '\n')
    f.write(f'TOTAL {len(rows)}\n')

leaf_ids = [o[3] for o in out if o[0]=='LEAF']
print('leaf count', len(leaf_ids))
print('unique ids', len(set(leaf_ids)))
