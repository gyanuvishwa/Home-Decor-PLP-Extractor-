from curl_cffi import requests
r = requests.get('https://www.allmodern.com/seo-category-sitemap~0.xml', impersonate='chrome120', timeout=30)
print(r.status_code)
print(len(r.text))
with open('sr201_category_sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(r.text)
print("saved")
