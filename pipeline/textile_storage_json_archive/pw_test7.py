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
    for path in ["/in/en/", "/in/"]:
        try:
            page.goto("https://www.zarahome.com" + path, wait_until="domcontentloaded", timeout=30000)
            time.sleep(4)
            print(path, "->", page.url, page.title())
        except Exception as e:
            print(path, "ERROR", e)
    browser.close()
