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
    time.sleep(6)
    try:
        btn = page.get_by_text("GO", exact=True)
        print("GO count:", btn.count())
        btn.first.click(timeout=10000)
    except Exception as e:
        print("click err", e)
    time.sleep(6)
    print("URL after GO click:", page.url)
    page.screenshot(path="zh_step3.png", full_page=False)
    html = page.content()
    with open("zh_after_go.html","w",encoding="utf-8") as f:
        f.write(html)
    browser.close()
