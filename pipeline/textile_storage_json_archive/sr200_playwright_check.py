import json, re, sys
from playwright.sync_api import sync_playwright

urls = [
    "https://www.indigo.ca/collections/organizing-storage",
    "https://www.indigo.ca/collections/organizing",
    "https://www.indigo.ca/collections/robes",
    "https://www.indigo.ca/collections/tofino-towel-co",
    "https://www.indigo.ca/collections/towel-to-go",
    "https://www.indigo.ca/collections/kids-mealtime-food-storage",
    "https://www.indigo.ca/collections/christmas-pillows-throws",
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    page = context.new_page()

    captured = {}

    def handle_response(response):
        if "ac.cnstrc.com/browse" in response.url or "ac.cnstrc.com/search" in response.url:
            try:
                data = response.json()
                total = data.get("response", {}).get("total_num_results")
                captured[response.url] = total
            except Exception:
                pass

    page.on("response", handle_response)

    for url in urls:
        captured.clear()
        entry = {}
        try:
            page.goto(url, wait_until="networkidle", timeout=45000)
        except Exception as e:
            entry["nav_error"] = str(e)
        try:
            page.wait_for_timeout(2500)
        except Exception:
            pass
        try:
            h1 = page.locator("h1").first.inner_text(timeout=5000)
        except Exception:
            h1 = None
        entry["h1"] = h1
        entry["final_url"] = page.url
        entry["cnstrc_totals"] = dict(captured)
        # try to find rendered products count text near grid header
        try:
            body_text = page.inner_text("body")
        except Exception:
            body_text = ""
        m = re.findall(r'(\d[\d,]*)\s+[Pp]roducts?', body_text)
        entry["products_text_matches"] = m[:5]
        results[url] = entry
        print(f"DONE {url} -> h1={h1!r} totals={captured} textmatches={m[:5]}")

    browser.close()

with open("sr200_pw_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
