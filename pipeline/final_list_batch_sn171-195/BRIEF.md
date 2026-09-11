# WORKER BRIEF — Home Decor Category & Qty Extraction (Final_Company_List, S.N. 171-195)

You are ONE of a rolling pool of parallel extraction workers on this roster range. Read
this whole brief before starting. **Check the DUPLICATE-COMPANY flags below FIRST for your
company before doing any real extraction work.**

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

- **0.1** Lighting organised by room is IN SCOPE — traverse every room node.
- **0.2** Traverse EVERY lighting branch, no depth limit (recessed, track, cabinet, picture
  lights, outdoor/landscape included). Still excluded: bulbs, ceiling fans, wiring hardware.
- **0.3** ALL mirrors are IN SCOPE, every type.
- **0.4/0.5** "Bathroom"/"Bedroom"/"Outdoor" are not blanket exclusions — include the
  decorative items, still exclude furniture/storage/fixtures/plumbing/hardware.
- **0.6** A site with both a type tree AND a room tree: emit both, document the overlap in
  `notes`. Only drop a node that's the exact same listing under a second URL, or a pure
  facet re-cut (colour/size/shape/material/price/style).

## WORKSPACE / OUTPUT RULES

Work in `scratchpad\w<SR>\`; only write `c<SR>.json` to the scratchpad **root**. Write it as
soon as you have a complete result. Never touch the `.xlsx`/`.xlsm` workbooks.

## THE ONE RULE THAT MATTERS

`qty` must be the EXACT number the site itself reports. Never estimate/round/infer/copy
from a sibling. If you can't verify it exactly, `"qty": null` + `"flag": "MANUAL REVIEW:
..."` — that's a correct answer. Every qty needs an `evidence` string.

## RULE 1: VERIFY THE COUNT EMPIRICALLY

Shopify `/collections.json` `products_count`, Magento `categoryList.product_count`, and
Searchspring totals are proven-inflated on this project — always exhaustion-check. Cheap
proofs: tiles at `start=N-1` zero at `start=N`; `ceil(total/pageSize)==pageCount`; children
sum to ~parent; enumerate to exhaustion counting unique product IDs. Counting tiles by href
is unreliable.

**Watch for space-style thousands separators** (e.g. French/Nordic "8 682" using U+202F or
U+00A0) — `probe.py`'s `count` command was fixed for this 2026-08-11 after it silently
truncated numbers on Castorama France; cross-check any suspiciously round/small count with
a raw text read regardless, since this is newly fixed and not verified at scale yet.

## RULE 2: NETWORK — HOW TO REACH BLOCKED SITES

1. Direct fetch. 2. `curl_cffi` impersonation — brute-force 10+ profiles. 3. `r.jina.ai/<url>`
(percent-encode). 4. `translate.goog`. 5. WebFetch. 6. Side doors: sitemaps almost always;
SFCC `Search-Refinebar`/`Search-UpdateGrid`; TJX `navMenuData.jsp`; Cornerstone `UnbxdAPI`;
React mega-navs in the JS bundle. 7. Akamai proof-of-work solver at
`pipeline\final_list_batch_sn21-30\inditex_interstitial_solver.py` (Zara Home platform,
5-for-5 so far). 8. Cloudflare IPv6 anycast pinning + curl_cffi.

Pace yourself, no retry storms. Canonical origin URLs in `link` only (never
translate.goog/r.jina.ai/Wayback). Wayback is structure-only, never counts.
**DO NOT USE BROWSER AUTOMATION — the pool shares one browser.**

## RULE 3: A RETIRED OR REDIRECTED CATALOGUE IS A REAL ANSWER

Check redirects, sitemap, shutdown/legal notices before extracting; don't assume decline
either. If gone: `"status":"ok"`, `"rows":[]` + evidence. If redirected elsewhere: extract
that, document the mismatch.

**Check `robots.txt` for a Claude-specific disallow** before any WAF-bypass. Confirmed cases
so far: Made In Design, Home24 DE (x2, S.N. 113 and 159), El Corte Ingles — all
`ClaudeBot`/`anthropic-ai`/`Claude-Web`/`Claude-User` named specifically, more restrictive
than the generic `*` group. A group merely LISTING ClaudeBot with the SAME restrictions as
`*` (confirmed on Westwing IT) is NOT a block — check restrictiveness, not just presence.

---

## DUPLICATE-COMPANY FLAGS — CHECK THESE FIRST

- **S.N. 179 "AM.PM"** — same domain (`laredoute.fr`) as already-completed **S.N. 105
  "AM.PM France"** (15 leaf + 4 parent, `ok`, redirects into laredoute.fr's platform via a
  brand-specific filter). Read `c105.json` first — very likely a literal duplicate roster
  row (note the country field is missing "France" here but the domain match is decisive).
- **S.N. 182 "HAY Denmark"** (`hay.dk`) — check against already-completed **S.N. 28 "HAY
  US"** (`c28.json`), which found `us.hay.com` retired/redirecting to `dwr.com`, with rows
  extracted from `www.hay.com` as ONE global catalogue (confirmed via
  `Hay.countrySelected=USA` — i.e. the "global" site actually serves a US-locale catalogue
  under the hood). Determine whether `hay.dk` is a genuinely separate Danish-market
  storefront/catalogue or redirects into the same `www.hay.com` global site already
  captured — don't assume either way, HAY's own site architecture is unusual (a "global"
  domain that's actually one country's catalogue) so this needs its own careful check.
