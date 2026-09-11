# WORKER BRIEF â€” Home Decor Category & Qty Extraction (Final_Company_List, S.N. 246-270)

You are ONE of a rolling pool of parallel extraction workers on this roster range. Read
this whole brief before starting. **This window has more literal-domain duplicates of
already-completed US companies, plus the project's first India-market companies. Check the
DUPLICATE-COMPANY flags below FIRST.**

**Scratchpad root:**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\be91bad7-b37a-4694-bdbe-c47fea1bb5d9\scratchpad`

**Work inside your own `w<SR>` subdirectory** (`mkdir` it first). Work synchronously
(foreground) â€” do not end your turn citing a background job, "cooldown," or "waiting for a
monitor"; wait for it in-turn. This has happened 10+ times on this project and always loses
progress â€” if you started a background fetch, either poll it yourself in a short in-turn
wait loop or switch to a synchronous approach entirely.

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

Shopify/Magento/Searchspring/Constructor.io raw totals, and marketplace count widgets that
round to nearest 100/1000 or cap at a page limit (confirmed on Noon UAE, Etsy US), are NOT
usable as exact qty â€” exhaustion-check everything, null+flag when a real count is
unobtainable. Watch for color/variant counts masquerading as product counts (caught on
Quince Home, Indigo Home this session) â€” always deduplicate to real distinct products.

## RULE 2: NETWORK â€” HOW TO REACH BLOCKED SITES

1. Direct fetch. 2. `curl_cffi` impersonation â€” brute-force 10+ profiles (the winning
profile is often unstable/rotating on Akamai-protected sites, e.g. Crate & Barrel/Kohl's â€”
don't assume a single lucky hit means the block is solved). 3. `r.jina.ai/<url>`.
4. `translate.goog` (works well against Imperva/Incapsula and Cloudflare managed challenges
â€” but its own `/robots.txt` is BOGUS for any domain, never trust it). 5. WebFetch.
6. Side doors: sitemaps, SFCC endpoints, exposed Constructor.io/Algolia/Searchspring keys
in `__NEXT_DATA__`/SSR state. 7. Akamai solver for Zara Home/Inditex platform. 8. Cloudflare
IPv6 anycast pinning + curl_cffi.
**DO NOT USE BROWSER AUTOMATION â€” the pool shares one browser.**

**If the ONLY working route is Wayback Machine, that is STRUCTURE ONLY, never counts** â€”
every qty sourced from an archived snapshot must be `null` + `MANUAL REVIEW`, never trusted
as a real count (confirmed cases: S.N. 104/126 Maisons du Monde, S.N. 162 BHV Marais,
S.N. 218 Costco US all did this correctly; S.N. 223 Simons Maison got it wrong and had to
be corrected before merge â€” don't repeat that mistake).

## RULE 3: A RETIRED OR REDIRECTED CATALOGUE IS A REAL ANSWER

Check redirects/sitemap/shutdown notices before extracting; don't assume decline either.

**Check `robots.txt` for a Claude-specific disallow** before any WAF-bypass. Confirmed
cases: Made In Design, Home24 DE (x2), El Corte Ingles, Amazon UAE, Amazon US (all named
ClaudeBot/Claude-User/Claude-SearchBot/Claude-Web with `Disallow: /`). **S.N. 264 Amazon
India in this window is very likely to carry the identical policy â€” check first.**

---

## DUPLICATE-COMPANY FLAGS â€” CHECK THESE FIRST (all confirmed via exact domain match)

- **S.N. 247 "Williams Sonoma"** â€” identical domain (`williams-sonoma.com`) to
  already-completed **S.N. 55 "Williams Sonoma Home"** (`c55.json`, 40 leaf + 11 parent,
  `ok`). Read `c55.json` first. Treat as duplicate: `"status": "ok"`, `"rows": []`.
- **S.N. 250 "Muuto US"** â€” identical domain (`muuto.com`) to already-completed **S.N. 184
  "Muuto"** (`c184.json`, Denmark, 9 leaf + 2 parent, `ok`), which already confirmed
  `muuto.com` serves ONE global catalogue (product qty API `hits` field, no locale split
  found). Read `c184.json` first. Given Muuto's own worker found no evidence of a
  country-specific catalogue split, this is very likely a duplicate â€” but verify with a
  quick locale/currency check before concluding (this project has seen the "bare domain,
  two roster rows" pattern go both ways â€” S.N. 138 Anthropologie UK turned out genuinely
  distinct from a shared bare domain, so don't assume without checking).
- **S.N. 256 "CB2"** â€” identical domain (`cb2.com`) to already-completed **S.N. 59** (whose
  company cell literally reads "US" due to a roster data-entry quirk, but is the same
  cb2.com catalogue â€” `c59.json`, `Partial`, 37 leaf/9 null, Akamai issues at the time).
  Read `c59.json` first. Treat as duplicate-reference (status `ok` regardless of c59's own
  Partial status â€” see the standing convention note below), or do a quick fresh Rule 2
  sweep first in case the block has cleared.
- **S.N. 257 "RH"** â€” identical domain (`rh.com`) to already-completed **S.N. 6
  "Restoration Hardware"** (`c6.json`, `Partial`, 46 leaf all null+flagged, A-record-only
  IPv4 access issue at the time). Read `c6.json` first. Same duplicate-reference guidance
  as CB2 above â€” quick fresh sweep permitted, but don't redo a full independent extraction.

**REMINDER on the standing convention** (two bugs already caught and fixed this session,
don't repeat either): for ANY confirmed duplicate-company case, (1) use `"rows": []` â€” never
re-populate the sibling's rows, and (2) use `status: "ok"` for the duplicate reference row
regardless of what status the referenced source itself carries (even if the source is
`Partial` or `failed`).

**Not flagged as a duplicate, but worth a quick sanity check**:
- S.N. 255 "Design Within Reach" (`dwr.com`) â€” this domain is already referenced in this
  project's notes (S.N. 28 HAY US's `us.hay.com` redirects to `dwr.com/brands-hay`, a HAY
  sub-brand page within DWR's broader catalogue). DWR itself is a separate general
  design-furniture retailer, not previously extracted as its own company â€” extract its full
  catalogue fresh, but be aware a HAY-branded subset within it may overlap with S.N. 28's
  data; document the overlap if you notice it, don't worry about deduplicating across
  companies (that's a cross-company overlap, not a duplicate-company case).
- S.N. 269 "H&M Home India" vs S.N. 97 UK / S.N. 134 IT / S.N. 154 FR (all confirmed
  genuinely independent per-locale on the `www2.hm.com/<locale>/home.html` pattern, now
  3-for-3) â€” expect a 4th genuinely independent locale, verify rather than assume.
- S.N. 270 "IKEA India" vs the 5 already-confirmed independent IKEA country rows (UK, DE,
  FR, UAE, JP) â€” expect a 6th genuinely independent country catalogue, verify via locale
  path (`ikea.com/in/en/` or similar) rather than assuming.

---

## THIS WINDOW'S FULL ROSTER

| S.N. | Company | Domain | Country |
|---|---|---|---|
| 246 | Shades of Light | shadesoflight.com | USA |
| 247 | Williams Sonoma | williams-sonoma.com | USA |
| 248 | Grandin Road | grandinroad.com | USA |
| 249 | Food52 | food52.com | USA |
| 250 | Muuto US | muuto.com | USA |
| 251 | 2Modern | 2modern.com | USA |
| 252 | Design Public | designpublic.com | USA |
| 253 | Lightology | lightology.com | USA |
| 254 | Terrain | shopterrain.com | USA |
| 255 | Design Within Reach | dwr.com | USA |
| 256 | CB2 | cb2.com | USA |
| 257 | RH | rh.com | USA |
| 258 | Hudson Valley Lighting | hvlgroup.com | USA |
| 259 | Visual Comfort | visualcomfort.com | USA |
| 260 | Cello World | celloworld.com | India |
| 261 | La Opala | laopala.in | India |
| 262 | Milton | milton.in | India |
| 263 | Pepperfry | pepperfry.com | India |
| 264 | Amazon India | amazon.in | India |
| 265 | Flipkart Home & Kitchen | flipkart.com | India |
| 266 | Myntra Home | myntra.com | India |
| 267 | AJIO Home | ajio.com | India |
| 268 | FOS Lighting | foslighting.in | India |
| 269 | H&M Home India | www2.hm.com | India |
| 270 | IKEA India | ikea.com | India |

**No-precedent companies, budget a fresh Rule 2 sweep on each**: S.N. 246 Shades of Light,
S.N. 253 Lightology, S.N. 258 Hudson Valley Lighting, S.N. 259 Visual Comfort (all US
lighting specialists â€” expect large focused catalogues, similar to Lamps Plus/Beacon
Lighting precedent), S.N. 248 Grandin Road (US outdoor/decor DTC brand), S.N. 249 Food52
(US food-media-brand-turned-retailer, mostly kitchenware â€” expect narrow decor scope,
similar discipline to Sur La Table), S.N. 251 2Modern and S.N. 252 Design Public (US
modern-design multi-brand e-tailers, similar to AmbienteDirect), S.N. 254 Terrain (US
garden/lifestyle DTC brand, Anthropologie-family â€” check for corporate-sibling overlap with
S.N. 7/138 Anthropologie but don't assume duplication), S.N. 260 Cello World and S.N. 262
Milton (Indian houseware/tableware manufacturers â€” first India-market DTC brands in this
project, expect solid glassware/tableware coverage per their core business), S.N. 261 La
Opala (Indian glassware/tableware manufacturer, likely strong Kitchen & Dining coverage,
minimal lighting/mirrors), S.N. 263 Pepperfry (large Indian furniture/decor marketplace,
expect a big catalogue), S.N. 265 Flipkart Home & Kitchen, S.N. 266 Myntra Home, S.N. 267
AJIO Home (large Indian general marketplaces â€” scope strictly to Home/Decor department
navigation like Amazon/Target/Walmart precedent, do not enumerate the whole site; also
check robots.txt for a Claude-specific disallow before extracting, per the Amazon
precedent â€” Flipkart/Myntra/AJIO are all Indian e-commerce majors that may have similar
AI-crawler policies), S.N. 268 FOS Lighting (Indian lighting specialist DTC brand).

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
appliances/cookware/cutlery/bar tools, hardware/plumbing/DIY, textiles, food/drink
consumables, cleaning/personal care, garden tools/seeds, ceiling fans, bulbs, wiring.

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

Plain English ASCII only in `category`/`sub_category`. India-market companies mostly render
in English natively (verify per-site); translate any Hindi/regional-language category
names into plain English if found.

## OUTPUT CONTRACT

One JSON file per company, `c<SR>.json`, in the scratchpad root:
```json
{
  "sr": 253, "company": "Lightology", "brand_site": "lightology.com", "country": "USA",
  "site_url": "https://www.lightology.com/", "status": "ok", "failure_reason": null,
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

