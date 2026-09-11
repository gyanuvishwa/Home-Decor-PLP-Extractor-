# WORKER BRIEF — Rule 0 Top-Up (Final_Company_List, 13 pre-Rule-0 companies)

You are one of 13 parallel top-up workers, each assigned ONE company that was extracted
**before** Rule 0 existed. Your job is NOT a re-extraction — it is a **targeted addition**.

**Scratchpad root (read AND write your file here):**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\1f283d8d-cb80-4780-a64e-bafcd565952d\scratchpad`

Your existing file is `c<SR>.json` in that scratchpad root — **read it first.**

---

## WHAT WENT WRONG (context, not a rule)

Before 2026-08-08, the extraction rules treated any category with a ROOM word in its name
(Bathroom, Bedroom, Outdoor, Vanity, Kitchen, etc.) as suspect and workers often dropped it,
even when the product itself — lighting or a mirror — was squarely in scope. Rule 0 reverses
that: **a room word never puts a category out of scope by itself; judge the product type.**
See the full Rule 0 text below. Your company's original extraction predates this correction,
so it likely has one or more missing room-based lighting/mirror branches.

---

# RULE 0 — PRODUCT TYPE BEATS ROOM NAME (full text, apply exactly as below)

**NEVER exclude a category because of a ROOM word in its name.** Room words — Bathroom,
Bedroom, Living Room, Dining Room, Kitchen, Entryway, Hallway, Office, Outdoor, Vanity —
describe *where a product is used*. They say nothing about whether the product is in scope.
Judge the **product type**.

Before skipping any category containing a room word, stop and ask:
**"Am I excluding this because the PRODUCT is out of scope, or only because the ROOM is?"**
If the product is an approved type (lighting, mirror, glassware, clock, wall decor,
decorative accessory or object), **INCLUDE it.**

### 0.1 Lighting organised by room is IN SCOPE
If the site has `Lighting > Lighting by Room` (or equivalent), **every one of those nodes
must be explored and extracted**: Living Room · Bedroom · Dining Room · Kitchen ·
**Bathroom** · **Vanity** · Entryway · Hallway · Office · **Outdoor** · Patio · Landscape
lighting — all IN.

### 0.2 Traverse EVERY lighting branch — no depth limit
Do not stop at Ceiling Lights. Expand all of: Lighting by Room · Wall Lighting · Pendants ·
Chandeliers · Table Lamps · Floor Lamps · Flush Mounts · **Recessed** · **Track** ·
**Cabinet/Under-cabinet** · Vanity · Bathroom · Outdoor · Landscape · Picture lights, and any
other lighting branch actually present. Expand until you reach real product listing pages.
*(Still excluded: light BULBS, ceiling FANS, and pure wiring/mounting hardware.)*

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

### 0.6 How Rule 0 interacts with de-duplication
De-duplication still matters, but "it overlaps a product-type category" is NOT a reason to
skip a room-based category.
- A site presenting **both** a type tree and a room tree is giving you two genuine nav
  branches. **Emit both**, each under its own parent grouping row, and state the overlap
  plainly in `notes`.
- Only drop a node when it is the **same listing under a second URL at the same level**, or
  a pure facet/filter re-cut (colour, size, shape, material, price, style).
- When in doubt: **include it and document the overlap.**

---

## YOUR TASK — TOP-UP, NOT RE-EXTRACTION

1. Read your existing `c<SR>.json` from the scratchpad root. Note what lighting/mirror
   branches it already has.
2. Re-visit the site's own navigation (mega-menu, sitemap, nav API) and find every
   room-based lighting or mirror branch **not already present** in your file — bathroom,
   vanity, outdoor, kitchen-island, recessed/track/under-cabinet lighting; bathroom/vanity
   mirrors; anything Rule 0 would now keep that the original pass skipped.
3. For each missing branch, extract it exactly like a normal row: exact qty from the site
   with `evidence`, canonical `link`, parent grouping rows if it has children. Follow THE
   ONE RULE THAT MATTERS below — no estimates.
4. **Do not touch, re-verify, or delete any row already in the file** unless you find it is
   now provably wrong (e.g. dead link) — if so, fix only that row and say why in `notes`.
5. Append the new rows into `rows` in a sensible position (near their category if one
   exists, e.g. new bathroom lighting rows go inside the Lighting parent block).
6. Update `notes` with an addendum: what Rule 0 top-up added, and how you verified it.
   Keep the original notes text, don't delete it.
7. Rewrite `c<SR>.json` to the scratchpad root, preserving `sr`/`company`/`brand_site`/
   `country`/`site_url` exactly as they were.
8. If your company's site is now hostile in a new way (was open before, blocked now, or
   vice versa), just do your best with Rule 2 network techniques below and flag anything you
   can't verify with `"flag": "MANUAL REVIEW: <reason>"` and `qty: null` rather than guessing.

**If you find nothing missing** (site never had a room-based branch, or everything was
already captured), that is a legitimate outcome — say so in `notes` and leave the file
otherwise unchanged (still fine to touch its mtime).

---

## THE ONE RULE THAT MATTERS

**`qty` must be the EXACT number of products the website itself reports for that
sub-category URL.** Never estimate. If you cannot verify it, `"qty": null` +
`"flag": "MANUAL REVIEW: <reason>"`. Every row with a qty needs an `evidence` string.

---

## RULE 2 — NETWORK: HOW TO REACH BLOCKED SITES (abbreviated, see memory for full detail)

1. Direct fetch first.
2. `curl_cffi` impersonation — brute-force the profile, it's per-site.
3. `r.jina.ai/<url>` (percent-encode multi-param query strings).
4. `translate.goog` mirrors.
5. `WebFetch` for JS interstitials.
6. Unprotected side doors: sitemaps, SFCC Search-Refinebar, Wayfair seo-sitemaps, TJX
   navMenuData.jsp, Cornerstone UnbxdAPI.
7. Keep canonical origin URLs in `link` — never a proxy URL.

`probe.py` is in the scratchpad root: `python ..\probe.py get/nav/count/sitemap/json/grep ...`
(work inside your own `w<SR>_topup\` subdirectory, only the final JSON goes to the root).

Validate before finishing:
`python -c "import json;d=json.load(open('c<SR>.json',encoding='utf-8'));print(len(d['rows']))"`

## FINAL MESSAGE

Compact summary: SR, company, how many rows existed before, how many you added, which
branches, qty of each new row, and any MANUAL REVIEW flags. No prose padding.
