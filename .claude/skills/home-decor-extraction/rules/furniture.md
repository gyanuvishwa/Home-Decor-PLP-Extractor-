# FURNITURE EXTRACTION — WORKER BRIEF

>> ACCESS RULE, ABSOLUTE: open every website ONLY through the Claude-in-Chrome browser
>> connector (`mcp__claude-in-chrome__*`). No curl, curl_cffi, requests, probe.py,
>> WebFetch, r.jina.ai, translate.goog or any other proxy. See section 5. <<

You are one of several parallel extraction workers. Read this whole brief before starting.
You are assigned **exactly one company**. Your job: find that company's **FURNITURE**
categories/sub-categories, capture the deepest valid listing URLs and the site's own exact
product counts, and write one JSON file.

**Scratchpad (your working dir — do ALL file work here):**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\e4fc7974-8068-4b60-967c-307d8ef819f2\scratchpad`

**The scratchpad is shared with ~19 other workers running at the same time.** Prefix EVERY
working file and directory you create with `w<SR>_` (e.g. `w42_tree.py`, `w42_cache/`). A worker
has already had its `tree.py` overwritten mid-run by a sibling. The ONLY unprefixed file you write
is your result `f<SR>.json`.

NEVER touch the user's project files in `C:\Users\GyanendraVishwakarma\Web Research Agent`
(the `.xlsx` / `.xlsm` workbooks). Four validated workbooks live there — Kitchen_and_Dining,
Lighting, Wall_Decor, Decorative_Home_Accessories — and writing anywhere in that folder is
forbidden. The orchestrator does the merge.

---

## 0. READ YOUR COMPANY'S ACCESS NOTES FIRST — THIS SAVES YOU AN HOUR

`notes/<SR>.md` in the scratchpad contains the **prior Home-Decor pass** for your exact
company: which proxy/route reached the site, whether it was blocked and by what, the URL
shape, and a list of category URLs that were **verified working**. Read it before your
first fetch. It tells you what already works. It does NOT tell you anything about
furniture — the prior pass deliberately EXCLUDED furniture, so an empty furniture result
there means nothing.

**Read those notes for the SITE STRUCTURE, not for the access route.** They describe how
earlier passes reached the site over HTTP — curl_cffi profiles, jina, translate.goog and
so on. Those routes are now FORBIDDEN (section 5). What is still valuable in them: the
URL shape, the category tree, which nodes were verified, where the counts live, and the
site-specific traps. Ignore their fingerprint/proxy advice entirely.

If that file says `status=failed`, still try — a real browser session frequently gets in
where the HTTP layer never could. But do not burn the whole session on one site; if
Chrome genuinely cannot reach it, mark it `blocked` with a precise reason.

---

## THE ONE RULE THAT MATTERS

**`qty` must be the EXACT number of products the website itself reports for that
sub-category URL.**

- NEVER estimate, approximate, round, infer, aggregate, average or combine.
- NEVER copy a qty from a parent or sibling category.
- NEVER sum children to make a parent number.
- If you cannot verify the exact number, set `"qty": null` and
  `"flag": "MANUAL REVIEW: <specific reason>"`. A null is a **correct** answer.
  A made-up number is a project-destroying error.
- Every row with a qty must carry an `evidence` string: the literal text or JSON path that
  produced it (e.g. `"listing header 'Showing 1-24 of 186'"`, or
  `"__NEXT_DATA__:props.pageProps.search.numFound=186"`).
  A qty without evidence will be nulled at merge.

Accuracy beats coverage. Beats speed. Always.

---

## 1. WHAT COUNTS AS FURNITURE

Include a category when the **PRIMARY PRODUCT TYPE** of the things it lists is furniture.

Priority of signals: **PRIMARY PRODUCT TYPE > PRODUCT PURPOSE > WEBSITE CATEGORY > ROOM NAME.**
A room name alone NEVER decides. "Bedroom" in a URL does not make a candle a bed.

### INCLUDE

- **Tables** — dining, kitchen, coffee, side, end, console, sofa, accent, nesting,
  bedside/nightstands, desks (writing/office/computer), dressing tables, vanity tables,
  meeting/work tables, sideboards.
- **Seating** — chairs of all kinds (dining, armchairs, accent, lounge, desk, office,
  rocking), recliners, bar/counter stools, stools, benches, ottomans, footstools,
  poufs **when the site files them as furniture/seating**.
- **Sofas** — sofas, couches, sectionals, corner sofas, modular sofas, loveseats,
  chaises, sofa beds, daybeds.
- **Bedroom** — beds, bed frames, headboards, dressers, chests of drawers, wardrobes,
  armoires, bedroom cabinets, bedroom benches, bedroom furniture sets.
- **Living room** — TV/media units, display cabinets, living-room cabinets, bookcases,
  furniture-style shelving, living-room furniture sets.
- **Dining** — dining tables/chairs/benches/sets, sideboards, dining cabinets.
- **Office** — desks, office chairs, filing cabinets, office storage furniture, office sets.
- **Outdoor / garden / patio** — outdoor tables, chairs, sofas, benches, sun loungers,
  outdoor dining sets, patio & garden furniture sets. (Outdoor furniture IS in scope.)
- **Cabinets / storage FURNITURE** — cabinets, sideboards, cupboards, dressers, chests,
  bookcases, display cabinets, TV units, media units, console cabinets, wardrobes,
  armoires, freestanding furniture shelving units, shoe cabinets, hall/entryway furniture.
- **Bathroom FURNITURE** — vanity units, vanity cabinets, bathroom cabinets, bathroom
  storage furniture, bathroom furniture sets, bathroom console units.
  (Do not exclude something just because it says "Bathroom" or "Vanity".)
- **Kids / nursery furniture** — cribs, kids beds, kids desks, changing tables, kids
  chairs/tables, nursery gliders. These are furniture; include them.

**Material is irrelevant.** Wood, metal, steel, iron, aluminium, glass, rattan, cane,
bamboo, fabric, stone, marble, plastic, composite, mixed — all fine. The Home Decor
project's material restrictions DO NOT apply here.

### EXCLUDE

- Lighting of every kind (lamps, chandeliers, sconces, floor/table lamps, vanity lighting).
- Mirrors of every kind (incl. floor/leaning/bathroom/vanity mirrors) — Wall Decor's job.
- Clocks, wall art, wall decor, tapestries, decals.
- Vases, candle holders, candles, home fragrance, photo/picture frames, sculptures,
  figurines, decorative objects, trays, decorative bowls, planters, artificial plants.
- Glassware, dinnerware, serveware, plates, bowls, cups, mugs, cutlery, cookware,
  kitchen utensils, small kitchen appliances.
- Textiles — rugs, cushions, throws, curtains, bedding, towels, table linen.
- **Standalone storage products** — storage baskets, boxes, bins, containers, organisers,
  decorative storage boxes. These belong to a future Storage task, NOT here.
- Bathroom **fixtures** — sinks, toilets, bathtubs, showers, taps/faucets, shower heads,
  bathroom accessories, bathroom mirrors, bathroom lighting.
- Mattresses, mattress toppers, bed bases sold as bedding, pillows.
  (**Mattresses**: exclude — they are bedding, not furniture. A "Beds" or "Bed Frames"
  category is furniture; a "Mattresses" category is not. If a site has only "Beds &
  Mattresses" with no split, take it and flag it.)
- Furniture **care/parts** — furniture legs, knobs, castors, polish, covers, protectors.
- Office supplies, hardware, plumbing, construction, garden tools, appliances.

### THE STORAGE-vs-FURNITURE LINE (important)

Furniture: wardrobe, dresser, sideboard, bookcase, TV unit, display cabinet, console
cabinet, chest of drawers, freestanding shelving unit → **INCLUDE**.
Standalone storage goods: baskets, boxes, bins, containers, organisers → **EXCLUDE**.

If the site itself files a node under a Furniture department, keep that classification
unless the products clearly contradict it (open the page and look at the tiles).

### THE SHELVING LINE

- Bookcases, bookshelves, freestanding shelving units, display shelf units, storage shelf
  units, furniture shelving → **Furniture**.
- Decorative **wall** shelves / "Shelves & Ledges" under a Wall Decor department →
  **NOT** furniture. Do not move them here.
- Genuinely ambiguous → include it with
  `"flag": "MANUAL REVIEW: ambiguous shelving — <what you saw>"`. Do not guess silently.

### FURNITURE SETS

Real furniture sets are fine (dining set, bedroom set, sofa set, outdoor set,
table & chair set). Marketing "collections" are not — see §3.

---

## 2. URL HIERARCHY RULE — MANDATORY

**Record the DEEPEST useful subcategory URLs, not the parent.**

If `Furniture > Tables` has children `Dining Tables`, `Coffee Tables`, `Side Tables`:
record the three children with their own qty+URL. `Furniture` and `Tables` become
**grouping rows** (name only, `qty: null`, `link: null`).

Only when a node has no valid children do you record the node itself with qty+URL.

Never record a parent that has extractable children as a leaf. Never record both a
parent-as-leaf and its children.

---

## 3. NEVER EXTRACT THESE AS CATEGORIES

View All · Shop All · All Furniture · Browse All · Explore All · Collections ·
Product/Promotional/Seasonal/Gift Collections · "Shop the Collection" · Discover ·
New Arrivals · Best Sellers · Sale · Clearance · Offers · Outlet · Lookbooks ·
Gift Guides · Blogs · Editorial · Landing pages · Homepage · Search result pages ·
Brand/designer listing pages · Price/colour/material filter pages ·
**Individual product-detail pages** · Room "shop the look" pages.

Also never record a URL that is a search query string (`?q=`, `/search?`) even if it
renders a nice grid.

---

## 4. QTY METHOD (priority order)

1. **Rendered listing header** — "186 products", "Showing 1–24 of 186", "186 items",
   "186 résultats", "186 producten", "186 Artikel". **This is normally the source of truth.**

   **But it is not sacred — it has been caught lying twice, in opposite directions:**
   - **Padded upward.** OTTO tops small result sets up with similar products: a 7-product
     category printed "500 Produkte". Its true per-category count came from the site's own
     nav `data-count`.
   - **Counting the wrong unit.** Muuto's "37 ITEMS" badge counts colourways, not products —
     a 3-product Sideboards page printed "6 ITEMS".

   So: take the header, then **corroborate it once** against an independent source (a small
   single-page category you can count by eye, a structured product-ID enumeration, or the
   site's own nav count). If they disagree, work out *which* is the product count and say in
   `evidence` which you used and why. Do not silently prefer either one.

   The disagreement is often confined to one regime — on OTTO the header is exact above ~600
   products and padded only below 500. Establishing *where* it is reliable beats discarding it.
2. **Structured data** — `__NEXT_DATA__`, `__NUXT__`, `window.__INITIAL_STATE__`,
   internal API/GraphQL, Algolia `nbHits`, Searchspring `totalResults`,
   Constructor `total_num_results`. Record the JSON path in `evidence`.
   **Only use these when the rendered header is unobtainable, and say so in `evidence`.**
3. **Full enumeration** — page to the true end and count unique product IDs. Only valid
   if you genuinely reach the end; record how in `evidence`. Do this by driving the page
   in your Chrome tab (scroll / load-more / paginate) or by same-origin `fetch()` via
   `javascript_tool` — never by fetching the endpoint from outside the browser.

**Known-inflated structured sources — do NOT prefer them over the rendered header:**
Shopify `products_count` (wrong on 6/6 stores) · Magento `categoryList.product_count`
(3–5x inflated on Marina Home) · Constructor.io on Williams-Sonoma properties (higher,
never lower) · Bloomreach (account-specific).
Known-exact-under-check: Target redsky `total_results` · TJX/Marshalls Endeca `itemCount` ·
1stDibs `totalResults` · Perigold RSC `resultCount` · Neiman Marcus `productListPage.total` ·
Cornerstone `UnbxdAPI numberOfProducts` · One Kings Lane `__NEXT_DATA__.total` ·
Wix `totalCount`.

**Do NOT count product tiles by counting hrefs.** It has failed three ways (non-ASCII
slugs undercount, recommendation carousels overcount, JSON-LD next-page prefetch
overcounts). Use a structured product-ID field.

**Sanity checks before accepting any qty:**
- Does the number change when you change category? A constant number = site-wide total → reject.
- Suspiciously round (1000/5000/10000)? Probably a display cap → `null` + flag.
- Does the h1 of the page you loaded actually match the category you think you loaded?
  (Magento/Cox&Cox silently serves the PARENT listing instead of 404ing on a bad slug.)
- Sponsored/PLA tiles are injected into grids but excluded from the total.
- Counts drift within a session on some sites — take two reads, flag if they differ.
- A parent total is not a child total.

**Sites that publish no count anywhere are a legitimate outcome** (rh.com proven three
ways). Emit the row with `qty: null` + a flag, not a guess.

---

## 5. HOW TO OPEN WEBSITES — MANDATORY, NO EXCEPTIONS

**You MUST open every website through the Claude-in-Chrome browser connector
(`mcp__claude-in-chrome__*` tools). Nothing else.**

This is a hard project rule set by the user, not a preference. It exists because the
HTTP layer is where every anti-bot failure in this project has come from — Akamai,
DataDome, PerimeterX, Cloudflare, IP throttles, fingerprint sweeps that burn an hour and
still fail. A real Chrome session executes the challenge JavaScript and carries the
right TLS fingerprint, cookies and session state, so those walls simply do not appear.
It has already been the ONLY thing that worked on CB2, Maisons du Monde and RH.

### FORBIDDEN — do not use any of these to reach a target site

- `requests`, `urllib`, `httpx`, `curl`, `wget`, `curl_cffi` (all impersonation profiles)
- `probe.py` and any script that imports it (`fetch`, `fetch_json`, `page_count`, ...)
- `WebFetch`, `WebSearch` as a page-reading route
- `r.jina.ai`, `translate.goog`, allorigins / codetabs / corsproxy / cors.sh, any CORS or
  reader proxy
- Wayback / webcache
- Googlebot- or Bingbot-UA tricks

Do not "just check quickly" with curl. Do not fall back to it when Chrome is slow. If the
Chrome connector cannot reach a site, that is a `blocked` result — write it up honestly.

### REQUIRED WORKFLOW

1. Load the connector tools in ONE ToolSearch call:
   `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__javascript_tool`
   (Do NOT load or use `select_browser` / `switch_browser`.)
2. Call `tabs_context_mcp` FIRST to see what tabs exist. Never reuse a tab ID from
   another session or another worker.
3. `tabs_create_mcp` — **create your OWN tab and work only in it.**

   ### THE TAB RULE — this is what keeps parallel workers from colliding
   There is ONE browser, shared by every worker running right now. Your isolation is
   your tab, nothing else.
   - Create exactly one tab, note its tabId, and use that tabId on every single call.
   - **Never** navigate, reload, read, click or close a tab you did not create. Another
     worker is mid-extraction in it. This has already gone wrong once.
   - **Never** call `select_browser` or `switch_browser`. There is one browser and it is
     already selected; those tools would disrupt every other worker.
   - Close your own tab with `tabs_close_mcp` when you finish the company, even if you
     end up `blocked`. Leaving tabs open starves the other workers.
   - If a call returns an error saying your tab no longer exists, call
     `tabs_context_mcp` for fresh state and create a new tab — do not grab an existing one.
4. `navigate` to the page, then read it with `get_page_text` / `read_page` / `find`.
5. For the category tree and for counts, `javascript_tool` running **same-origin
   `fetch()` from the loaded page context** is the workhorse: the page's own cookies and
   challenge clearance apply, so the site's internal JSON/category/search endpoints
   answer normally. This is how Maisons du Monde and CB2 were solved.
6. Pace yourself *before* trouble: roughly one request every 5-8 seconds. A real session
   still gets rate-limited — Maisons du Monde 403'd after 12 rapid fetches.
   **But once a block actually lands, do NOT back off and retry — stop. See the HARD BLOCK RULE in §7c.**
   Spacing requests out is productive; waiting for a wall to lift is not.

### Still true, and still required

- **Check `robots.txt` for a Claude-specific `Disallow: /`** before extracting (fetch it
  by navigating to it in your tab). `anthropic-ai` / `ClaudeBot` / `Claude-Web` /
  `Claude-User` / `Claude-SearchBot` named with a full-site disallow means STOP and mark
  the company `blocked` with that finding. Read it carefully: several sites
  (H&M, Conforama, Noon, Serena & Lily, Scully & Scully) name Claude and then `Allow: /`
  — that is explicit permission, the opposite of a block.
- Sitemaps are still the best source for a full category tree — open them in the tab.
- **`link` must always be the canonical origin URL.** Never a proxy or a redirect host.

### Local scripting is still fine

You may still use Bash/Python in the scratchpad for anything that does NOT fetch a target
site: parsing text you captured from the browser, set arithmetic on product IDs,
building and validating your `f<SR>.json`. The ban is specifically on reaching the
website by any route other than Chrome.


## 6. PROVING ABSENCE (when a company genuinely has no furniture)

"No furniture found" is a real and common answer — many of these companies are decor,
tableware or lighting specialists. But you must EARN it:

1. Load the site's actual navigation / mega-menu (not a search engine result).
2. Check the sitemap / category tree for furniture slugs: `furniture`, `sofa`, `chair`,
   `table`, `bed`, `desk`, `cabinet`, `wardrobe`, `stool`, `bench`, `dresser`, `shelving`,
   `bookcase`, `seating`, `dining-table`, `nightstand`, `armchair`, `meubles`, `möbel`,
   `meubelen`, `muebles`, `mobili`, plus the local-language terms for your Country.
3. **A site search returning 0 is NOT proof.** Two sites here returned a default product
   set or a flat "1000 results" for every query. Before trusting search, run a
   discrimination check: query something the site certainly does NOT sell and something it
   certainly does, and confirm the counts differ. If they don't, enumerate the catalogue
   and title-scan instead.
4. State in `notes` exactly what you inspected to conclude absence.

An accessible site with a genuinely inspected nav and no furniture → `"status": "ok"`,
`"rows": []`. That is a valid, valuable result.

---

## 7. OUTPUT CONTRACT

Write **one JSON file**, named `f<SR>.json`, into the scratchpad, **as soon as your
company is done**. If you get part way and then hit a wall, still write the file with
`"status": "partial"`.

```json
{
  "sr": 9,
  "company": "Article",
  "brand_site": "article.com",
  "country": "USA",
  "site_url": "https://www.article.com/",
  "status": "ok",
  "failure_reason": null,
  "notes": "How you reached the site, where the tree came from, where the counts came from, what you excluded and why, and any sanity checks you ran.",
  "rows": [
    {
      "category": "Furniture",
      "sub_category": "Living Room",
      "qty": null,
      "link": null,
      "is_group": true,
      "evidence": null,
      "flag": null
    },
    {
      "category": "Furniture",
      "sub_category": "Sofas",
      "qty": 124,
      "link": "https://www.article.com/browse/1/sofas",
      "is_group": false,
      "evidence": "listing header text '124 items'",
      "flag": null
    }
  ]
}
```

Field rules:

- `sr`, `company`, `brand_site`, `country`, `site_url` — copy EXACTLY from your assignment.
- `status` — one of:
  - `"ok"`      site read, tree inspected, extraction complete (rows may be `[]`)
  - `"partial"` site read but you could not finish (some rows missing/unverified)
  - `"blocked"` site could not be properly accessed at all
  - `"error"`   something else went wrong; explain it
- `failure_reason` — required and specific for `blocked` / `error` / `partial`. Say the
  mechanism: "Cloudflare challenge on every route incl. 12 curl_cffi profiles, jina 403,
  translate.goog 400". Not "site down".
- `category` — the top bucket. Use **`"Furniture"`** for essentially everything. Only use
  a different top bucket if the site itself puts furniture under a differently-named
  department AND that name is more truthful (e.g. `"Outdoor Furniture"`,
  `"Bathroom Furniture"`, `"Office Furniture"`). Keep it English, plain ASCII.
- `sub_category` — the site's own node name, **in English** (translate French/German/
  Dutch/Spanish/Italian/Japanese names; do not keep the original in parentheses). Faithful
  to the site's wording, not invented.
- `is_group` — `true` for a grouping/parent row (name only). Grouping rows MUST have
  `qty: null` and `link: null`. `false` for a real leaf with qty+URL.
- `qty` — integer, or `null`. Never a string, never `"N/A"`.
- `link` — absolute canonical origin URL you actually verified. `null` on grouping rows.
- `evidence` — required whenever `qty` is not null.
- `flag` — `null`, or `"MANUAL REVIEW: <reason>"`.

**Row ordering matters** — emit rows in reading order: each grouping row immediately
followed by its children. The merge writes them to the sheet in the order you give.

**Hierarchy depth**: the workbook has two name columns — `Category` (top) and
`Sub-Category` (everything below, one row per node, parents as grouping rows). So a
3-level tree `Furniture > Living Room > Sofas` becomes:
`category="Furniture", sub_category="Living Room", is_group=true` then
`category="Furniture", sub_category="Sofas", is_group=false, qty, link`.

Do not emit a grouping row with no children. Do not emit duplicate rows (same
sub_category + same link). If two genuinely different listing pages exist for a
similarly-named node, keep both and explain in `notes`.

Validate before finishing:
`python -c "import json;d=json.load(open('f9.json',encoding='utf-8'));print(d['status'],len(d['rows']))"`

---

## 7b. FOUR TRAPS PROVEN IN THE SR 105-127 BATCH — CHECK ALL FOUR

1. **The nav under-reports the tree. Cross-check the sitemap — this is MANDATORY, not optional.**
   Four companies in one batch had real, countable furniture categories reachable only from the
   category sitemap: vtwonen's whole Bathroom Furniture branch (373) plus three nursery leaves,
   Kave Home's folding-chairs and garden-rocking-chairs, Anthropologie's Desks, and KARE, whose
   own category-page tile block listed 14 children where the mega-menu showed 11. Walk the
   mega-menu AND the category sitemap AND each category page's own sub-category chip/tile strip,
   then take the union.

2. **A bad slug usually does NOT 404 — it serves a plausible wrong number.** Three different
   platforms in one batch: H&M redirects a bogus slug to the department and reports the parent's
   total; Anthropologie serves the parent listing under a 200; a Searchanise store returns the
   SITE-WIDE total (79,619) for an invented handle. Assume this is true until you disprove it.
   For every leaf URL confirm HTTP 200 **and** that the h1/canonical is the node you asked for.

3. **Node identity comes from the slug, never the display label.** On H&M IT, `tables/side` and
   `tables/coffee` both render the identical label "Tavolini da salotto" (76 vs 82 products).
   Label-keyed dedup would silently eat one. Same failure mode as the merge dedup-key bug.

4. **`qty` is an in-stock snapshot on stock-gated storefronts.** Proven on Fenwick: the rendered
   header counts purchasable products, not the published catalogue (Sofas header 110 = 135
   published / 110 in stock). Record the header per Rule 1 anyway — but if a furniture node reads
   0 or absurdly low, say so in `notes` rather than assuming you misread it.

**Live categories with 0 products: EMIT them** as a normal leaf row with `qty: 0`, its URL, and
evidence quoting the site's own empty-state text. Do not silently omit them. (Workers split on
this; emitting is recoverable at merge, omitting is not.) A node that 404s or has no listing page
is different — that one is not a row at all.

## 7c. EFFICIENCY RULES — MANDATORY, THESE ARE NOT SUGGESTIONS

Accuracy is still the top priority. But repeated verification of an already-established fact is
**prohibited**. The objective is a correct classification from the fewest browser calls and tokens,
not the largest number of checks. A worker was stopped mid-run for violating these.

### Structured data first, browser second

Before any repeated browser interaction, ask whether the information already exists in SSR HTML,
embedded JSON, `__NEXT_DATA__` / `__NUXT__` / `__APOLLO_STATE__`, an API response you already
captured, or data you already extracted. If it does, **parse it locally with Python**. Pull the
dataset ONCE, then work on it offline.

### Never enumerate by hand what you can filter programmatically

    Extract product dataset once
      -> deterministic title/category scan (local)
      -> small exception list
      -> browser-verify ONLY the exceptions

If a category has 94 products and 3 titles look furniture-ish, you inspect **3**, not 94.
Report the split explicitly: `TOTAL n / clear non-furniture X / potential furniture Y /
needs verification Z`, then open only the Z.

Keyword scans generate CANDIDATES ONLY — they never classify. "Table Lamp" is lighting.
"Console Bowl" is decor. "Wooden Table Sculpture" is a decorative object. "Bedside Table" is a
real candidate and needs looking at. Decide on product evidence, never on the site's facet alone.

### Checkpoint before anything expensive

Write `w<SR>_checkpoint.json` at each expensive milestone: URL, product count, pagination status,
item IDs, titles, candidate exceptions, verified exceptions, remaining work, rate-limit status.
If you are interrupted or blocked, this file is what survives. On resume, READ IT FIRST and
continue from the last incomplete phase. Never rediscover the site from scratch.

### Rate limits and bot walls: the HARD BLOCK RULE

**The FIRST time a target produces a block, you stop requesting that target. Not the third
time, not after a backoff — the first.**

A block is any of: 403, DataDome, Akamai, Cloudflare challenge, CAPTCHA, "Access Denied",
rate-limit response, or a page that repeatedly fails to load.

    first block
      -> STOP browser requests to that target
      -> save w<SR>_checkpoint.json
      -> use the data you already hold
      -> process it locally
      -> identify what is ACTUALLY still missing
      -> report that, honestly

**Banned outright, no exceptions:** `sleep` / `time.sleep()` / `timeout` / `while sleep` /
cooldown timers / backoff loops / "wait N minutes and try again" / polling a blocked host.
A shell command whose only purpose is to wait for a website is not productive work and must
not be run. Waiting is not progress, and an agent kept alive waiting is worse than one that
finished with a gap.

Then write `f<SR>.json` with `"status": "partial"` and a `failure_reason` naming exactly which
nodes could not be verified and why. **An honest partial beats another blocked hour** — and a
partial with a precise gap can be topped up later in minutes, which a burned hour cannot.

Do not chase the same block on a different route either. If Chrome cannot reach it, that is
the answer; record it and move on.

**What is NOT a block — do not abort a company on these:**
- `[BLOCKED: Cookie/query string data]` from a tool call. That is the MCP connector's own
  output-redaction filter, not the site. It fires when your collected data carries query
  strings. Strip the query strings and re-run; it works immediately.
- An HTTP 500, a `NoSuchKey`, or a missing/empty sitemap. Those are server errors or dead
  files, not anti-bot walls. Substitute another tree source (mega-menu parse, the union of
  category links across pages, product-URL taxonomy, or a numeric-ID sweep) and carry on.
- A `chrome-error://` page with no HTTP response at all is a NETWORK/connect failure, not a
  wall. Record it as blocked with that precise distinction — it usually means the host is
  unreachable from this machine and will work on a later retry.
