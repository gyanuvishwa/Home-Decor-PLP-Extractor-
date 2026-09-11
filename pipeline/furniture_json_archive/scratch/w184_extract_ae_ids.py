import json, re
d = json.load(open('f164.json', encoding='utf-8'))
rows = d['rows']
ids = []
for r in rows:
    if not r['is_group']:
        m = re.search(r'-([A-Za-z0-9]+)/?$', r['link'])
        ids.append(m.group(1) if m else None)
print(len(ids))
print(','.join('"' + i + '"' for i in ids))
