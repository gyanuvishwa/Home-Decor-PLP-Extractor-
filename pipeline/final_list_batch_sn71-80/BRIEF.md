# WORKER BRIEF — Home Decor Category & Qty Extraction (Final_Company_List, S.N. 71–80)

You are one of 10 parallel extraction workers. Read this whole brief before starting.

**Scratchpad root:**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\59d13edb-541c-4fad-93db-71d49f65f6f6\scratchpad`

**Your own `w<SR>` subdirectory may already contain files from a prior interrupted attempt**
(saved HTML/JSON fetches, helper scripts). Feel free to reuse anything still valid — check
timestamps/content freshness — instead of re-fetching from scratch, but verify counts
independently rather than trusting a half-finished prior read.

---

# RULE 0 — PRODUCT TYPE BEATS ROOM NAME (NEW, HIGHEST PRIORITY)

**This is a correction to previous batches. It overrides anything below that conflicts.**

**NEVER exclude a category because of a ROOM word in its name.** Room words —
Bathroom, Bedroom, Living Room, Dining Room, Kitchen, Entryway, Hallway, Office,
Outdoor, Vanity — describe *where a product is used*. They say nothing about whether the
product is in scope. Judge the **product type**.

Before skipping any category containing a room word, stop and ask:
**"Am I excluding this because the PRODUCT is out of scope, or only because the ROOM is?"**
If the product is an approved type (lighting, mirror, glassware, clock, wall decor,
decorative accessory or object), **INCLUDE it.**

### 0.1 Lighting organised by room is IN SCOPE
If the site has `Lighting > Lighting by Room` (or equivalent), **every one of those nodes
must be explored and extracted**:
Living Room · Bedroom · Dining Room · Kitchen · **Bathroom** · **Vanity** · Entryway ·
Hallway · Office · **Outdoor** · Patio · Landscape lighting — all IN.

### 0.2 Traverse EVERY lighting branch — no depth limit
Do not stop at Ceiling Lights. Expand all of: Lighting by Room · Wall Lighting · Pendants ·
Chandeliers · Table Lamps · Floor Lamps · Flush Mounts · **Recessed** · **Track** ·
**Cabinet/Under-cabinet** · Vanity · Bathroom · Outdoor · Landscape · Picture lights, and
any other lighting branch actually present. Expand until you reach real product listing
pages.
*(Still excluded: light BULBS, ceiling FANS, and pure wiring/mounting hardware — those are
not fixtures.)*

### 0.3 ALL mirrors are IN SCOPE, every type
Wall · Decorative · **Bathroom** · **Vanity** · **Makeup** · Dressing · Bedroom ·
Full-length · Floor · Leaner · Over-the-door · Hanging · Framed · Frameless · Round ·
Rectangular · Oval · Arch · Accent · Statement · Oversized · Large · Small · Beveled ·
**LED / Backlit / Lighted / Illuminated / Smart** · Console · Entryway · Hallway ·
Living/Dining/Bedroom mirrors · Mirror collections. Medicine-cabinet mirrors count **only**
if sold as mirrors/decor rather than as bathroom hardware.

### 0.4 "Bathroom" is NOT a blanket exclusion
- **INCLUDE**: bathroom mirrors, vanity mirrors, bathroom/vanity lighting, and bathroom
  accessories that are genuinely decorative under the normal rules.
- **STILL EXCLUDE**: bathroom furniture, storage, fixtures/fittings, plumbing, toilets,
  sinks, basins, taps/faucets, showers, bathtubs, bathroom hardware and utility products.

### 0.5 "Bedroom" and "Outdoor" are NOT blanket exclusions
- **INCLUDE**: bedroom lighting, bedroom mirrors, bedroom wall decor and decorative
  accessories; outdoor lighting of every kind, outdoor lanterns, decorative outdoor mirrors.
- **STILL EXCLUDE**: beds, bed frames, wardrobes, dressers, nightstands, bedroom furniture;
  outdoor/garden furniture, outdoor storage, garden utility products.

### 0.6 How Rule 0 interacts with the de-duplication rule (READ THIS)
De-duplication still matters, but **"it overlaps a product-type category" is NOT a reason
to skip a room-based category.** Resolve it this way:

- A site that presents **both** a type tree and a room tree is giving you two genuine nav
  branches. **Emit both**, each under its own parent grouping row, and state the overlap
  plainly in `notes`. The overlap belongs to the site's own taxonomy, not to your method.
- Only drop a node when it is the **same listing under a second URL at the same level**
  (e.g. Perigold's "All Mirrors" returning the identical population as "Wall Mirrors"), or
  a pure facet/filter re-cut (by colour, size, shape, material, price, style).
- When in doubt with a room node: **include it and document the overlap.** Under this rule
  a documented overlap is much better than a missing category.

---

## WORKSPACE RULE

**Work inside your OWN subdirectory: `scratchpad\w<SR>\`.** The only file you write to the
scratchpad **root** is your final `c<SR>.json`.

**WRITE `c<SR>.json` AS SOON AS YOU HAVE A COMPLETE RESULT — do not save it for the very
end.** Last batch three workers were killed mid-run by a rate limit; the two that had
already written their JSON kept all their work, the one that hadn't lost everything and
had to be resumed. If some categories are still unverified, write what you have with
`"status": "partial"` and flag them.

Never touch the user's project files (the `.xlsx` / `.xlsm` workbooks) — the orchestrator
merges.

---

## THE ONE RULE THAT MATTERS

**`qty` must be the EXACT number of products the website itself reports for that sub-category URL.**

- NEVER estimate, approximate, round, or infer a qty.
- NEVER copy a qty from a parent/sibling category.
- If you cannot verify the exact number, set `"qty": null` and
  `"flag": "MANUAL REVIEW: <specific reason>"`. A null is a *correct* answer.
- Every row must carry an `evidence` string: the literal text or JSON path that produced
  the number. A row with a qty but no evidence is invalid and will be nulled at merge.

Accuracy beats coverage. Beats speed. Always.

---

## RULE 1: VERIFY THE COUNT EMPIRICALLY — DON'T ASSUME EITHER WAY

**Measured INFLATED** (never trust unchecked): Shopify `/collections.json`
`products_count` (6 of 6 wrong) · Magento `categoryList.product_count` (169 vs 43 live) ·
Constructor.io `total_num_results` (**disputed** — 8 divergences originally, but a retest
reproduced the header exactly on 12 of 15 slugs).

**Measured EXACT under an exhaustion check** (batches 3–5, ~15 platforms): Target redsky ·
Marshalls & TJX Endeca `itemCount` · 1stDibs · Perigold RSC `resultCount` · Neiman Marcus ·
Cornerstone `UnbxdAPI` · One Kings Lane · Wix · Searchspring `pagination.totalResults` ·
Shopline · Dunelm `totalProducts` · John Lewis · Habitat · Beyond/Overstock `resultCount`.

**So: run the check, then use whichever number survives it.** Default to the rendered
"N items" header; a structured total that passes exhaustion is equally valid. Say in
`evidence` which you used and how you proved it.

Cheap proofs:
- tiles at `start=N-1`, **zero** at `start=N`; one page past the end 404s
- `ceil(total/pageSize)` equals the rendered page count — **but verify the page size is
  stable**; John Lewis A/B-tests 48 vs 72, which invalidates this check there
- children sum to roughly the parent
- enumerate to exhaustion and count unique product IDs

**COUNTING TILES BY HREF IS UNRELIABLE — it has now failed three ways:**
- **undercounts** when product slugs contain non-ASCII characters (Neiman Marcus 82 vs 90)
- **overcounts** when recommendation carousels inject links (Habitat 51 vs 48)
- **overcounts** when JSON-LD carries a next-page prefetch (Beyond: 81 tiles per 60-item page)
Use a structured product-ID field (JSON-LD ItemList, `data-product-id`, `"id":"prodN"`).

Also: **sponsored/PLA tiles** may be injected into the grid but excluded from the total
(Target, Dunelm). And counts can genuinely **drift during a session** — Dunelm's Ceiling
Lights moved 867 → 872 → 871; take several reads and flag it.

**The trap:** a worker once read a JS bundle, proved the code maps the API total to the
rendered header, and concluded they must be identical. They were not. *Reading the code
proves what the page renders, not what your request returns.*

Sites that publish **no count at all** are a legitimate outcome. Blank qty + a flag.

---

## RULE 2: NETWORK — HOW TO REACH BLOCKED SITES

**IPv4 egress is INTERMITTENT.** Test it, don't assume. **Never infer "unreachable" from a
missing AAAA record.**

1. **Direct fetch.** Try first — it carried half of last batch outright.
2. **`curl_cffi` impersonation. The winning profile is per-site: BRUTE-FORCE IT.** Mobile
   (`safari18_0_ios`) beat Marshalls and Ashley where all desktop profiles failed; the
   exact inverse held on Perigold. Neiman Marcus needed `safari17_0`; Frontgate/Ballard
   took `chrome124`/`chrome131`; John Lewis `chrome131`. Sweep 10+ profiles before
   concluding a site is blocked.
3. **`r.jina.ai/<url>`** — **percent-encode** the target URL if it has a multi-param query
   string or it 400s. Shared across all 10 of you and rate-limits under concurrency; a
   Cloudflare challenge usually means contention, so wait and retry.
4. **`translate.goog`** — `https://www-<domain-with-dashes>-com.translate.goog/<path>?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=en`.
   Returns genuine server-rendered origin HTML. **This was the ONLY route that worked for
   Bed Bath & Beyond last batch** after a 13-profile sweep failed. Can 429 for ~50 min.
