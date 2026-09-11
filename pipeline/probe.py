#!/usr/bin/env python3
"""Shared extraction harness for Batch 7 Home Decor category/qty extraction.

Usage:
  python probe.py get <url> [outfile]        # fetch + save, print status/size/title
  python probe.py nav <url>                  # dump nav/menu candidate category links
  python probe.py count <url>                # try hard to find EXACT product count on a listing page
  python probe.py shopify <base> <handle>    # exact count via /collections/<handle>/products.json
  python probe.py shopifycolls <base>        # list all collections + product counts (sitemap/json)
  python probe.py sitemap <base>             # dump sitemap index
  python probe.py json <url>                 # fetch and pretty-print JSON
  python probe.py grep <file> <regex>        # regex search a saved file

Design notes:
  - NEVER guesses a quantity. Every count function returns the *evidence* string it
    matched, so the caller can verify. If nothing is found it returns None.
"""
import sys, os, re, json, gzip, io, time, random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlencode, parse_qs, urlsplit

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    # Do NOT advertise "br": this venv has no brotli/brotlicffi decoder, so any origin
    # that honours it returns a body requests cannot decompress — you get binary
    # garbage that reads like a broken or blocked page. (Found on dwr.com.)
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def fetch(url, timeout=45, tries=3, headers=None, method="GET", data=None, allow_redirects=True):
    """Fetch with retry/backoff. Returns (status, text, final_url) or (None, err, url)."""
    last = None
    h = dict(HEADERS)
    if headers:
        h.update(headers)
    for i in range(tries):
        try:
            r = SESSION.request(method, url, timeout=timeout, headers=h,
                                data=data, allow_redirects=allow_redirects)
            return r.status_code, r.text, r.url
        except Exception as e:
            last = str(e)
            time.sleep(1.5 * (i + 1) + random.random())
    return None, f"ERROR: {last}", url


def fetch_json(url, timeout=45, tries=3, headers=None, method="GET", data=None):
    h = {"Accept": "application/json, text/plain, */*"}
    if headers:
        h.update(headers)
    st, txt, fu = fetch(url, timeout=timeout, tries=tries, headers=h, method=method, data=data)
    if st != 200:
        return st, None, txt[:400]
    try:
        return st, json.loads(txt), None
    except Exception as e:
        return st, None, f"not json: {e}: {txt[:300]}"


# --------------------------------------------------------------------------
# EXACT COUNT DETECTION
# --------------------------------------------------------------------------
# Ordered patterns. Each returns (count, evidence). Multilingual: EN/FR/DE/AR/JA.
# Digit run allowing comma/period/space/NBSP/narrow-NBSP as thousands separators —
# French/Nordic/some German sites render counts like "8 682" using U+202F or U+00A0,
# which a bare [\d,]+ class silently truncates to "682" (caught on S.N. 143 Castorama
# France, where it undercounted "8 682 produits" as 682). Must start/end on a digit so
# it doesn't swallow surrounding words via the bare space alternative.
_NUM = r'(?:\d[\d,.   ]*\d|\d)'

COUNT_PATTERNS = [
    # "Showing 1-24 of 186 products" / "1 - 24 of 186 results"
    (r'(?:showing|show|displaying)?\s*\d[\d,]*\s*[-–—to]+\s*\d[\d,]*\s*(?:of|from|out of)\s*(' + _NUM + r')', 'range-of'),
    # "186 products" / "186 items" / "186 results" / "186 Produkte" / "186 produits"
    (r'\b(' + _NUM + r')\s*(?:products?|items?|results?|styles?|produkte?|produits?|artikel|productos|prodotti|producten|商品|件|منتج|منتجات)\b', 'n-products'),
    # "Products: 186" / "Results: 186"
    (r'(?:products?|items?|results?|total)\s*[:：]\s*(' + _NUM + r')', 'label-n'),
    # "(186)"  -- only used as a weak fallback, caller must confirm
    (r'\(\s*(' + _NUM + r')\s*\)', 'paren'),
]

# JSON keys that commonly hold an exact total
JSON_COUNT_KEYS = [
    "total", "totalCount", "total_count", "totalResults", "total_results",
    "totalProducts", "total_products", "totalHits", "nbHits", "numFound",
    "resultCount", "result_count", "count", "productCount", "product_count",
    "totalItems", "total_items", "recordsFiltered", "totalRecords", "totalSize",
    "collection_product_count", "products_count", "itemCount", "hitCount",
]


