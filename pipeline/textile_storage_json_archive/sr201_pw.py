from playwright.sync_api import sync_playwright
import sys

url = "https://www.allmodern.com/storage/cat/storage-c1875304.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
    )
    page = context.new_page()
    try:
        resp = page.goto(url, timeout=30000, wait_until="domcontentloaded")
        print("status:", resp.status if resp else None)
        page.wait_for_timeout(4000)
        title = page.title()
        print("title:", title)
        content = page.content()
        with open("sr201_pw_storage_top.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("len:", len(content))
    except Exception as e:
        print("ERROR:", e)
    finally:
        browser.close()
