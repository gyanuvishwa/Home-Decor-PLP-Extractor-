import re, sys, json

fname = sys.argv[1]
prefix = sys.argv[2] if len(sys.argv) > 2 else ''
html = open(fname, encoding='utf-8').read()

# find navigateUrl entries under the given prefix, with their name
pattern = re.compile(r'\{"id":(\d+),"name":"([^"]*)"[^}]*?"navigateUrl":"(' + re.escape(prefix) + r'[^"]*)"')
seen = {}
for m in pattern.finditer(html):
    seen[m.group(3)] = m.group(2)

for url, name in sorted(seen.items()):
    print(f"{url}\t{name}")
print(f"--- {len(seen)} matches ---", file=sys.stderr)
