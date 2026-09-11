# WORKER BRIEF — Home Decor Category & Qty Extraction (Final_Company_List, S.N. 141–150)

You are one of 10 parallel extraction workers. Read this whole brief before starting.

**Scratchpad root:**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\5889af5e-4d19-4b75-84dd-1e4166afe96d\scratchpad`

**Work inside your own `w<SR>` subdirectory** (`mkdir` it first) — no prior attempt exists
for these companies, so you're starting fresh, not resuming.

**Work synchronously (foreground).** Do not launch a background shell fetch/job and end your
turn saying you're "waiting for it to finish" — the orchestrator cannot see or resume
background jobs a subagent started. This has happened repeatedly on this project (at least
5 confirmed cases). If something needs a cooldown, wait for it yourself in-turn, or fall
back to a different access route, then finish and write your `c<SR>.json` before ending
your turn.

---

# RULE 0 — PRODUCT TYPE BEATS ROOM NAME (HIGHEST PRIORITY)

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
end.** If some categories are still unverified, write what you have with
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
`products_count` (repeatedly wrong across dozens of prior batches) · Magento
`categoryList.product_count` · Searchspring `pagination.totalResults` (+1 on one prior
site).

**Measured EXACT under an exhaustion check** (many prior platforms): Target redsky ·
Marshalls & TJX Endeca `itemCount` · 1stDibs · Perigold RSC `resultCount` · Neiman Marcus ·
Cornerstone `UnbxdAPI` · One Kings Lane · Wix · Shopline · Dunelm `totalProducts` · John
Lewis · Habitat · Beyond/Overstock `resultCount` · IKEA search API.

**So: run the check, then use whichever number survives it.** Default to the rendered
"N items" header; a structured total that passes exhaustion is equally valid. Say in
`evidence` which you used and how you proved it.

Cheap proofs:
- tiles at `start=N-1`, **zero** at `start=N`; one page past the end 404s
- `ceil(total/pageSize)` equals the rendered page count — **but verify the page size is
  stable**
- children sum to roughly the parent
- enumerate to exhaustion and count unique product IDs

**COUNTING TILES BY HREF IS UNRELIABLE.** Use a structured product-ID field (JSON-LD
ItemList, `data-product-id`, `"id":"prodN"`).

Sites that publish **no count at all** are a legitimate outcome. Blank qty + a flag.

---

## RULE 2: NETWORK — HOW TO REACH BLOCKED SITES

**IPv4 egress is INTERMITTENT.** Test it, don't assume. **Never infer "unreachable" from a
missing AAAA record.**

1. **Direct fetch.** Try first.
2. **`curl_cffi` impersonation. The winning profile is per-site: BRUTE-FORCE IT.** Sweep
   10+ profiles before concluding a site is blocked.
3. **`r.jina.ai/<url>`** — **percent-encode** the target URL if it has a multi-param query
   string or it 400s. Shared across all 10 of you and rate-limits under concurrency; a
   Cloudflare challenge usually means contention, so wait and retry.
4. **`translate.goog`** — `https://www-<domain-with-dashes>-com.translate.goog/<path>?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=en`.
   Returns genuine server-rendered origin HTML. Can 429 for ~50 min.
5. **WebFetch** — renders past JS interstitials that curl cannot.
6. **UNPROTECTED SIDE DOORS — check before fighting the WAF:**
   - **Sitemaps**, almost always.
   - **Salesforce Commerce Cloud**: `/on/demandware.store/Sites-<siteid>-Site/default/Search-Refinebar?cgid=<slug>`
     and `Search-UpdateGrid` while SEO URLs 403.
   - **Wayfair-platform**: `seo-category-sitemap~0.xml`, `seo-sb0-sitemap~0.xml`.
   - **TJX**: `/store/sitewide/json/navMenuData.jsp` carries an `itemCount` per node.
   - **Cornerstone**: `SiteMap_CAT_00{1..4}_v2.xml` + `/UnbxdAPI?categoryId=<id>`.
   - **React mega-navs absent from HTML** are often embedded in the JS bundle.
