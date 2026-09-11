# WORKER BRIEF — Home Decor Category & Qty Extraction (Final_Company_List batch, S.N. 1–10)

You are one of 10 parallel extraction workers. Read this whole brief before starting.

**Scratchpad (your working dir):**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\a88ab55b-d1ce-49c5-aa01-254454cb0d8c\scratchpad`

Do all file work there. **Never touch the user's project files** (the `.xlsm` / `.xlsx`
workbooks in `C:\Users\GyanendraVishwakarma\Web Research Agent`) — the orchestrator
merges. Writing to those files would corrupt validated records.

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

## CRITICAL ENVIRONMENT FACT — IPv4 EGRESS IS DEAD ON THIS MACHINE

Hosts that resolve **A-only (no AAAA)** are simply **unreachable**: TCP times out at
SYN, no TLS handshake. The symptom is indistinguishable from a bot block, and past
workers wrongly wrote off three companies as "Cloudflare is blocking us".

**Before you conclude anything about bot protection, run:**
```
nslookup -type=AAAA <domain>
```
No AAAA record → the site is unreachable directly, it is NOT blocking you.

**The workaround that works** — Google's translate proxy host is IPv6-reachable and
returns the origin's genuine server-rendered HTML, including full Next.js RSC payloads:

```
https://www-<domain-with-dashes>-com.translate.goog/<path>?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=en
```

e.g. `https://www-wayfair-com.translate.goog/lighting/cat/...?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=en`

**Known affected in this batch: wayfair.com** (and the whole Wayfair family). Others
may be too — check AAAA first for any site that "silently drops TCP".

Traps:
- `<host>.translate.goog/robots.txt` returns translate.goog's *own* robots, not the
  origin's. It looks like the proxy works when it doesn't. Test a real content path.
- Some origins refuse Google's fetcher outright (HTTP 400 "Can't translate this page").
- **Keep canonical origin URLs in your output `link` field. NEVER write a
  translate.goog URL as `link`.**

Other fallbacks that have worked: `r.jina.ai/<url>` reader proxy, and plain `curl`
where python `requests` got 429.

---

## SHOPIFY: `products_count` IS UNRELIABLE — DO NOT USE IT

`/collections.json` → `products_count` was **wrong on 6 of 6** Shopify stores tested,
always **inflated** (it counts products not published to the Online Store channel,
plus stale legacy collections). Divergences seen: 2937 vs 1466; 79 vs 23; 282 vs 136.

Use instead, in this order:
1. The storefront's **rendered listing header** ("N items" / "N products").
2. The site's **own search layer** — Searchspring `pagination.totalResults`,
   Algolia `nbHits` (on Algolia pass `distinct=true`; the index holds one record per
   *variant* and will over-count otherwise).
3. **Full enumeration** of `/collections/<handle>/products.json?limit=250` paged to
   exhaustion, counting unique product IDs.

Cheap proofs of which number is right:
- children must sum to the parent
- `ceil(total / pageSize)` must equal the page's own rendered `data-total-pages`
- the grid endpoint returns tiles at `start=N-1` and **zero** at `start=N`

---

## TOOLS

A shared harness `probe.py` is in the scratchpad. Run from that directory:

```bash
python probe.py get <url> [outfile]     # fetch, save, show status/size/title
python probe.py nav <url>               # dump candidate category links
python probe.py count <url>             # hunt exact product count (text + embedded JSON)
python probe.py shopify <base> <handle> # count via /collections/<h>/products.json
python probe.py shopifycolls <base>     # all collections + products_count
python probe.py sitemap <base>          # sitemap index / robots sitemaps
python probe.py json <url>              # fetch + pretty-print JSON
python probe.py grep <file> <regex>     # regex a saved file with context
```

You may also `import probe` from your own throwaway scripts — usually the fastest path
(`from probe import fetch, fetch_json, page_count, shopify_count`).

Use the project venv python:
`"C:\Users\GyanendraVishwakarma\Web Research Agent\.venv - Copy\Scripts\python.exe"`

`probe.py count` **reports candidates, it does not decide.** You must read the evidence
strings and pick the one that genuinely is the listing total. Ignore review counts,
prices, item IDs, nav badges.

Also available: WebFetch (renders to markdown — good when raw HTML is JS-heavy),
WebSearch, Bash/PowerShell with curl.

### DO NOT USE BROWSER AUTOMATION
Chrome MCP tools may appear available, but 10 workers share **one** browser instance and
will fight over tabs. Stay on the HTTP layer. If a site truly needs a real browser,
mark it `partial`/`failed` with that as the reason and let the orchestrator decide.

When HTML is blocked, work the HTTP layer:
1. **Sitemaps** — often served even when HTML is blocked. Gives category URLs.
2. **Internal JSON/search APIs** — richest source of exact totals. Grep saved HTML/JS
   for `/api/`, `algolia`, `searchspring`, `bloomreach`, `constructor.io`, `graphql`,
   `_next/data`, `?format=json`, `.json?`.
