import pickle, re
from sr202_fetch_lib import extract_info

with open("sr202_batch1.pkl", "rb") as f:
    results = pickle.load(f)

for url, html in results.items():
    if not html:
        continue
    section = url.split("birchlane.com/")[1].split("/")[0]
    info = extract_info(html)
    links = sorted(set(re.findall(r'/%s/(?:cat|sb0)/[a-z0-9-]*' % section, html)))
    print("="*100)
    print(url)
    print("  h1:", info.get('h1'), "| rendered:", info.get('renderedItems'), "| numberOfItems:", info.get('numberOfItems'), "| capped:", info.get('capped'))
    for l in links:
        print("   ", l)