7. **Akamai JS interstitials are often computable** — Zara Home's proof-of-work was inline
   JS; solver at `pipeline\final_list_batch_sn21-30\inditex_interstitial_solver.py`.
8. **Cloudflare IPv6 anycast pinning + `curl_cffi`.**

**Sites hard-block by IP after sustained access.** Pace yourself; no retry storms.

**Keep canonical origin URLs in `link`.** Never a translate.goog, r.jina.ai, `m.<host>` or
Wayback URL. Checked at merge. Wayback is for STRUCTURE ONLY, never counts.

### DO NOT USE BROWSER AUTOMATION — 10 workers share one browser.

---

## RULE 3: A RETIRED OR REDIRECTED CATALOGUE IS A REAL ANSWER

Establish what the site actually IS before extracting: check redirects, read the sitemap,
look for a shutdown notice, verify real registration/legal notices (this caught a scam
domain at S.N. 109 Alinea previously — French "LIQUIDATION TOTALE" language, no SIRET; and
a legitimate-but-absorbed case at S.N. 133 Coincasa, which now 301s into coin.it).

But **do not assume decline** — verify, don't guess either way.

If the catalogue is genuinely gone: `"status": "ok"`, `"rows": []`, and a note with the
evidence. If it redirects to a different live catalogue, extract that and say so —
your links won't match the roster domain, which is fine when documented.

**Check `robots.txt` for a Claude-specific disallow** (`ClaudeBot`, `anthropic-ai`,
`Claude-Web`) before any WAF-bypass attempt — this caught real cases at Made In Design,
Home24 DE, and El Corte Ingles previously. If found, mark `failed` with the finding as the
reason rather than bypassing it. **Important nuance, confirmed on S.N. 132 Westwing IT**:
a bot-policy group that simply LISTS ClaudeBot alongside other AI crawlers is NOT itself a
block — check whether that group's `Disallow` list is actually MORE RESTRICTIVE than the
generic `User-agent: *` group. If it's the same list (standard duplicate-content SEO
exclusions applied evenly to all crawlers), it's not a Claude-specific opt-out — proceed
normally. Only a `Disallow: /` (or similar, materially broader restriction) that singles
out ClaudeBot/anthropic-ai/Claude-Web/Claude-User specifically is the real opt-out to
respect.

**This batch's roster:**

| S.N. | Company | Domain | Country |
|---|---|---|---|
| 141 | Mömax Germany | moemax.de | Germany |
| 142 | XXXLutz Germany | xxxlutz.de | Germany |
| 143 | Castorama France | castorama.fr | France |
| 144 | OTTO Home | otto.de | Germany |
| 145 | DEPOT | depot-online.de | Germany |
| 146 | JYSK Denmark | jysk.dk | Denmark |
| 147 | Leroy Merlin France | leroymerlin.fr | France |
| 148 | Xenos | xenos.nl | Netherlands |
| 149 | Nordic Nest | nordicnest.com | Sweden |
| 150 | RoyalDesign | royaldesign.com | Sweden |

**Company-specific notes — READ BEFORE STARTING:**

- **S.N. 142 XXXLutz Germany is very likely THE SAME COMPANY as S.N. 115 "XXXLutz DE"**
  (`c115.json` in the scratchpad root — 158 leaf + 29 parent, `ok`, the largest single
  extraction in the project so far), which the roster already lists with the identical
  domain `xxxlutz.de`. **Your first step, before any extraction work**: read `c115.json`
  and confirm this is genuinely the same catalogue (same domain, same locale, no distinct
  scope). If confirmed identical, follow the established project precedent for
  duplicate-company rows (S.N. 82 OKA, S.N. 85 Overstock, S.N. 88 Cost Plus World Market,
  S.N. 137 John Lewis & Partners in the prior batch): `"status": "ok"`, `"rows": []`, and
  document the match with concrete evidence in `notes` — do NOT re-extract from scratch.
  Only do a fresh full extraction if you find genuine evidence of a materially different
  scope. **Note this is a different case from S.N. 141 Momax Germany** — Momax and XXXLutz
  are sister brands under the same parent group (Lutz) but are separate storefronts with
  separate domains (moemax.de vs xxxlutz.de); do not assume S.N. 141 is also a duplicate
  just because of the corporate relationship — verify S.N. 141 independently as a fresh
  extraction, only S.N. 142 has the exact roster-domain match with an existing S.N.
