import re, sys

fname = sys.argv[1]
html = open(fname, encoding='utf-8').read()

h1 = re.search(r'class="plp-header"[^>]*>([^<]*)<', html)
item_count = re.search(r'class="item-count"[^>]*>\s*(?:<!-- -->)?(\d+)(?:<!-- -->)?\s*Items', html)
canon = re.search(r'<link rel="canonical" href="([^"]*)"', html)
title = re.search(r'<title[^>]*>([^<]*)</title>', html)
breadcrumb = re.search(r'"@type":"BreadcrumbList","itemListElement":(\[[^\]]*\])', html)
noresults = re.search(r'(?i)no results|nothing found|no products found', html)

print("H1:", h1.group(1) if h1 else None)
print("ItemCount:", item_count.group(1) if item_count else None)
print("Canonical:", canon.group(1) if canon else None)
print("Title:", title.group(1) if title else None)
print("Breadcrumb:", breadcrumb.group(1) if breadcrumb else None)
print("NoResultsText:", bool(noresults))
