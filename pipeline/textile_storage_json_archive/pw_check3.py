import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36", viewport={"width":1400,"height":1000})

    all_reqs = []
    def on_req(request):
        all_reqs.append(request.url)
    page.on("request", on_req)

    page.goto(url, wait_until="load", timeout=60000)
    page.wait_for_timeout(2000)
    page.mouse.wheel(0, 2000)
    page.wait_for_timeout(3000)
    page.mouse.wheel(0, 2000)
    page.wait_for_timeout(5000)

    print("=== requests containing 'collection-page' or 'algolia' or 'net/1/indexes' ===")
    for r in all_reqs:
        if "collection-page" in r or "algolia" in r.lower() or "indexes" in r:
            print(r)

    grid = page.query_selector("#algolia-product-grid")
    print("=== GRID HTML (first 2000 chars) ===")
    print(grid.inner_html()[:2000] if grid else "NO GRID ELEMENT")
    print("TOTAL REQS:", len(all_reqs))
    browser.close()
