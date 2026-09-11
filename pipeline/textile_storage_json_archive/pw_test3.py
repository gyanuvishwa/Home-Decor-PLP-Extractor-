from playwright.sync_api import sync_playwright
import time, json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context(
        viewport={"width":1366,"height":900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        locale="en-US",
    )
    page = context.new_page()
    page.goto("https://www.zarahome.com/ww/", wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    page.screenshot(path="zh_step1.png", full_page=False)
    # look for continue/accept/confirm buttons
    for txt in ["Continue","CONTINUE","Accept","Confirm","Shop now","SHOP NOW","Go to site","Enter site"]:
        try:
            loc = page.get_by_text(txt, exact=False)
            if loc.count() > 0:
                print("found button text:", txt, loc.count())
        except Exception as e:
            pass
    browser.close()
