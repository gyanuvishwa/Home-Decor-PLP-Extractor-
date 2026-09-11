# BATCH 8 WORKER BRIEF — Home Decor Category & Qty Extraction

You are one of 3 parallel extraction workers. Read this whole brief before starting.

**Scratchpad (your working dir):**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\2e3e1cb2-8144-4c48-9f0b-ba12a8f9d211\scratchpad`

Do all file work there. Never touch the user's project files (the `.xlsm` / `.xlsx`
workbooks in `C:\Users\GyanendraVishwakarma\Web Research Agent`) — the orchestrator
merges. Writing to those files would corrupt validated batch 1–7 records.

---

## THE ONE RULE THAT MATTERS

**`qty` must be the EXACT number of products the website itself reports for that sub-category URL.**

- NEVER estimate, approximate, round, or infer a qty.
- NEVER copy a qty from a parent/sibling category.
- If you cannot verify the exact number, set `"qty": null` and
  `"flag": "MANUAL REVIEW: <specific reason>"`. A null is a *correct* answer.
  A made-up number is a project-destroying error.
- Every row must carry an `evidence` string: the literal text or JSON path that
  produced the number (e.g. `"Showing 1-24 of 186"`, or
  `"__NEXT_DATA__:props.pageProps.search.numFound=186"`).
  A row with a qty but no evidence is invalid and will be nulled at merge.

Accuracy beats coverage. Beats speed. Always.

---

## TOOLS

A shared harness is at `probe.py` in the scratchpad. Run from that directory:

```bash
python probe.py get <url> [outfile]     # fetch, save, show status/size/title
python probe.py nav <url>               # dump candidate category links
python probe.py count <url>             # hunt exact product count (text + embedded JSON)
python probe.py shopify <base> <handle> # EXACT count via /collections/<h>/products.json
python probe.py shopifycolls <base>     # all collections + products_count
python probe.py sitemap <base>          # sitemap index / robots sitemaps
python probe.py json <url>              # fetch + pretty-print JSON
python probe.py grep <file> <regex>     # regex a saved file with context
```

You may also `import probe` from your own throwaway Python scripts — that is usually
the fastest path (`from probe import fetch, fetch_json, page_count, shopify_count`).

Use the project venv python:
`"C:\Users\GyanendraVishwakarma\Web Research Agent\.venv - Copy\Scripts\python.exe"`

**`probe.py count` reports candidates, it does not decide.** You must look at the
evidence strings and pick the one that genuinely is the listing total. Ignore
counts that are obviously review counts, price values, item IDs, or nav badges.

Other tools: WebFetch (renders to markdown — good when raw HTML is JS-heavy),
WebSearch, Bash/PowerShell with curl. Write your own scripts freely.

### There is NO browser automation in this session
No Chrome/Playwright MCP tools exist. If a site needs a real browser (Cloudflare
"Just a moment...", Akamai/Imperva "Access Denied" / "Pardon Our Interruption"),
work the HTTP layer instead:

1. **Sitemaps** — often served even when HTML is blocked. Gives category URLs.
2. **Internal JSON/search APIs** — the richest source of exact totals. Find them by
   grepping saved HTML/JS for `/api/`, `algolia`, `searchspring`, `bloomreach`,
   `constructor.io`, `graphql`, `_next/data`, `?format=json`, `.json?`.
   Algolia/Searchspring responses expose `nbHits` / `totalResults` = exact totals.
3. **Shopify** — `/collections.json`, `/collections/<h>/products.json?limit=250&page=N`,
   and `/collections/<h>?view=...`. `products_count` from `/collections.json` is exact.
4. **Alternate hosts/locales** — e.g. `m.` mobile site, a different country domain
   running the same catalogue, or the brand's global site with a region selector.
   Use the locale that matches the assigned Country.
5. **Retry with backoff** — 429/timeouts are often transient. Try 2–3 times, spaced.

If after genuine effort the site cannot be read, mark the company
`"status": "failed"` with a precise `failure_reason`. Do not fabricate rows.
Partial success is fine and valuable: `"status": "partial"`.

---

## WHAT TO EXTRACT

Only **real Home Decor product categories/sub-categories** — pages that list products.

### INCLUDE
- **Glassware (ALL)**: wine/champagne/whiskey/beer/cocktail glasses, tumblers, tea &
  coffee cups, mugs, serving glassware, glass bowls/plates/pitchers/bottles/jars/
  containers, decorative glassware.
- **Tableware / dinnerware**: plates, bowls, dinner sets, serveware, trays, cutlery-
  adjacent tabletop decor (the earlier batches file these under `Kitchen & Dining`).
- **Lighting**: pendant, wall, ceiling, floor lamps, table lamps, lanterns, chandeliers.
- **Decorative Accessories**: decorative bowls/trays/plates, mirrors, wall art, wall
  decor, vases, sculptures, figurines, decorative lanterns, candle holders, candles,
  home fragrance/diffusers, artificial plants, decorative planters/pots.
- **Decorative material lines**: wooden (decorative only), ceramic, resin, marble,
  stone, terracotta, bamboo, cane, rattan.

### EXCLUDE (never extract)
Bathroom · Furniture (beds, tables incl. dining/coffee, chairs, cabinets, wardrobes)
· Storage · Kitchen appliances · Cookware/pans · Hardware · Plumbing · Construction ·
Home improvement · Office furniture · Outdoor furniture · Steel/iron/aluminium/copper
products · Industrial · Utility · Food & drink consumables · Cleaning products ·
Personal care · Garden tools/seeds · Textiles (rugs, cushions, curtains, bedding,
tea towels) unless the site files them under a decor sub-category you were told to
include — when unsure, exclude.

### NEVER EXTRACT (navigation/marketing, not product categories)
Collections · Featured Collections · Shop All · View All · Browse All · Explore All ·
Discover · Blogs · Editorial · Gift Guides · Lookbooks · Landing pages · Sale · Offers ·
Clearance · New Arrivals · Best Sellers · Navigation pages ·
**Clocks of every kind** (wall/desk/alarm/clock collections).

Brand-name/designer listing pages are not categories. Price/colour filter pages are
not categories.

---

## QTY METHOD (in priority order)

1. **Displayed total** — "Showing 1–24 of 186", "186 products", "186 résultats",
   "186 producten". Use the exact number. This is the best source.
2. **Structured data** — embedded JSON (`__NEXT_DATA__`, `__NUXT__`, `window.__INITIAL_STATE__`),
   internal API/GraphQL responses, Algolia `nbHits`, Shopify `products_count`.
   Record the JSON path in `evidence`.
3. **Full enumeration** — page through the complete listing (or paginate a products.json)
   and count unique product IDs. Only valid if you truly reach the end. Record how.

**Sanity checks before you accept a qty:**
- Does the number move when you change the category? (A constant number across
  different categories means you grabbed a site-wide total — reject it.)
- Is it suspiciously round (1000, 5000, 10000)? Many sites cap displayed counts.
  If it's a cap, that is NOT exact → `null` + flag.
- Does "of N" N exceed what pagination implies? Cross-check page count × page size.
- A parent category total is not a sub-category total.
- Beware counts that include out-of-stock or variant rows if the site says so.

Deduplicate: if two sub-category names resolve to the same URL, keep one.

---

## LANGUAGE / NAMING CONVENTION

Batches 1–7 set the precedent, follow it exactly:

- **French and Dutch sites → English sub-category names.** Batch 4's
  `Galeries Lafayette Maison` (a French site) used pure English:
  `Indoor Table Lamps`, `Chandeliers & Pendant Lights`, `Dinner Plates`, `Soup &
  Pasta Plates`. Do the same. Do NOT keep the French/Dutch original in parentheses.
  (Native + `(English)` was used only for Japanese sites.)
- `category` should be the normalised English bucket the earlier batches use, in
  order of preference: `Lighting`, `Kitchen & Dining`, `Home Accessories`,
  `Home Decor`, `Home Fragrance`, `Wall Decor & Mirrors`, `Garden`.
  Use `Lighting` / `Kitchen & Dining` / `Home Accessories` whenever they fit — those
  three cover the large majority of existing rows.
- Keep sub-category wording faithful to the site's own naming (translated), not invented.

---

## OUTPUT CONTRACT

Write **one JSON file per company**, named `c<SR>.json`, into the scratchpad,
**immediately after finishing that company** (this is the save-after-every-company
requirement — do not batch them to the end). You have one company each, so write it
as soon as it is done; if you finish partially and then hit a wall, still write the
file with `"status": "partial"`.

```json
{
  "sr": 36,
  "company": "Made In Design",
  "brand_site": "madeindesign.com",
  "country": "France",
  "site_url": "https://www.madeindesign.com/",
  "status": "ok",
  "failure_reason": null,
  "notes": "Counts from the listing header 'N produits'.",
  "rows": [
    {
      "category": "Lighting",
      "sub_category": "Pendant Lights",
      "qty": 1240,
      "link": "https://www.madeindesign.com/cat-suspensions.html",
      "evidence": "listing header text '1240 produits'",
      "flag": null
    }
  ]
}
```

Field rules:
- `sr`, `company`, `brand_site`, `country`: copy EXACTLY from your assignment below.
- `status`: `"ok"` | `"partial"` | `"failed"`
- `category`: normalised English bucket (see naming convention above).
- `sub_category`: the site's own sub-category name, in English.
- `qty`: integer, or `null` when unverified. Never a string.
- `link`: the absolute, working sub-category URL (the locale URL you actually verified).
- `evidence`: required whenever `qty` is not null.
- `flag`: `null`, or `"MANUAL REVIEW: <reason>"`.
- Failed company: `"rows": []` and a precise `failure_reason`.

Validate your JSON parses before finishing:
`python -c "import json;d=json.load(open('c36.json',encoding='utf-8'));print(len(d['rows']))"`

---

## WORKFLOW

1. Open the site; find the real region/locale URL (follow redirects).
2. Find the category tree — mega-menu, sitemap, or nav API. `probe.py nav` helps.
3. Select only the qualifying decor categories/sub-categories per the rules above.
4. For each sub-category: open it, establish the exact total, capture the URL.
5. Verify the qty (sanity checks above), then record the row.
6. Write `c<SR>.json`.

Aim for genuine coverage of the decor tree — typically 10–40 sub-category rows for a
large retailer, fewer for a boutique. Depth matters, but never invent rows to pad.

## FINAL MESSAGE

End with a compact summary: SR, name, status, row count, how many qty are
null/flagged, and any failure reason. No prose padding.
