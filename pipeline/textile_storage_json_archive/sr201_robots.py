from curl_cffi import requests
r = requests.get('https://www.allmodern.com/robots.txt', impersonate='chrome120', timeout=20)
print(r.status_code)
print(r.text[:5000])