def _clean_int(s):
    try:
        t = str(s)
        for sep in (",", ".", " ", " ", " "):
            t = t.replace(sep, "")
        return int(t)
    except Exception:
        return None


def counts_from_text(text, weak=False):
    """Return list of (count, evidence, pattern_name) found in visible text."""
    out = []
    for pat, name in COUNT_PATTERNS:
        if name == 'paren' and not weak:
            continue
        for m in re.finditer(pat, text, re.I):
            n = _clean_int(m.group(1))
            if n is None or n <= 0 or n > 5_000_000:
                continue
            s = max(0, m.start() - 60)
            ev = re.sub(r'\s+', ' ', text[s:m.end() + 40]).strip()
            out.append((n, ev, name))
    return out


def walk_json_for_counts(obj, path="", out=None, depth=0):
    """Recursively find plausible total-count keys in a JSON blob."""
    if out is None:
        out = []
    if depth > 12:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if k in JSON_COUNT_KEYS and isinstance(v, (int, float, str)):
                n = _clean_int(v)
                if n is not None and 0 < n <= 5_000_000:
                    out.append((n, p))
            walk_json_for_counts(v, p, out, depth + 1)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:60]):
            walk_json_for_counts(v, f"{path}[{i}]", out, depth + 1)
    return out


def embedded_json_blobs(html):
    """Yield (label, parsed_json) for __NEXT_DATA__, __NUXT__, ld+json, dataLayer etc."""
    soup = BeautifulSoup(html, "lxml")
    for sc in soup.find_all("script"):
        sid = sc.get("id") or ""
        stype = sc.get("type") or ""
        raw = sc.string or sc.get_text() or ""
        if not raw.strip():
            continue
        if sid in ("__NEXT_DATA__", "__NUXT_DATA__") or "json" in stype.lower():
            try:
                yield (sid or stype, json.loads(raw))
            except Exception:
                pass
        else:
            for pat in (r'window\.__NUXT__\s*=\s*(\{.*?\});?\s*$',
                        r'window\.__INITIAL_STATE__\s*=\s*(\{.*\});',
                        r'window\.__PRELOADED_STATE__\s*=\s*(\{.*\});',
                        r'window\.dataLayer\s*=\s*(\[.*?\]);'):
                m = re.search(pat, raw, re.S | re.M)
                if m:
                    try:
                        yield ("inline", json.loads(m.group(1)))
                    except Exception:
                        pass


def page_count(url, verbose=True):
    """Best-effort EXACT count for a listing URL. Returns dict of evidence (never guesses)."""
    st, html, fu = fetch(url)
    res = {"url": url, "final_url": fu, "status": st,
           "text_counts": [], "json_counts": [], "shopify": None}
    if st != 200 or not html:
        res["error"] = html[:300] if html else "no body"
        return res

    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    vis = re.sub(r'\s+', ' ', soup.get_text(" "))
    res["text_counts"] = counts_from_text(vis)[:14]
    res["title"] = (soup.title.get_text(strip=True) if soup.title else "")[:120]

    for label, blob in embedded_json_blobs(html):
        for n, p in walk_json_for_counts(blob)[:40]:
            res["json_counts"].append({"n": n, "path": f"{label}:{p}"})
    res["json_counts"] = res["json_counts"][:40]

    # Shopify collection hint
    m = re.search(r'collection_product_count["\']?\s*[:=]\s*["\']?(\d+)', html)
    if m:
        res["shopify"] = int(m.group(1))
    return res


# --------------------------------------------------------------------------
# SHOPIFY
# --------------------------------------------------------------------------
def shopify_count(base, handle, hard_cap=8000):
    """EXACT count by paging /collections/<handle>/products.json (250/page)."""
    base = base.rstrip("/")
    total, page, seen = 0, 1, set()
    while total < hard_cap:
        u = f"{base}/collections/{handle}/products.json?limit=250&page={page}"
        st, data, err = fetch_json(u)
        if st != 200 or not isinstance(data, dict):
            return None, f"http {st} {err}"
        prods = data.get("products", [])
        if not prods:
            break
        for p in prods:
            seen.add(p.get("id"))
        total = len(seen)
        if len(prods) < 250:
            break
        page += 1
        if page > 60:
            break
        time.sleep(0.3)
    return total, f"{base}/collections/{handle}/products.json paged x{page}"


