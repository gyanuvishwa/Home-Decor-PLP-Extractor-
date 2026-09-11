import re, json, time
from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests

urls = [
"https://www.birchlane.com/bedding/cat/bedding-c1804406.html",
"https://www.birchlane.com/bedding/cat/bedding-essentials-c1875727.html",
"https://www.birchlane.com/bedding/cat/bedding-sets-accessories-c1875726.html",
"https://www.birchlane.com/bathroom/cat/bath-linens-accessories-c1860612.html",
"https://www.birchlane.com/bathroom/cat/bathroom-c1867193.html",
"https://www.birchlane.com/decor-pillows/cat/pillows-throws-c1870870.html",
"https://www.birchlane.com/decor-pillows/cat/organizational-decor-c1873880.html",
"https://www.birchlane.com/decor-pillows/cat/home-decor-c1870918.html",
"https://www.birchlane.com/decor-pillows/cat/decor-pillows-c1804408.html",
"https://www.birchlane.com/wall-decor-mirrors/cat/curtains-curtain-hardware-c1872495.html",
"https://www.birchlane.com/wall-decor-mirrors/cat/wall-decor-c1870917.html",
"https://www.birchlane.com/wall-decor-mirrors/cat/wall-decor-mirrors-c1875387.html",
"https://www.birchlane.com/storage/cat/storage-c1875307.html",
"https://www.birchlane.com/storage/cat/storage-by-product-c1875735.html",
"https://www.birchlane.com/storage/cat/storage-solutions-by-room-c1875736.html",
"https://www.birchlane.com/storage/cat/entryway-storage-solutions-c1875438.html",
"https://www.birchlane.com/storage/cat/kitchen-storage-solutions-c1875436.html",
"https://www.birchlane.com/storage/cat/bathroom-laundry-storage-solutions-c1875437.html",
"https://www.birchlane.com/storage/cat/home-office-storage-solutions-c1875435.html",
"https://www.birchlane.com/storage/cat/storage-cabinets-c1875431.html",
"https://www.birchlane.com/kitchen-tabletop/cat/kitchen-linens-c1875337.html",
"https://www.birchlane.com/kitchen-tabletop/cat/table-kitchen-linens-c1807211.html",
"https://www.birchlane.com/kitchen-tabletop/cat/kitchen-tabletop-c1804418.html",
"https://www.birchlane.com/baby-kids/cat/baby-bedding-c1875649.html",
"https://www.birchlane.com/baby-kids/cat/baby-kids-c1861144.html",
"https://www.birchlane.com/outdoor/cat/outdoor-c1845014.html",
"https://www.birchlane.com/holiday/cat/holiday-c1837548.html",
"https://www.birchlane.com/furniture/cat/organizational-furniture-c1874081.html",
"https://www.birchlane.com/furniture/cat/storage-benches-trunks-c1875288.html",
]

def fetch_one(url):
    for attempt in range(3):
        try:
            r = requests.get(url, impersonate="chrome124", timeout=25)
            if r.status_code == 200:
                return url, r.text
            else:
                time.sleep(1.5)
        except Exception as e:
            time.sleep(1.5)
    return url, None

results = {}
with ThreadPoolExecutor(max_workers=6) as ex:
    for url, text in ex.map(fetch_one, urls):
        results[url] = text
        print(url, "OK" if text else "FAIL", len(text) if text else 0)

import pickle
with open("sr202_batch1.pkl", "wb") as f:
    pickle.dump(results, f)
