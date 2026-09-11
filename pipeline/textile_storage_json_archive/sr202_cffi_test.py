from curl_cffi import requests
r = requests.get("https://www.birchlane.com/bedding/sb0/comforters-sets-c1874122.html", impersonate="chrome124", timeout=20)
print(r.status_code)
print(r.text[:500])