def shopify_collections(base):
    """List collections via /collections.json (paged)."""
    base = base.rstrip("/")
    out, page = [], 1
    while page <= 20:
        st, data, err = fetch_json(f"{base}/collections.json?limit=250&page={page}")
        if st != 200 or not isinstance(data, dict):
            break
        cs = data.get("collections", [])
        if not cs:
            break
        for c in cs:
            out.append({"handle": c.get("handle"), "title": c.get("title"),
                        "count": c.get("products_count")})
        if len(cs) < 250:
            break
        page += 1
    return out


# --------------------------------------------------------------------------
# NAV DISCOVERY
# --------------------------------------------------------------------------
NAV_NOISE = re.compile(
    r'(login|sign\s?in|account|cart|basket|wishlist|checkout|store\s?locator|contact|'
    r'about|career|blog|press|faq|help|terms|privacy|policy|return|shipping|delivery|'
    r'track|gift\s?card|newsletter|app|download|facebook|instagram|twitter|tiktok|'
    r'youtube|pinterest|linkedin|whatsapp)', re.I)


def nav_links(url, limit=400):
    st, html, fu = fetch(url)
    if st != 200:
        return {"status": st, "error": (html or "")[:300]}
    soup = BeautifulSoup(html, "lxml")
    seen, out = set(), []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        txt = re.sub(r'\s+', ' ', a.get_text(" ")).strip()
        if not txt or len(txt) > 70:
            continue
        if NAV_NOISE.search(txt):
            continue
        full = urljoin(fu, href)
        key = (txt.lower(), full)
        if key in seen:
            continue
        seen.add(key)
        out.append({"text": txt, "href": full})
        if len(out) >= limit:
            break
    return {"status": st, "final_url": fu, "count": len(out), "links": out}


def sitemap(base):
    base = base.rstrip("/")
    out = []
    for cand in ("/sitemap.xml", "/sitemap_index.xml", "/robots.txt"):
        st, txt, fu = fetch(base + cand)
        if st == 200:
            if cand == "/robots.txt":
                out.append({"url": fu, "sitemaps": re.findall(r'(?i)sitemap:\s*(\S+)', txt)})
            else:
                out.append({"url": fu, "locs": re.findall(r'<loc>\s*([^<]+?)\s*</loc>', txt)[:400]})
    return out


# --------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "get":
        url = sys.argv[2]
        st, txt, fu = fetch(url)
        print(f"HTTP {st}  size={len(txt or '')}  final={fu}")
        if len(sys.argv) > 3:
            with io.open(sys.argv[3], "w", encoding="utf-8", errors="replace") as f:
                f.write(txt or "")
            print("saved ->", sys.argv[3])
        else:
            soup = BeautifulSoup(txt or "", "lxml")
            print("title:", soup.title.get_text(strip=True) if soup.title else "")
    elif cmd == "nav":
        print(json.dumps(nav_links(sys.argv[2]), indent=1, ensure_ascii=False))
    elif cmd == "count":
        print(json.dumps(page_count(sys.argv[2]), indent=1, ensure_ascii=False))
    elif cmd == "shopify":
        n, ev = shopify_count(sys.argv[2], sys.argv[3])
        print(json.dumps({"count": n, "evidence": ev}, indent=1))
    elif cmd == "shopifycolls":
        print(json.dumps(shopify_collections(sys.argv[2]), indent=1, ensure_ascii=False))
    elif cmd == "sitemap":
        print(json.dumps(sitemap(sys.argv[2]), indent=1, ensure_ascii=False))
    elif cmd == "json":
        st, d, err = fetch_json(sys.argv[2])
        print(json.dumps(d, indent=1, ensure_ascii=False)[:12000] if d else f"{st} {err}")
    elif cmd == "grep":
        with io.open(sys.argv[2], encoding="utf-8", errors="replace") as f:
            t = f.read()
        for m in re.finditer(sys.argv[3], t, re.I):
            s = max(0, m.start() - 80)
            print(re.sub(r'\s+', ' ', t[s:m.end() + 80]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
