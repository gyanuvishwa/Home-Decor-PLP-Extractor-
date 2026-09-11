# WORKER BRIEF — Home Decor Category & Qty Extraction (Final_Company_List, S.N. 271-327)

You are ONE of a rolling pool of parallel extraction workers on this roster range. Read
this whole brief before starting. **This window is the India-market block (S.N. 271-314)
plus the final UK block (S.N. 315-327). Several literal-domain duplicates of
already-completed companies are flagged below — check those FIRST.**

**Scratchpad root:**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\be91bad7-b37a-4694-bdbe-c47fea1bb5d9\scratchpad`

**Work inside your own `w<SR>` subdirectory** (`mkdir` it first). Work synchronously
(foreground) — do not end your turn citing a background job, "cooldown," or "waiting for a
monitor"; wait for it in-turn. This has happened 10+ times on this project and always loses
progress — if you started a background fetch, either poll it yourself in a short in-turn
wait loop or switch to a synchronous approach entirely.

---

# RULE 0 — PRODUCT TYPE BEATS ROOM NAME (HIGHEST PRIORITY)

**NEVER exclude a category because of a ROOM word in its name.** Judge the **product type**.
- **0.1** Lighting organised by room is IN SCOPE — traverse every room node.
- **0.2** Traverse EVERY lighting branch, no depth limit. Still excluded: bulbs, ceiling
  fans, wiring hardware.
- **0.3** ALL mirrors are IN SCOPE, every type.
- **0.4/0.5** "Bathroom"/"Bedroom"/"Outdoor" are not blanket exclusions.
- **0.6** A site with both a type tree AND a room tree: emit both, document overlap. Only
  drop a node that's the exact same listing under a second URL, or a pure facet re-cut.

## WORKSPACE / OUTPUT RULES

Work in `scratchpad\w<SR>\`; only write `c<SR>.json` to the scratchpad **root**, as soon as
complete. Never touch the `.xlsx`/`.xlsm` workbooks.

## THE ONE RULE THAT MATTERS

`qty` must be the EXACT number the site itself reports. Never estimate/round/infer/copy
from a sibling. If you can't verify exactly, `"qty": null` + `"flag": "MANUAL REVIEW: ..."`.
Every qty needs `evidence`.

## RULE 1: VERIFY THE COUNT EMPIRICALLY

Shopify/Magento/Searchspring/Constructor.io/Algolia raw totals, and marketplace count
widgets that round to the nearest 100/1000 or cap at a page limit (confirmed on Noon UAE,
Etsy US), are NOT usable as exact qty — exhaustion-check everything, null+flag when a real
count is unobtainable. Watch for colour/variant records masquerading as product counts
(caught on Quince Home, Indigo Home, RoyalDesign) — always deduplicate to distinct products.
**Most India-market DTC brands in this window are Shopify** — `products_count` has been
inflated on essentially every Shopify site in this project (up to 230x on Rockett St
George), so never use it; enumerate product IDs instead.

## RULE 2: NETWORK — HOW TO REACH BLOCKED SITES

1. Direct fetch. 2. `curl_cffi` impersonation — brute-force 10+ profiles (the winning
profile is often unstable/rotating on Akamai-protected sites — don't assume a single lucky
hit means the block is solved). 3. `r.jina.ai/<url>`. 4. `translate.goog` (works well
against Imperva/Incapsula and Cloudflare managed challenges — but its own `/robots.txt` is
BOGUS for any domain, never trust it). 5. WebFetch. 6. Side doors: sitemaps, SFCC endpoints,
exposed Constructor.io/Algolia/Searchspring keys in `__NEXT_DATA__`/SSR state. 7. Akamai
solver for the Zara Home/Inditex platform:
`pipeline\final_list_batch_sn21-30\inditex_interstitial_solver.py` (has worked unmodified on
all 6 Zara Home country sites tried so far). 8. Cloudflare IPv6 anycast pinning + curl_cffi.
**DO NOT USE BROWSER AUTOMATION — the pool shares one browser.**

**If the ONLY working route is Wayback Machine, that is STRUCTURE ONLY, never counts** —
every qty sourced from an archived snapshot must be `null` + `MANUAL REVIEW`, never trusted
as a real count (S.N. 104/126/162/218 did this correctly; S.N. 223 got it wrong and had to
be corrected before merge — don't repeat that mistake).

## RULE 3: A RETIRED OR REDIRECTED CATALOGUE IS A REAL ANSWER

Check redirects / sitemap / shutdown notices before extracting; don't assume decline either.
Precedent: S.N. 193 Pottery Barn UAE and S.N. 198 West Elm UAE were both **permanently
closed Alshaya-run GCC franchises** — a franchised country storefront being dead is a real,
correct answer (`status: ok`, `rows: []`, documented). **This is directly relevant to S.N.
283 Pottery Barn India and S.N. 298 West Elm India in this window** — verify liveness before
assuming either way. Also sanity-check that a site is a genuine retailer, not a
liquidation/impersonation scam (S.N. 109 Alinea precedent) — a company-registration /
GST / legal-notices check is cheap.

**Check `robots.txt` for a Claude-specific disallow** before any WAF-bypass. Confirmed
cases: Made In Design, Home24 DE, El Corte Ingles, Amazon UAE, Amazon US (all named
ClaudeBot / Claude-User / Claude-SearchBot / Claude-Web with `Disallow: /`). **S.N. 316
Amazon UK in this window is very likely to carry the identical policy — check first and stop
if so.** Distinguish a real Claude-specific block from a bot-policy group that merely lists
Claude alongside everyone else with the SAME disallow list as `User-agent: *` (S.N. 132
Westwing IT precedent — that is not an opt-out, proceed).

---

## DUPLICATE-COMPANY FLAGS — CHECK THESE FIRST

- **S.N. 325 "Oliver Bonas"** (`oliverbonas.com`) — identical domain to already-completed
  **S.N. 96 "Oliver Bonas Home"** (`c96.json`, 32 leaf + 7 parent, `ok`). Read `c96.json`
  first. Almost certainly a duplicate: `"status": "ok"`, `"rows": []`, evidence in `notes`.
- **S.N. 320 "Etsy UK"** (`etsy.com`) — same bare domain as already-completed **S.N. 234
  "Etsy US"** (`c234.json`, `partial`). Etsy is one global marketplace with locale
  query/region params rather than separate country catalogues — verify whether a UK-scoped
  storefront produces genuinely different per-category counts (a `ship_to=GB` / `/uk/`
  region cut is a FACET of one marketplace, not a separate catalogue). Expect duplicate, but
  prove it before concluding.
- **S.N. 324 "La Redoute Interiors UK"** (`laredoute.co.uk`) — same domain as
  already-completed **S.N. 90 "La Redoute UK"** (`c90.json`, 23 leaf + 1 parent, `ok`).
  **This is NOT automatically a duplicate.** Direct precedent: **S.N. 106 "La Redoute
  Interieurs FR"** was judged genuinely distinct from S.N. 90 because it was scoped to the
  "La Redoute Interieurs" house-brand subset via a `?brndid=` filter — a materially
  different SCOPE of the same site, not a re-read. Read `c106.json` AND `c90.json` first and
  follow the c106 approach: extract the house-brand-filtered subset if that filter exists on
  the UK site. If no such brand filter exists on `laredoute.co.uk`, then it IS a duplicate of
  S.N. 90 — say so with evidence.
- **S.N. 286 "Zara Home India"** (`zarahome.com`) — six Zara Home rows already completed
  (S.N. 21 UAE, 98 UK, 116 DE, 127 ES, 153 Spain, 167 France), and every country pair
  checked so far has been genuinely INDEPENDENT (different store/catalog IDs, shared
  taxonomy IDs but different per-country populations). Expect a 7th independent catalogue —
  but verify via store/catalog ID rather than assuming. Use the Inditex solver above.
- **S.N. 287 "Home Centre India"** (`homecentre.in`) vs already-completed **S.N. 15 "Home
  Centre"** (`homecentre.com/ae/en/`, UAE — `c15.json`). Same Landmark Group brand, different
  ccTLD and country. Expect a genuinely separate India storefront (different currency/stock),
  but verify with platform/catalog evidence. Note `c15.json` has a known open item: a Baby &
  Kids decor tree deliberately left out — do NOT replicate that exclusion decision blindly,
  just follow this brief's scope rules.
- **S.N. 283 "Pottery Barn India"** (`potterybarn.in`) and **S.N. 298 "West Elm India"**
  (`westelm.in`) — distinct ccTLDs from the already-completed US rows (S.N. 3/244 Pottery
  Barn, S.N. 2/233 West Elm), so a franchised India storefront is plausible. **But see Rule 3
  above: the UAE franchises of both brands (S.N. 193, 198) turned out permanently closed.**
  Check liveness first; if the storefront is dead/redirecting, that is the answer.

**STANDING CONVENTION for ANY confirmed duplicate-company case** (two bugs already caught on
this project, don't repeat either): (1) use `"rows": []` — never re-populate the sibling's
rows, and (2) use `status: "ok"` for the duplicate reference row regardless of what status
the referenced source itself carries (even if the source is `Partial` or `failed`).

---

## THIS WINDOW'S FULL ROSTER

| S.N. | Company | Domain | Country |
|---|---|---|---|
| 271 | Nestasia | nestasia.in | India |
| 272 | Urban Ladder | urbanladder.com | India |
| 273 | Vaaree | vaaree.com | India |
| 274 | Westside Home | westside.com | India |
| 275 | WoodenStreet | woodenstreet.com | India |
| 276 | @home by Nilkamal | nilkamalhomes.com | India |
| 277 | Clay Craft India | claycraftindia.com | India |
| 278 | Ankur Lighting | ankurlighting.com | India |
| 279 | Borosil | myborosil.com | India |
| 280 | Fabindia | fabindia.com | India |
| 281 | Jainsons Lights | jainsonslightsonline.com | India |
| 282 | Nykaa Fashion Home | nykaafashion.com | India |
| 283 | Pottery Barn India | potterybarn.in | India |
| 284 | Pure Home + Living | purehomeandliving.com | India |
| 285 | Tata CLiQ Luxury Home | luxury.tatacliq.com | India |
| 286 | Zara Home India | zarahome.com | India |
| 287 | Home Centre India | homecentre.in | India |
| 288 | HomeStop | shoppersstop.com | India |
| 289 | Meesho Home & Kitchen | meesho.com | India |
| 290 | Wonderchef | wonderchef.com | India |
| 291 | Address Home | addresshome.com | India |
| 292 | Chumbak | chumbak.com | India |
| 293 | Ikiru | ikiru.in | India |
| 294 | Mason Home | masonhome.in | India |
| 295 | The Decor Kart | thedecorkart.com | India |
| 296 | Whispering Homes | whisperinghomes.com | India |
| 297 | ellementry | ellementry.com | India |
| 298 | West Elm India | westelm.in | India |
| 299 | The White Teak Company | whiteteak.com | India |
| 300 | The Bombay Store | thebombaystore.com | India |
| 301 | Beruru | beruru.com | India |
| 302 | Freedom Tree | freedomtree.in | India |
| 303 | Good Earth | goodearth.in | India |
| 304 | India Circus | indiacircus.com | India |
| 305 | Objectry | objectry.com | India |
| 306 | Oorjaa | oorjaa.in | India |
| 307 | Sarita Handa | saritahanda.com | India |
| 308 | The Purple Turtles | thepurpleturtles.com | India |
| 309 | Kapoor E-Illuminations | kapooreilluminations.com | India |
| 310 | Jaypore | jaypore.com | India |
| 311 | The Artment | theartment.com | India |
| 312 | Orange Tree | orangetree.in | India |
| 313 | Nicobar | nicobar.com | India |
| 314 | SPIN | spin.co.in | India |
| 315 | The Range | therange.co.uk | UK |
| 316 | Amazon UK | amazon.co.uk | UK |
| 317 | Wayfair UK | wayfair.co.uk | UK |
| 318 | Lakeland | lakeland.co.uk | UK |
| 319 | ProCook | procook.co.uk | UK |
| 320 | Etsy UK | etsy.com | UK |
| 321 | Argos Home | argos.co.uk | UK |
| 322 | Harrods Home | harrods.com | UK |
| 323 | Selfridges Home | selfridges.com | UK |
| 324 | La Redoute Interiors UK | laredoute.co.uk | UK |
| 325 | Oliver Bonas | oliverbonas.com | UK |
| 326 | Liberty London Home | libertylondon.com | UK |
| 327 | The Conran Shop | conranshop.co.uk | UK |

### Per-company expectations

- **Large Indian marketplaces** — S.N. 282 Nykaa Fashion Home, S.N. 285 Tata CLiQ Luxury
  Home, S.N. 289 Meesho Home & Kitchen, S.N. 288 HomeStop (on shoppersstop.com): scope
  STRICTLY to the Home/Decor department navigation, do NOT enumerate the whole site (same
  discipline as Target/Amazon/Walmart/Flipkart precedent). Marketplace count widgets often
  round or cap — Rule 1 applies hard.
- **Indian houseware/tableware manufacturers** — S.N. 277 Clay Craft, S.N. 279 Borosil,
  S.N. 290 Wonderchef: expect strong glassware/tableware/serveware coverage, minimal or zero
  lighting/mirrors (confirm absence via site search, don't just assume). Wonderchef is mostly
  cookware/appliances — expect a narrow in-scope slice.
- **Indian lighting specialists** — S.N. 278 Ankur Lighting, S.N. 281 Jainsons Lights,
  S.N. 299 The White Teak Company, S.N. 306 Oorjaa, S.N. 308 The Purple Turtles, S.N. 309
  Kapoor E-Illuminations: focused lighting catalogues, traverse every branch with no depth
  limit; exclude bulbs, fans, wiring.
- **Indian decor/lifestyle DTC brands** (mostly Shopify) — S.N. 271 Nestasia, S.N. 273
  Vaaree, S.N. 291 Address Home, S.N. 292 Chumbak, S.N. 293 Ikiru, S.N. 294 Mason Home,
  S.N. 295 The Decor Kart, S.N. 296 Whispering Homes, S.N. 297 ellementry, S.N. 301 Beruru,
  S.N. 302 Freedom Tree, S.N. 303 Good Earth, S.N. 304 India Circus, S.N. 305 Objectry,
  S.N. 310 Jaypore, S.N. 311 The Artment, S.N. 312 Orange Tree, S.N. 313 Nicobar, S.N. 314
  SPIN, S.N. 284 Pure Home + Living: expect solid decorative-accessory / tableware coverage.
  Rule 1 on Shopify `products_count` applies to every one of these.
- **Furniture-led Indian retailers** — S.N. 272 Urban Ladder, S.N. 275 WoodenStreet, S.N. 276
  @home by Nilkamal: core business is furniture (out of scope); expect a modest but real
  decor/lighting/mirrors footprint, same as the Burrow/Joybird/Loaf precedents.
- **Apparel-led with a home line** — S.N. 274 Westside Home, S.N. 280 Fabindia, S.N. 307
  Sarita Handa: mostly textiles (out of scope); extract only the genuine decor/lighting/
  tableware nodes, same discipline as Garnet Hill (S.N. 79).
- **UK block** — S.N. 315 The Range (large general discount retailer, big genuine decor
  footprint), S.N. 318 Lakeland and S.N. 319 ProCook (kitchenware specialists — narrow scope,
  tableware/glassware only, same discipline as Sur La Table), S.N. 321 Argos Home (general
  catalogue retailer, scope to Home & Garden department), S.N. 322 Harrods Home, S.N. 323
  Selfridges Home, S.N. 326 Liberty London Home (luxury department stores — expect a WAF,
  budget a full Rule 2 sweep, scope to the Home department only), S.N. 327 The Conran Shop
  (design retailer, expect solid lighting/decor coverage), S.N. 317 Wayfair UK (verify it is
  a genuinely separate catalogue from S.N. 1/221 Wayfair US via platform/catalog evidence —
  expect independent, but prove it).

---

## TOOLS

`probe.py` is in the scratchpad root, run from your own subdirectory:
```bash
python ..\probe.py get <url> [outfile]     # fetch, save, show status/size/title
python ..\probe.py nav <url>               # dump candidate category links
python ..\probe.py count <url>             # hunt product count
python ..\probe.py shopify <base> <handle> # count via /collections/<h>/products.json
python ..\probe.py shopifycolls <base>     # all collections + products_count
python ..\probe.py sitemap <base>          # sitemap index / robots sitemaps
python ..\probe.py json <url>              # fetch + pretty-print JSON
python ..\probe.py grep <file> <regex>     # regex a saved file with context
```
Venv python: `"C:\Users\GyanendraVishwakarma\Web Research Agent\.venv - Copy\Scripts\python.exe"`.
Also available: WebFetch, WebSearch, Bash/PowerShell with curl.

---

## WHAT TO EXTRACT

### INCLUDE
Lighting (every fixture type, every room), Mirrors (every type), Glassware (all —
decorative and functional), Tableware/dinnerware (file under Kitchen & Dining), Decorative
accessories (bowls, trays, wall art, vases, sculptures, figurines, candle holders,
unscented candles, planters, centerpieces), Clocks (all types), decorative
wood/ceramic/resin/marble/stone/rattan lines, decorative metal (wall art, sculptures,
hooks, racks, curtain rods/tiebacks), genuinely decorative bathroom accessories.

### EXCLUDE
Home Fragrance (diffusers, sprays, oils, incense, **scented candles** — read actual
titles), artificial/faux plants & flowers, wallpaper, Holiday & Gift, bathroom
furniture/storage/fixtures/plumbing (not mirrors/lighting), all furniture, kitchen
appliances/cookware/cutlery/bar tools, hardware/plumbing/DIY, textiles (incl. cushions,
throws, rugs, curtains, bed/bath linen), food/drink consumables, cleaning/personal care,
garden tools/seeds, ceiling fans, bulbs, wiring, apparel/jewellery/bags.

### NEVER EXTRACT
Shop All, Collections, Featured, New Arrivals, Best Sellers, Sale, Gift Guide, Blog,
Inspiration, Designers, Brands, Trending, brand/designer listing pages, filter pages.

**Mixed roll-ups: drop, don't pad — inspect actual titles.** **Facet/material/shape
re-cuts: compare product-ID sets, not names** (a genuine ROOM branch is not a facet re-cut).

## HIERARCHY

Parent row before children: `{"category":"Lighting","sub_category":"Lighting by Room","parent":true,"qty":null,"link":null,"evidence":null,"flag":null}`.
Only leaf rows carry qty/link. Nested levels each get their own parent row. Exception: a
childless category emits ONE leaf row (category == sub_category).

## LANGUAGE / NAMING

Plain English ASCII only in `category`/`sub_category`. India-market sites render in English
natively in almost every case (verify per-site); translate any Hindi/regional-language
category names into plain English if found. Original-language text is allowed inside
`evidence`/`notes` only.

## OUTPUT CONTRACT

One JSON file per company, `c<SR>.json`, in the scratchpad root:
```json
{
  "sr": 299, "company": "The White Teak Company", "brand_site": "whiteteak.com",
  "country": "India", "site_url": "https://www.whiteteak.com/", "status": "ok",
  "failure_reason": null,
  "notes": "Access route, count verification, exclusions, Rule 0.6 overlaps, duplicate-company determination if flagged.",
  "rows": [
    {"category":"Lighting","sub_category":"Lighting by Room","parent":true,"qty":null,"link":null,"evidence":null,"flag":null},
    {"category":"Lighting","sub_category":"Bathroom Lighting","parent":false,"qty":124,"link":"https://www.example.com/lighting/bathroom/","evidence":"listing header text '124 Results'","flag":null}
  ]
}
```
`status`: `"ok"`|`"partial"`|`"failed"`. `qty`: integer or null. `link`: absolute canonical
origin URL, null on parents. `evidence` required with any qty. Failed: `"rows": []` +
precise `failure_reason`.

**A company that's "mostly ok but a large fraction of qty came back null+flagged" should be
`status: "partial"`, not `"ok"`.** Reserve `"ok"` for extractions where qty is fully or
nearly-fully resolved.

Validate: `python -c "import json;d=json.load(open('c<SR>.json',encoding='utf-8'));print(len(d['rows']))"`

## FINAL MESSAGE

Compact: SR, name, status, leaf/parent counts, nulls/flags, access route, failure reason if
any, Rule 0 gains, duplicate-company determination with evidence if flagged.
