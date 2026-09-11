import pickle, json
from sr202_fetch_lib import extract_info

with open("sr202_final_fetch.pkl","rb") as f:
    results = pickle.load(f)

out = {}
for name, (url, html) in results.items():
    info = extract_info(html)
    out[name] = {"url": url, **info}
    print(f"{name:35s} | h1={info.get('h1','')!s:40s} | rendered={info.get('renderedItems')!s:8s} | numberOfItems={info.get('numberOfItems')} | capped={info.get('capped')}")

with open("sr202_qty_results.json","w",encoding="utf-8") as f:
    json.dump(out, f, indent=2)