- **S.N. 146 JYSK Denmark is the project's first Danish-market company** and **S.N. 149
  Nordic Nest / S.N. 150 RoyalDesign are the project's first Swedish-market companies.**
  See the LANGUAGE/NAMING section below — translate Danish/Swedish category names into
  plain English; this approach has now proven out cleanly across French, German, Dutch,
  Spanish and Italian batches, so apply the same method here. Budget extra time for
  unfamiliar UI vocabulary (Danish/Swedish differ enough from the Germanic languages seen
  so far that some category names may need extra care to translate accurately — verify
  against product images/titles if a translation is ambiguous).
- **S.N. 144 OTTO Home and S.N. 145 DEPOT** are large/mid-size German multi-category
  retailers — OTTO is one of Germany's largest general e-commerce platforms (expect a
  large but possibly noisy catalogue requiring careful mixed-roll-up filtering, similar to
  El Corte Ingles or Bloomingdale's); DEPOT is a dedicated home-decor specialty chain
  (expect strong, focused decor coverage).
- **S.N. 143 Castorama France and S.N. 147 Leroy Merlin France** are both large French DIY/
  home-improvement chains (Castorama and Leroy Merlin are both Kingfisher/ADEO-family
  competitors) — expect the bulk of the catalogue to be out-of-scope hardware/building
  materials/tools, with a comparatively narrow genuine decor sub-tree (lighting, mirrors,
  decorative accessories) to find and extract carefully; don't pad with functional DIY
  categories.
- **S.N. 141 Mömax Germany and S.N. 148 Xenos** are no-precedent companies in this project
  — Momax is a value-priced furniture/homeware chain (sister brand to XXXLutz, see above);
  Xenos is a Dutch discount/lifestyle variety chain. Budget time for a fresh Rule 2
  access-route discovery sweep on each.
- **S.N. 149 Nordic Nest and S.N. 150 RoyalDesign** are both online marketplaces for
  Scandinavian design brands (overlapping catalogues of third-party Nordic design labels
  sold as first-party inventory) — expect large multi-brand catalogues with genuine, likely
  substantial, lighting/mirror/decorative-accessory coverage; verify whether these two
  sites' catalogues themselves overlap with each other significantly (both are Nordic
  design multi-brand retailers) — if you find major cross-listing between them worth
  documenting, note it, but do NOT treat them as a duplicate-company pair without
  buyer/seller/legal-entity verification (multiple marketplaces legitimately carrying the
  same third-party brand's products is normal and different from the single-owner-two-
  domains cases like S.N. 142).

Given how often this project's roster has produced same-domain or corporate-sibling
near-duplicates, **apply the same scrutiny used in every recent batch**: read the earlier
company's worker JSON before assuming a different roster row means a different site, but
don't assume duplication either — prove it either way with concrete evidence (store/catalog
IDs, schema.org metadata, product-ID overlap, currency + locale).

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
  node.** Take unscented children (tapers, candle holders) where they exist as their own
  listing; drop the whole node where they don't.
- **Artificial / faux plants & flowers** — faux plants, artificial flowers, faux trees,
  greenery, wreaths, garlands, botanical decor.
