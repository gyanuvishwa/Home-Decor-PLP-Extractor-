from curl_cffi import requests
import sys

s = requests.Session(impersonate='chrome124')
r1 = s.get('https://www.homedepot.com/', timeout=25)
print('home', r1.status_code)

url = sys.argv[1]
r2 = s.get(url, timeout=25)
print('target', r2.status_code, len(r2.text))
if r2.status_code == 200:
    with open('sr197_last_fetch.html', 'w', encoding='utf-8') as f:
        f.write(r2.text)
    print('SAVED')
else:
    print(r2.text[:500])
