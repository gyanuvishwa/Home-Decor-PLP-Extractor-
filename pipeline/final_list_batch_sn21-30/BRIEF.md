# WORKER BRIEF — Home Decor Category & Qty Extraction (Final_Company_List, S.N. 21–30)

You are one of 10 parallel extraction workers. Read this whole brief before starting.

**Scratchpad root:**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\c05a5947-7e52-4f26-ac04-90f4757c80c0\scratchpad`

## WORKSPACE RULE — READ FIRST

**Create and work inside your OWN subdirectory: `scratchpad\w<SR>\`** (e.g. `w21\`).
Put every scratch file, script, HTML dump and cache in there.

Two batches ago, workers used generic filenames in the shared root and **clobbered each
other mid-run** — `build.py`, `retry.py`, `cio.py` and `counts.json` were all overwritten
by other workers, causing parse failures and lost state. Your subdirectory makes that
impossible. The only file you write to the scratchpad **root** is your final `c<SR>.json`.

Never touch the user's project files (the `.xlsx` / `.xlsm` workbooks in
`C:\Users\GyanendraVishwakarma\Web Research Agent`) — the orchestrator merges.

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

## RULE 1: STRUCTURED COUNT APIs ARE INFLATED. USE THE RENDERED HEADER.

**Confirmed across four platforms and twenty companies. The convenient structured number
counts a different population than the one shoppers see, and it is almost always higher.**

- **Shopify `/collections.json` → `products_count`** — wrong on 6 of 6 stores.
- **Constructor.io `ac.cnstrc.com` → `total_num_results`** — inflated on all 4
  Williams-Sonoma properties tested.
- **Bloomreach `core.dxpapi.com`** — returns HTTP 451 from here; unusable directly.
- **Salesforce Commerce Cloud** (Ethan Allen, Bassett, last batch) — the PLP *does*
  server-render its own `N Results` header, and that header was confirmed exact by
  enumerating `?start=` to exhaustion. SFCC is the one platform where the rendered
  header is trivially available; still verify by enumeration where cheap.

**Use the storefront's own rendered "N items" / "N products" / "N results" header.**
Structured APIs are still excellent for *discovering the category tree* — just never
for the count.

**The trap that nearly beat us:** a worker read the storefront JS bundle, proved the code
maps the API's `total_num_results` straight to the rendered header, and concluded the two
must be identical. **They were not** — 6 divergences. The storefront's own request carries
session/segment context that your outside API call does not reproduce. *Reading the code
proves what the page renders, not what your request returns.* Only empirical comparison
settles it. If you find yourself reasoning from code to a count, stop and compare against
the rendered page instead.

Cheap proofs of which number is right:
- children must sum to roughly the parent
- `ceil(total / pageSize)` must equal the page's own rendered page count
- the grid returns tiles at `start=N-1` and **zero** at `start=N`
- enumerate to exhaustion and count unique product IDs

Sites that publish **no count at all** are a legitimate outcome, not a failure
(rh.com shows none to anyone). Blank qty + a MANUAL REVIEW flag is the right answer.

---

## RULE 2: NETWORK — HOW TO REACH BLOCKED SITES

**IPv4 egress on this machine is INTERMITTENT.** It was dead 2026-08-06, working
2026-08-07. Test it, don't assume it.

**Do NOT infer "unreachable" from a missing AAAA record.** `potterybarn.com` has **no
AAAA and connects fine** — its 403 is a genuine Akamai block. A missing AAAA is a hint
about *which route to try*, never evidence about *why a request failed*. Test
reachability by actually fetching.

**Routes, in the order they have succeeded:**

1. **Direct fetch.** Try it first. It carried 8 of 10 companies last batch, including
   several that earlier notes predicted would fail.
2. **`r.jina.ai/<url>` reader proxy** — the workhorse. Carries Akamai/URBN 403s and
   renders SPA storefronts *including their product-count headers*.
   **It is shared across all 10 of you and rate-limits under concurrency.** A
   Cloudflare challenge from it usually means contention, NOT a permanent block —
   **wait and retry**. One worker gave up on it and fell back to six-month-old Wayback
   snapshots; a later retry succeeded and verified all 35 of its URLs live.
3. **`translate.goog`** —
   `https://www-<domain-with-dashes>-com.translate.goog/<path>?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=en`
   Returns genuine origin HTML incl. Next.js RSC payloads. Can return HTTP 429
   (`/sorry/index`) for ~50 minutes at a stretch across every language. Some origins
   refuse Google's fetcher with HTTP 400 (etsy, anthropologie, rh).