5. **WebFetch** — renders past JS interstitials that curl cannot. It was the only thing
   that beat Nordstrom's ISTL interstitial after a **15-profile sweep failed**.
6. **UNPROTECTED SIDE DOORS — check before fighting the WAF:**
   - **Sitemaps**, almost always. Nordstrom's `navigation-sitemap.xml` gave the whole nav
     tree while every content route was interstitialed.
   - **Salesforce Commerce Cloud**: `/on/demandware.store/Sites-<siteid>-Site/default/Search-Refinebar?cgid=<slug>`
     and `Search-UpdateGrid` while SEO URLs 403.
   - **Wayfair-platform**: `seo-category-sitemap~0.xml`, `seo-sb0-sitemap~0.xml`.
   - **TJX**: `/store/sitewide/json/navMenuData.jsp` carries an `itemCount` per node.
   - **Cornerstone**: `SiteMap_CAT_00{1..4}_v2.xml` + `/UnbxdAPI?categoryId=<id>`.
   - **React mega-navs absent from HTML** are often embedded in the JS bundle (Z Gallerie).
7. **Akamai JS interstitials are often computable** — Zara Home's proof-of-work was inline
   JS; solver at `pipeline\final_list_batch_sn21-30\inditex_interstitial_solver.py`.
8. **Cloudflare IPv6 anycast pinning + `curl_cffi`** — cracked Wayfair.

