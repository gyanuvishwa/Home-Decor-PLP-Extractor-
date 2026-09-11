# TEST-PERFORMANCE WORKER BRIEF — Home Decor Category & Qty Extraction

You are one of several parallel extraction workers. Read this whole brief before starting.

This is a **benchmark run**: 10 companies are being re-extracted from scratch so the
user can measure extraction quality. Do NOT look at, copy from, or be influenced by
any existing extraction output. Work only from the live websites.

**Scratchpad (your working dir):**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\fedf25c1-1796-4833-a753-72351a39cd33\scratchpad`

Do all file work there. **Never touch the user's project files** — the `.xlsm` /
`.xlsx` workbooks in `C:\Users\GyanendraVishwakarma\Web Research Agent`. The
orchestrator merges. Writing to those files would corrupt validated records.

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

### READ THIS FIRST: this machine's IPv4 egress is DEAD

Hosts that resolve **A-only are unreachable** — TCP times out at SYN, no TLS
handshake, on :443 and :80, sandboxed or not. Only hosts publishing **AAAA** records
connect. This looks EXACTLY like a bot block and three workers in the previous batch
misdiagnosed it as "Cloudflare/PerimeterX is blocking our IP", writing off companies
as failed that were perfectly extractable.

**Before you conclude anything about bot protection, run:**
```bash
nslookup -type=AAAA <host>          # no AAAA address => it is the dead IPv4 egress
```

**The workaround that works.** Google's translate proxy host is IPv6-reachable and
returns the origin's genuine server-rendered HTML, including full Next.js RSC payloads:

```
https://www-<domain-with-dashes>-com.translate.goog/<path>?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=en
```
e.g. `www.birchlane.com/foo` -> `https://www-birchlane-com.translate.goog/foo?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=en`

This turned two "PerimeterX-blocked" companies into clean 47- and 49-row extractions
with **zero** challenges — proving the px-captcha those workers saw came from the
third-party relays they fell back to, not from the origin.

Traps:
- `<host>.translate.goog/robots.txt` returns 200 with translate.goog's *own* robots,
  not the origin's. It looks like the proxy works when it doesn't. Test a real path.
- Some origins refuse Google's fetcher outright (HTTP 400 "Can't translate this page").
- **Always write the canonical origin URL as `link`**, never the translate.goog URL.

Other paths that worked in the previous batch, in rough order of preference:
1. `translate.goog` as above (best — real HTML, no challenges)
2. `r.jina.ai/<url>` reader proxy — renders JS; good for React/SPA listing pages
3. plain `curl` where python `requests` got 429 (different TLS fingerprint)

### Browser automation: DO NOT USE
Chrome MCP tools exist in this session but there is only ONE shared browser and
several of you running at once — you would fight over tabs. Work the HTTP layer:

1. **Sitemaps** — often served even when HTML is blocked. Gives category URLs.
2. **Internal JSON/search APIs** — the richest source of exact totals. Find them by
   grepping saved HTML/JS for `/api/`, `algolia`, `searchspring`, `bloomreach`,
   `constructor.io`, `graphql`, `_next/data`, `?format=json`, `.json?`.
   Algolia/Searchspring responses expose `nbHits` / `totalResults` = exact totals.
3. **Shopify** — `/collections.json`, `/collections/<h>/products.json?limit=250&page=N`,
   and `/collections/<h>?view=...`. `products_count` from `/collections.json` is exact.
4. **Alternate hosts/locales** — e.g. `m.` mobile site, a different country domain
   running the same catalogue. Use the locale that matches the assigned Country.
5. **Retry with backoff** — 429/timeouts are often transient. Try 2–3 times, spaced.

If the site is hard-blocked (Cloudflare "Just a moment...", Akamai/Imperva
"Access Denied" / "Pardon Our Interruption") and no HTTP path works after genuine
effort, mark the company `"status": "failed"` with a precise `failure_reason`, or
`"partial"` if you got some of it. **Report the block precisely** — the orchestrator
has a real browser and may finish those companies itself. Do not fabricate rows.

---

## WHAT TO EXTRACT

Only **real Home Decor product categories/sub-categories** — pages that list products.

### INCLUDE
- **Glassware (ALL)**: wine/champagne/whiskey/beer/cocktail glasses, tumblers, tea &
  coffee cups, mugs, serving glassware, glass bowls/plates/pitchers/bottles/jars/
  containers, decorative glassware.
- **Tableware / dinnerware**: plates, bowls, dinner sets, serveware, trays, cutlery-
  adjacent tabletop decor (file these under `Kitchen & Dining`).
- **Lighting**: pendant, wall, ceiling, floor lamps, table lamps, lanterns, chandeliers,
  sconces, lamp shades.
