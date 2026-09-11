import time, pickle
from curl_cffi import requests
from sr202_final_urls import TEXTILE, STORAGE

all_urls = {}
all_urls.update(TEXTILE)
all_urls.update(STORAGE)

with open("sr202_final_fetch.pkl","rb") as f:
    results = pickle.load(f)

fails = [name for name, (url, text) in results.items() if not text]
print("Fails to retry:", fails)

for name in fails:
    url = all_urls[name]
    ok = False
    for attempt in range(5):
        try:
            r = requests.get(url, impersonate="chrome124", timeout=25)
            if r.status_code == 200:
                results[name] = (url, r.text)
                print(name, "OK on attempt", attempt+1)
                ok = True
                break
            else:
                print(name, "status", r.status_code, "attempt", attempt+1)
        except Exception as e:
            print(name, "err", e, "attempt", attempt+1)
        time.sleep(4 + attempt*2)
    if not ok:
        print(name, "STILL FAILING")

with open("sr202_final_fetch.pkl","wb") as f:
    pickle.dump(results, f)