- **A Cloudflare "Just a moment..." page that never finishes in your tab.** Check
  `document.visibilityState` first: if it is `hidden`, Chrome's background-tab timer
  throttling is starving the challenge script, and the challenge is growing but can never
  complete. Foreground the tab (taking a screenshot does it) and it clears instantly. A
  stuck interstitial in a background MCP tab is a visibility problem to fix, not a block to
  abort on. A challenge that completes and *then* denies you is a real block.

The discriminator: a real block comes **from the target**, as an HTTP status or a challenge
page. Anything originating in the tool layer, or a server error, is not a block.

### Before every browser call, and every re-read

Ask: *what NEW information does this produce?* If the answer is "something I already have", do not
make the call. Do not write "let me confirm the count / re-check pagination / verify the facets
again" unless you have direct evidence the earlier finding was WRONG. Two independent confirmations
of a fact are enough; a third is waste. Do not push large page dumps through your own context when
a local parse can reduce them to a small structured table first.

## 8. WORKFLOW

1. Read `notes/<SR>.md`. Use the route that already worked.
2. Open the site at the locale matching your assigned Country; follow redirects.
3. Get the real category tree — mega-menu, sitemap, or nav API. `probe.py nav` helps.
4. Locate every furniture department: a top-level `Furniture` nav item, and/or room-based
   furniture sections (Living Room / Bedroom / Dining / Office / Outdoor / Bathroom
   furniture), and/or product-type sections (Sofas, Beds, Tables, Seating, Storage).
   Some sites scatter furniture across rooms with no single Furniture department — check
   every room department for furniture-typed children.
5. Walk down to the deepest valid subcategory level (§2).
6. Apply §1 include/exclude. Drop the §3 navigation junk.
7. For each leaf: open it, establish the exact total, capture the canonical URL, run the
   §4 sanity checks.
8. Emit grouping rows for the parents you walked through.
9. Write `f<SR>.json`.

Typical output: 15–60 leaf rows for a large furniture retailer, 3–15 for a boutique,
0 for a pure decor/tableware/lighting brand. Depth matters; never pad.

Work **synchronously**. Do not launch a background job and end your turn waiting to be
notified — the orchestrator cannot see your background jobs, and your turn will simply
stop with a missing file. Finish the company in the foreground.

## 9. FINAL MESSAGE

End with a compact summary: SR, name, status, leaf-row count, grouping-row count, how many
qty are null/flagged, and the failure reason if any. No prose padding.
