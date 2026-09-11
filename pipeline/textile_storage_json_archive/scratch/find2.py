import re
with open(r'C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\textile_storage_json_archive\cushions.html', encoding='utf-8') as f:
    html = f.read()
for m in re.finditer(r'baseSite', html):
    idx = m.start()
    print(idx, html[idx-30:idx+200])
    print('---')
