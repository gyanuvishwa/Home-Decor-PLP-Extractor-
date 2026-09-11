import re, sys, time
from curl_cffi import requests

urls = sys.argv[1:]
for path in urls:
    url = f"https://www.crateandbarrel.com{path}"
    r = None
    for attempt in range(3):
        try:
            r = requests.get(url, impersonate='chrome124', timeout=45)
            break
        except Exception as e:
            last_err = e
            time.sleep(3)
    if r is None:
        print(f"{path}\tERROR {last_err}")
        time.sleep(2)
        continue
    time.sleep(1.5)
    text = r.text
    fname = 'cb_' + re.sub(r'[^a-zA-Z0-9]+', '_', path).strip('_') + '.html'
    open(fname, 'w', encoding='utf-8').write(text)
    m = re.search(r'"title":"([^"]*)","totalCount":(\d+)', text)
    if m:
        print(f"{path}\t{r.status_code}\ttitle={m.group(1)}\ttotalCount={m.group(2)}\tfile={fname}")
    else:
        m2 = re.search(r'"totalCount":(\d+)', text)
        print(f"{path}\t{r.status_code}\tNO_TITLE_MATCH\ttotalCount={m2.group(1) if m2 else 'NONE'}\tfile={fname}")