**Sites hard-block by IP after sustained access.** Pace yourself; no retry storms.

**Keep canonical origin URLs in `link`.** Never a translate.goog, r.jina.ai, `m.<host>` or
Wayback URL. Checked at merge. Wayback is for STRUCTURE ONLY, never counts.

### DO NOT USE BROWSER AUTOMATION — 10 workers share one browser.

---

## RULE 3: A RETIRED OR REDIRECTED CATALOGUE IS A REAL ANSWER

Establish what the site actually IS before extracting: check redirects, read the sitemap,
look for a shutdown notice. Precedents: Kirkland's shut online shopping 2026-07-10;
HomeGoods has no e-commerce; `us.hay.com` 301s to dwr.com; `horchow.com` 302s wholesale to
neimanmarcus.com; John Lewis's roster URL 404s (department pages moved schemes);
bedbathandbeyond.com now runs Beyond Inc.'s ex-Overstock platform.

But **do not assume decline** — Habitat was expected to have folded into Argos and in fact
runs its own live storefront. Verify.

If the catalogue is genuinely gone: `"status": "ok"`, `"rows": []`, and a note with the
evidence. If it redirects to a different live catalogue, extract that and say so —
your links won't match the roster domain, which is fine when documented.

**This batch's roster:**

| S.N. | Company | Domain | Country |
|---|---|---|---|
| 71 | Brooklinen | brooklinen.com | USA |
| 72 | Burrow | burrow.com | USA |
| 73 | Joybird | joybird.com | USA |
| 74 | Macy's Home | macys.com/shop/home?id=22672 | USA |
| 75 | Lowe's Home Decor | lowes.com/c/Home-decor | USA |
| 76 | TJ Maxx Home | tjmaxx.tjx.com/store/index.jsp | USA |
| 77 | Urban Outfitters Home | urbanoutfitters.com/home | USA |
| 78 | Ferm Living US | fermliving.us | USA |
| 79 | Garnet Hill Home | garnethill.com | USA |
| 80 | Scully & Scully | scullyandscully.com | USA |

