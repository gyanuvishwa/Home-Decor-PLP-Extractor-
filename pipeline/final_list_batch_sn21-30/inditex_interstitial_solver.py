import re, json, time
from curl_cffi import requests as r

BASE = "https://www.zarahome.com"

class ZH:
    def __init__(self):
        self.s = r.Session(impersonate="chrome")
        self.s.headers.update({
            "Accept-Language": "en-AE,en;q=0.9",
        })

    def _solve(self, html, url):
        # extract pow ingredients
        m = re.search(r'var i = (\d+);\s*var j = i \+ Number\("(\d+)"\s*\+\s*"(\d+)"\)', html)
        if not m:
            return False
        i = int(m.group(1))
        j = i + int(m.group(2) + m.group(3))
        bm = re.search(r'"bm-verify":\s*"([^"]+)"', html)
        if not bm:
            return False
        payload = {"bm-verify": bm.group(1), "pow": j}
        resp = self.s.post(BASE + "/_sec/verify?provider=interstitial",
                           json=payload,
                           headers={"Content-Type": "application/json", "Referer": url},
                           timeout=60)
        return resp.status_code == 200

    def get(self, url, tries=4, **kw):
        for n in range(tries):
            resp = self.s.get(url, timeout=90, **kw)
            t = resp.text if resp.headers.get("content-type","").startswith(("text","application/json","application/xml")) or len(resp.content) < 3_000_000 else ""
            if "bm-verify" in t and "interstitial" in t:
                self._solve(t, url)
                time.sleep(1.0)
                continue
            return resp
        return resp


if __name__ == "__main__":
    z = ZH()
    resp = z.get("https://www.zarahome.com/ae/candle-holders-n1003")
    print(resp.status_code, len(resp.text))
    open("cat_test.html", "w", encoding="utf-8").write(resp.text)
