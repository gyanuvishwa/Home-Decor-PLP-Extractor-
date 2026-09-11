import re, sys
fname = sys.argv[1]
html = open(fname, encoding='utf-8').read()
# find all distinct JSON keys (rough) to look for product-list-like keys
keys = set(re.findall(r'"([a-zA-Z][a-zA-Z0-9_]{2,40})":', html))
interesting = sorted(k for k in keys if re.search(r'(?i)product|sku|item|result|grid|listing|plp|categ|total|count', k))
for k in interesting:
    print(k)
