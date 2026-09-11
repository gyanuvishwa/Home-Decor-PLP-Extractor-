import requests, json, re, time, sys

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch(url, retries=2):
    for i in range(retries):
        try:
            r = requests.get(url, timeout=25, headers=HEADERS)
            return r
        except Exception as e:
            print("fetch err", url, e, file=sys.stderr)
            time.sleep(1)
    return None

def parse_state(html):
    idx = html.find('id="nitoristore-state"')
    if idx == -1:
        return None
    start = html.find('>', idx) + 1
    end = html.find('</script>', start)
    data = html[start:end]
    try:
        return json.loads(data)
    except Exception as e:
        print("json parse err", e, file=sys.stderr)
        return None

def get_category_info(url):
    r = fetch(url)
    if r is None or r.status_code != 200:
        return {"url": url, "status_code": None if r is None else r.status_code, "error": "fetch_failed"}
    html = r.text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find('h1')
    h1text = h1.get_text(' ', strip=True) if h1 else None
    subcats = []
    for a in soup.select('a.categories-link'):
        href = a.get('href')
        text = a.get_text(' ', strip=True)
        if href and text:
            subcats.append({"text": text, "href": href})
    state = parse_state(html)
    pagination = None
    total_results = None
    if state:
        try:
            results = state['cx-state']['product']['search']['results']
            pagination = results.get('pagination')
            if pagination:
                total_results = pagination.get('totalResults')
        except Exception as e:
            pass
    return {
        "url": url,
        "status_code": r.status_code,
        "h1": h1text,
        "subcats": subcats,
        "total_results": total_results,
    }

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    info = get_category_info(url)
    print(json.dumps(info, ensure_ascii=False, indent=1))
