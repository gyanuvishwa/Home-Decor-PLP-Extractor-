# WORKER BRIEF — Home Decor Category & Qty Extraction (Final_Company_List, S.N. 151-170)

You are ONE of a rolling pool of parallel extraction workers on this roster range. Read
this whole brief before starting. **This batch is unusually duplicate-heavy — roughly half
the companies here are re-listings of a company already extracted under an earlier S.N.
Do the duplicate-check step FIRST for any company flagged below before doing any real
extraction work; do not extract first and check later.**

**Scratchpad root:**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\5889af5e-4d19-4b75-84dd-1e4166afe96d\scratchpad`

**Work inside your own `w<SR>` subdirectory** (`mkdir` it first). Work synchronously
(foreground) — do not end your turn citing a background job; wait for it in-turn. This has
happened repeatedly on this project (5+ confirmed cases) and always loses progress.

---

# RULE 0 — PRODUCT TYPE BEATS ROOM NAME (HIGHEST PRIORITY)

**NEVER exclude a category because of a ROOM word in its name.** Room words — Bathroom,
Bedroom, Living Room, Dining Room, Kitchen, Entryway, Hallway, Office, Outdoor, Vanity —
describe *where a product is used*, never whether it's in scope. Judge the **product type**.

- **0.1** Lighting organised by room is IN SCOPE — traverse every room node (incl.
  Bathroom/Vanity/Outdoor/Landscape).
- **0.2** Traverse EVERY lighting branch, no depth limit (recessed, track, cabinet,
  picture lights, outdoor/landscape included). Still excluded: bulbs, ceiling fans, wiring
  hardware.
- **0.3** ALL mirrors are IN SCOPE, every type (bathroom, vanity, makeup, LED/backlit,
  full-length, etc).
- **0.4/0.5** "Bathroom"/"Bedroom"/"Outdoor" are not blanket exclusions — include the
  decorative items (mirrors, lighting, wall decor), still exclude furniture/storage/
  fixtures/plumbing/hardware.
- **0.6** A site with both a type tree AND a room tree: emit both, document the overlap in
  `notes`. Only drop a node that's the exact same listing under a second URL, or a pure
  facet re-cut (colour/size/shape/material/price/style).

---

## WORKSPACE / OUTPUT RULES

- Work in `scratchpad\w<SR>\`; only write `c<SR>.json` to the scratchpad **root**.
- Write `c<SR>.json` as soon as you have a complete result — don't save it for the end.
- Never touch the `.xlsx`/`.xlsm` workbooks — the orchestrator merges.

## THE ONE RULE THAT MATTERS

`qty` must be the EXACT number the site itself reports. Never estimate/round/infer/copy
from a sibling. If you can't verify it exactly, `"qty": null` + `"flag": "MANUAL REVIEW: ..."`
— that's a correct answer. Every qty needs an `evidence` string or it gets nulled at merge.

## RULE 1: VERIFY THE COUNT EMPIRICALLY

**Measured INFLATED, never trust unchecked**: Shopify `/collections.json` `products_count`,
Magento `categoryList.product_count`, Searchspring `pagination.totalResults` (+1 seen once).
**Measured EXACT under an exhaustion check**: Target redsky, TJX Endeca, 1stDibs, Perigold
RSC, Cornerstone UnbxdAPI, Dunelm `totalProducts`, IKEA search API, and many more — always
run the check, don't assume either way.

Cheap proofs: tiles at `start=N-1` zero at `start=N`; `ceil(total/pageSize)==pageCount`
(verify page size is stable); children sum to ~parent; enumerate to exhaustion counting
unique product IDs.

**Counting tiles by href is unreliable** — use a structured product-ID field.

**Watch for space-style thousands separators (French/Nordic sites)** — e.g. "8 682" using
U+202F or U+00A0 as the separator. `probe.py`'s `count` command was JUST FIXED
(2026-08-11) to handle these after it silently truncated "8 682 produits" to 682 on
Castorama France — if you use the tool it should now be correct, but still cross-check any
suspiciously-small count on a French/Nordic/German site with a raw text read, since the fix
is new and unverified at scale.

## RULE 2: NETWORK — HOW TO REACH BLOCKED SITES

1. Direct fetch first. 2. `curl_cffi` impersonation — brute-force 10+ profiles, the winner
is per-site. 3. `r.jina.ai/<url>` (percent-encode multi-param URLs). 4. `translate.goog`.
5. WebFetch (renders past JS interstitials). 6. Side doors: sitemaps almost always;
Salesforce Commerce Cloud `Search-Refinebar`/`Search-UpdateGrid`; TJX `navMenuData.jsp`;
Cornerstone `UnbxdAPI`; React mega-navs in the JS bundle. 7. Akamai proof-of-work is often
computable — Zara Home's solver at
`pipeline\final_list_batch_sn21-30\inditex_interstitial_solver.py` has worked unmodified on
every Zara Home country site tried (5 for 5 so far). 8. Cloudflare IPv6 anycast pinning +
curl_cffi.

Sites hard-block by IP after sustained access — pace yourself, no retry storms. Keep
canonical origin URLs in `link` (never translate.goog/r.jina.ai/Wayback). Wayback is
structure-only, never counts. **DO NOT USE BROWSER AUTOMATION — the pool shares one browser.**

## RULE 3: A RETIRED OR REDIRECTED CATALOGUE IS A REAL ANSWER

Check redirects, sitemap, shutdown notices, legal/registration info before extracting.
Don't assume decline either — verify. If gone: `"status":"ok"`, `"rows":[]` + evidence in
notes. If redirected to a different live catalogue: extract that, document the mismatch.

**Check `robots.txt` for a Claude-specific disallow** before any WAF-bypass. Real cases so
far: Made In Design (`anthropic-ai`/`ClaudeBot`/`Claude-Web`), Home24 DE (`ClaudeBot`
specifically), El Corte Ingles (`ClaudeBot` + `Claude-User` site-wide). **Nuance confirmed
on Westwing IT**: a bot-policy group merely LISTING ClaudeBot alongside other AI crawlers
is not itself a block — only proceed-vs-respect based on whether that group's `Disallow`
list is MORE RESTRICTIVE than the generic `User-agent: *` group.

---

## DUPLICATE-COMPANY / KNOWN-ISSUE FLAGS — CHECK THESE FIRST

This roster range has an unusually high rate of re-listed companies. For every flagged S.N.
below, **your first step is reading the referenced prior `c<N>.json` in the scratchpad
root** and making a documented determination — do not extract first.

- **S.N. 151 Maisons du Monde France** — same domain (`maisonsdumonde.com`) and same
  country as already-completed **S.N. 104 "Maisons du Monde FR"** (`Partial`,
  DataDome-blocked, 36 leaf all null+flagged). Read `c104.json` first. If genuinely the
  same catalogue/scope, this is a duplicate-company case (`rows: []`, document it) — BUT
  since S.N. 104 itself was only `Partial` (structure recovered, no verified qty), consider
  whether a fresh attempt might succeed where the old one didn't (DataDome blocks have
  sometimes cleared between sessions on this project). Use judgment: if you get further
  than c104 did, extract properly and note the improvement; if you hit the identical
  DataDome wall, treat it as either a duplicate reference to c104's structure or a fresh
  `Partial`, whichever the evidence supports — just don't silently re-do a full independent
  extraction if the underlying catalogue is confirmed identical AND still blocked the same way.
- **S.N. 153 Zara Home Spain** — same domain (`zarahome.com`) and same country as
  already-completed **S.N. 127 "Zara Home ES"** (36 leaf + 5 parent, `ok`, store
  84009900/catalog 80290093). Read `c127.json` first. This is very likely a literal
  duplicate roster row for the exact same catalogue — confirm via store/catalog ID match,
  then treat as duplicate (`rows: []`, document) rather than re-extracting.
- **S.N. 156 IKEA Germany** — same domain (`ikea.com`) and same country as
  already-completed **S.N. 117 "IKEA DE"** (58 leaf + 10 parent, `ok`). Read `c117.json`
  first. Very likely a literal duplicate roster row — confirm via locale path
  (`ikea.com/de/de/`) match, then treat as duplicate.
- **S.N. 159 home24 Germany** — same domain (`home24.de`) as already-completed **S.N. 113
  "Home24 DE"**, which is `failed` because `robots.txt` names `ClaudeBot` with a
  Claude-specific `Disallow: /`. Read `c113.json` first. Do a quick fresh robots.txt check
  (policies occasionally change) but expect the same finding — if confirmed identical
  policy block, mark `failed` with the same reasoning rather than attempting a bypass or a
  full re-extraction.
- **S.N. 161 Made In Design** — this exact site (`madeindesign.com`) was already
  characterized in this project's memory as robots.txt-blocking `anthropic-ai`, `ClaudeBot`,
  and `Claude-Web` explicitly (an earlier carry-forward note, not yet its own roster S.N.
  until now). Do a fresh robots.txt check to confirm the disallow still stands, then mark
  `failed` with that finding as the reason — do not attempt a WAF bypass around a
  Claude-specific opt-out.
- **S.N. 162 BHV Marais Maison** (`bhv.fr`) — already characterized as a site-wide
  Cloudflare managed challenge in this project's memory, with a verified 588-path Maison URL
  tree already recovered and sitting in `pipeline/c37.json`'s `notes` field as a ready retry
  map (from an early-batch carry-forward, separate from the actual S.N. 37 company). Read
  that structure first — it may save significant rediscovery time — then attempt Rule 2's
  full access sweep for counts; if still blocked, write `Partial` with the structure and
  null+flagged qty rather than abandoning it.
- **S.N. 164 KARE Design** — likely the same company as already-completed **S.N. 119
  "KARE"** (Germany, 27 leaf + 5 parent, `ok`). Read `c119.json` first and confirm the
  `brand_site` domain matches (`kare-design.com` or similar) before deciding — if
  confirmed identical, treat as duplicate; if S.N. 119 was scoped differently (e.g. a
  different country/locale), extract fresh and document why.
- **S.N. 165 La Redoute Interieurs France** — same domain (`laredoute.fr`) and same brand
  scope as already-completed **S.N. 106 "La Redoute Interieurs FR"** (23 leaf + 2 flagged +
  5 parent, `ok`, scoped via a `?brndid=` filter). Read `c106.json` first — very likely a
  literal duplicate roster row.
- **S.N. 166 Westwing Germany** — same domain (`westwing.de`) as already-completed **S.N.
  112 "Westwing DE"** (65 leaf + 11 parent, `ok`). Read `c112.json` first — very likely a
  literal duplicate roster row.
- **S.N. 168 vtwonen Shop** — domain given as bare `vtwonen.nl`, which S.N. 122's own
  findings (`c122.json`) already established redirects/gates behind a JS consent wall, with
  the REAL storefront living at `shop.vtwonen.nl` ("vtwonen by fonQ") — the exact catalogue
  S.N. 122 already extracted (32 leaf + 3 parent, `ok`). Read `c122.json` first; very likely
  a literal duplicate roster row under a different display name.

**Companies below are NOT flagged as duplicates but sit close enough to existing
extractions to warrant a quick sanity check before assuming independence** (read the
referenced file, confirm distinctness via store/catalog ID, currency, or product-ID
overlap, same discipline as every prior country-sibling case in this project — Zara Home,
IKEA, Westwing, H&M Home have all had both TRUE-duplicate and TRUE-independent outcomes,
so never assume either way):
- **S.N. 154 H&M Home France** vs S.N. 97 UK (`c97.json`, Partial) and S.N. 134 IT
  (`c134.json`, ok) — same `www2.hm.com/<locale>/home.html` pattern, expect genuinely
  separate per prior 2-for-2 precedent, but verify.
- **S.N. 155 IKEA France** vs S.N. 100 UK / S.N. 117 DE / S.N. 156 (this batch) — expect
  genuinely separate (IKEA's per-country pattern is 2-for-2 independent so far), verify via
  locale path and category-ID scoping differences (S.N. 117 already found one DE/UK
  scoping difference on Wall Clocks).
- **S.N. 167 Zara Home France** vs S.N. 21 UAE / 98 UK / 116 DE / 127 ES / 153 (this batch,
  if not a duplicate) — expect a genuinely separate 5th-or-6th country catalogue (4-for-4
  independent so far on this platform), verify store/catalog ID.
- **S.N. 170 Ferm Living** (bare `fermliving.com`, likely global/EU site) vs S.N. 78 "Ferm
  Living US" (`c78.json`, 20 leaf + 3 parent, `ok`) — check whether this is a genuinely
  separate EU/global catalogue or the same brand's US site under a different locale path;
  don't assume either way (this project has seen both outcomes on "bare domain vs. country
  roster row" cases — S.N. 137/142/156/165/166 turned out to be true duplicates, S.N. 138
  Anthropologie UK turned out to be genuinely distinct despite an identical bare domain).

---

## THIS BATCH'S FULL ROSTER

| S.N. | Company | Domain | Country |
|---|---|---|---|
| 151 | Maisons du Monde France | maisonsdumonde.com | France |
| 152 | Mango Home | shop.mango.com | Spain |
| 153 | Zara Home Spain | zarahome.com | Spain |
| 154 | H&M Home France | www2.hm.com | France |
| 155 | IKEA France | ikea.com | France |
| 156 | IKEA Germany | ikea.com | Germany |
| 157 | Monoprix Maison | monoprix.fr | France |
| 158 | Sostrene Grene | sostrenegrene.com | Denmark |
| 159 | home24 Germany | home24.de | Germany |
| 160 | Finnish Design Shop | finnishdesignshop.com | Finland |
| 161 | Made In Design | madeindesign.com | France |
| 162 | BHV Marais Maison | bhv.fr | France |
| 163 | Galeries Lafayette Maison | galerieslafayette.com | France |
| 164 | KARE Design | kare-design.com | Germany |
| 165 | La Redoute Interieurs France | laredoute.fr | France |
| 166 | Westwing Germany | westwing.de | Germany |
| 167 | Zara Home France | zarahome.com | France |
| 168 | vtwonen Shop | vtwonen.nl | Netherlands |
| 169 | Normann Copenhagen | normann-copenhagen.com | Denmark |
| 170 | Ferm Living | fermliving.com | Denmark |

**No-precedent companies, budget a fresh Rule 2 access sweep**: S.N. 152 Mango Home
(Spanish fashion retailer's home line), S.N. 157 Monoprix Maison (French supermarket-chain
home department, likely narrow scope), S.N. 158 Sostrene Grene (Danish variety/lifestyle
chain, first Danish company after JYSK — likely solid decor coverage), S.N. 160 Finnish
Design Shop (first Finnish company, Nordic multi-brand design marketplace like Nordic
Nest/RoyalDesign — expect large catalogue), S.N. 163 Galeries Lafayette Maison (French
department store, may need Wayback/side-door workarounds like other department-store
platforms seen in this project), S.N. 169 Normann Copenhagen (Danish design brand, DTC).

---

## TOOLS

`probe.py` is in the scratchpad root, run from your own subdirectory:
```bash
python ..\probe.py get <url> [outfile]     # fetch, save, show status/size/title
python ..\probe.py nav <url>               # dump candidate category links
python ..\probe.py count <url>             # hunt product count (JUST FIXED for space-separated thousands)
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
Lighting (every fixture type, every room — see Rule 0), Mirrors (every type — Rule 0.3),
Glassware (all — decorative and functional: glasses, tumblers, mugs, bowls, plates, trays,
bottles), Tableware/dinnerware (file under Kitchen & Dining), Decorative accessories (bowls,
trays, wall art, vases, sculptures, figurines, candle holders, unscented candles, planters,
centerpieces), Clocks (all types), decorative wood/ceramic/resin/marble/stone/rattan lines,
decorative metal (wall art, sculptures, hooks, racks, curtain rods/tiebacks), genuinely
decorative bathroom accessories.

