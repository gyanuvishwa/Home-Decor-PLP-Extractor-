import re, sys
fname = sys.argv[1]
html = open(fname, encoding='utf-8').read()
for kw in ['numFound','hits','recordCount','productCount','resultsCount','"count":','numberOfProducts','totalProducts','itemCount','"products":','"skip"','"take"','showingText','resultText']:
    idxs = [m.start() for m in re.finditer(re.escape(kw), html)]
    print(kw, len(idxs))
    if idxs and kw in ('"count":','showingText','resultText'):
        i = idxs[0]
        print('  ctx:', html[max(0,i-80):i+80])
