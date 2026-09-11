import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-http2"])
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    try:
        page.goto("https://www.nitori-net.jp/ec/", wait_until="load", timeout=90000)
        print("goto ok", flush=True)
    except Exception as e:
        print("goto err:", repr(e), flush=True)

    try:
        print("readyState:", page.evaluate("document.readyState"), flush=True)
    except Exception as e:
        print("evaluate err:", repr(e), flush=True)

    page.wait_for_timeout(4000)

    try:
        html = page.content()
        open("sr177_home_rendered2.html", "w", encoding="utf-8").write(html)
        print("content len", len(html), flush=True)
    except Exception as e:
        print("content err:", repr(e), flush=True)

    browser.close()
print("DONE_SCRIPT", flush=True)
