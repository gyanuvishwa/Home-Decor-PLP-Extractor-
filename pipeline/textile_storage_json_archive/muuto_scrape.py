import json, sys
from playwright.sync_api import sync_playwright

urls = {
    "modular-storage-systems": "https://www.muuto.com/products/storage/modular-storage-systems/",
    "bookcases": "https://www.muuto.com/products/storage/bookcases/",
    "sideboards": "https://www.muuto.com/products/storage/sideboards/",
    "hallway-storage": "https://www.muuto.com/products/storage/hallway-storage/",
    "office-storage": "https://www.muuto.com/products/storage/office-storage/",
    "small-storage": "https://www.muuto.com/products/storage/small-storage/",
    "accessories-storage": "https://www.muuto.com/products/accessories/storage/",
    "rugs": "https://www.muuto.com/products/accessories/rugs/",
    "cushions": "https://www.muuto.com/products/accessories/cushions/",
    "throws": "https://www.muuto.com/products/accessories/throws/",
    "sofa-cushions": "https://www.muuto.com/products/sofas/sofa-cushions/",
    "hangers": "https://www.muuto.com/products/accessories/hangers/",
    "storage-parent": "https://www.muuto.com/products/storage/",
    "accessories-parent": "https://www.muuto.com/products/accessories/",
}

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    for key, url in urls.items():
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(1500)
            h1 = page.locator("h1").first.inner_text() if page.locator("h1").count() > 0 else None
            canonical = page.locator('link[rel="canonical"]').get_attribute("href") if page.locator('link[rel="canonical"]').count() > 0 else None
            tiles = page.locator("article.product-tile").count()
            # try to find a count text
            body_text = page.inner_text("body")
            results[key] = {
                "url": url,
                "h1": h1,
                "canonical": canonical,
                "tile_count": tiles,
            }
            print(key, tiles, h1, canonical)
        except Exception as e:
            results[key] = {"url": url, "error": str(e)}
            print(key, "ERROR", e)
    browser.close()

with open("muuto_playwright_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
