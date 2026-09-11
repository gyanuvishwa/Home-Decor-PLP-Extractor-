from sr202_fetch_lib import fetch
import sys
r = fetch(sys.argv[1])
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write(r.text)
print(r.status_code, len(r.text))
