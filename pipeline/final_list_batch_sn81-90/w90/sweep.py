import sys
from curl_cffi import requests as creq

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.laredoute.co.uk/"
profiles = [
    "chrome124","chrome131","chrome120","chrome110","chrome99_android",
    "safari15_3","safari17_0","safari18_0","safari18_0_ios",
    "edge99","edge101","firefox133","firefox135",
]
for p in profiles:
    try:
        r = creq.get(url, impersonate=p, timeout=25)
        title = ""
        if "<title>" in r.text:
            title = r.text.split("<title>")[1].split("</title>")[0]
        print(f"{p:20s} status={r.status_code} len={len(r.text):7d} title={title[:60]!r}")
    except Exception as e:
        print(f"{p:20s} ERROR {e}")
