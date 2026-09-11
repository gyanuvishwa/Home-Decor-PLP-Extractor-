from playwright.sync_api import sync_playwright
import sys

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width":1366,"height":900}
    )
    page = context.new_page()
    try:
        page.goto("https://www.jossandmain.com/storage/cat/storage-c1858987.html", timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        title = page.title()
        print("TITLE:", title)
        content = page.content()
        print("LEN:", len(content))
        print(content[:1000])
    except Exception as e:
        print("ERROR:", e)
    browser.close()
