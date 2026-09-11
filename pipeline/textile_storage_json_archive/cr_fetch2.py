import json, re, time
from playwright.sync_api import sync_playwright

urls = [
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
]

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for u in urls:
        full = "https://www.countryroad.com.au" + u
        ok = False
        for attempt in range(3):
            try:
                page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                page.goto(full, timeout=45000, wait_until='domcontentloaded')
                page.wait_for_timeout(3500)
                content = page.content()
                m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', content, re.S)
                data = json.loads(m.group(1))
                pp = data['props']['pageProps']
                canonical = pp.get('canonicalPath')
                routeParams = pp.get('routeParams', {})
                catId = routeParams.get('categoryId')
                crg = pp['initialState']['crgApi']['queries']
                totalCount = None
                navname = None
                for k, v in crg.items():
                    if k.startswith('getProductLanding-'):
                        try:
                            totalCount = v['data']['ProductLanding']['totalCount']
                        except Exception:
                            pass
                    if k.startswith('getProductListInitialData'):
                        try:
                            nav = v['data']['CategoryNavigation']
                            def find(node, target):
                                if str(node['categoryId']) == str(target):
                                    return node
                                for c in node.get('items', []):
                                    r = find(c, target)
                                    if r:
                                        return r
                                return None
                            n = find(nav, catId)
                            if n:
                                navname = n['name']
                        except Exception:
                            pass
                results[u] = {"canonical": canonical, "categoryId": catId, "totalCount": totalCount, "navname": navname}
                print(u, "->", totalCount, "| catId:", catId, "| navname:", navname, "| canonical:", canonical, flush=True)
                page.close()
                ok = True
                break
            except Exception as e:
                print(u, "attempt", attempt, "ERROR", e, flush=True)
                try:
                    page.close()
                except Exception:
                    pass
                time.sleep(2)
        if not ok:
            results[u] = {"error": "failed after retries"}
        json.dump(results, open("cr_candidates2.json", "w", encoding="utf-8"), indent=2)
    browser.close()

print("DONE2", flush=True)
