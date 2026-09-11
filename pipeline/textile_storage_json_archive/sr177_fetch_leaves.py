# -*- coding: utf-8 -*-
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from sr177_lib import get_category_info
from sr177_plan import PLAN

def worker(item):
    info = get_category_info(item["href"])
    return {
        **item,
        "h1": info.get("h1"),
        "total_results": info.get("total_results"),
        "status_code": info.get("status_code"),
    }

results = []
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(worker, item): item for item in PLAN}
    for fut in as_completed(futs):
        r = fut.result()
        results.append(r)
        print(r["cat"], "|", r["sub_en"], "|", r["h1"], "|", r["total_results"], flush=True)

with open("sr177_leaves_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

print("TOTAL", len(results))