4. **`curl_cffi` with browser impersonation** (already in the project venv) — beats
   PerimeterX and TLS-fingerprint blocks where plain curl/requests fail. Last batch
   Ashley Furniture only yielded to `curl_cffi` with a **MOBILE** impersonation profile
   after every desktop profile was captcha'd; if desktop profiles fail, try
   `impersonate="chrome"` variants and mobile ones before declaring a block.
   Cloudflare IPv6 anycast pinning (`CURLOPT_RESOLVE` to a Cloudflare edge such as
   `2606:4700::6810:84e5` with correct SNI) cracked Wayfair when everything else was dead.
5. **Sitemaps are often served WITHOUT bot protection even when HTML is blocked.**
   Wayfair's `/seo-category-sitemap~0.xml` gave a 2,414-URL category tree unchallenged;
   RH's `/us/en/sitemap` rendered its whole nav. Always try these.

**Keep canonical origin URLs in your output `link` field.** Never write a
translate.goog, r.jina.ai, or web.archive.org URL as `link`. This is checked at merge.

**Wayback is a last resort for STRUCTURE ONLY**, never for counts, and any row built
from it must be flagged unless you re-verify the URL live.

### DO NOT USE BROWSER AUTOMATION
Chrome MCP tools may appear available, but 10 workers share one browser and will fight
over tabs. Stay on the HTTP layer.

---

## TOOLS

`probe.py` is in the scratchpad root. Run it from your own subdirectory:

```bash
python ..\probe.py get <url> [outfile]     # fetch, save, show status/size/title
python ..\probe.py nav <url>               # dump candidate category links
python ..\probe.py count <url>             # hunt product count (text + embedded JSON)
python ..\probe.py shopify <base> <handle> # count via /collections/<h>/products.json
python ..\probe.py shopifycolls <base>     # all collections + products_count
python ..\probe.py sitemap <base>          # sitemap index / robots sitemaps
python ..\probe.py json <url>              # fetch + pretty-print JSON
python ..\probe.py grep <file> <regex>     # regex a saved file with context
```

You may also `import probe` from your own scripts — usually fastest.
Venv python: `"C:\Users\GyanendraVishwakarma\Web Research Agent\.venv - Copy\Scripts\python.exe"`

`probe.py count` **reports candidates, it does not decide.** Read the evidence strings
and pick the one that genuinely is the listing total. Ignore review counts, prices,
item IDs, nav badges.

Also available: WebFetch, WebSearch, Bash/PowerShell with curl.

If after genuine effort the site cannot be read, mark `"status": "failed"` with a
precise `failure_reason`. Do not fabricate rows. Partial is fine: `"status": "partial"`.

---

## WHAT TO EXTRACT

Only **real Home Decor product categories/sub-categories** — pages that list products.

### INCLUDE
- **Glassware (ALL — decorative AND functional)**: wine / champagne / whiskey / beer /
  cocktail / water / juice glasses, tumblers, tea & coffee cups, mugs, glass bowls,
  plates, trays, bottles, pitchers, jugs, containers, glass accessories.
- **Tableware / dinnerware**: plates, bowls, dinner sets, serveware, serving dishes,
  platters, trays, tabletop decor. File under `Kitchen & Dining`.
- **Lighting**: pendant, wall, ceiling, floor lamps, table lamps, lanterns, chandeliers,
  lamp shades.
