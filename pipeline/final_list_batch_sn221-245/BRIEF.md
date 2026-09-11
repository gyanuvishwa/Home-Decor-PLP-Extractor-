# WORKER BRIEF â€” Home Decor Category & Qty Extraction (Final_Company_List, S.N. 221-245)

You are ONE of a rolling pool of parallel extraction workers on this roster range. Read
this whole brief before starting. **This window is heavy with literal duplicates of the
project's original S.N. 1-70 US batch â€” 5 of 25 companies here share an EXACT domain with
an already-completed company. Check the DUPLICATE-COMPANY flags below FIRST.**

**Scratchpad root:**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\1294ee4d-a82f-4c1e-875d-2530fa2ecfd7\scratchpad`

**Work inside your own `w<SR>` subdirectory** (`mkdir` it first). Work synchronously
(foreground) â€” do not end your turn citing a background job, "cooldown," or "waiting for a
monitor"; wait for it in-turn. This has happened repeatedly on this project (10+ confirmed
cases) and always loses progress â€” if you started a background fetch, either poll it
yourself in a short in-turn wait loop or switch to a synchronous approach entirely.

---

# RULE 0 â€” PRODUCT TYPE BEATS ROOM NAME (HIGHEST PRIORITY)

**NEVER exclude a category because of a ROOM word in its name.** Judge the **product type**.
- **0.1** Lighting organised by room is IN SCOPE â€” traverse every room node.
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

Shopify/Magento/Searchspring/Constructor.io raw totals are proven-inflated repeatedly on
this project â€” always exhaustion-check (unique product IDs, boundary tests,
`ceil(total/pageSize)`). Marketplace count widgets that round to nearest 100/1000 (found on
Noon UAE) are NOT usable as exact qty â€” null+flag instead.

## RULE 2: NETWORK â€” HOW TO REACH BLOCKED SITES

1. Direct fetch. 2. `curl_cffi` impersonation â€” brute-force 10+ profiles. 3. `r.jina.ai/<url>`.
4. `translate.goog` (works well against Imperva/Incapsula and Cloudflare managed challenges
â€” confirmed on David Jones Home and Temple & Webster this session; **but its own
`/robots.txt` response is BOGUS/synthetic for any domain proxied through it â€” always fetch
the real robots.txt directly or via Wayback, never trust translate.goog's own robots.txt**).
5. WebFetch. 6. Side doors: sitemaps, SFCC `Search-Refinebar`, TJX `navMenuData.jsp`,
Cornerstone `UnbxdAPI`, JS-bundle mega-navs, exposed Constructor.io/Algolia/Searchspring
keys embedded in `__NEXT_DATA__`/SSR state (used successfully on Kmart AU, Target AU this
session). 7. Akamai solver for Zara Home/Inditex:
`pipeline\final_list_batch_sn21-30\inditex_interstitial_solver.py`. 8. Cloudflare IPv6
anycast pinning + curl_cffi. Pace yourself, no retry storms.
**DO NOT USE BROWSER AUTOMATION â€” the pool shares one browser.**

## RULE 3: A RETIRED OR REDIRECTED CATALOGUE IS A REAL ANSWER

Check redirects/sitemap/shutdown notices before extracting; don't assume decline either.

**Check `robots.txt` for a Claude-specific disallow** before any WAF-bypass. Confirmed
cases so far: Made In Design, Home24 DE (x2), El Corte Ingles, Amazon UAE (ClaudeBot,
Claude-User, Claude-SearchBot, Claude-Web all `Disallow: /`). **S.N. 229 Amazon US in this
window is very likely to carry the identical policy â€” check first before any extraction
attempt.** A group merely LISTING ClaudeBot with the SAME restrictions as `*` (confirmed on
Westwing IT, Noon UAE) is NOT a block.

---

## DUPLICATE-COMPANY FLAGS â€” CHECK THESE FIRST (all confirmed via exact domain match)

- **S.N. 221 "Wayfair US"** â€” identical domain (`wayfair.com`) to already-completed **S.N.
  1 "Wayfair"** (`c1.json`, 85 leaf + 18 parent, `ok`). Read `c1.json` first. Treat as
  duplicate-company case: `"status": "ok"`, `"rows": []`, document in notes.
- **S.N. 225 "Target"** â€” identical domain (`target.com`) to already-completed **S.N. 22
  "Target Home"** (`c22.json`, 109 leaf + 18 parent, `ok`). Read `c22.json` first. Treat as
  duplicate.
- **S.N. 231 "Crate & Barrel"** â€” identical domain (`crateandbarrel.com`) to
  already-completed **S.N. 58 "Crate & Barrel US"** (`c58.json`, `Partial`, 66 leaf all
  null+flagged â€” Akamai hard-blocked, confirmed durable across a 2-day retry gap earlier in
  this project). Read `c58.json` first. Given the block was already proven durable, a
  duplicate-reference (not a full re-attempt) is the likely right call, but a quick fresh
  Rule 2 sweep is still reasonable in case something changed.
- **S.N. 233 "West Elm"** â€” identical domain (`westelm.com`) to already-completed **S.N. 2
  "West Elm US"** (`c2.json`, 40 leaf + 9 parent, `ok`). Read `c2.json` first. Treat as
  duplicate.
- **S.N. 244 "Pottery Barn"** â€” identical domain (`potterybarn.com`) to already-completed
  **S.N. 3 "Pottery Barn US"** (`c3.json`, 41 leaf + 11 parent, `ok`). Read `c3.json` first.
  Treat as duplicate.

**For ANY confirmed duplicate-company case, use `"rows": []` â€” do NOT re-populate the
sibling's rows.** (A worker deviated from this earlier this session on a different company
and it had to be corrected before merge.)

**Not flagged as a duplicate, but worth a quick sanity check**: S.N. 245 "Lumens"
(lumens.com) â€” a large lighting/design multi-brand marketplace, no direct precedent in this
project, but check it isn't secretly the same catalogue as any already-completed lighting
retailer before assuming independence (no strong signal either way, just standard
diligence).

**No-precedent companies, budget a fresh Rule 2 sweep on each**: S.N. 222 Quince Home (US
DTC value brand), S.N. 223 Simons Maison and S.N. 235 Indigo Home (Canadian department/
lifestyle retailers â€” first Canada-market companies), S.N. 224 Structube, S.N. 239 EQ3
(Canadian furniture/decor chains), S.N. 226 Walmart US, S.N. 227 JCPenney Home, S.N. 228
Kohl's Home (US general/department retailers â€” scope strictly to Home/Decor department,
same discipline as Target/Amazon/Costco precedent, do not enumerate the whole site), S.N.
229 Amazon US (see robots.txt warning above), S.N. 230 The Home Depot (US DIY chain â€”
expect narrow genuine decor scope like Castorama/Leroy Merlin, most of catalogue is
hardware/building materials), S.N. 232 Sur La Table (US kitchenware specialist â€” expect
narrow but genuine tableware/glassware coverage, minimal lighting/mirrors), S.N. 234 Etsy
US (a handmade/vintage marketplace â€” this is structurally very different from a normal
retailer; scope to its Home & Living / Home Decor category taxonomy, expect huge listing
counts from many independent sellers, verify empirically and don't be surprised if most
qty needs a MANUAL REVIEW flag like Noon UAE's rounded-count problem), S.N. 236 AllModern,
S.N. 237 Birch Lane, S.N. 238 Joss & Main (Wayfair-family sister brands â€” same corporate
group as S.N. 1/221 Wayfair but distinct storefronts/catalogues, verify independence via
platform/catalog-ID rather than assuming duplication just from corporate relationship,
same discipline as the Momax/XXXLutz sister-brand case earlier in this project), S.N. 240
Lamps Plus (US lighting specialist, expect a large focused catalogue), S.N. 241 Bouclair
(Canadian home-decor chain), S.N. 242 Neiman Marcus Home (already has a project precedent
at S.N. 34 1stDibs/S.N. 33 Perigold's sibling relationship â€” Neiman Marcus itself has no
direct prior S.N., but note S.N. 35 Horchow was found to redirect INTO Neiman Marcus's own
site; read c35.json for context on that platform before extracting, since your rows may
overlap it), S.N. 243 Saks Home (US luxury department store home department, may need
Wayback/side-door workarounds like other department stores in this project).

---

## THIS WINDOW'S FULL ROSTER

| S.N. | Company | Domain | Country |
|---|---|---|---|
| 221 | Wayfair US | wayfair.com | USA |
| 222 | Quince Home | quince.com | USA |
| 223 | Simons Maison | simons.ca | Canada |
| 224 | Structube | structube.com | Canada |
| 225 | Target | target.com | USA |
| 226 | Walmart US | walmart.com | USA |
| 227 | JCPenney Home | jcpenney.com | USA |
| 228 | Kohl's Home | kohls.com | USA |
| 229 | Amazon US | amazon.com | USA |
| 230 | The Home Depot | homedepot.com | USA |
| 231 | Crate & Barrel | crateandbarrel.com | USA |
| 232 | Sur La Table | surlatable.com | USA |
| 233 | West Elm | westelm.com | USA |
| 234 | Etsy US | etsy.com | USA |
| 235 | Indigo Home | indigo.ca | Canada |
| 236 | AllModern | allmodern.com | USA |
| 237 | Birch Lane | birchlane.com | USA |
| 238 | Joss & Main | jossandmain.com | USA |
| 239 | EQ3 | eq3.com | Canada |
| 240 | Lamps Plus | lampsplus.com | USA |
| 241 | Bouclair | bouclair.com | Canada |
| 242 | Neiman Marcus Home | neimanmarcus.com | USA |
| 243 | Saks Home | saksfifthavenue.com | USA |
| 244 | Pottery Barn | potterybarn.com | USA |
| 245 | Lumens | lumens.com | USA |

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
Lighting (every fixture type, every room), Mirrors (every type), Glassware (all â€”
decorative and functional), Tableware/dinnerware (file under Kitchen & Dining), Decorative
accessories (bowls, trays, wall art, vases, sculptures, figurines, candle holders,
unscented candles, planters, centerpieces), Clocks (all types), decorative
wood/ceramic/resin/marble/stone/rattan lines, decorative metal (wall art, sculptures,
hooks, racks, curtain rods/tiebacks), genuinely decorative bathroom accessories.

### EXCLUDE
Home Fragrance (diffusers, sprays, oils, incense, **scented candles** â€” read actual
titles), artificial/faux plants & flowers, wallpaper, Holiday & Gift, bathroom
furniture/storage/fixtures/plumbing (not mirrors/lighting), all furniture, kitchen
appliances/cookware/cutlery/bar tools, hardware/plumbing/DIY (**especially relevant for
S.N. 230 Home Depot**), textiles, food/drink consumables, cleaning/personal care, garden
tools/seeds, ceiling fans, bulbs, wiring.

### NEVER EXTRACT
Shop All, Collections, Featured, New Arrivals, Best Sellers, Sale, Gift Guide, Blog,
Inspiration, Designers, Brands, Trending, brand/designer listing pages, filter pages.

**Mixed roll-ups: drop, don't pad â€” inspect actual titles.** **Facet/material/shape
re-cuts: compare product-ID sets, not names** (a genuine ROOM branch is not a facet re-cut).

## HIERARCHY

Parent row before children: `{"category":"Lighting","sub_category":"Lighting by Room","parent":true,"qty":null,"link":null,"evidence":null,"flag":null}`.
Only leaf rows carry qty/link. Nested levels each get their own parent row. Exception: a
childless category emits ONE leaf row (category == sub_category).

## LANGUAGE / NAMING

Plain English ASCII only in `category`/`sub_category`. All companies in this window are
English-market (US/Canada), no translation needed.

## OUTPUT CONTRACT

One JSON file per company, `c<SR>.json`, in the scratchpad root:
```json
{
  "sr": 240, "company": "Lamps Plus", "brand_site": "lampsplus.com", "country": "USA",
  "site_url": "https://www.lampsplus.com/", "status": "ok", "failure_reason": null,
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
`status: "partial"`, not `"ok"`** â€” even if every individual null decision was well-justified
(this project's convention, confirmed via S.N. 86 QVC, S.N. 97 H&M, S.N. 118 Connox, S.N.
191 Noon UAE). Reserve `"ok"` for extractions where qty is fully or nearly-fully resolved.

Validate: `python -c "import json;d=json.load(open('c<SR>.json',encoding='utf-8'));print(len(d['rows']))"`

## FINAL MESSAGE

Compact: SR, name, status, leaf/parent counts, nulls/flags, access route, failure reason if
any, Rule 0 gains, duplicate-company determination with evidence if flagged.

