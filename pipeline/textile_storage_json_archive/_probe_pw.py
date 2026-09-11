from playwright.sync_api import sync_playwright
import sys

url = "https://andtradition.com/"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    try:
        resp = page.goto(url, timeout=30000, wait_until="domcontentloaded")
        print("STATUS:", resp.status if resp else None)
        print("TITLE:", page.title())
    except Exception as e:
        print("ERROR:", repr(e))
    browser.close()
