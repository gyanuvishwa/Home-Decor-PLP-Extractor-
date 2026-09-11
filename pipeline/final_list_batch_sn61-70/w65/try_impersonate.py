import sys
from curl_cffi import requests as creq

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.rejuvenation.com/"
profiles = ["chrome124","chrome131","chrome120","chrome110","chrome99","safari17_0",
            "safari18_0","safari18_0_ios","safari15_5","safari15_3","edge101","edge99",
            "firefox133","firefox135"]
for p in profiles:
    try:
        r = creq.get(url, impersonate=p, timeout=25)
        print(p, r.status_code, len(r.text))
        if r.status_code == 200:
            with open(f"ok_{p}.html", "w", encoding="utf-8", errors="replace") as f:
                f.write(r.text)
    except Exception as e:
        print(p, "ERR", str(e)[:150])
