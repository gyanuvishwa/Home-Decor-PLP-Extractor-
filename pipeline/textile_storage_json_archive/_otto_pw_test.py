import sys, re, json
from playwright.sync_api import sync_playwright

URL = "https://www.otto.de/heimtextilien/kissen/dekokissen/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        locale="de-DE",
        viewport={"width": 1400, "height": 1000},
    )
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(2000)
    html = page.content()
    with open(r"C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\c796539f-ebc8-4338-b591-e5d11e875246\scratchpad\otto_pw_dekokissen.html", "w", encoding="utf-8") as f:
        f.write(html)
    # try to find h1 and any count text
    h1 = page.locator("h1").first.inner_text()
    print("H1:", h1)
    body_text = page.inner_text("body")
    for m in re.finditer(r"\d[\d\.\s]*\s*(Ergebnisse|Artikel|Produkte|Treffer)", body_text):
        print("MATCH:", m.group(0))
    browser.close()
