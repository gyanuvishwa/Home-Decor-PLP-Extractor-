import sys, os, json, re, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import probe

def extract_product_list(html):
    key = '"productList":['
    i = html.find(key)
    if i == -1:
        return None
    start = i + len(key) - 1
    depth = 0
    in_str = False
    esc = False
    j = start
    while j < len(html):
        c = html[j]
        if in_str:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == '"': in_str = False
        else:
            if c == '"': in_str = True
            elif c == '[': depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    j += 1
                    break
        j += 1
    return json.loads(html[start:j])

def collect_all(url, label, pages_hint=None):
    all_products = {}
    page = 1
    total = None
    while True:
        sep = '&' if '?' in url else '?'
        u = f"{url}{sep}pageNumber={page}"
        st, html, fu = probe.fetch(u)
        m = re.search(r'"productTotalCount":(\d+)', html)
        if total is None and m:
            total = int(m.group(1))
        arr = extract_product_list(html)
        if not arr:
            break
        for p in arr:
            all_products[p.get('id')] = p
        if total and page * 48 >= total:
            break
        if len(arr) < 48:
            break
        page += 1
        if page > 30:
            break
        time.sleep(0.4)
    print(f"{label}: collected {len(all_products)} products (declared total {total})")
    return all_products

# Bathroom Accessories
pa = collect_all("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories", "Accessories parent")
org = collect_all("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/acessories-854100-1", "Organisation")
tb = collect_all("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/toilet-brushes", "ToiletBrushes")
sd = collect_all("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/soap-dispensers", "SoapDispensers")
bm = collect_all("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/bathroom-mirrors", "Mirrors")
bs = collect_all("https://www.myer.com.au/c/home/allbathroom/bathroom-accessories/bathroom-scales", "Scales")

child_ids = set(org) | set(tb) | set(sd) | set(bm) | set(bs)
residue_ids = set(pa) - child_ids
print(f"\nACCESSORIES RESIDUE: {len(residue_ids)} products")
for pid in sorted(residue_ids):
    p = pa[pid]
    print(f"  {pid}: {p.get('name')} | brand={p.get('brand')} | merch={p.get('merchCategory')}")

with open("sr188_accessories_residue_detail.json", "w", encoding="utf-8") as f:
    json.dump({pid: pa[pid] for pid in residue_ids}, f, indent=1)

print("\n\n=== FURNITURE ===")
pf = collect_all("https://www.myer.com.au/c/home/all-furniture/furniture-bathroom", "Furniture parent")
cv = collect_all("https://www.myer.com.au/c/home/all-furniture/furniture-bathroom/cabinets-vanities", "CabinetsVanities")
ft = collect_all("https://www.myer.com.au/c/home/all-furniture/furniture-bathroom/fittings", "Fittings")

fchild_ids = set(cv) | set(ft)
fresidue_ids = set(pf) - fchild_ids
print(f"\nFURNITURE RESIDUE: {len(fresidue_ids)} products")
for pid in sorted(fresidue_ids):
    p = pf[pid]
    print(f"  {pid}: {p.get('name')} | brand={p.get('brand')} | merch={p.get('merchCategory')}")

with open("sr188_furniture_residue_detail.json", "w", encoding="utf-8") as f:
    json.dump({pid: pf[pid] for pid in fresidue_ids}, f, indent=1)
