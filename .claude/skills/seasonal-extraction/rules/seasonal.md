# Seasonal / Holiday — category boundary rules

Load with `../../home-decor-extraction/rules/_decor-extraction-core.md` (see
`../SKILL.md` §1). This file defines only the Seasonal category boundary and
classification rules — it does not restate the shared browser/navigation/PLP/
qty/checkpoint/merge/verify engine, and it must not be turned into PDP
extraction: don't crawl PDPs for titles, prices, SKU, materials, dimensions,
descriptions, variants, or attributes. A PDP may be opened only to resolve a
genuine category ambiguity.

**This is one unified extraction, not one run per holiday.** A single
company visit discovers and extracts every genuine seasonal/holiday category
the site's own taxonomy presents — Christmas, Diwali, Halloween, whatever
combination that company actually has. There is no per-occasion routing:
`../SKILL.md` §1 has one row, "Extract Seasonal," not one row per holiday.

---

## 1. TASK

Extract genuine Seasonal product-listing/category pages. A valid row:

1. is a genuine PLP/category page,
2. is a category the website itself associates with a specific holiday,
   festival, celebration, seasonal event, annual occasion, festive period, or
   seasonal shopping period,
3. lists products,
4. has a valid category/sub-category name,
5. has its own PLP URL,
6. has an exact site-reported qty where available (shared qty rules).

`WEBSITE → real navigation → seasonal/holiday category tree → seasonal
sub-categories → valid PLPs → exact qty+evidence → category/sub-category/
link → JSON → merge/reconciliation.`

The exact seasonal categories present will vary company to company. Do not
assume every company has every festival/holiday — absence of one is not an
error, and presence of several unrelated ones on the same company is normal
(see §5, multiple festival nodes).

---

## 2. WHAT COUNTS AS A SEASONAL CATEGORY

The strongest evidence is the site's own navigation/category taxonomy. A
category qualifies when the website presents it as associated with a
holiday/festival/celebration/seasonal event — not because a product happens
to be seasonal, and not because a page merely uses seasonal colors or
timing.

Valid examples: `Christmas`, `Christmas Decorations`, `Christmas Ornaments`,
`Christmas Lighting`, `Christmas Tableware`, `Christmas Gifts`; `Diwali`,
`Diwali Decor`, `Diwali Lighting`, `Diwali Candles`, `Diwali Gifts`;
`Halloween`, `Halloween Decor`, `Halloween Decorations`, `Halloween
Lighting`, `Halloween Party`, `Halloween Accessories` — when each is a
genuine product-listing page.

---

## 3. DISCOVERY VOCABULARY — NOT A REQUIREMENT LIST

Use the lists below to *find* categories, never to require or invent them. A
company that lacks a holiday entirely is a correct `NO_SEASONAL` outcome for
that holiday, not a gap to fill.

**Christmas** — Christmas, Christmas Decor, Christmas Decorations, Christmas
Ornaments, Christmas Tree, Christmas Tree Decor, Christmas Lighting,
Christmas Tableware, Christmas Party, Christmas Stockings, Christmas
Wreaths, Christmas Accessories, Christmas Gifts, Festive Decor, Holiday
Decor, Holiday Decorations.

**Halloween** — Halloween, Halloween Decor, Halloween Decorations, Halloween
Ornaments, Halloween Lighting, Halloween Party, Halloween Tableware,
Halloween Accessories, Halloween Costumes, Halloween Props, Halloween
Outdoor Decor, Halloween Indoor Decor. Only include a subcategory when it is
a genuine product-listing category.

**Diwali** — Diwali, Diwali Decor, Diwali Decorations, Diwali Lighting,
Diwali Diyas, Diwali Candles, Diwali Lanterns, Diwali Tableware, Diwali
Gifts, Diwali Accessories, Festive Decor, Festival Decor. **Do not assume
every "Festive" category means Diwali** — use the site's actual context to
determine the real seasonal association (see §9).

**Valentine's Day** — Valentine's Day, Valentine, Valentine's, Valentine
Gifts, Valentine's Decor, Valentine Decorations, Valentine Accessories,
Valentine Tableware, Valentine Party, Valentine Lighting.

