import json, glob, io, re, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
d0 = sys.argv[1] if len(sys.argv) > 1 else "."
files = sorted(glob.glob(os.path.join(d0, "c*.json")),
               key=lambda x: int(re.findall(r"\d+", os.path.basename(x))[0]))
for f in files:
    d = json.load(io.open(f, encoding="utf-8"))
    leaf = [r for r in d["rows"] if not r.get("parent")]
    nn = sum(1 for r in leaf if r.get("qty") is None)
    print("%3s %-22s %-8s leaf=%-4s null=%-3s | %s" % (
        d.get("sr"), str(d.get("company"))[:22], d.get("status"),
        len(leaf), nn, str(d.get("notes"))[:200]))
