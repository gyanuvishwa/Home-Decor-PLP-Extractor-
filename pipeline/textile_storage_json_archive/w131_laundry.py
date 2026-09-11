import re, json, time
from playwright.sync_api import sync_playwright

BASE = "https://www.otto.de"
URLS = [
 "/haushalt/waeschepflege/waeschesammler/waescheboxen/",
 "/haushalt/waeschepflege/waeschesammler/waeschekoerbe/",
 "/haushalt/waeschepflege/waeschesammler/waeschesack/",
 "/haushalt/waeschepflege/waeschesammler/waeschesortierer/",
 "/haushalt/waeschepflege/waeschesammler/waeschetaschen/",
 "/haushalt/waeschepflege/waeschesammler/waeschetonne/",
 "/haushalt/waeschepflege/waeschesammler/waeschetruhe/",
 "/haushalt/waeschepflege/waeschesammler/waeschewannen/",
]
COUNT_RE = re.compile(r'data-product-count="([\d\.]+)"')

def fetch_stable(page, path, max_wait=12):
    url = BASE + path
    last = None
    stable = 0
    start = time.time()
    html = ""
    while time.time() - start < max_wait:
        html = page.content()
        m = COUNT_RE.search(html)
        val = m.group(1) if m else None
        if val == last and val not in (None, "0"):
            stable += 1
            if stable >= 2:
                break
        else:
            stable = 0
        last = val
        page.wait_for_timeout(1200)
    m2 = re.search(r'<h1[^>]*>\s*([^<]*?)\s*</h1>', html)
    h1 = m2.group(1).strip() if m2 else None
    return last, h1

results = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for path in URLS:
        page.goto(BASE + path, wait_until="domcontentloaded", timeout=30000)
        val, h1 = fetch_stable(page, path)
        print(path, "->", val, "h1:", h1)
        results.append({"path": path, "qty": val, "h1": h1})
    browser.close()

with open("w131_laundry_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
