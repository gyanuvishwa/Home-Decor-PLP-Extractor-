from curl_cffi import requests
r = requests.get('https://www.allmodern.com/storage/cat/storage-c1875304.html', impersonate='chrome120', timeout=30)
print(r.status_code)
print(len(r.text))
with open('sr201_storage_top.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
print("saved")