3. **Alternate hosts/locales** — `m.` mobile site, or a different country domain running
   the same catalogue. Use the locale matching the assigned Country.
4. **Retry with backoff** — 429/timeouts are often transient. Try 2–3 times, spaced.

If after genuine effort the site cannot be read, mark `"status": "failed"` with a precise
`failure_reason`. Do not fabricate rows. Partial success is fine: `"status": "partial"`.

---

## WHAT TO EXTRACT

Only **real Home Decor product categories/sub-categories** — pages that list products.

### INCLUDE
- **Glassware (ALL — decorative AND functional)**: wine / champagne / whiskey / beer /
  cocktail / water / juice glasses, tumblers, tea & coffee cups, mugs, glass bowls,
  glass plates, glass trays, glass bottles, glass pitchers, jugs, containers,
  glass accessories, decorative glassware.
- **Tableware / dinnerware**: plates, bowls, dinner sets, serveware, serving dishes,
  platters, trays, tabletop decor. File these under `Kitchen & Dining`.
- **Lighting**: pendant, wall, ceiling, floor lamps, table lamps, lanterns, chandeliers,
  lamp shades.
- **Decorative accessories**: decorative bowls / trays / plates, mirrors, wall art,
  wall decor, vases, sculptures, figurines, decorative lanterns, candle holders,
  candles, decorative planters & pots, centerpieces.
- **Clocks — ALL TYPES ARE NOW IN SCOPE.** Wall clocks, table clocks, desk clocks,
  alarm clocks, decorative clocks, mantel clocks, wooden/glass/metal clocks.
  (This is a **change from earlier batches**, which excluded clocks. Include them now.)
- **Decorative material lines**: decorative wooden, ceramic, resin, marble, stone, clay,
  terracotta, bamboo, cane, rattan.
- **Decorative metal**: metal wall art, metal sculptures, decorative metal bowls/trays,
  decorative lanterns, metal vases, metal-framed mirrors, decorative hooks, decorative
  wall racks/shelves, curtain rods, curtain tiebacks.

### EXCLUDE — never extract
- **Home Fragrance** — diffusers, reed diffusers, room sprays, essential/aroma oils,
  wax melts, potpourri, incense. *(Changed from earlier batches, which included these.)*
- **Artificial / faux plants & flowers** — faux plants, artificial flowers, faux trees,
  greenery, wreaths, garlands, botanical decor. *(Also a change from earlier batches.)*
- **Holiday & Gift** — Christmas, holiday collection, seasonal decor, gifts, gift sets,
  gift cards.
- Bathroom (accessories, furniture, storage, fittings)
- Furniture of every kind — beds, sofas, chairs, dining/coffee/side/console tables,
  cabinets, wardrobes, shelves, storage units, office furniture, outdoor & garden furniture
- Kitchen appliances, cookware, pots, pans, pressure cookers, kitchen tools
- Hardware, plumbing, construction/building materials, home improvement, industrial
- Steel utensils, door hinges/locks, fasteners, pipes, electrical components
- Textiles (rugs, cushions, curtains, bedding, throws, tea towels) — exclude when unsure
- Food & drink consumables, cleaning products, personal care, garden tools/seeds

### NEVER EXTRACT — navigation/marketing, not product categories
Shop All · View All · Browse All · Explore All · See All · All Products · Discover ·
Collections / Collection · Featured · New Arrivals · New In · Best Sellers · Sale ·
Offers · Clearance · Outlet · Gift Guide · Lookbook · Blog · Journal · Magazine ·
Inspiration · Ideas · Stories · Designers · Brands · Trending · Recently Viewed ·
landing/promo pages.

Brand-name/designer listing pages are not categories. Price/colour filter pages are not
categories.

### DECISION RULE
The product's **primary purpose must be home decoration**. If a category primarily serves
a functional, construction, storage, hardware, furniture, plumbing or appliance purpose,
skip it. If a category mixes decorative and non-decorative items, extract only its
decorative sub-categories. **When uncertain, skip rather than guess.**

---

## HIERARCHY — PARENT GROUPING ROWS (IMPORTANT, NEW THIS BATCH)

Preserve the website's navigation hierarchy in your rows.

If a category has child categories, emit a **parent grouping row** immediately before
its children:

```json
{"category":"Kitchen & Dining","sub_category":"Glassware","parent":true,
 "qty":null,"link":null,"evidence":null,"flag":null}
```

- Parent rows: `"parent": true`, **`qty` null, `link` null**. They exist only to show
  hierarchy and will be highlighted in Excel. Never assign them a PLP URL or a count.
- Only **leaf** (deepest) product-listing rows carry `qty` and `link`.
- Emit rows in navigation order: parent, then its children, then the next parent.
- Nested levels each get their own parent row.

**Exception:** if a main category opens directly onto a product listing and has no
sub-categories, emit exactly ONE leaf row where `category` and `sub_category` are both
that category name (e.g. `category: "Lighting"`, `sub_category: "Lighting"`), with qty
and link.