- **Wallpaper and wall coverings.**
- **Holiday & Gift** — Christmas, holiday collection, seasonal decor, gifts, gift sets.
- Bathroom furniture, storage, fixtures, fittings, plumbing, taps, sinks, showers, tubs,
  bathroom hardware *(but NOT bathroom mirrors or bathroom lighting — see Rule 0.4)*
- Furniture of every kind, indoor and outdoor
- Kitchen appliances, cookware, pots, pans, kitchen tools, flatware/cutlery, bar tools
- Hardware, plumbing, construction/building materials, home improvement, industrial
  **(especially relevant for S.N. 143 Castorama and S.N. 147 Leroy Merlin — DIY chains)**
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

**Mixed roll-ups: drop them, don't pad. Inspect actual product titles first.**

**Facet/material/shape re-cuts are the most common error — compare product-ID sets, never
names.** A good trick: read the **canonical category inside each tile's own
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
  curly quotes, no accented characters, and on UK sites **no GBP sign**.
- `category` should be a normalised English bucket, preferring: `Lighting`,
  `Kitchen & Dining`, `Home Accessories`, `Home Decor`, `Wall Decor & Mirrors`.
- Keep `sub_category` faithful to the site's own naming **translated into plain English** —
  this batch includes German (S.N. 141, 142, 144, 145), French (S.N. 143, 147), Danish
  (S.N. 146), Dutch (S.N. 148), and English-native Swedish sites (S.N. 149, 150 — verify
  which locale/language actually renders before assuming translation is needed; Nordic
  design retailers often default to English for international customers). Translate the
  site's own German/French/Danish/Dutch category name into natural English (e.g.
  `Beleuchtung`/`Eclairage`/`Belysning`/`Verlichting` -> `Lighting`,
  `Spiegel`/`Miroirs`/`Spejle`/`Spiegels` -> `Mirrors`, `Vasen`/`Vases`/`Vaser`/`Vazen` ->
  `Vases`); do not leave non-English text or accented characters in
  `category`/`sub_category`. This translate-to-English approach has now proven out cleanly
  across French, German, Dutch, Spanish and Italian batches — same method applies here.
  `evidence` and `notes` may quote the original-language text/UI strings for verification
  purposes, but `category`/`sub_category` themselves must be ASCII-only English strings,
  same as every other company in this project.

---

## OUTPUT CONTRACT

Write **one JSON file per company**, named `c<SR>.json`, into the scratchpad **root**.

```json
{
  "sr": 146, "company": "JYSK Denmark", "brand_site": "jysk.dk", "country": "Denmark",
  "site_url": "https://jysk.dk/", "status": "ok", "failure_reason": null,
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
excluded, **and any room/type overlap you documented under Rule 0.6**, and for S.N. 142
specifically, the duplicate-company determination and evidence either way.

Validate: `python -c "import json;d=json.load(open('c<SR>.json',encoding='utf-8'));print(len(d['rows']))"`

---

## WORKFLOW

1. `mkdir` your `w<SR>` subdirectory and work there.
2. Establish what the site actually is (Rule 3), then try a direct fetch; if blocked, work
   down Rule 2. For S.N. 142, first read the referenced prior `c115.json` and decide on
   duplication before doing full extraction work.
3. Find the full category tree — mega-menu, sitemap, nav API, or JS bundle.
4. Select qualifying categories. **Apply Rule 0: never skip on a room word.**
5. For each: open it, get the exact total, capture the canonical URL.
6. Verify the qty empirically (Rule 1), then record the row with its evidence.
7. Emit parent grouping rows so the hierarchy is visible.
8. **Write `c<SR>.json` to the scratchpad root as soon as it is complete.**

Aim for genuine coverage — typically 10–40 leaf rows for a large retailer, fewer for a
boutique, possibly more for large multi-category marketplaces. **Never invent rows to pad.**

## FINAL MESSAGE

Compact summary: SR, name, status, leaf count, parent count, nulls/flags, access route,
any failure reason — plus **what Rule 0 gained you** (which room-based lighting/mirror
categories you included that the old rules would have skipped). No prose padding.
