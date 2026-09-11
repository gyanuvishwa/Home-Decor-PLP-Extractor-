import re, time
from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests

urls = [
"https://www.birchlane.com/bathroom/sb0/bath-accessories-c1877098.html",
"https://www.birchlane.com/storage/sb0/kitchen-sink-accessories-c1875346.html",
"https://www.birchlane.com/storage/cat/bedroom-closet-storage-solutions-c1875434.html",
"https://www.birchlane.com/storage/cat/living-room-storage-solutions-c1875433.html",
"https://www.birchlane.com/storage/sb0/boxes-baskets-c1875445.html",
]

def fetch_one(url):
    for attempt in range(3):
        try:
            r = requests.get(url, impersonate="chrome124", timeout=25)
            if r.status_code == 200:
                return url, r.text
        except Exception:
            pass
        time.sleep(1.5)
    return url, None

results = {}
with ThreadPoolExecutor(max_workers=5) as ex:
    for url, text in ex.map(fetch_one, urls):
        results[url] = text
        print(url, "OK" if text else "FAIL")

import pickle
with open("sr202_ambig.pkl","wb") as f:
    pickle.dump(results, f)