- **S.N. 194 "Home Centre UAE"** (`homecentre.com`) — check against already-completed
  **S.N. 15 "Home Centre"** (`c15.json`, 42 leaf + 10 parent, `ok`), which was ALREADY
  extracted via the `/ae/en/` (UAE, English) storefront. Read `c15.json` first — this is
  very likely the identical catalogue under a re-listed S.N., since S.N. 15's own
  extraction was already UAE-scoped.

**Not flagged as duplicates, but worth a quick sanity check given the roster's density of
near-misses in recent batches** (read the closest prior extraction if one plausibly
overlaps, don't assume independence or duplication either way):
- S.N. 190 "IKEA UAE" — no direct IKEA-UAE precedent yet (S.N. 100 UK, S.N. 117/156 DE,
  S.N. 155 France all done and independent) — expect genuinely separate per IKEA's
  established per-country pattern, but verify via locale path `ikea.com/ae/en/` (or similar)
  and category-ID scoping.
- S.N. 193 "Pottery Barn UAE" (`potterybarn.ae`) — different TLD from S.N. 3 "Pottery Barn
  US" (`potterybarn.com`); Middle East Pottery Barn storefronts are typically run by a local
  franchisee (e.g. Al-Futtaim/M.H. Alshaya) with a distinct catalogue — expect genuinely
  separate, but verify rather than assume.

**No-precedent companies, budget a fresh Rule 2 sweep on each**: S.N. 171 Seletti (Italian
design brand), S.N. 172 Iittala (Finnish design brand — also a brand carried by S.N. 149/150
Nordic marketplaces, but this is the direct-to-consumer site, a different question from
marketplace overlap), S.N. 173 Bloomingville, S.N. 174 Broste Copenhagen, S.N. 176 House
Doctor, S.N. 178 &Tradition, S.N. 181 Georg Jensen, S.N. 184 Muuto (all Danish design
brands — first-time DTC sites for brands otherwise seen only as marketplace listings),
S.N. 175 Dille & Kamille (Dutch lifestyle chain), S.N. 177 Manufactum (German curated
household-goods retailer), S.N. 180 AmbienteDirect (German design-furniture e-tailer),
S.N. 183 Merci Paris (French concept store), S.N. 185 Pols Potten (Dutch design brand),
S.N. 186 Serax (Belgian design brand), S.N. 187 Home Box UAE, S.N. 188 PAN Emirates UAE,
S.N. 192 Home R Us UAE, S.N. 195 OC Home UAE (UAE home-goods retailers, no precedent).
- **S.N. 189 "Amazon UAE"** (`amazon.ae`) and **S.N. 191 "Noon UAE"** (`noon.com`) are huge
  general marketplaces, not home-decor specialists — scope strictly to their Home/Decor
  department navigation (similar discipline to how S.N. 22 Target Home and S.N. 47 Bed Bath
  & Beyond were scoped in this project), do not attempt to enumerate the whole site. Expect
  this to be a genuinely large but carefully-filtered extraction; watch for marketplace
  noise (third-party listings, wildly inflated category counts) — verify empirically per
  Rule 1, don't trust a raw department facet count.

---

## THIS WINDOW'S FULL ROSTER

| S.N. | Company | Domain | Country |
|---|---|---|---|
| 171 | Seletti | seletti.it | Italy |
| 172 | Iittala | iittala.com | Finland |
| 173 | Bloomingville | bloomingville.com | Denmark |
| 174 | Broste Copenhagen | brostecopenhagen.com | Denmark |
| 175 | Dille & Kamille | dille-kamille.com | Netherlands |
| 176 | House Doctor | housedoctor.com | Denmark |
| 177 | Manufactum | manufactum.com | Germany |
| 178 | &Tradition | andtradition.com | Denmark |
| 179 | AM.PM | laredoute.fr | France |
| 180 | AmbienteDirect | ambientedirect.com | Germany |
| 181 | Georg Jensen | georgjensen.com | Denmark |
| 182 | HAY Denmark | hay.dk | Denmark |
| 183 | Merci Paris | merci-merci.com | France |
| 184 | Muuto | muuto.com | Denmark |
| 185 | Pols Potten | polspotten.com | Netherlands |
| 186 | Serax | serax.com | Belgium |
| 187 | Home Box UAE | homeboxstores.com | UAE |
| 188 | PAN Emirates UAE | panemirates.com | UAE |
| 189 | Amazon UAE | amazon.ae | UAE |
| 190 | IKEA UAE | ikea.com | UAE |
| 191 | Noon UAE | noon.com | UAE |
| 192 | Home R Us UAE | homesrus.ae | UAE |
| 193 | Pottery Barn UAE | potterybarn.ae | UAE |
| 194 | Home Centre UAE | homecentre.com | UAE |
| 195 | OC Home UAE | ochomefurniture.com | UAE |

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

Plain English ASCII only in `category`/`sub_category`. Translate
Danish/Dutch/German/French/Italian/Finnish names into natural English (proven across 8
languages in this project). `evidence`/`notes` may quote the original text.

## OUTPUT CONTRACT

One JSON file per company, `c<SR>.json`, in the scratchpad root:
```json
{
  "sr": 172, "company": "Iittala", "brand_site": "iittala.com", "country": "Finland",
  "site_url": "https://www.iittala.com/", "status": "ok", "failure_reason": null,
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

Validate: `python -c "import json;d=json.load(open('c<SR>.json',encoding='utf-8'));print(len(d['rows']))"`

## FINAL MESSAGE

Compact: SR, name, status, leaf/parent counts, nulls/flags, access route, failure reason if
any, Rule 0 gains, duplicate-company determination with evidence if flagged.
