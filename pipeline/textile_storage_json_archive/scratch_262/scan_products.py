import json, time
from curl_cffi import requests

all_products = []
page = 1
while True:
    r = requests.get(f'https://www.oorjaa.in/products.json?limit=250&page={page}', impersonate='chrome')
    data = r.json()
    prods = data.get('products', [])
    if not prods:
        break
    all_products.extend(prods)
    page += 1
    if page > 20:
        break

print("total products:", len(all_products))

types = {}
for p in all_products:
    t = p.get('product_type','')
    types[t] = types.get(t,0)+1

print("=== product_types ===")
for t,c in sorted(types.items(), key=lambda x:-x[1]):
    print(c, '|', t)

keywords = ['basket','box','storage','organiz','cushion','curtain','rug','towel','blanket','tray','bedding','sheet','quilt','throw','pillow','duvet','mat ','doormat','bag','bin','shelf','rack','cabinet','crate','trunk','container','hamper']
print("=== title keyword matches ===")
found = []
for p in all_products:
    title = p['title'].lower()
    for k in keywords:
        if k in title:
            found.append((p['title'], p.get('product_type'), p.get('handle')))
            break
for f in found:
    print(f)
print("matches:", len(found))
