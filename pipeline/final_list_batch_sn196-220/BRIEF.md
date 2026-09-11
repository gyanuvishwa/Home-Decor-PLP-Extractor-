# WORKER BRIEF — Home Decor Category & Qty Extraction (Final_Company_List, S.N. 196-220)

You are ONE of a rolling pool of parallel extraction workers on this roster range. Read
this whole brief before starting. **This window moves into new geographies: more UAE
franchise storefronts, then the project's first Japan/Australia/Singapore companies, plus
three big US retailers. Check the DUPLICATE-COMPANY flags below FIRST for your company.**

**Scratchpad root:**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\5889af5e-4d19-4b75-84dd-1e4166afe96d\scratchpad`

**Work inside your own `w<SR>` subdirectory** (`mkdir` it first). Work synchronously
(foreground) — do not end your turn citing a background job or a "cooldown"; wait for it
in-turn. This has happened repeatedly on this project (7+ confirmed cases) and always
loses progress.

---

# RULE 0 — PRODUCT TYPE BEATS ROOM NAME (HIGHEST PRIORITY)

**NEVER exclude a category because of a ROOM word in its name.** Judge the **product type**.
- **0.1** Lighting organised by room is IN SCOPE — traverse every room node.
- **0.2** Traverse EVERY lighting branch, no depth limit. Still excluded: bulbs, ceiling
  fans, wiring hardware.
- **0.3** ALL mirrors are IN SCOPE, every type.
- **0.4/0.5** "Bathroom"/"Bedroom"/"Outdoor" are not blanket exclusions — include the
  decorative items, still exclude furniture/storage/fixtures/plumbing/hardware.
- **0.6** A site with both a type tree AND a room tree: emit both, document overlap in
  `notes`. Only drop a node that's the exact same listing under a second URL, or a pure
  facet re-cut.

## WORKSPACE / OUTPUT RULES

Work in `scratchpad\w<SR>\`; only write `c<SR>.json` to the scratchpad **root**, as soon as
complete. Never touch the `.xlsx`/`.xlsm` workbooks.

## THE ONE RULE THAT MATTERS

`qty` must be the EXACT number the site itself reports. Never estimate/round/infer/copy
from a sibling. If you can't verify exactly, `"qty": null` + `"flag": "MANUAL REVIEW: ..."`.
Every qty needs `evidence`.

## RULE 1: VERIFY THE COUNT EMPIRICALLY

Shopify/Magento/Searchspring raw totals are proven-inflated on this project repeatedly —
always exhaustion-check (unique product IDs, boundary tests, `ceil(total/pageSize)`).
Counting tiles by href is unreliable. Watch for space-style thousands separators on
French/Nordic sites (`probe.py`'s `count` fixed 2026-08-11, cross-check anyway).

## RULE 2: NETWORK — HOW TO REACH BLOCKED SITES

1. Direct fetch. 2. `curl_cffi` impersonation — brute-force 10+ profiles. 3. `r.jina.ai/<url>`
(percent-encode). 4. `translate.goog`. 5. WebFetch. 6. Side doors: sitemaps, SFCC
`Search-Refinebar`, TJX `navMenuData.jsp`, Cornerstone `UnbxdAPI`, JS-bundle mega-navs.
7. Akamai solver for Zara Home/Inditex platform:
`pipeline\final_list_batch_sn21-30\inditex_interstitial_solver.py`. 8. Cloudflare IPv6
anycast pinning + curl_cffi. Pace yourself, no retry storms. Canonical origin URLs in
`link` only. Wayback is structure-only, never counts.
**DO NOT USE BROWSER AUTOMATION — the pool shares one browser.**

## RULE 3: A RETIRED OR REDIRECTED CATALOGUE IS A REAL ANSWER

Check redirects/sitemap/shutdown notices before extracting; don't assume decline either.
If gone: `"status":"ok"`, `"rows":[]` + evidence (precedent: S.N. 193 Pottery Barn UAE,
the whole Alshaya-run GCC Pottery Barn/West Elm franchise wound down through 2025 — if
this window's other UAE franchise stores show the same closure pattern, check for it).

**Check `robots.txt` for a Claude-specific disallow** before any WAF-bypass. Confirmed
cases: Made In Design, Home24 DE (x2), El Corte Ingles, Amazon UAE (ClaudeBot, Claude-User,
Claude-SearchBot, Claude-Web all `Disallow: /`). If found, mark `failed`, don't bypass. A
group merely LISTING ClaudeBot with the SAME restrictions as `*` (confirmed on Westwing IT)
is NOT a block.

---

## DUPLICATE-COMPANY FLAGS — CHECK THESE FIRST

- **S.N. 219 "Lowe's"** — same domain (`lowes.com`) as already-completed **S.N. 75 "Lowe's
  Home Decor"** (`c75.json`, `Partial`, 29 leaf all null+flagged — Akamai hard-blocked
  every counting route, live but no working access pattern established at the time). Read
  `c75.json` first. If genuinely the same catalogue, this is a duplicate-company case, but
  consider whether a fresh attempt gets further than c75 did (blocks sometimes clear
  between sessions on this project) — use judgment, same as the S.N. 151/104 precedent.

**Not flagged as duplicates, but worth a quick sanity check** (different TLD from an
already-completed sibling — this project has seen BOTH outcomes on TLD variants: most
UAE-suffix/country-suffix domains have turned out genuinely independent franchise
operations, e.g. S.N. 15 Home Centre UAE vs no US sibling exists, S.N. 193 Pottery Barn UAE
vs S.N. 3 US turned out independent-but-closed; but do not assume, verify each):
- **S.N. 196 "Crate & Barrel UAE"** (`crateandbarrel.me`) vs S.N. 58 "Crate & Barrel US"
  (`c58.json`, `crateandbarrel.com`, Partial) — different TLD, likely a separate
  franchise-run storefront (same pattern as Pottery Barn UAE) — verify independently,
  including whether it's still open (check for closure notices per Rule 3).
- **S.N. 198 "West Elm UAE"** (`westelm.ae`) vs S.N. 2 "West Elm US" (`c2.json`,
  `westelm.com`) and S.N. 60 "West Elm UK" (`c60.json`, `westelm.co.uk`) — different TLD,
  likely a separate franchise storefront (same Alshaya-family pattern as Pottery Barn
  UAE/West Elm UAE are often co-franchised) — verify independently, check for closure.
- **S.N. 213 "IKEA Japan"** vs S.N. 100 UK / S.N. 117-156 DE / S.N. 155 France / S.N. 190
  UAE (all already confirmed genuinely independent, 3-4 for 3-4 so far on this platform) —
  expect a genuinely independent 5th-ish country catalogue, verify via locale path
  (`ikea.com/jp/ja/`) rather than assuming.

**No-precedent companies, budget a fresh Rule 2 sweep on each**: S.N. 197 Tavola UAE, S.N.
199 Tanagra, S.N. 200 Aura Living UAE, S.N. 201 The Bowery Company, S.N. 202 Chattels &
More (all UAE home-decor retailers, no prior extraction), S.N. 203 MUJI Japan (Japanese
lifestyle/minimalist brand — first Japan company, likely modest but genuine decor line),
S.N. 204 Beacon Lighting (Australian lighting specialist — first Australia company, expect
large lighting-focused catalogue), S.N. 205 Kmart Australia and S.N. 207 Target Australia
(general mass-market retailers — scope strictly to Home/Decor department like Amazon/Target
US precedent, do not enumerate the whole site), S.N. 206 Nitori Japan (Japanese
furniture/homeware chain, large), S.N. 208 Temple & Webster (Australian online home/decor
marketplace, likely large focused catalogue), S.N. 209 David Jones Home and S.N. 217 Myer
Home (Australian department stores — may need Wayback/side-door workarounds like other
department-store platforms in this project), S.N. 210 Freedom Australia and S.N. 212 House
(Australian furniture/homeware chains), S.N. 211 HipVan and S.N. 214 Castlery Singapore
(first Singapore companies, furniture/decor DTC brands), S.N. 215 Country Road Home
(Australian fashion/lifestyle brand's home line), S.N. 216 Francfranc Japan (Japanese
lifestyle/decor chain), S.N. 218 Costco US and S.N. 220 Sam's Club (huge US warehouse
marketplaces — scope strictly to Home/Decor department, same discipline as Amazon/Target,
expect real but bounded decor coverage, verify counts empirically since warehouse-club
sites can have unusual inventory-driven count behavior different from standard retail).

---

## THIS WINDOW'S FULL ROSTER

| S.N. | Company | Domain | Country |
|---|---|---|---|
| 196 | Crate & Barrel UAE | crateandbarrel.me | UAE |
| 197 | Tavola UAE | tavolashop.com | UAE |
| 198 | West Elm UAE | westelm.ae | UAE |
| 199 | Tanagra | tanagra.me | UAE |
| 200 | Aura Living UAE | auraliving.com | UAE |
| 201 | The Bowery Company | thebowerycompany.com | UAE |
| 202 | Chattels & More | chattelsandmore.com | UAE |
| 203 | MUJI Japan | muji.com | Japan |
| 204 | Beacon Lighting | beaconlighting.com.au | Australia |
| 205 | Kmart Australia | kmart.com.au | Australia |
| 206 | Nitori Japan | nitori-net.jp | Japan |
| 207 | Target Australia | target.com.au | Australia |
| 208 | Temple & Webster | templeandwebster.com.au | Australia |
| 209 | David Jones Home | davidjones.com | Australia |
| 210 | Freedom Australia | freedom.com.au | Australia |
| 211 | HipVan | hipvan.com | Singapore |
| 212 | House | house.com.au | Australia |
| 213 | IKEA Japan | ikea.com | Japan |
| 214 | Castlery Singapore | castlery.com | Singapore |
| 215 | Country Road Home | countryroad.com.au | Australia |
| 216 | Francfranc Japan | francfranc.com | Japan |
| 217 | Myer Home | myer.com.au | Australia |
| 218 | Costco US | costco.com | USA |
| 219 | Lowe's | lowes.com | USA |
| 220 | Sam's Club | samsclub.com | USA |

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
appliances/cookware/cutlery/bar tools, hardware/plumbing/DIY, textiles, food/drink
consumables, cleaning/personal care, garden tools/seeds, ceiling fans, bulbs, wiring.

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

Plain English ASCII only in `category`/`sub_category`. Translate Japanese category names
into natural English (first Japan companies this batch — apply the same translate-to-
English discipline proven across 8 other languages in this project). Australian/Singapore
companies are natively English, no translation needed.

## OUTPUT CONTRACT

One JSON file per company, `c<SR>.json`, in the scratchpad root:
```json
{
  "sr": 204, "company": "Beacon Lighting", "brand_site": "beaconlighting.com.au",
  "country": "Australia", "site_url": "https://www.beaconlighting.com.au/",
  "status": "ok", "failure_reason": null,
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

**For any confirmed duplicate-company case, use `"rows": []` — do NOT re-populate the
sibling's rows.** (A worker deviated from this on S.N. 182 HAY Denmark earlier this
session and it had to be corrected before merge — leave duplicate rows empty and point to
the authoritative S.N. in `notes`.)

Validate: `python -c "import json;d=json.load(open('c<SR>.json',encoding='utf-8'));print(len(d['rows']))"`

## FINAL MESSAGE

Compact: SR, name, status, leaf/parent counts, nulls/flags, access route, failure reason if
any, Rule 0 gains, duplicate-company determination with evidence if flagged.
