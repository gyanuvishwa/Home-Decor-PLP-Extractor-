from curl_cffi import requests
r = requests.get('https://www.allmodern.com/seo-category-index.xml', impersonate='chrome120', timeout=20)
print(r.status_code)
print(len(r.text))
print(r.text[:3000])
