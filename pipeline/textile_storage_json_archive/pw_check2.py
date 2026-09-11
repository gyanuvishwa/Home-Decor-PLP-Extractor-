import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")

    reqs = []
    def on_req(request):
        if "algolia" in request.url.lower():
            reqs.append(request.url)
    page.on("request", on_req)

    resps = []
    def on_resp(response):
        if "algolia" in response.url.lower():
            resps.append((response.status, response.url))
    page.on("response", on_resp)

    console_msgs = []
    page.on("console", lambda msg: console_msgs.append(f"{msg.type}: {msg.text}"))

    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(8000)

    print("=== ALGOLIA REQUESTS ===")
    for r in reqs[:10]:
        print(r)
    print("=== ALGOLIA RESPONSES ===")
    for s, u in resps[:10]:
        print(s, u)
    print("=== CONSOLE (last 20) ===")
    for c in console_msgs[-20:]:
        print(c)

    grid = page.query_selector("#algolia-product-grid")
    print("=== GRID HTML (first 1000 chars) ===")
    print(grid.inner_html()[:1000] if grid else "NO GRID ELEMENT")

    browser.close()
