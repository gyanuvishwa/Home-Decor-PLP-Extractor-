import re, sys
html = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
for m in re.finditer(r'collections/(decor|lighting|mirrors)"', html):
    s = max(0, m.start()-250)
    print('---', m.group(0), '@', m.start())
    print(html[s:m.start()+60].replace('\n',' '))
