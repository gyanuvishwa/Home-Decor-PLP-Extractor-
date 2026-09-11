import json, io, os, re, sys, glob, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = (r"C:\Users\GYANEN~1\AppData\Local\Temp\claude"
     r"\C--Users-GyanendraVishwakarma-Web-Research-Agent"
     r"\be91bad7-b37a-4694-bdbe-c47fea1bb5d9\scratchpad")

# Flag leaf rows that the merge would silently drop: same (category, sub_category)
# key within one company, but a DIFFERENT link (i.e. genuinely distinct listings).
for p in sorted(glob.glob(os.path.join(S, "c*.json")),
                key=lambda x: int(re.findall(r"\d+", os.path.basename(x))[0])):
    b = os.path.basename(p)
    if not re.match(r"^c\d+\.json$", b):
        continue
    try:
        d = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    keys = collections.defaultdict(list)
    for r in d.get("rows") or []:
        if r.get("parent"):
            continue
        k = ((r.get("category") or "").strip().lower(),
             (r.get("sub_category") or "").strip().lower())
        keys[k].append((r.get("link"), r.get("qty")))
    for k, v in keys.items():
        if len(v) > 1 and len({x[0] for x in v}) > 1:
            print(f"SR {d.get('sr')} {d.get('company')}: COLLIDING KEY {k}")
            for link, qty in v:
                print(f"    qty={qty}  {link}")