**Company-specific notes:**
- **S.N. 71 Brooklinen, S.N. 72 Burrow, S.N. 73 Joybird** are primarily bedding/textiles
  (Brooklinen), furniture (Burrow, Joybird) DTC brands — most or all of their catalogue may
  be out of scope. Check thoroughly for any lighting/mirror/decor-object line before
  concluding a low or zero-row result; a genuine zero/low count is still legitimate if
  that's really all they sell (same precedent as S.N. 69 The Inside, S.N. 70 Parachute Home
  from the prior batch, both correctly near-zero).
- **S.N. 74 Macy's Home and S.N. 75 Lowe's Home Decor** are department-store home sections
  inside much larger multi-category retailers — expect large numbers, verify carefully
  against inflation (these platforms' own count APIs have not been checked yet in this
  project; run the empirical exhaustion checks in Rule 1 rather than assuming a structured
  total is exact).
- **S.N. 76 TJ Maxx Home** may be another reading of the same contradictory roster row that
  S.N. 24 already resolved as HomeGoods (both are TJX-family off-price retailers, and a
  prior worker found a valid 6-row `tjmaxx.tjx.com` extraction while investigating S.N. 24,
  kept as `pipeline/final_list_batch_sn21-30/c24_alt_REJECTED_tjmaxx.json` and rejected as
  a duplicate reading at the time). Verify S.N. 76 independently as its own roster entry —
  it has its own S.N. and its own row in the master list, so treat it as a real target,
  but the earlier c24_alt file may be a useful (needs re-verification, don't just copy it)
  starting point since the site's structure won't have changed much.
- **S.N. 77 Urban Outfitters Home** — Urban Outfitters is a general apparel/lifestyle
  retailer; its Home department is usually a well-defined section, should have real
  lighting/mirror/decor categories to extract.

Site-specific access hints: TJX properties (TJ Maxx) hard-block by IP after sustained
access in this project's prior experience — budget roughly two page loads per cooldown
window, and check `/store/sitewide/json/navMenuData.jsp` (carries an `itemCount` per node)
and `/store/resources/xml/categorySiteMap.xml` as unprotected side doors before fighting
the WAF directly. Macy's and Lowe's have not been touched by this project before — start
fresh, no known access pattern to reuse.

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

Venv python: `"C:\Users\GyanendraVishwakarma\Web Research Agent\.venv - Copy\Scripts\python.exe"`
`probe.py count` **reports candidates, it does not decide.** Also available: WebFetch,
WebSearch, Bash/PowerShell with curl.

---

## WHAT TO EXTRACT

Only **real Home Decor product categories/sub-categories** — pages that list products.

### INCLUDE
- **Lighting — every fixture type and every room branch** (see Rule 0.1/0.2): pendant,
  wall, ceiling, floor, table, desk lamps, lanterns, chandeliers, flush mounts, sconces,
  lamp shades, recessed, track, cabinet, picture lights, vanity/bathroom lighting,
  outdoor and landscape lighting.
- **Mirrors — every type and every room** (see Rule 0.3).
- **Glassware (ALL — decorative AND functional)**: wine / champagne / whiskey / beer /
  cocktail / water / juice glasses, tumblers, tea & coffee cups, mugs, glass bowls,
  plates, trays, bottles, pitchers, jugs, containers, glass accessories.
- **Tableware / dinnerware**: plates, bowls, dinner sets, serveware, serving dishes,
  platters, trays, tabletop decor. File under `Kitchen & Dining`.
- **Decorative accessories**: decorative bowls / trays / plates, wall art, wall decor,
  vases, sculptures, figurines, decorative lanterns, candle holders, candles
  (unscented/decorative only), decorative planters & pots, centerpieces.
- **Clocks — ALL TYPES.** Wall, table, desk, alarm, mantel, decorative.
- **Decorative material lines**: decorative wooden, ceramic, resin, marble, stone, clay,
  terracotta, bamboo, cane, rattan.
- **Decorative metal**: metal wall art, metal sculptures, decorative metal bowls/trays,
  decorative lanterns, metal vases, metal-framed mirrors, decorative hooks, decorative
  wall racks/shelves, curtain rods, curtain tiebacks.
- **Decorative bathroom accessories** — only when genuinely decorative per the normal rules.

### EXCLUDE — never extract
- **Home Fragrance** — diffusers, room sprays, essential/aroma oils, wax melts, potpourri,
  incense, **scented candles**. **Read actual product titles before taking a "Candles"
  node.** Proven: World Market 73 of 107 scented; Perigold 81%; Dunelm 87%; Jonathan Adler
  and Caitlin Wilson 100%. Take unscented children (tapers, candle holders) where they
  exist as their own listing; drop the whole node where they don't.
- **Artificial / faux plants & flowers** — faux plants, artificial flowers, faux trees,
  greenery, wreaths, garlands, botanical decor.
- **Wallpaper and wall coverings** — settled by four workers independently.
- **Holiday & Gift** — Christmas, holiday collection, seasonal decor, gifts, gift sets.
- Bathroom furniture, storage, fixtures, fittings, plumbing, taps, sinks, showers, tubs,
  bathroom hardware *(but NOT bathroom mirrors or bathroom lighting — see Rule 0.4)*
- Furniture of every kind, indoor and outdoor
- Kitchen appliances, cookware, pots, pans, kitchen tools, flatware/cutlery, bar tools
- Hardware, plumbing, construction/building materials, home improvement, industrial
- Textiles (rugs, cushions, curtains, bedding, throws, tea towels, table linens)
- Food & drink consumables, cleaning products, personal care, garden tools/seeds
- Ceiling fans, light bulbs, wiring/mounting hardware

### NEVER EXTRACT — navigation/marketing, not product categories
Shop All · View All · Browse All · Explore All · See All · All Products · Discover ·
Collections / Collection · Featured · New Arrivals · New In · Best Sellers · Sale ·
Offers · Clearance · Outlet · Gift Guide · Lookbook · Blog · Journal · Magazine ·
Inspiration · Ideas · Stories · Designers · Brands · Trending · Recently Viewed ·
landing/promo pages. Brand/designer listing pages and price/colour filter pages are not
categories.

### DECISION RULE
The product's **primary purpose must be home decoration** — judged on **product type, not
room** (Rule 0). If a category primarily serves a functional, construction, storage,
hardware, furniture, plumbing or appliance purpose, skip it. If a category mixes
decorative and non-decorative items, extract only its decorative sub-categories.

**Mixed roll-ups: drop them, don't pad. Inspect actual product titles first.** Proven:
Blu Dot's `home-decor` (132) whose children summed to 90; Nordstrom's "Decorative Accents"
(7,928) which was a superset of two kept rows.

**Facet/material/shape re-cuts are the most common error — compare product-ID sets, never
names.** Proven: Jonathan Adler's entire POTTERY department was 100% contained in its
Decor/Dining equivalents; 1stDibs' "Decorative Lighting & Lamps" (17,324) was 1.7%
canonically its own; John Lewis's "Crystal glasses" spanned glasses, decanters, vases,
frames and clocks. A good trick: read the **canonical category inside each tile's own
product URL**. *(But re-read Rule 0.6 first — a ROOM branch is not a facet re-cut.)*

---

## HIERARCHY — PARENT GROUPING ROWS

If a category has child categories, emit a **parent grouping row** immediately before its
children:

```json
{"category":"Lighting","sub_category":"Lighting by Room","parent":true,
 "qty":null,"link":null,"evidence":null,"flag":null}
```

- Parent rows: `"parent": true`, **`qty` null, `link` null**. Never a URL or count.
- Only **leaf** (deepest) rows carry `qty` and `link`.
- Emit rows in navigation order: parent, then its children, then the next parent.
- **Nested levels each get their own parent row** — `Home Decor` → `Mirrors` →
  `Bathroom Mirrors` → `Vanity Mirrors` (leaf) is correct and fully supported.
- Do not create a parent row for a category with no children.

**Exception:** if a main category opens directly onto a product listing with no
sub-categories, emit ONE leaf row where `category` and `sub_category` are both that
category name, with qty and link.

---

## LANGUAGE / NAMING

- **Plain English only. No non-ASCII in `category` or `sub_category`** — no em-dashes, no
  curly quotes, and on UK sites **no GBP sign**.
- `category` should be a normalised English bucket, preferring: `Lighting`,
  `Kitchen & Dining`, `Home Accessories`, `Home Decor`, `Wall Decor & Mirrors`.
- Keep `sub_category` faithful to the site's own naming.

---

## OUTPUT CONTRACT

Write **one JSON file per company**, named `c<SR>.json`, into the scratchpad **root**.

```json
{
  "sr": 51, "company": "Made.com UK", "brand_site": "made.com", "country": "UK",
  "site_url": "https://www.made.com/", "status": "ok", "failure_reason": null,
  "notes": "Access route, how counts were verified, what was excluded and why.",
  "rows": [
    {"category":"Lighting","sub_category":"Lighting by Room","parent":true,
     "qty":null,"link":null,"evidence":null,"flag":null},
    {"category":"Lighting","sub_category":"Bathroom Lighting","parent":false,
     "qty":124,"link":"https://www.example.com/lighting/bathroom/",
     "evidence":"listing header text '124 Results'","flag":null}
  ]
}
```

- `sr`, `company`, `brand_site`, `country`: copy EXACTLY from your assignment.
- `status`: `"ok"` | `"partial"` | `"failed"`; `qty` integer or null, never a string;
  `link` absolute canonical origin URL, null on parents; `evidence` required with any qty.
- Failed company: `"rows": []` and a precise `failure_reason`.

In `notes` record: the access route that worked, how counts were verified, what you
excluded, **and any room/type overlap you documented under Rule 0.6.**

Validate: `python -c "import json;d=json.load(open('c51.json',encoding='utf-8'));print(len(d['rows']))"`

---

## WORKFLOW

1. `mkdir` your `w<SR>` subdirectory and work there.
2. Establish what the site actually is (Rule 3), then try a direct fetch; if blocked, work
   down Rule 2.
3. Find the full category tree — mega-menu, sitemap, nav API, or JS bundle.
4. Select qualifying categories. **Apply Rule 0: never skip on a room word.**
5. For each: open it, get the exact total, capture the canonical URL.
6. Verify the qty empirically (Rule 1), then record the row with its evidence.
7. Emit parent grouping rows so the hierarchy is visible.
8. **Write `c<SR>.json` to the scratchpad root as soon as it is complete.**

Aim for genuine coverage — typically 10–40 leaf rows for a large retailer, fewer for a
boutique. **Never invent rows to pad.**

## FINAL MESSAGE

Compact summary: SR, name, status, leaf count, parent count, nulls/flags, access route,
any failure reason — plus **what Rule 0 gained you** (which room-based lighting/mirror
categories you included that the old rules would have skipped). No prose padding.