- **Decorative accessories**: decorative bowls / trays / plates, mirrors, wall art,
  wall decor, vases, sculptures, figurines, decorative lanterns, candle holders,
  candles (unscented/decorative only), decorative planters & pots, centerpieces.
- **Clocks — ALL TYPES ARE IN SCOPE.** Wall, table, desk, alarm, mantel, decorative.
  (This is a **change from batches 1–8**, which excluded clocks. Include them now.)
- **Decorative material lines**: decorative wooden, ceramic, resin, marble, stone, clay,
  terracotta, bamboo, cane, rattan.
- **Decorative metal**: metal wall art, metal sculptures, decorative metal bowls/trays,
  decorative lanterns, metal vases, metal-framed mirrors, decorative hooks, decorative
  wall racks/shelves, curtain rods, curtain tiebacks.

### EXCLUDE — never extract
- **Home Fragrance** — diffusers, reed diffusers, room sprays, essential/aroma oils,
  wax melts, potpourri, incense, **scented candles**. *(Changed from batches 1–8.)*
- **Artificial / faux plants & flowers** — faux plants, artificial flowers, faux trees,
  greenery, wreaths, garlands, botanical decor. *(Also changed from batches 1–8.)*
- **Holiday & Gift** — Christmas, holiday collection, seasonal decor, gifts, gift sets,
  gift cards.
- Bathroom (accessories, furniture, storage, fittings)
- Furniture of every kind — beds, sofas, chairs, dining/coffee/side/console tables,
  cabinets, wardrobes, shelves, storage units, office furniture, outdoor & garden furniture
- Kitchen appliances, cookware, pots, pans, kitchen tools, flatware/cutlery, bar tools
- Hardware, plumbing, construction/building materials, home improvement, industrial
- Textiles (rugs, cushions, curtains, bedding, throws, tea towels, table linens)
- Food & drink consumables, cleaning products, personal care, garden tools/seeds
- Ceiling fans, light bulbs, lighting hardware/accessories

### NEVER EXTRACT — navigation/marketing, not product categories
Shop All · View All · Browse All · Explore All · See All · All Products · Discover ·
Collections / Collection · Featured · New Arrivals · New In · Best Sellers · Sale ·
Offers · Clearance · Outlet · Gift Guide · Lookbook · Blog · Journal · Magazine ·
Inspiration · Ideas · Stories · Designers · Brands · Trending · Recently Viewed ·
landing/promo pages. Brand-name/designer listing pages and price/colour filter pages
are not categories.

### DECISION RULE
The product's **primary purpose must be home decoration**. If a category primarily
serves a functional, construction, storage, hardware, furniture, plumbing or appliance
purpose, skip it. If a category mixes decorative and non-decorative items, extract only
its decorative sub-categories. **When uncertain, skip rather than guess.**

**Mixed roll-ups: drop them, don't pad.** PB Kids dropped "Nursery Decor" (240 items)
because it bundled wallpaper, hampers and storage in with decor, and PB Teen dropped
"Clocks & Desk Accessories" (108) because its own H1 was "Teen Desk Accessories" and it
was mostly functional desk goods. Taking either would have inflated coverage with
out-of-scope product. **Inspect actual product titles before including a broad category.**

**Off-price retailers (S.N. 24, 25 this batch):** HomeGoods/Marshalls-style sites often
list "departments" that are really rotating assortment buckets. Only take a node if it is
a genuine product-listing category with a stable URL and its own count. If the site
publishes no online catalogue at all (in-store-only inventory), that is a legitimate
`"status": "ok"` with `"rows": []` and an explanatory note — say so plainly rather than
inventing a tree.

---

## HIERARCHY — PARENT GROUPING ROWS

If a category has child categories, emit a **parent grouping row** immediately before
its children:

```json
{"category":"Kitchen & Dining","sub_category":"Glassware","parent":true,
 "qty":null,"link":null,"evidence":null,"flag":null}
```

