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
    # try to find country selector button
    try:
        page.get_by_text("Select your country", exact=False).first.click(timeout=5000)
        time.sleep(2)
    except Exception as e:
        print("no select country text", e)
    html = page.content()
    print("HTML length after attempt:", len(html))
    # search for india text link
    import re
    idx = html.find('India')
    print(html[max(0,idx-500):idx+500])
    with open("zh_country_selector.html","w",encoding="utf-8") as f:
        f.write(html)
    browser.close()
