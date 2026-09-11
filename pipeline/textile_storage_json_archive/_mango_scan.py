import json, sys
from playwright.sync_api import sync_playwright

BASE = "https://shop.mango.com/us/en/c/home/"

CATEGORIES = [
    # (key, slug, expected_group)
    ("cushion-covers", "cushion-covers/e50c6bbc", "textile"),
    ("sofa-blankets", "sofa-blankets/4ef15714", "textile"),
    ("duvet-covers", "duvet-covers/4c955217", "textile"),
    ("bottom-sheets", "bottom-sheets/0b7ebd50", "textile"),
    ("flat-sheets", "flat-sheets/28910b57", "textile"),
    ("pillow-cases", "pillow-cases/2a97d7ee", "textile"),
    ("bedroom-cushion-covers", "bedroom-cushion-covers/7535b5a8", "textile"),
    ("fillings-and-protectors", "fillings-and-protectors/c59a73cc", "textile"),
    ("bedspreads-and-duvets", "bedspreads-and-duvets/06fd0d24", "textile"),
    ("sheets-and-pillows", "sheets-and-pillows/7708cf7e", "textile"),
    ("bedroom-blankets", "bedroom-blankets/b360a1b6", "textile"),
    ("tablecloths", "tablecloths/1922ea48", "textile"),
    ("table-linen-and-kitchen-textiles", "table-linen-and-kitchen-textiles/8f4ef503", "textile"),
    ("kitchen-textiles", "kitchen-textiles/21ff05e7", "textile"),
    ("table-items", "table-items/7859e826", "textile"),
    ("towels", "towels/349dbd1f", "textile"),
    ("bathrobes-and-slippers", "bathrobes-and-slippers/f16b676a", "textile"),
    ("bathroom-textiles", "bathroom-textiles/56fc38b7", "textile"),
    ("beach-towels-1", "beach-towels/0a5cbb32", "textile"),
    ("outdoor-tablecloths", "outdoor-tablecloths/12800140", "textile"),
    ("outdoor-cushion-cases", "outdoor-cushion-cases/049dcc9d", "textile"),
    ("soft-furnishings", "soft-furnishings/beef0699", "textile"),
    ("rugs", "rugs/4f75af4c", "textile"),
    ("bathroom-baskets", "bathroom-baskets/3e2faeba", "storage"),
    ("boxes-and-jewelry-boxes", "boxes-and-jewelry-boxes/78e4caf0", "storage"),
]

def get_count(page):
    return page.eval_on_selector_all('form[class*="ProductCard-module"]', 'els => els.length')

def scan(page, url):
    page.goto(url, wait_until="load", timeout=45000)
    page.wait_for_timeout(1500)
    stable_at_bottom = 0
    it = 0
    max_iters = 220
    last_count = -1
    while stable_at_bottom < 5 and it < max_iters:
        it += 1
        page.evaluate("window.scrollBy(0, 900)")
        page.wait_for_timeout(550)
        sy = page.evaluate("window.scrollY")
        ih = page.evaluate("window.innerHeight")
        sh = page.evaluate("document.body.scrollHeight")
        c = get_count(page)
        at_bottom = (sy + ih) >= (sh - 5)
        if at_bottom:
            if c == last_count:
                stable_at_bottom += 1
            else:
                stable_at_bottom = 0
        else:
            stable_at_bottom = 0
        last_count = c
    h1 = page.eval_on_selector("h1", "e => e ? e.innerText : null")
    return {"count": last_count, "iters": it, "h1": h1}

def main():
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 900}, locale="en-US"
        )
        page = context.new_page()
        for key, slug, grp in CATEGORIES:
            url = BASE + slug
            try:
                r = scan(page, url)
                r["group"] = grp
                r["url"] = url
                results[key] = r
                print(f"{key}: count={r['count']} iters={r['iters']} h1={r['h1']}", flush=True)
            except Exception as e:
                results[key] = {"error": str(e)[:300], "group": grp, "url": url}
                print(f"{key}: ERROR {str(e)[:150]}", flush=True)
        browser.close()
    with open("C:/Users/GyanendraVishwakarma/Web Research Agent/pipeline/textile_storage_json_archive/_mango_scan_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
