import re, json, time, sys
from curl_cffi import requests

def fetch(url, retries=2):
    last_exc = None
    for i in range(retries):
        try:
            r = requests.get(url, impersonate="chrome124", timeout=25)
            return r
        except Exception as e:
            last_exc = e
            time.sleep(1)
    raise last_exc

def extract_info(html):
    info = {}
    m = re.search(r'"numberOfItems":(\d+)', html)
    if m:
        info['numberOfItems'] = int(m.group(1))
    m2 = re.search(r'>([\d,]+)\s+Items?<', html)
    if m2:
        info['renderedItems'] = m2.group(1)
    m3 = re.search(r'<h1[^>]*>.*?<span[^>]*>([^<]+)</span>', html)
    if m3:
        info['h1'] = m3.group(1)
    else:
        m3b = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        if m3b:
            info['h1'] = m3b.group(1)
    m4 = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if m4:
        info['canonical'] = m4.group(1)
    # capped indicator
    if re.search(r'Over\s+[\d,]+\s+Items', html):
        mc = re.search(r'(Over\s+[\d,]+\s+Items)', html)
        info['capped'] = mc.group(1)
    return info

if __name__ == "__main__":
    url = sys.argv[1]
    r = fetch(url)
    print("status", r.status_code)
    info = extract_info(r.text)
    print(json.dumps(info, indent=2))