- **Decorative Accessories**: decorative bowls/trays/plates, mirrors, wall art, wall
  decor, vases, sculptures, figurines, decorative objects, decorative lanterns, candle
  holders, candles, home fragrance/diffusers, artificial plants, decorative
  planters/pots, photo frames, bookends, decorative boxes.
- **Decorative material lines**: wooden (decorative only), ceramic, resin, marble,
  stone, terracotta, bamboo, cane, rattan.

### EXCLUDE (never extract)
Bathroom · Furniture (beds, tables incl. dining/coffee, chairs, cabinets, wardrobes)
· Storage · Kitchen appliances · Cookware/pans · Cutlery/flatware sets · Hardware ·
Plumbing · Construction · Home improvement · Office furniture · Outdoor furniture ·
Steel/iron/aluminium/copper utility products · Industrial · Utility · Food & drink
consumables · Cleaning products · Personal care · Garden tools/seeds · Textiles
(rugs, cushions, curtains, bedding, throws, tea towels) · Kids/baby · Pet.

### NEVER EXTRACT (navigation/marketing, not product categories)
Collections · Featured Collections · Shop All · View All · Browse All · Explore All ·
Discover · Blogs · Editorial · Gift Guides · Lookbooks · Landing pages · Sale · Offers ·
Clearance · New Arrivals · Best Sellers · Navigation pages ·
**Clocks of every kind** (wall/desk/alarm/clock collections).

Brand-name/designer listing pages are not categories. Price/colour filter pages are
not categories.

---

## QTY METHOD (in priority order)

1. **Displayed total** — "Showing 1–24 of 186", "186 products", "186 résultats".
   Use the exact number. This is the best source.
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

Deduplicate: if two sub-category names resolve to the same URL, keep one.
Drop categories that genuinely have 0 products rather than writing a zero row.

---

## LANGUAGE / NAMING CONVENTION

- All output text must be plain **English**.
- `category` should be the normalised English bucket, in order of preference:
  `Lighting`, `Kitchen & Dining`, `Home Accessories`, `Home Decor`, `Home Fragrance`,
  `Wall Decor & Mirrors`, `Garden`.
  Use `Lighting` / `Kitchen & Dining` / `Home Accessories` whenever they fit.
- Keep `sub_category` wording faithful to the site's own naming (translated to
  English if needed), not invented. Fix the site's typos to correct English.

---

## OUTPUT CONTRACT

Write **one JSON file per company**, named `t<SR>.json` (t for test), into the
scratchpad, **immediately after finishing that company**. If you finish partially and
then hit a wall, still write the file with `"status": "partial"`.

```json
{
  "sr": 1,
  "company": "Quince Home",
  "brand_site": "quince.com",
  "country": "USA",
  "site_url": "https://www.quince.com/",
  "status": "ok",
  "failure_reason": null,
  "notes": "Counts from the listing header 'N items'.",
  "rows": [
    {
      "category": "Lighting",
      "sub_category": "Table & Floor Lamps",
      "qty": 27,
      "link": "https://www.quince.com/shop/home/lighting/table-floor-lamps",
      "evidence": "listing header text '27 items'",
      "flag": null
    }
  ]
}
```

Field rules:
- `sr`, `company`, `brand_site`, `country`: copy EXACTLY from your assignment below.
- `site_url`: the real homepage URL you actually landed on (follow redirects).
- `status`: `"ok"` | `"partial"` | `"failed"`
- `category`: normalised English bucket (see naming convention above).
- `sub_category`: the site's own sub-category name, in English.
- `qty`: integer, or `null` when unverified. Never a string.
- `link`: the absolute, working sub-category URL you actually verified.
- `evidence`: required whenever `qty` is not null.
- `flag`: `null`, or `"MANUAL REVIEW: <reason>"`.
- Failed company: `"rows": []` and a precise `failure_reason`.

Validate your JSON parses before finishing:
`python -c "import json;d=json.load(open('t1.json',encoding='utf-8'));print(len(d['rows']))"`

---

## WORKFLOW

1. Open the site; find the real region/locale URL (follow redirects).
2. Find the category tree — mega-menu, sitemap, or nav API. `probe.py nav` helps.
3. Select only the qualifying decor categories/sub-categories per the rules above.
4. For each sub-category: open it, establish the exact total, capture the URL.
5. Verify the qty (sanity checks above), then record the row.
6. Write `t<SR>.json`.

Aim for genuine coverage of the decor tree — typically 10–40 sub-category rows for a
large retailer, fewer for a boutique. Depth matters, but never invent rows to pad.

## FINAL MESSAGE

End with a compact summary: SR, name, status, row count, how many qty are
null/flagged, and any failure reason. No prose padding.
