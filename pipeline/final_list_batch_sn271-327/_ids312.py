import sys, json
sys.path.insert(0, r"C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\1294ee4d-a82f-4c1e-875d-2530fa2ecfd7\scratchpad")
import probe

base = "https://www.orangetree.in"

def ids(handle):
    b = base.rstrip("/")
    out = set()
    page = 1
    while True:
        u = f"{b}/collections/{handle}/products.json?limit=250&page={page}"
        st, data, err = probe.fetch_json(u)
        if st != 200 or not isinstance(data, dict):
            break
        prods = data.get("products", [])
        if not prods:
            break
        for p in prods:
            out.add(p.get("id"))
        if len(prods) < 250:
            break
        page += 1
        if page > 20:
            break
    return out

handles = ["hanging-lamps","pendant-lamp","cluster-hanging-lamps","lanterns",
           "mirrors","wall-mirror","floor-mirror",
           "wall-accents","wall-decor",
           "tealight-holders","candle-holder",
           "bowl","table-decor","tea-coaster-set","platter","serveware",
           "bookend","table-styling","candle-holder2" ]
handles = list(dict.fromkeys(handles))
data = {}
for h in handles:
    if h == "candle-holder2":
        continue
    s = ids(h)
    data[h] = s
    print(h, len(s))

def rel(a, b):
    A, B = data[a], data[b]
    print(f"{a} ({len(A)}) vs {b} ({len(B)}): A-B={len(A-B)} B-A={len(B-A)} intersect={len(A&B)}")

print("---")
rel("hanging-lamps","pendant-lamp")
rel("hanging-lamps","cluster-hanging-lamps")
rel("hanging-lamps","lanterns")
combo = data["pendant-lamp"] | data["cluster-hanging-lamps"] | data["lanterns"]
print("hanging-lamps - (pendant+cluster+lanterns) =", len(data["hanging-lamps"] - combo))
print("(pendant+cluster+lanterns) - hanging-lamps =", len(combo - data["hanging-lamps"]))

print("---mirrors---")
rel("mirrors","wall-mirror")
rel("mirrors","floor-mirror")
combo2 = data["wall-mirror"] | data["floor-mirror"]
print("mirrors - (wall+floor) =", len(data["mirrors"] - combo2))
print("(wall+floor) - mirrors =", len(combo2 - data["mirrors"]))

print("---wall-accents vs wall-decor---")
rel("wall-accents","wall-decor")

print("---tealight vs candle-holder---")
rel("tealight-holders","candle-holder")

print("---bowl vs table-decor---")
rel("bowl","table-decor")

with open("ids312.json","w",encoding="utf-8") as f:
    json.dump({k: sorted(v) for k,v in data.items()}, f, indent=1)
