# Home Decor extraction core — shared by the four decor categories

Load this together with exactly one of `lighting.md`, `kitchen-and-dining.md`,
`wall-decor.md`, `decorative-home-accessories.md`. Not used by Furniture —
`furniture.md` is self-contained.

**Source of truth:** `pipeline/BRIEF.md` (the Home Decor worker brief) and the
Rule 0 family as applied across the archived worker notes in
`pipeline/json_archive/`. This module preserves those rules; it does not restate
them more loosely. Where this file and `pipeline/BRIEF.md` disagree, the brief and
the observed behaviour of the archived extractions win.

> **One caveat about `pipeline/BRIEF.md`:** it is the batch-8 copy and its TOOLS
> section says there is no browser automation in the session. That is obsolete.
> The current standing rule is browser-only via the Claude-in-Chrome connector
> (SKILL.md §2.1). Everything else in the brief still holds.

---

## THE ONE RULE THAT MATTERS

`qty` must be the exact number the website itself reports for that sub-category
URL, carried by an `evidence` string. Never estimate, round, infer, aggregate a
parent, or sum children. `null` + `MANUAL REVIEW: <reason>` is a correct answer.
A merge nulls any qty that arrives without evidence.

---

## RULE 0 — PRODUCT TYPE BEATS ROOM

**Priority: PRIMARY PRODUCT TYPE > PRODUCT PURPOSE > WEBSITE CATEGORY > ROOM NAME.**
A room word never decides on its own, and a room word is never grounds for
exclusion. "Bathroom Lighting" and the whole Outdoor Lighting branch are in scope
as lighting; a candle filed under "Bedroom" is still a candle. Items filed under a
site's home-improvement or furniture aisles still count if the product type is in
scope.

- **Rule 0.3 — mirrors are always in scope** regardless of how the site groups them.
- **Rule 0.6 — overlap.** If two nav nodes are the same underlying listing under a
  second name/URL at the same level (identical count *and* identical facet
  breakdown), keep one and record why in `notes`. A genuine parent whose children
  are subsets becomes a grouping row rather than a double-counted leaf.

State in `notes` when a room word was kept or overridden — this is audited by
`pipeline/_roomscan.py`.

---

## WHAT TO EXTRACT

Only real product categories/sub-categories — pages that list products.

### INCLUDE
- **Glassware (ALL)**: wine/champagne/whiskey/beer/cocktail glasses, tumblers, tea
  & coffee cups, mugs, serving glassware, glass bowls/plates/pitchers/bottles/jars/
  containers, decorative glassware.
- **Tableware / dinnerware**: plates, bowls, dinner sets, serveware, trays,
  cutlery-adjacent tabletop decor (filed under `Kitchen & Dining`).
- **Lighting**: pendant, wall, ceiling, floor lamps, table lamps, lanterns,
  chandeliers.
- **Decorative Accessories**: decorative bowls/trays/plates, mirrors, wall art, wall
  decor, vases, sculptures, figurines, decorative lanterns, candle holders, candles,
  home fragrance/diffusers, artificial plants, decorative planters/pots.
- **Decorative material lines**: wooden (decorative only), ceramic, resin, marble,
  stone, terracotta, bamboo, cane, rattan.

### EXCLUDE (never extract)
Bathroom · Furniture (beds, tables incl. dining/coffee, chairs, cabinets, wardrobes)
· Storage · Kitchen appliances · Cookware/pans · Hardware · Plumbing · Construction
· Home improvement · Office furniture · Outdoor furniture · Steel/iron/aluminium/
copper products · Industrial · Utility · Food & drink consumables · Cleaning
products · Personal care · Garden tools/seeds · Textiles (rugs, cushions, curtains,
bedding, tea towels) unless the site files them under an included decor
sub-category — when unsure, exclude.

### NEVER EXTRACT (navigation/marketing, not product categories)
Collections · Featured Collections · Shop All · View All · Browse All · Explore All
· Discover · Blogs · Editorial · Gift Guides · Lookbooks · Landing pages · Sale ·
Offers · Clearance · New Arrivals · Best Sellers · Navigation pages ·
**Clocks of every kind** (wall/desk/alarm/clock collections).

Brand-name/designer listing pages are not categories. Price/colour filter pages are
not categories.

> **Note the tension, and keep it:** clocks are excluded from *extraction* by this
> brief, but the classification split routes any clock rows that do exist to Wall
> Decor. Both statements are live — do not "resolve" one by editing the other.

---

## QTY METHOD (priority order)

1. **Displayed total** — "Showing 1–24 of 186", "186 products", "186 résultats",
   "186 producten". The exact number. Best source.
2. **Structured data** — `__NEXT_DATA__`, `__NUXT__`, `window.__INITIAL_STATE__`,
   internal API/GraphQL, Algolia `nbHits`, Shopify `products_count`. Record the JSON
   path in `evidence`. (Shopify `products_count` is known-inflated — see SKILL.md §7;
   prefer the rendered header and say so.)
3. **Full enumeration** — page to the true end and count unique product IDs. Only
   valid if you genuinely reach the end. Record how.

**Sanity checks before accepting a qty**
- Does the number move when you change category? A constant number is a site-wide
  total — reject it.
- Suspiciously round (1000/5000/10000)? Probably a display cap → `null` + flag.
- Does "of N" exceed what pagination implies? Cross-check pages × page size.
- A parent total is not a sub-category total.
- Beware counts that include out-of-stock or variant rows if the site says so.

Deduplicate: if two sub-category names resolve to the same URL, keep one.

---

## LANGUAGE / NAMING

- **French, Dutch, and other non-English sites → English sub-category names.** Do
  not keep the original in parentheses. (Native + `(English)` was used only for
  Japanese sites.)
- `category` is the normalised English bucket, in order of preference: `Lighting`,
  `Kitchen & Dining`, `Home Accessories`, `Home Decor`, `Home Fragrance`,
  `Wall Decor & Mirrors`, `Garden`. The first three cover the large majority of rows.
- Sub-category wording stays faithful to the site's own naming (translated), never
  invented.
- Output cells must be plain ASCII English; `merge_final.py` enforces this and
  `_verify.py` reports a non-ASCII count of 0 after every clean merge.

---

## OUTPUT CONTRACT

One JSON file per company, `c<SR>.json`, written as soon as that company is done —
`sr`, `company`, `brand_site`, `country`, `site_url`, `status`, `failure_reason`,
`notes`, `rows[]`, each row `category` / `sub_category` / `qty` / `link` /
`is_group` / `evidence` / `flag`. Grouping rows carry name only (`qty: null`,
`link: null`). Rows in reading order, each parent immediately followed by its
children. See `pipeline/BRIEF.md` for the full field-by-field contract.

**0-product categories are dropped rather than written as a zero row** in the Home
Decor run. (The Furniture run's newer brief takes the opposite default — emit
`qty: 0`. Do not unify these without a ruling; they are separate deliverables.)

A failed company still gets a row reading `NOT EXTRACTED - <reason>`, with the
diagnosis in the companion manual-review file — except a company the user
explicitly says to skip, which is recorded only in the review file.

---

## PROVING ABSENCE

Earn it: load the real nav, check the sitemap/category tree for the relevant slugs
in English **and the site's local language**, and state in `notes` exactly what you
inspected. A site search returning 0 is not proof — two sites in this project
returned a default product set or a flat count for every query. Run a
discrimination check before trusting search.
