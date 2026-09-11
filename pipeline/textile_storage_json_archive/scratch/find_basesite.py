with open(r'C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline\textile_storage_json_archive\cushions.html', encoding='utf-8') as f:
    html = f.read()
idx = html.find('baseSite')
print(idx)
if idx > 0:
    print(html[idx-50:idx+400])
