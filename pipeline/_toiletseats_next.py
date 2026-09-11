import re, json

with open("pipeline/_toiletseats.html", encoding="utf-8", errors="replace") as f:
    html = f.read()
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
data = json.loads(m.group(1))
with open("pipeline/_toiletseats_next.json", "w", encoding="utf-8") as out:
    json.dump(data, out)

def walk_find_pills(obj, out, path=""):
    if isinstance(obj, dict):
        for key in ("pillsV2", "pills", "categoryPills"):
            if key in obj and isinstance(obj[key], list):
                for p in obj[key]:
                    if isinstance(p, dict):
                        out.append({
                            "name": p.get("name") or p.get("title") or p.get("text"),
                            "link": p.get("link") or p.get("url") or p.get("seeMoreLink"),
                        })
        for k, v in obj.items():
            walk_find_pills(v, out, path + "." + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:200]):
            walk_find_pills(v, out, path + f"[{i}]")

out = []
walk_find_pills(data, out)
seen = set()
for p in out:
    key = (p["name"], p["link"])
    if key in seen:
        continue
    seen.add(key)
    print(p["name"], "|", p["link"])

# also try to find shelfName / breadCrumb
def find_key(obj, key, out):
    if isinstance(obj, dict):
        if key in obj:
            out.append(obj[key])
        for v in obj.values():
            find_key(v, key, out)
    elif isinstance(obj, list):
        for v in obj:
            find_key(v, key, out)

sn = []
find_key(data, "shelfName", sn)
print("shelfName candidates:", sn[:5])
