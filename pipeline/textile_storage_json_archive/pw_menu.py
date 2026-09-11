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
    time.sleep(6)
    # click GO on interstitial country select if present
    try:
        btn = page.get_by_text("GO", exact=True)
        if btn.count() > 0:
            btn.first.click(timeout=10000)
            time.sleep(6)
    except Exception as e:
        print("go click issue", e)
    print("URL now:", page.url)
    # open hamburger menu
    try:
        page.locator("button, a").filter(has_text="").first
    except Exception:
        pass
    # click the menu icon (hamburger) - usually first element top-left
    try:
        page.mouse.click(41, 49)
        time.sleep(3)
    except Exception as e:
        print("menu click err", e)
    page.screenshot(path="zh_menu.png", full_page=False)
    html = page.content()
    with open("zh_menu.html","w",encoding="utf-8") as f:
        f.write(html)
    print("saved menu html len", len(html))
    browser.close()