### EXCLUDE
Home Fragrance (diffusers, room sprays, oils, wax melts, incense, **scented candles** — read
actual titles), artificial/faux plants & flowers, wallpaper/wall coverings, Holiday & Gift,
bathroom furniture/storage/fixtures/plumbing (not mirrors/lighting), all furniture, kitchen
appliances/cookware/cutlery/bar tools, hardware/plumbing/DIY/construction materials, textiles
(rugs, cushions, curtains, bedding, linens), food/drink consumables, cleaning/personal care,
garden tools/seeds, ceiling fans, bulbs, wiring hardware.

### NEVER EXTRACT (nav/marketing)
Shop All, View All, Browse All, Collections, Featured, New Arrivals, Best Sellers, Sale,
Clearance, Gift Guide, Blog, Inspiration, Designers, Brands, Trending, Recently Viewed,
brand/designer listing pages, price/colour filter pages.

**Mixed roll-ups: drop, don't pad — inspect actual product titles first.**
**Facet/material/shape re-cuts: compare product-ID sets, not names** (but a genuine ROOM
branch under Rule 0.6 is not a facet re-cut).

---

## HIERARCHY — PARENT GROUPING ROWS

Parent row before children: `{"category":"Lighting","sub_category":"Lighting by Room","parent":true,"qty":null,"link":null,"evidence":null,"flag":null}`.
Only leaf rows carry qty/link. Nested levels each get their own parent row. No parent row
for a childless category. Exception: a category with no sub-categories emits ONE leaf row
(category == sub_category).

