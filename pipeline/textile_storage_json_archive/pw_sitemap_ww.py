from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context(
        viewport={"width":1366,"height":900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        locale="en-US",
    )
    page = context.new_page()
    page.goto("https://www.zarahome.com/ww/", wait_until="domcontentloaded", timeout=60000)
    for i in range(15):
        time.sleep(2)
        try:
            btn = page.get_by_text("GO", exact=True)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(timeout=5000)
                break
        except Exception:
            pass
    time.sleep(5)

    resp = page.goto("https://www.zarahome.com/8/info/sitemaps/sitemap-home-categories-zh-ww-0.xml.gz", timeout=30000)
    print("status:", resp.status if resp else None)
    body = resp.body()
    with open("sitemap_ww.xml.gz","wb") as f:
        f.write(body)
    print("bytes:", len(body))
    browser.close()
