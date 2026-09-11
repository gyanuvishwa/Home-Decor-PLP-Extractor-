import sys, re, json
from playwright.sync_api import sync_playwright

urls = [
 "https://www.structube.com/en_ca/decor/home-accents/cushions",
 "https://www.structube.com/en_ca/decor/home-accents/rugs",
 "https://www.structube.com/en_ca/furniture/bedroom/bedding",
 "https://www.structube.com/en_ca/furniture/storage-organization",
 "https://www.structube.com/en_ca/furniture/storage-organization/bookcases-shelves",
 "https://www.structube.com/en_ca/furniture/storage-organization/cabinets",
 "https://www.structube.com/en_ca/furniture/storage-organization/ottomans",
]

results = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    for url in urls:
        try:
            page.goto(url, wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(1500)
            h1 = page.query_selector("h1")
            h1text = h1.inner_text().strip() if h1 else None
            final_url = page.url
            body_text = page.inner_text("body")
            items_match = re.findall(r'(\d+)\s*items?', body_text, re.IGNORECASE)
            # try to find subcategory chip/nav links
            sublinks = []
            for a in page.query_selector_all("a"):
                href = a.get_attribute("href")
                if href and "/en_ca/" in href and href not in sublinks:
                    txt = (a.inner_text() or "").strip()
                    if txt:
                        sublinks.append((txt, href))
            results.append({
                "url": url, "final_url": final_url, "h1": h1text,
                "items_matches": items_match,
            })
            print("=== ", url)
            print("H1:", h1text, "| final:", final_url)
            print("items:", items_match)
        except Exception as e:
            print("ERROR", url, e)
            results.append({"url": url, "error": str(e)})
    browser.close()

with open("sr193_probe2_out.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
