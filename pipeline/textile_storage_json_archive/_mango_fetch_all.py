import re, json, time, sys
import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}

NODES = {
 "cushion-covers": "/us/en/c/home/cushion-covers/e50c6bbc",
 "rugs": "/us/en/c/home/rugs/4f75af4c",
 "frames-and-paintings": "/us/en/c/home/frames-and-paintings/bd5cd4ab",
 "vases": "/us/en/c/home/vases/4a8facf5",
 "baskets": "/us/en/c/home/baskets/fff11705",
 "sofa-blankets": "/us/en/c/home/sofa-blankets/4ef15714",
 "mirrors": "/us/en/c/home/mirrors/7c4ec3a7",
 "boxes-and-jewelry-boxes": "/us/en/c/home/boxes-and-jewelry-boxes/78e4caf0",
 "lamps": "/us/en/c/home/lamps/6afd056c",
 "candles-and-chandeliers": "/us/en/c/home/candles-and-chandeliers/36942433",
 "living-room-accessories": "/us/en/c/home/living-room-accessories/009c9e08",
 "flowerpots": "/us/en/c/home/flowerpots/e904c430",
 "christmas-decorations": "/us/en/c/home/christmas-decorations/7088a32a",
 "soft-furnishings": "/us/en/c/home/soft-furnishings/beef0699",
 "decorative-items": "/us/en/c/home/decorative-items/635e8a8d",
 "table-linen-and-kitchen-textiles": "/us/en/c/home/table-linen-and-kitchen-textiles/8f4ef503",
 "duvet-covers": "/us/en/c/home/duvet-covers/4c955217",
 "bottom-sheets": "/us/en/c/home/bottom-sheets/0b7ebd50",
 "flat-sheets": "/us/en/c/home/flat-sheets/28910b57",
 "pillow-cases": "/us/en/c/home/pillow-cases/2a97d7ee",
 "bedroom-cushion-covers": "/us/en/c/home/bedroom-cushion-covers/7535b5a8",
 "fillings-and-protectors": "/us/en/c/home/fillings-and-protectors/c59a73cc",
 "bedroom-decoration": "/us/en/c/home/bedroom-decoration/9866e476",
 "bedspreads-and-duvets": "/us/en/c/home/bedspreads-and-duvets/06fd0d24",
 "sheets-and-pillows": "/us/en/c/home/sheets-and-pillows/7708cf7e",
 "bedroom-blankets": "/us/en/c/home/bedroom-blankets/b360a1b6",
 "tablecloths": "/us/en/c/home/tablecloths/1922ea48",
 "trays": "/us/en/c/home/trays/de76ade2",
 "table-accessories": "/us/en/c/home/table-accessories/069ecb58",
 "kitchen-accessories": "/us/en/c/home/kitchen-accessories/5a84887f",
 "kitchen-textiles": "/us/en/c/home/kitchen-textiles/21ff05e7",
 "tableware-and-kitchenware": "/us/en/c/home/tableware-and-kitchenware/85f9fbd0",
 "table-items": "/us/en/c/home/table-items/7859e826",
 "towels": "/us/en/c/home/towels/349dbd1f",
 "bathroom-accessories": "/us/en/c/home/bathroom-accessories/be54191a",
 "bathrobes-and-slippers": "/us/en/c/home/bathrobes-and-slippers/f16b676a",
 "bathroom-baskets": "/us/en/c/home/bathroom-baskets/3e2faeba",
 "bathroom-textiles": "/us/en/c/home/bathroom-textiles/56fc38b7",
 "beach-towels-1": "/us/en/c/home/beach-towels/0a5cbb32",
 "pajamas": "/us/en/c/home/pajamas/b684d940",
 "nightgowns-and-robes": "/us/en/c/home/nightgowns-and-robes/214e5edb",
 "silk": "/us/en/c/home/silk/ffdd80ec",
 "knitwear": "/us/en/c/home/knitwear/f5f6dad9",
 "slippers-and-socks": "/us/en/c/home/slippers-and-socks/327c68b8",
 "accessories": "/us/en/c/home/accessories/8b45a8a2",
 "homewear": "/us/en/c/home/homewear/762f0d30",
 "outdoor-tablecloths": "/us/en/c/home/outdoor-tablecloths/12800140",
 "beach-towels-2": "/us/en/c/home/beach-towels/e6995eb1",
 "outdoor-cushion-cases": "/us/en/c/home/outdoor-cushion-cases/049dcc9d",
 "terrace": "/us/en/c/home/terrace/d67318b7",
 "decoration": "/us/en/c/home/decoration/328fa15e",
 "christmas-collection": "/us/en/c/home/christmas-collection/1b78a466",
 "set-the-table": "/us/en/c/home/set-the-table/fb9edbe5",
 # subnav children discovered earlier
 "baskets-decorative": "/us/en/c/home/baskets/decorative/8f292b3c",
 "baskets-storage": "/us/en/c/home/baskets/storage/a147af00",
 "baskets-with-lid": "/us/en/c/home/baskets/with-lid/aad19226",
 "bathroom-baskets-laundry": "/us/en/c/home/bathroom-baskets/laundry-basket/67f74417",
 "bathroom-baskets-storage": "/us/en/c/home/bathroom-baskets/storage/3a435b64",
 "bathroom-accessories-boxes-jars": "/us/en/c/home/bathroom-accessories/bathroom-boxes-and-jars/1f3eb2f3",
}

BASE = "https://shop.mango.com"

def fetch_page(path):
    url = BASE + path
    try:
        r = requests.get(url, headers=HEADERS, timeout=25)
    except Exception as e:
        return {"error": str(e)[:200], "url": url}
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}", "url": url}
    html = r.text
    m_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    h1 = re.sub(r'<[^>]+>', '', m_h1.group(1)).strip() if m_h1 else None
    m_cat = re.search(r'catalogId[^a-zA-Z0-9_.]+([a-zA-Z0-9_.]+)', html)
    catalog_id = m_cat.group(1) if m_cat else None
    m_canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    canonical = m_canon.group(1) if m_canon else None
    return {"url": url, "status": r.status_code, "h1": h1, "catalog_id": catalog_id, "canonical": canonical}

def fetch_catalog_qty(catalog_id):
    if not catalog_id:
        return {"error": "no catalog_id"}
    all_pids = set()
    page = 1
    total_items = None
    total_pages = None
    title = None
    while True:
        api_url = f"https://api.shop.mango.com/cs/product-lists-drive-thru/v2/channels/shop/countries/us/catalogs/{catalog_id}?languageIso=en&page={page}"
        try:
            r = requests.get(api_url, headers=HEADERS, timeout=25)
        except Exception as e:
            return {"error": str(e)[:200]}
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}", "page": page}
        d = r.json()
        if total_items is None:
            total_items = d.get("totalItems")
            total_pages = d.get("totalPages")
            title = d.get("title")
        items = d.get("items", [])
        for it in items:
            pid = it.get("productId")
            if pid:
                all_pids.add(pid)
        if page >= (total_pages or 1):
            break
        page += 1
        time.sleep(0.15)
    return {"total_items_variant": total_items, "total_pages": total_pages, "unique_products": len(all_pids), "api_title": title}

def main():
    results = {}
    for key, path in NODES.items():
        pg = fetch_page(path)
        entry = {"page": pg}
        if pg.get("catalog_id"):
            entry["catalog"] = fetch_catalog_qty(pg["catalog_id"])
        results[key] = entry
        print(key, "->", pg.get("h1"), "|", entry.get("catalog", {}).get("unique_products"), flush=True)
        time.sleep(0.1)
    with open("_mango_final_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