**Easter** — Easter, Easter Decor, Easter Decorations, Easter Eggs, Easter
Tableware, Easter Party, Easter Gifts, Easter Accessories, Easter Ornaments.

**Thanksgiving** — Thanksgiving, Thanksgiving Decor, Thanksgiving
Decorations, Thanksgiving Tableware, Thanksgiving Party, Thanksgiving
Accessories, Thanksgiving Lighting.

**New Year** — New Year, New Year's, New Year Decor, New Year Decorations,
New Year Party, New Year Tableware, New Year Accessories, New Year Lighting.

**Indian festivals** — Holi, Raksha Bandhan, Rakhi, Navratri, Dussehra, Eid,
Eid Decor, Eid Decorations, Ganesh Chaturthi, Janmashtami, Pongal, Onam,
Durga Puja, Karwa Chauth, Makar Sankranti, Baisakhi. Only extract categories
that actually exist on the website — never manufacture a festival category
from individual product names.

**Other genuine seasonal events** — Mother's Day, Father's Day, St.
Patrick's Day, Independence Day, Black Friday, Back to School, Summer,
Winter, Spring, Autumn/Fall, Wedding Season, Party Season, and any other
genuine seasonal/holiday category that appears in the site's own taxonomy.
**Do not automatically classify every seasonal-looking marketing page as a
Seasonal product category** — it must still satisfy §4's PLP requirement.

**Search-discovery terms** (for finding categories, never as proof of
inclusion): Christmas, Xmas, Holiday, Festive, Halloween, Diwali, Deepavali,
Easter, Valentine, Thanksgiving, New Year, Holi, Rakhi, Raksha Bandhan, Eid,
Navratri, Dussehra, Festival, Festivals, Seasonal, Season, Holiday Shop,
Festive Shop. The site's actual taxonomy is always the final authority, not
the vocabulary list.

---

## 4. CATEGORY VS. MARKETING PAGE — CRITICAL

A seasonal nav item is not automatically a valid row.

**Valid:** `Christmas → Christmas Decorations`, where "Christmas
Decorations" is a genuine PLP listing products.

**Invalid:** `Christmas Sale` as a pure promotional campaign page. Also
exclude, unless the existing extraction core's PLP test says otherwise:
Christmas Sale, Diwali Offers, Halloween Sale, Black Friday Sale, Festive
Offers, Holiday Deals, Christmas Landing Page, Gift Guide, Christmas
Inspiration, Christmas Lookbook, Holiday Blog, Festival Blog. The shared
core's existing marketing/navigation exclusions (Collections, Shop All, View
All, Sale, Offers, Editorial, Gift Guides, and similar) apply here
unmodified.

**"Collection" is not itself disqualifying.** `Christmas Collection` as a
pure landing/marketing page → exclude. `Christmas Collection` as a genuine
product-listing category with a product grid and category-level quantity →
evaluate normally under the shared PLP rules. Never decide on the word
"Collection" alone — inspect the actual page type.

---

## 5. SEASONAL PRODUCT TYPE ≠ SEASONAL CATEGORY

Do not create a Seasonal row just because an otherwise-normal category
contains some seasonal products. `Home Decor` containing some Christmas
products does not make Home Decor a Christmas category. `Lighting`
containing Diwali lamps does not make all of Lighting Diwali. The category
itself must be seasonally defined or explicitly associated with the seasonal
event by the site's own taxonomy — not merely host some seasonal inventory.

---

## 6. SEASONAL THEME VS. SEASONAL CATEGORY

