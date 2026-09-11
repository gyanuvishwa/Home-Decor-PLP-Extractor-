from curl_cffi import requests
import re, json

s = requests.Session(impersonate='chrome124')
r1 = s.get('https://www.homedepot.com/', timeout=25)
html = r1.text
print('status', r1.status_code, len(html))

urls = set(re.findall(r'https://www\.homedepot\.com/b/[^"\\]+', html))
for u in sorted(urls):
    print(u)
print('TOTAL', len(urls))
