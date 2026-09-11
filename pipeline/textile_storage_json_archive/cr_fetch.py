import json, re, time
from playwright.sync_api import sync_playwright

urls = [
    "/home-bathroom-towels-and-mats/",
    "/home-bathroom-bath-robes/",
    "/home-bathroom-bathroom-accessories/",
    "/home-bedroom-double-quilt-covers/",
    "/home-bedroom-queen-quilt-covers/",
    "/home-bedroom-king-quilt-covers/",
    "/home-bedroom-super-king-quilt-covers/",
    "/home-bedroom-quilts/",
    "/home-bedroom-sheets-single-sheets/",
    "/home-bedroom-sheets-king-single-sheets/",
    "/home-bedroom-sheets-double-sheets/",
    "/home-bedroom-sheets-queen-sheets/",
    "/home-bedroom-sheets-king-sheets/",
    "/home-bedroom-pillowcases-silk-pillowcases/",
    "/home-bedroom-pillowcases-european-pillowcases/",
    "/home-bedroom-bed-covers/",
    "/home-bedroom-mattress-toppers/",
    "/home-home-accessories-throws/",
    "/home-home-accessories-cushions/",
    "/home-rugs-indoor-rugs/",
    "/home-rugs-outdoor-rugs/",
    "/home-rugs-/",
    "/home-kitchen-and-dining-table-linen-and-accessories/",
    "/home-kitchen-and-dining-tea-towels/",
    "/home-kids-home-kids-bedding/",
    "/home-kids-home-kids-towels/",
    "/home-beach-towels-and-accessories-beach-towels/",
    "/home-home-accessories-storage/",
]

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    for u in urls:
        print("FETCHING", u, flush=True)
        full = "https://www.countryroad.com.au" + u
        try:
            page.goto(full, timeout=30000, wait_until='domcontentloaded')
            page.wait_for_timeout(2500)
            content = page.content()
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', content, re.S)
            if not m:
                results[u] = {"error": "no NEXT_DATA"}
                continue
            data = json.loads(m.group(1))
            canonical = data['props']['pageProps'].get('canonicalPath')
            ist = data['props']['pageProps']['initialState']
            crg = ist['crgApi']['queries']
            totalCount = None
            catnav_name = None
            catnav_items = None
            for k, v in crg.items():
                if k.startswith('getProductLanding-'):
                    try:
                        totalCount = v['data']['ProductLanding']['totalCount']
                    except Exception:
                        pass
                if k.startswith('getProductListInitialData'):
                    try:
                        nav = v['data']['CategoryNavigation']
                        catnav_name = nav['name']
                        catnav_items = [(it['name'], it['url'], it['categoryId']) for it in nav.get('items', [])]
                    except Exception:
                        pass
            # h1
            h1m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.S)
            h1 = re.sub('<[^>]+>', '', h1m.group(1)).strip() if h1m else None
            results[u] = {
                "canonical": canonical,
                "totalCount": totalCount,
                "h1": h1,
                "catnav_name": catnav_name,
                "catnav_items": catnav_items,
            }
            print(u, "->", totalCount, "|", h1, "| subitems:", catnav_items, flush=True)
        except Exception as e:
            results[u] = {"error": str(e)}
            print(u, "ERROR", e, flush=True)
        json.dump(results, open("cr_candidates.json", "w", encoding="utf-8"), indent=2)
    browser.close()

print("DONE", flush=True)
