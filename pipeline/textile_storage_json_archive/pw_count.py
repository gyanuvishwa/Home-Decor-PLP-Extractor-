import sys, json
from playwright.sync_api import sync_playwright

url = sys.argv[1]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36", viewport={"width":1400,"height":1000})

    results = []
    def on_resp(response):
        if "algolia" in response.url and "queries" in response.url:
            try:
                body = response.json()
                results.append(body)
            except Exception as e:
                pass
    page.on("response", on_resp)

    page.goto(url, wait_until="load", timeout=60000)
    page.wait_for_timeout(1500)
    page.mouse.wheel(0, 2000)
    page.wait_for_timeout(2500)
    page.mouse.wheel(0, 2000)
    page.wait_for_timeout(4000)

    h1 = page.query_selector("h1")
    print("H1:", h1.inner_text() if h1 else None)
    print("NUM ALGOLIA RESPONSES CAPTURED:", len(results))
    for r in results:
        if "results" in r:
            for res in r["results"]:
                idx = res.get("index")
                nb = res.get("nbHits")
                query = res.get("query")
                params = res.get("params")
                print(f"index={idx} nbHits={nb} query={query!r} params={params}")
    browser.close()
