import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.structube.com/en_ca/decor/home-accents/cushions"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    page.goto(url, wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(2000)
    h1 = page.query_selector("h1")
    h1text = h1.inner_text() if h1 else None
    print("H1:", h1text)
    print("URL:", page.url)
    # Try common toolbar amount selectors
    body_text = page.inner_text("body")
    import re
    # search for patterns like "123 products" or "Items 1-24 of 123"
    for m in re.finditer(r'(\d+)\s*(products?|items?)', body_text, re.IGNORECASE):
        print("MATCH:", m.group(0))
    for m in re.finditer(r'of\s*(\d+)', body_text, re.IGNORECASE):
        print("OF-MATCH:", m.group(0))
    browser.close()
