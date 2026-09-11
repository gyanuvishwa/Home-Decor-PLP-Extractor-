import json, re, time
from playwright.sync_api import sync_playwright

BASE = "https://www.otto.de"

TEXTILE_URLS = [
 "/heimtextilien/auflagen/",
 "/heimtextilien/badematten/",
 "/heimtextilien/bettdecken/",
 "/heimtextilien/bettdecken/bettdecken-sets/",
 "/heimtextilien/bettdecken/unterbetten/",
 "/heimtextilien/bettlaken/",
 "/heimtextilien/bettwaesche/",
 "/heimtextilien/bezuege/",
 "/heimtextilien/fussmatten/",
 "/heimtextilien/gardinen/",
 "/heimtextilien/gardinen/raffrollos/",
 "/heimtextilien/handtuecher/",
 "/heimtextilien/handtuecher/saunatuecher/hamamtuecher/",
 "/heimtextilien/handtuecher/saunatuecher/sarongs/",
 "/heimtextilien/handtuecher/saunatuecher/saunakilts/",
 "/heimtextilien/handtuecher/waschlappen/",
 "/heimtextilien/hussen/",
 "/heimtextilien/hussen/sesselschoner/",
 "/heimtextilien/hussen/sofaschoner/",
 "/heimtextilien/hussen/sofaueberwuerfe/",
 "/heimtextilien/kissen/",
 "/heimtextilien/kissenbezuege/",
 "/heimtextilien/kniekissen/",
 "/heimtextilien/matratzen/matratzenschutz/encasings/",
 "/heimtextilien/matratzen/matratzenschutz/matratzenbezuege/",
 "/heimtextilien/matratzen/topper/",
 "/heimtextilien/nestchen/",
 "/heimtextilien/rollos-plissees/",
 "/heimtextilien/rollos-plissees/lamellenvorhaenge/",
 "/heimtextilien/rollos-plissees/plissees/",
 "/heimtextilien/rollos-plissees/rollos/",
 "/heimtextilien/rollos-plissees/rollos/doppelrollos/",
 "/heimtextilien/schlafsaecke/",
 "/heimtextilien/schuerzen/",
 "/heimtextilien/stoffe/",
 "/heimtextilien/teppiche/",
 "/heimtextilien/tischdecken/",
 "/heimtextilien/tischdecken/mitteldecken/",
 "/heimtextilien/tischdecken/tischsets/",
 "/heimtextilien/wohndecken/",
 "/heimtextilien/wohndecken/tagesdecken/",
 "/heimtextilien/zubehoer/kissenfuellungen/",
]

STORAGE_URLS = [
 "/dekoration/aufbewahrung/",
 "/dekoration/aufbewahrung/boxen/",
 "/dekoration/aufbewahrung/boxen/aufbewahrungsboxen/",
 "/dekoration/aufbewahrung/koerbe/",
 "/dekoration/aufbewahrung/kisten/",
 "/dekoration/aufbewahrung/truhen/",
 "/dekoration/aufbewahrung/aufbewahrungstaschen/",
 "/dekoration/aufbewahrung/ablagen/",
 "/dekoration/aufbewahrung/etuis/",
 "/dekoration/aufbewahrung/schirmstaender/",
 "/dekoration/aufbewahrung/schluesselaufbewahrung/",
 "/dekoration/aufbewahrung/schluesselaufbewahrung/schluesselbretter/",
 "/dekoration/aufbewahrung/schmuckaufbewahrungen/",
 "/dekoration/aufbewahrung/tuerregale/",
 "/dekoration/aufbewahrung/unterbettkommoden/",
 "/dekoration/aufbewahrung/wandhaken/",
 "/dekoration/aufbewahrung/zeitungsstaender/",
 "/haushalt/waeschepflege/waeschesammler/",
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
H1_RE = re.compile(r'<h1[^>]*>\s*([^<]*?)\s*</h1>')
CANON_RE = re.compile(r'<link rel="canonical" href="([^"]*)"')

def fetch(page, path):
    url = BASE + path
    result = {"path": path, "url": url, "qty": None, "h1": None, "canonical": None, "error": None}
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        try:
            page.wait_for_selector('[data-product-count]', timeout=9000)
        except Exception:
            page.wait_for_timeout(3000)
        html = page.content()
        m = COUNT_RE.search(html)
        if m:
            result["qty"] = int(m.group(1).replace(".", ""))
        m2 = H1_RE.search(html)
        if m2:
            result["h1"] = m2.group(1).strip()
        m3 = CANON_RE.search(html)
        if m3:
            result["canonical"] = m3.group(1)
    except Exception as e:
        result["error"] = str(e)
    return result

def main():
    all_urls = [("textile", u) for u in TEXTILE_URLS] + [("storage", u) for u in STORAGE_URLS]
    results = {"textile": {}, "storage": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        for cat, path in all_urls:
            r = fetch(page, path)
            results[cat][path] = r
            print(cat, path, "->", r["qty"], "| h1:", r["h1"], "| canon:", r["canonical"], "| err:", r["error"])
        browser.close()
    with open("w131_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
