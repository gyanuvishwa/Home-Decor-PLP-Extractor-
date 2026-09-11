from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-http2"])
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    page.set_default_timeout(60000)
    try:
        resp = page.goto("https://www.nitori-net.jp/ec/", wait_until="domcontentloaded", timeout=60000)
        print("goto status:", resp.status if resp else None, flush=True)
    except Exception as e:
        print("goto err:", repr(e), flush=True)
        browser.close()
        raise SystemExit(0)
    page.wait_for_timeout(4000)
    html = page.content()
    open("sr177_home_rendered3.html", "w", encoding="utf-8").write(html)
    print("content len", len(html), flush=True)
    browser.close()
print("DONE_SCRIPT", flush=True)
