import re, glob, os

files = sorted(glob.glob("sr192_*.html"))
for f in files:
    if f.startswith("sr192_categorySitemap") or f.startswith("sr192_homedecor"):
        continue
    html = open(f, encoding="utf-8", errors="ignore").read()
    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    h1 = re.sub(r'<[^>]+>', '', h1m.group(1)).strip() if h1m else None
    cm = re.search(r'js-categoryFiltersList-productCount">([\d,]+)</span>', html)
    count = cm.group(1) if cm else None
    # canonical
    canm = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    canon = canm.group(1) if canm else None
    print(f"{f} | h1={h1!r} | count={count} | canon={canon}")