Do not create a parent row for a category that has no children.

---

## QTY METHOD (in priority order)

1. **Displayed total** — "Showing 1–24 of 186", "186 products", "186 items".
   Use the exact number. Best source.
2. **Structured data** — embedded JSON (`__NEXT_DATA__`, `__NUXT__`,
   `window.__INITIAL_STATE__`), internal API/GraphQL, Algolia `nbHits`,
   Searchspring `totalResults`. Record the JSON path in `evidence`.
   **Not** Shopify `products_count` (see above).
3. **Full enumeration** — page through the complete listing and count unique product IDs.
   Only valid if you truly reach the end. Record how in `evidence`.

**Sanity checks before you accept a qty:**
- Does the number change when you change category? A constant number across different
  categories means you grabbed a site-wide total — reject it.
- Suspiciously round (1000, 5000, 10000)? Many sites cap displayed counts. A cap is NOT
  exact → `null` + flag.
- Does "of N" exceed what pagination implies? Cross-check page count × page size.
- A parent total is not a sub-category total.
- Children should sum to roughly the parent (overlap is normal, wild excess is not).

If a sub-category genuinely has **0 products**, set `"qty": 0` — it will be dropped at
merge, which is correct.

Deduplicate: **one URL = one record.** If two nav paths resolve to the same URL, keep one.

---

## LANGUAGE / NAMING

- **Output must be plain English only.** No non-ASCII characters in `category` or
  `sub_category`. Translate foreign category names to English; do not keep the original
  in parentheses.
- `category` should be a normalised English bucket, in order of preference:
  `Lighting`, `Kitchen & Dining`, `Home Accessories`, `Home Decor`,
  `Wall Decor & Mirrors`. Use the first three wherever they fit.
- Keep `sub_category` wording faithful to the site's own naming (translated), not invented.

---

## OUTPUT CONTRACT

Write **one JSON file per company**, named `c<SR>.json`, into the scratchpad,
**immediately after finishing that company**. If you finish partially and then hit a
wall, still write the file with `"status": "partial"`.

```json
{
  "sr": 1,
  "company": "Wayfair",
  "brand_site": "wayfair.com",
  "country": "USA",
  "site_url": "https://www.wayfair.com/",
  "status": "ok",
  "failure_reason": null,
  "notes": "Counts from listing header 'N Results'. Reached via translate.goog (IPv4 dead).",
  "rows": [
    {
      "category": "Lighting",
      "sub_category": "Ceiling Lighting",
      "parent": true,
      "qty": null,
      "link": null,
      "evidence": null,
      "flag": null
    },
    {
      "category": "Lighting",
      "sub_category": "Chandeliers",
      "parent": false,
      "qty": 1240,
      "link": "https://www.wayfair.com/lighting/sb0/chandeliers-c215622.html",
      "evidence": "listing header text '1240 Results'",
      "flag": null
    }
  ]
}
```

Field rules:
- `sr`, `company`, `brand_site`, `country`: copy EXACTLY from your assignment.
- `status`: `"ok"` | `"partial"` | `"failed"`
- `category`: normalised English bucket. Repeat it on every row (merge handles collapsing).
- `sub_category`: the site's own sub-category name, in English.
- `parent`: `true` for grouping rows, `false` for leaf product-listing rows.
- `qty`: integer, or `null` when unverified. Never a string. Always `null` on parent rows.
- `link`: the absolute, working, **canonical origin** sub-category URL. `null` on parents.
  Never a translate.goog or r.jina.ai URL.
- `evidence`: required whenever `qty` is not null.
- `flag`: `null`, or `"MANUAL REVIEW: <reason>"`.
- Failed company: `"rows": []` and a precise `failure_reason`.

Validate your JSON parses before finishing:
```
python -c "import json;d=json.load(open('c1.json',encoding='utf-8'));print(len(d['rows']))"
```

---

## WORKFLOW

1. `nslookup -type=AAAA <domain>` — know up front whether you need the proxy.
2. Open the site; find the real region/locale URL (follow redirects).
3. Find the category tree — mega-menu, sitemap, or nav API. `probe.py nav` helps.
4. Select only the qualifying decor categories/sub-categories per the rules above.
5. For each sub-category: open it, establish the exact total, capture the canonical URL.
6. Verify the qty (sanity checks), then record the row with its evidence.
7. Emit parent grouping rows so the hierarchy is visible.
8. Write `c<SR>.json`.

Aim for genuine coverage of the decor tree — typically 10–40 leaf rows for a large
retailer, fewer for a boutique. Depth matters, but **never invent rows to pad**.

Some companies in this batch are furniture-led (Article, Interior Define). If a company
genuinely has little or no in-scope decor, a short row list — or an empty one with
`"status": "ok"` and a note — is the correct answer. Do not stretch the scope rules to
manufacture rows.

## FINAL MESSAGE

End with a compact summary: SR, name, status, leaf row count, parent row count, how many
qty are null/flagged, and any failure reason. No prose padding.
