import json, re
from playwright.sync_api import sync_playwright

BASE = "https://shop.mango.com/us/en/c/home/"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 900}, locale="en-US"
        )
        page = context.new_page()
        page.goto(BASE, wait_until="load", timeout=60000)
        page.wait_for_timeout(2500)
        # try to open the mega menu / nav - get all links matching /us/en/c/home/
        hrefs = page.eval_on_selector_all("a[href*='/us/en/c/home/']", "els => els.map(e => [e.getAttribute('href'), e.innerText.trim()])")
        uniq = {}
        for href, text in hrefs:
            if href not in uniq:
                uniq[href] = text
        with open("_mango_nav_fresh.json", "w", encoding="utf-8") as f:
            json.dump(uniq, f, indent=1, ensure_ascii=False)
        print("total links:", len(uniq))
        # also grab full body text to check for a products-count pattern
        body_text = page.inner_text("body")
        print("BODY LEN", len(body_text))
        browser.close()

if __name__ == "__main__":
    main()
