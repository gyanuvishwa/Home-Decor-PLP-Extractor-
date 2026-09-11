import gzip, sys, os, re
import urllib.request

SCRATCH = r"C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\c796539f-ebc8-4338-b591-e5d11e875246\scratchpad"

def gunzip_file(path):
    with gzip.open(path, 'rb') as f:
        return f.read()

if __name__ == "__main__":
    p = os.path.join(SCRATCH, "otto_catsitemap.gz")
    data = gunzip_file(p)
    out = os.path.join(SCRATCH, "otto_catsitemap.xml")
    with open(out, "wb") as f:
        f.write(data)
    print(len(data))
    print(data[:2000].decode("utf-8", errors="replace"))
