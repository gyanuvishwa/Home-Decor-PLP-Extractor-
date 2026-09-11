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

    # Wait up to 30s for GO button to appear, click it
    clicked = False
    for i in range(15):
        time.sleep(2)
        try:
            btn = page.get_by_text("GO", exact=True)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(timeout=5000)
                clicked = True
                break
        except Exception as e:
            pass
    print("clicked GO:", clicked)
    time.sleep(8)
    print("URL now:", page.url)

    # open hamburger menu (top-left icon)
    try:
        page.locator("button[aria-label], .menu-icon, .header-menu-icon, [class*='menu']").first
    except Exception:
        pass
    page.mouse.click(41, 49)
    time.sleep(3)
    page.screenshot(path="zh_menu2.png", full_page=False)
    html = page.content()
    with open("zh_menu2.html","w",encoding="utf-8") as f:
        f.write(html)
    print("saved, len", len(html))
    browser.close()
