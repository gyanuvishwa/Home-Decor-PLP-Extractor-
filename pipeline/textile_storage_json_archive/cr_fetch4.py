import json, re, time
from playwright.sync_api import sync_playwright

urls = [
    "/home-kids-home-nursery/",
    "/home-home-accessories-decorator/",
    "/home-outdoor-picnic/",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for u in urls:
        full = "https://www.countryroad.com.au" + u
        page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        page.goto(full, timeout=45000, wait_until='domcontentloaded')
        page.wait_for_timeout(3500)
        content = page.content()
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', content, re.S)
        data = json.loads(m.group(1))
        crg = data['props']['pageProps']['initialState']['crgApi']['queries']
        for k, v in crg.items():
            if k.startswith('getProductLanding-'):
                d = v['data']['ProductLanding']
                print("===", u, "totalCount:", d['totalCount'], flush=True)
                for r in d.get('results', []):
                    print("  -", r.get('title'), flush=True)
        page.close()
    browser.close()
print("DONE4", flush=True)
