import json, io, os, re, sys, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PIPE = r"C:\Users\GyanendraVishwakarma\Web Research Agent\pipeline"
S = (r"C:\Users\GYANEN~1\AppData\Local\Temp\claude"
     r"\C--Users-GyanendraVishwakarma-Web-Research-Agent"
     r"\be91bad7-b37a-4694-bdbe-c47fea1bb5d9\scratchpad")

DIRS = [os.path.join(PIPE, d) for d in
        ("final_list_batch_sn1-10", "final_list_batch_sn11-20",
         "final_list_batch_sn21-30", "final_list_batch_sn31-40")] + [S]

# Room/product words whose EXCLUSION is now wrong under Rule 0.
HIT = re.compile(
    r'(bath\s?(room)?\s*(light|vanit|mirror)|vanity\s*(light|mirror)|'
    r'lighting\s*by\s*room|light(ing|s)?\s*by\s*room|'
    r'outdoor\s*(light|lantern|mirror)|landscape\s*light|'
    r'bedroom\s*(light|mirror|decor)|kitchen\s*(island\s*)?light|'
    r'dining\s*room\s*light|living\s*room\s*light|entryway|hallway\s*light|'
    r'recessed|track\s*light|under-?cabinet|cabinet\s*light|'
    r'makeup\s*mirror|dressing\s*mirror|medicine\s*cabinet)', re.I)

seen = {}
for d in DIRS:
    for p in sorted(glob.glob(os.path.join(d, "c*.json"))):
        b = os.path.basename(p)
        if not re.match(r"^c\d+\.json$", b):
            continue
        sr = int(re.findall(r"\d+", b)[0])
        if sr in seen or sr > 60:
            continue
        try:
            data = json.load(io.open(p, encoding="utf-8"))
        except Exception:
            continue
        seen[sr] = data

print("company files scanned:", len(seen))
print()
affected = []
for sr in sorted(seen):
    d = seen[sr]
    notes = str(d.get("notes") or "")
    # sentences in notes that mention an excluded room/lighting concept
    frags = [s.strip() for s in re.split(r'(?<=[.;])\s+', notes) if HIT.search(s)]
    # rows already present that ARE room-based (i.e. worker included them)
    kept = [r.get("sub_category") for r in d.get("rows") or []
            if HIT.search(str(r.get("sub_category") or ""))]
    if frags or kept:
        affected.append(sr)
        print(f"=== SR {sr}  {d.get('company')} ===")
        if kept:
            print("   ALREADY KEPT :", ", ".join(sorted(set(kept))[:8]))
        for f in frags[:4]:
            print("   NOTE:", f[:240])
        print()
print("companies with room/lighting signal:", affected)
