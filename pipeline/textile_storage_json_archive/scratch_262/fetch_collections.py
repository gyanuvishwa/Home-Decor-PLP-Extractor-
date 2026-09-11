import json
from curl_cffi import requests

all_cols = []
page = 1
while True:
    r = requests.get(f'https://www.oorjaa.in/collections.json?limit=250&page={page}', impersonate='chrome')
    data = r.json()
    cols = data.get('collections', [])
    if not cols:
        break
    all_cols.extend(cols)
    page += 1
    if page > 10:
        break

print("total collections:", len(all_cols))
with open('collections_full.json', 'w', encoding='utf-8') as f:
    json.dump(all_cols, f, ensure_ascii=False, indent=1)

for c in all_cols:
    print(c['id'], '|', c['handle'], '|', c['title'], '|', c['products_count'])
