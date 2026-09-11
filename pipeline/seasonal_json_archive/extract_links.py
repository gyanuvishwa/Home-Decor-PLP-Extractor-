import re, sys

fname = sys.argv[1] if len(sys.argv) > 1 else 'cb_home.html'
html = open(fname, encoding='utf-8').read()

hrefs = set(re.findall(r'"(?:href|url)":"(\/[^"]*)"', html))
hrefs |= set(re.findall(r'href="(\/[^"]*)"', html))

kw = re.compile(r'(?i)christmas|halloween|thanksgiv|valentine|easter|holiday|festive|new-year|newyear|seasonal|fall-decor|autumn|deepavali|diwali')
matches = sorted(h for h in hrefs if kw.search(h))
for m in matches:
    print(m)
print(f"--- {len(matches)} matches / {len(hrefs)} total hrefs ---", file=sys.stderr)
