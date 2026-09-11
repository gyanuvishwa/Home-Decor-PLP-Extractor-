import sys, json, time
sys.path.insert(0, r"C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\1294ee4d-a82f-4c1e-875d-2530fa2ecfd7\scratchpad")
import probe

base = "https://www.orangetree.in"
handles = [
 "wall-lamps","floor-lamps","table-lamps","study-table-lamps","lanterns",
 "hanging-lamps","pendant-lamp","cluster-hanging-lamps","chandelier",
 "table-styling","bookend","candle-holder","table-decor","vases",
 "serveware","tea-coaster-set","platter","wall-decor","wall-mirror",
 "floor-mirror","mirrors","tray","wall-accents","tealight-holders","bowl",
]

results = {}
for h in handles:
    try:
        cnt, ev = probe.shopify_count(base, h)
    except Exception as e:
        cnt, ev = None, str(e)
    results[h] = {"count": cnt, "evidence": ev}
    print(h, cnt)

with open("counts312.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=1)
