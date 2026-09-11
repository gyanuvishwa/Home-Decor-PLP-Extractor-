import json, re, time
from playwright.sync_api import sync_playwright

BASE = "https://www.otto.de"

SUSPECTS = [
 "/heimtextilien/gardinen/raffrollos/",
 "/heimtextilien/teppiche/teppichunterlagen/",
 "/heimtextilien/tischdecken/mitteldecken/",
 "/heimtextilien/buegeltuecher/",
 "/haushalt/tischaccessoires/tischdecken/tischbaender/",
 "/babys/ausstattung/krabbeldecken/",
 "/babys/ausstattung/schmusetuecher/",
 "/heimtextilien/matratzen/matratzenschutz/matratzenbezuege/",
 "/heimtextilien/matratzen/matratzenschutz/encasings/",
 "/dekoration/aufbewahrung/tuerregale/",
 "/dekoration/aufbewahrung/flaschenhalter/",
 "/dekoration/aufbewahrung/schirmstaender/",
 "/dekoration/aufbewahrung/unterbettkommoden/",
 "/haushalt/waeschepflege/waeschenetz/",
 # control (known good non-round value)
 "/heimtextilien/bettlaken/",
]

COUNT_RE = re.compile(r'data-product-count="([\d\.]+)"')

def fetch_stable(page, path, max_wait=15):
    url = BASE + path
    out = {"path": path, "samples": [], "final": None, "h1": None, "error": None}
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        start = time.time()
        last = None
        stable_count = 0
        while time.time() - start < max_wait:
            html = page.content()
            m = COUNT_RE.search(html)
            val = m.group(1) if m else None
            out["samples"].append(val)
            if val == last and val not in (None, "0"):
                stable_count += 1
                if stable_count >= 2:
                    break
            else:
                stable_count = 0
            last = val
            page.wait_for_timeout(1500)
        out["final"] = last
        m2 = re.search(r'<h1[^>]*>\s*([^<]*?)\s*</h1>', html)
        if m2:
            out["h1"] = m2.group(1).strip()
    except Exception as e:
        out["error"] = str(e)
    return out

def main():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        for path in SUSPECTS:
            r = fetch_stable(page, path)
            results.append(r)
            print(path, "-> samples:", r["samples"], "final:", r["final"], "h1:", r["h1"], "err:", r["error"])
        browser.close()
    with open("w131_verify500_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
