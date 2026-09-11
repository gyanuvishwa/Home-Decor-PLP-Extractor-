import re, sys
fname = sys.argv[1]
needle = sys.argv[2]
before = int(sys.argv[3]) if len(sys.argv) > 3 else 200
after = int(sys.argv[4]) if len(sys.argv) > 4 else 300
html = open(fname, encoding='utf-8').read()
for m in re.finditer(re.escape(needle), html):
    i = m.start()
    print(html[max(0,i-before):i+after])
    print('=====')
