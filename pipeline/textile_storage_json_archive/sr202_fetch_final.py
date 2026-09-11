import time, pickle
from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests
from sr202_final_urls import TEXTILE, STORAGE

all_urls = {}
all_urls.update(TEXTILE)
all_urls.update(STORAGE)

def fetch_one(item):
    name, url = item
    for attempt in range(3):
        try:
            r = requests.get(url, impersonate="chrome124", timeout=25)
            if r.status_code == 200:
                return name, url, r.text
            else:
                print(name, url, "status", r.status_code)
        except Exception as e:
            print(name, url, "err", e)
        time.sleep(1.5)
    return name, url, None

results = {}
with ThreadPoolExecutor(max_workers=6) as ex:
    for name, url, text in ex.map(fetch_one, all_urls.items()):
        results[name] = (url, text)
        print(name, "OK" if text else "FAIL")

with open("sr202_final_fetch.pkl", "wb") as f:
    pickle.dump(results, f)
