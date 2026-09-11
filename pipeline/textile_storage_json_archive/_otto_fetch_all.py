# -*- coding: utf-8 -*-
import json, re, time, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _otto_rows import TEXTILE_ROWS, STORAGE_ROWS, BASE
from playwright.sync_api import sync_playwright

OUT_PATH = r"C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\c796539f-ebc8-4338-b591-e5d11e875246\scratchpad\otto_results.json"

def collect_urls():
    urls = []
    for arr in (TEXTILE_ROWS, STORAGE_ROWS):
        for kind, name, path, conf, note in arr:
            if kind == "leaf" and path:
                urls.append(BASE + path)
    # dedupe preserving order
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

def load_existing():
    if os.path.exists(OUT_PATH):
        with open(OUT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save(results):
    tmp = OUT_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    os.replace(tmp, OUT_PATH)

def fetch_one(page, url, timeout_ms=16000):
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
    except Exception as e:
        return {"error": "goto_failed: %s" % str(e)[:200]}
    try:
        page.wait_for_selector(".reptile-item-count__item-count", timeout=timeout_ms)
    except Exception:
        pass  # fall through, try to read whatever is there (may be 0 results / different layout)
    try:
        h1 = page.locator("h1").first.inner_text(timeout=3000)
    except Exception:
        h1 = None
    count_attr = None
    count_text = None
    try:
        el = page.locator(".reptile-item-count__item-count").first
        count_attr = el.get_attribute("data-item-count", timeout=3000)
        count_text = el.inner_text(timeout=3000)
    except Exception:
        pass
    canonical = None
    try:
        canonical = page.locator('link[rel="canonical"]').first.get_attribute("href", timeout=2000)
    except Exception:
        pass
    zero_result = False
    if count_attr is None:
        try:
            body_txt = page.inner_text("body", timeout=3000)
            if re.search(r"\bkeine\s+(Ergebnisse|Treffer|Produkte)\b", body_txt, re.I) or "0 Produkte" in body_txt:
                zero_result = True
        except Exception:
            pass
    return {
        "h1": h1,
        "item_count_attr": count_attr,
        "item_count_text": count_text,
        "canonical": canonical,
        "zero_result": zero_result,
    }

def main():
    urls = collect_urls()
    results = load_existing()
    todo = [u for u in urls if u not in results]
    print("Total URLs: %d, already done: %d, todo: %d" % (len(urls), len(results), len(todo)))
    if not todo:
        print("Nothing to do.")
        return
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="de-DE",
            viewport={"width": 1400, "height": 1000},
        )
        page = ctx.new_page()
        page.set_default_navigation_timeout(16000)
        count = 0
        for u in todo:
            t0 = time.time()
            res = fetch_one(page, u)
            results[u] = res
            count += 1
            dt = time.time() - t0
            print("[%d/%d] %.1fs %s -> %s" % (count, len(todo), dt, u, res))
            if count % 10 == 0:
                save(results)
        save(results)
        browser.close()
    print("DONE. Saved %d results to %s" % (len(results), OUT_PATH))

if __name__ == "__main__":
    main()