## LANGUAGE / NAMING

Plain English ASCII only in `category`/`sub_category` — no accents, em-dashes, curly quotes,
currency signs. Translate French/German/Dutch/Danish/Finnish/Spanish/Italian names into
natural English (this has now proven out cleanly across seven language batches in this
project). `evidence`/`notes` may quote the original-language text.

## OUTPUT CONTRACT

One JSON file per company, `c<SR>.json`, in the scratchpad root:
```json
{
  "sr": 158, "company": "Sostrene Grene", "brand_site": "sostrenegrene.com",
  "country": "Denmark", "site_url": "https://www.sostrenegrene.com/",
  "status": "ok", "failure_reason": null,
  "notes": "Access route, count verification, exclusions, Rule 0.6 overlaps, duplicate-company determination if flagged above.",
  "rows": [
    {"category":"Lighting","sub_category":"Lighting by Room","parent":true,"qty":null,"link":null,"evidence":null,"flag":null},
    {"category":"Lighting","sub_category":"Bathroom Lighting","parent":false,"qty":124,"link":"https://www.example.com/lighting/bathroom/","evidence":"listing header text '124 Results'","flag":null}
  ]
}
```
`status`: `"ok"`|`"partial"`|`"failed"`. `qty`: integer or null, never a string. `link`:
absolute canonical origin URL, null on parents. `evidence` required with any qty. Failed
company: `"rows": []` + precise `failure_reason`.

Validate: `python -c "import json;d=json.load(open('c<SR>.json',encoding='utf-8'));print(len(d['rows']))"`

## FINAL MESSAGE

Compact: SR, name, status, leaf/parent counts, nulls/flags, access route, failure reason if
any, Rule 0 gains, and — for any flagged S.N. above — your duplicate-company determination
with evidence.
