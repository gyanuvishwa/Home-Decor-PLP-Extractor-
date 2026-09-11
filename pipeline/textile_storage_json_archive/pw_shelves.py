from playwright.sync_api import sync_playwright

url = "https://serax.com/collections/shelves"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36", viewport={"width":1400,"height":1000})
    page.goto(url, wait_until="load", timeout=60000)
    page.wait_for_timeout(1500)
    page.mouse.wheel(0, 2000)
    page.wait_for_timeout(2500)
    print("Final URL:", page.url)
    h1s = page.query_selector_all("h1")
    for h in h1s:
        print("H1 elem:", h.inner_text())
    grid = page.query_selector("#algolia-product-grid")
    print("GRID:", grid.inner_html()[:1500] if grid else "none")
    browser.close()
