import json, sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    try:
        page.goto("https://www.nitori-net.jp/ec/", wait_until="commit", timeout=45000)
        print("commit ok", flush=True)
        page.wait_for_load_state("domcontentloaded", timeout=45000)
        print("dom ok", flush=True)
    except Exception as e:
        print("goto err:", e, flush=True)
    page.wait_for_timeout(6000)
    try:
        html = page.content()
        open("sr177_home_rendered.html", "w", encoding="utf-8").write(html)
        print("content len", len(html), flush=True)
    except Exception as e:
        print("content err:", e, flush=True)
    try:
        links = page.eval_on_selector_all("a", "els => els.map(e => ({href: e.href, text: e.textContent.trim()}))")
        with open("sr177_home_links.json", "w", encoding="utf-8") as f:
            json.dump(links, f, ensure_ascii=False, indent=2)
        print("total links", len(links), flush=True)
    except Exception as e:
        print("links err:", e, flush=True)
    browser.close()
print("DONE_SCRIPT", flush=True)
