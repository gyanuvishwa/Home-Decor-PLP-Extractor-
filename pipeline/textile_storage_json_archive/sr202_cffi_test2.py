from curl_cffi import requests
r = requests.get("https://www.birchlane.com/bedding/sb0/comforters-sets-c1874122.html", impersonate="chrome124", timeout=20)
html = r.text
with open("sr202_comforters.html", "w", encoding="utf-8") as f:
    f.write(html)
print(len(html))
import re
# search for item count patterns
for m in re.finditer(r'"resultsCount"\s*:\s*(\d+)', html):
    print("resultsCount", m.group(1))
for m in re.finditer(r'"totalCount"\s*:\s*(\d+)', html):
    print("totalCount", m.group(1))
for m in re.finditer(r'"itemCount"\s*:\s*(\d+)', html):
    print("itemCount", m.group(1))
for m in re.finditer(r'([0-9,]{1,7})\s+[Ii]tems', html):
    print("Items text", m.group(0))
for m in re.finditer(r'"h1"\s*:\s*"([^"]+)"', html):
    print("h1", m.group(1))
for m in re.finditer(r'<h1[^>]*>([^<]+)</h1>', html):
    print("h1tag", m.group(1))
