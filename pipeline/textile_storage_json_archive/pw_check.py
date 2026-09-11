import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    try:
        page.wait_for_selector("#algolia-product-grid .m-product-card", timeout=15000)
    except Exception as e:
        print("NO PRODUCT CARDS FOUND:", e)
    page.wait_for_timeout(2000)
    h1 = page.query_selector("h1")
    print("H1:", h1.inner_text() if h1 else None)
    # try to find any results count text
    body_text = page.inner_text("body")
    import re
    for line in body_text.split("\n"):
        if re.search(r"\d+\s*(product|result|item)", line, re.I):
            print("COUNT LINE:", line.strip())
    cards = page.query_selector_all("#algolia-product-grid .m-product-card")
    print("CARD COUNT (rendered, may be paginated):", len(cards))
    print("URL:", page.url)
    browser.close()