Distinguish: `Christmas Decorations` (a real seasonal category → include);
`Decorative Accessories` that happens to contain Christmas ornaments (a
normal category with seasonal-themed products → not automatically Seasonal);
`Christmas Gifts` (investigate whether it's a genuine PLP or a landing/
marketing page before deciding — don't include on the name alone).

---

## 7. PRODUCT-TYPE OVERLAP WITH OTHER CATEGORIES — COEXISTENCE, NOT THEFT

**This differs from every prior category's boundary discipline.** Furniture/
Textile/Storage/Pet Care each avoid claiming a record another category owns
more strongly (a strict either/or). Seasonal does not work that way: a
Seasonal category may legitimately contain products that would normally
belong to Home Decor, Lighting, Kitchen & Dining, Wall Decor, Decorative
Accessories, Furniture, Textile, Pet Care, etc. **Do not move those products
into their normal category, and do not exclude a genuine seasonal PLP just
because its products also fit another category.** If the site provides a
genuine seasonal PLP such as `Christmas Lighting`, that PLP belongs to the
Seasonal extraction — full stop. The same product may correctly appear in
both a Christmas PLP and a Home Decor PLP, because these are different
taxonomic contexts on the site, not competing claims on one product. The
extraction is based on the website's seasonal category taxonomy, not on
forcing every product into exactly one global category.

This also means: **do not reassign or edit records in the other completed
category workbooks.** Seasonal is a separate deliverable (`Seasonal.xlsx`)
layered on top of the existing ones, never a correction to them.

---

## 8. ROOM NAMES DO NOT DECIDE THIS ALONE

`Christmas Kitchen`, `Christmas Living Room`, `Halloween Outdoor`, `Diwali
Home`, `Christmas Bedroom` — a room name doesn't determine Seasonal status
either way. If the website clearly establishes the branch as seasonal and
the page is a genuine product-listing page, it may qualify; follow the
site's actual category hierarchy, not the room word alone.

---

## 9. PARENT / CHILD STRUCTURE

Preserve the shared grouping logic. Example:

```
Christmas
 +-- Christmas Decor
 +-- Christmas Lighting
 +-- Christmas Tableware
 +-- Christmas Ornaments
 +-- Christmas Gifts
```

A genuine parent whose children are subsets stays a grouping row (name
only, `qty: null`, `link: null`) rather than becoming duplicate leaf data —
never double-count parent and child quantities.

---

## 10. MULTIPLE FESTIVAL NODES — DISCOVER, DON'T ASSUME A SINGLE ROOT

A company may organize seasonal categories as:

```
Festivals                      Holiday Shop
 +-- Diwali                     +-- Christmas
 +-- Holi                       +-- Halloween
 +-- Christmas                  +-- Valentine's Day
 +-- Eid
```

or as flat top-level nav items with no shared parent at all. Discover the
actual structure on each company; do not assume a single "Seasonal" root
category exists, and search seasonal branches throughout the site's real
navigation, not just one expected location.

---

## 11. MULTILINGUAL DISCOVERY

Do not search only English terms — inspect the site's local-language
navigation and category structure; local-language seasonal terminology can
differ significantly from English. Normalize the final `category`/
`sub_category` into English per the shared output convention, faithful to
the site's actual meaning. Do not invent a translation when the category
meaning is unclear.

---

## 12. SEARCH STRATEGY / DISCOVERY PRIORITY

1. Main navigation
2. Mega menu
3. Seasonal/Holiday navigation
4. Category/subcategory tree
5. Internal site search
6. Sitemap/category tree
7. Other internal category links

Search terms (§3) are for discovery, never proof. The site's actual taxonomy
is the final authority.

**A zero-result internal search is not proof of absence** — some sites
return default/non-discriminating results for any query (shared trap, see
`../../home-decor-extraction/SKILL.md` §7). Before marking a company
`NO_SEASONAL`: inspect navigation, mega menus, relevant sitemap/category
structures, likely seasonal/local-language slugs, and run a discrimination
check where needed. Only then record absence, with `notes` documenting what
was checked.

---

## 13–14. QTY AND OVERLAP

Use the shared qty method and priority exactly (displayed PLP total →
structured/API count → full enumeration only when genuinely required).
Record the exact number with evidence (`"Showing 1-24 of 128"`, `"128
products"`). Never estimate, round, infer, sum children, or copy a parent/
site-wide number; `qty: null` + `MANUAL REVIEW: <reason>` when it can't be
established — never fabricate.

The same seasonal PLP may be reachable through Seasonal, a named holiday,
Holiday, Decorations, Festive, Search, or another nav branch. If two nodes
resolve to the same underlying listing with identical evidence/count/facet
structure, keep one row and record the overlap in `notes` — the shared
overlap rule, no exception here.

---

## 15. URL NORMALIZATION

Use the shared URL normalization. `link` must be the actual category/PLP
URL. Never output a PDP URL, search URL, tracking/campaign URL, blog/
editorial URL, image URL, or pagination URL, unless the shared core
explicitly identifies it as the canonical category/PLP URL.

---

## 16. NO PDP CRAWLING FOR BULK VALIDATION

If the page itself clearly establishes `Christmas → Christmas Decorations`
and is a genuine product listing, classify the PLP directly. Never open
every product, or a large sample of products, just to decide whether a
category is seasonal. PDP inspection is exceptional — only to resolve an
actual ambiguity or technical issue.

---

## 17. WHAT NOT TO EXTRACT

Never extract: Blog, Editorial, Lookbook, Inspiration, Gift Guide, Sale,
Offers, Clearance, Coupon pages, promotional landing pages, Brand pages,
Designer pages, search-result pages, filter-only pages, price-only pages,
colour-only pages, general campaign pages, generic Shop All / View All /
Browse All / Explore All — unless the shared extraction engine's own PLP
test says the page genuinely is a product-listing category and the rules
above permit it.

---

## 18. COMPANY STATUS — LEDGER VALUES

Every company gets a final status; never leave one silently incomplete:

`FOUND` (real Seasonal categories captured) · `NO_SEASONAL` (no genuine
seasonal category exists, after real investigation per §12 — `notes` must
document what was checked) · `BLOCKED` (site inaccessible per the shared
access-tier rules) · `POLICY_OPT_OUT` (a Claude-specific robots.txt
disallow, per the shared core's rule 3) · `ERROR` · `PENDING`.

---

## 19. OUTPUT CONTRACT

Same company JSON shape as every other category run: `sr, company,
brand_site, country, site_url, status, failure_reason, notes, rows[]`. Each
row: `category, sub_category, qty, link, is_group, evidence, flag` — no new
schema.

**Category naming:** `category` is the holiday/festival name itself,
normalized to clear English — `Christmas`, `Halloween`, `Diwali`, `Easter`,
`Valentine's Day`, `Thanksgiving`, `New Year`, `Holi`, `Raksha Bandhan`,
`Eid`, etc. `sub_category` is the specific product type under that holiday,
faithful to the site's actual taxonomy — `Christmas Decorations`,
`Christmas Ornaments`, `Christmas Lighting`, `Diwali Decorations`, `Diwali
Lighting`, `Halloween Decorations`, `Halloween Party`. Do not invent a more
specific subcategory than the website actually provides.

---

## 20. FINAL DECISION TEST — run for every candidate

1. Is this a real product-listing page? No → exclude.
2. Does the website explicitly associate this page/category with a holiday,
   festival, or seasonal event? No → exclude, or keep investigating if
   genuinely unclear (don't exclude on ambiguity alone).
3. Is it a real category/sub-category rather than a marketing/editorial
   page? No → exclude.
4. Does it have its own valid PLP/category URL? No → exclude.
5. Can exact qty be established? Yes → record with evidence. No → `qty:
   null` + manual-review flag.
6. Is it a duplicate/overlap of another seasonal PLP already captured? Yes →
   apply the overlap rule (§13–14).

---

## 21. NEVER DUPLICATE THE ENGINE

Browser automation, navigation discovery, PLP detection, qty extraction,
evidence handling, checkpointing, JSON generation, merge, reconciliation,
verification, logging — all shared, unchanged. This module adds only the
Seasonal classification boundary and taxonomy.

```
SHARED EXTRACTION CORE
        |
        +-- Furniture / Textile / Storage / Pet Care rules
        |
        +-- Kitchen & Dining / Lighting / Wall Decor / Decorative rules
        |
        +-- Seasonal rules   <- this module (all holidays, one pass)
```

---

## 22. ACCURACY PRIORITY

```
Correct seasonal PLP
      >
Correct category hierarchy
      >
Exact qty + evidence
      >
Complete seasonal coverage
      >
Deduplication
      >
Performance
```

Never sacrifice category accuracy merely to increase Seasonal row count.

---

## 23. STANDARD

For every company: discover every genuine seasonal/holiday branch actually
present (never assume a fixed set), inspect the relevant PLPs, distinguish
grouping nodes from leaves, capture exact qty with evidence, avoid duplicate
listing URLs, exclude marketing/navigation and theme-only (non-category)
pages, let seasonal PLPs coexist with other categories rather than stealing
from them, record absence only after real investigation, write the company
JSON immediately on completion.