- Parent rows: `"parent": true`, **`qty` null, `link` null**. They show hierarchy only
  and get highlighted in Excel. Never give them a PLP URL or a count.
- Only **leaf** (deepest) rows carry `qty` and `link`.
- Emit rows in navigation order: parent, then its children, then the next parent.
- Nested levels each get their own parent row.
- Do not create a parent row for a category with no children.

**Exception:** if a main category opens directly onto a product listing with no
sub-categories, emit ONE leaf row where `category` and `sub_category` are both that
category name (e.g. `Lighting` / `Lighting`), with qty and link.

---

## LANGUAGE / NAMING

- **Output must be plain English only.** No non-ASCII in `category` or `sub_category`.
  Translate foreign names to English; do not keep the original in parentheses.
  **Relevant this batch: S.N. 21 (Zara Home UAE) may serve Arabic — always use the
  English locale** and English category names.
- `category` should be a normalised English bucket, preferring: `Lighting`,
  `Kitchen & Dining`, `Home Accessories`, `Home Decor`, `Wall Decor & Mirrors`.
- Keep `sub_category` faithful to the site's own naming (translated), not invented.

---

## OUTPUT CONTRACT

Write **one JSON file per company**, named `c<SR>.json`, into the scratchpad **root**
(not your subdirectory), **immediately after finishing**.

```json
{
  "sr": 21,
  "company": "Zara Home UAE",
  "brand_site": "zarahome.com",
  "country": "UAE",
  "site_url": "https://www.zarahome.com/ae/",
  "status": "ok",
  "failure_reason": null,
  "notes": "Counts from rendered listing header 'N items'. Reached directly.",
  "rows": [
    {"category":"Lighting","sub_category":"Ceiling Lighting","parent":true,
     "qty":null,"link":null,"evidence":null,"flag":null},
    {"category":"Lighting","sub_category":"Chandeliers","parent":false,
     "qty":124,"link":"https://www.example.com/lighting/chandeliers/",
     "evidence":"listing header text '124 Results'","flag":null}
  ]
}
```

Field rules:
- `sr`, `company`, `brand_site`, `country`: copy EXACTLY from your assignment.
- `status`: `"ok"` | `"partial"` | `"failed"`
- `category`: normalised English bucket. Repeat on every row (merge collapses it).
- `sub_category`: the site's own sub-category name, in English.
- `parent`: `true` for grouping rows, `false` for leaf rows.
- `qty`: integer, or `null` when unverified. Never a string. Always `null` on parents.
- `link`: absolute, working, **canonical origin** URL. `null` on parents.
- `evidence`: required whenever `qty` is not null.
- `flag`: `null`, or `"MANUAL REVIEW: <reason>"`.
- Failed company: `"rows": []` and a precise `failure_reason`.

Validate before finishing:
`python -c "import json;d=json.load(open('c21.json',encoding='utf-8'));print(len(d['rows']))"`

---

## WORKFLOW

1. `mkdir` your `w<SR>` subdirectory and work there.
2. Try a direct fetch first. If blocked, work down the route list in Rule 2.
3. Find the category tree — mega-menu, sitemap, or nav API. Sitemaps often survive
   bot protection when HTML doesn't.
4. Select only qualifying decor categories per the rules above.
5. For each: open it, get the exact total from the **rendered header**, capture the
   canonical URL.
6. Sanity-check the qty, then record the row with its evidence.
7. Emit parent grouping rows so the hierarchy is visible.
8. Write `c<SR>.json` to the scratchpad root.

Aim for genuine coverage — typically 10–40 leaf rows for a large retailer, fewer for a
boutique. **Never invent rows to pad.** Several companies in this batch are furniture-led
(Blu Dot, Room & Board, HAY); a short list, or an empty one with `"status": "ok"` and an
explanatory note, is the correct answer when the catalogue genuinely has little in-scope
decor.

## FINAL MESSAGE

Compact summary: SR, name, status, leaf row count, parent row count, how many qty are
null/flagged, access route used, and any failure reason. No prose padding.
