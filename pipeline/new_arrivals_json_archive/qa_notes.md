# New Arrivals — QA notes / open adjudication items

Log flagged judgement calls here as they arrive during batches, don't batch them
to the end (`.claude/skills/home-decor-extraction/SKILL.md` §5.8).

## Open policy question (block merging any batch that hits this at scale)

**"New Collection" / "New Season" / "New Range" — ambiguous by name alone.**
Per the user's explicit spec: do not classify based purely on the word
"Collection" — a "New Collection" page can be a genuine new-arrivals listing
or an editorial/campaign landing page, and only page inspection (products
actually listed, PLP mechanics present) tells them apart.
`merge_new_arrivals.py` force-flags any bare Collection-style name lacking an
unambiguous New Arrivals signal word (new arrivals/new in/just in/latest/
what's new/recently added) with `MANUAL REVIEW: 'COLLECTION'-STYLE NAME
WITHOUT A CLEAR NEW-ARRIVALS SIGNAL`. Adjudicate each flagged row on the
worker's page-inspection evidence in `notes`, not on the name pattern alone.

## Standing safety net (not an open question)

`merge_new_arrivals.py` also force-flags PDP-shaped links, same as the
Bestsellers/Clearance siblings — see their qa_notes.md for the caveat.

## Status

**Batch 1 (SR 1-10) done and merged 2026-09-07.** 9/10 companies have New
Arrivals, 1/10 confirmed absent after real investigation (Restoration
Hardware — no New nav item anywhere, only Labor Day promo copy mentions
"new"). 26 Review rows.

**2 genuine "New Collection" ambiguity flags this batch (SR 7 Anthropologie
Home):**
- "Seasonal Home Decor" (qty 487): passes the real-listing test, sits under
  the "New!" nav tab, but the product mix is almost entirely Christmas/
  holiday items — may belong to a Seasonal/Holiday category instead.
- "Fall Home Decor & Furniture" (qty 1122, the "New Home" hub page): passes
  the real-listing test, but its relationship to the 838-item "New Arrivals
  This Week" page and the 10 department rows under it is unclear (count is
  close to but not exactly their sum/union — may be a dedup aggregate), and
  its copy leans seasonal/editorial.

**One data-hygiene fix applied during this batch:** SR 7's source JSON
(`na7.json`) had non-ASCII "é" (Décor) in 5 category/sub_category fields —
normalized to "Decor" before merging, per the project's plain-ASCII-English
output rule. Re-merged clean afterward.

PB Kids US (SR 5) is Akamai-blocked on all 3 access tiers — 22 candidate
new-arrivals sub-pages recorded from sitemap+nav-pattern evidence only, all
flagged that even genuine-PLP status (not just qty) is unverified, since the
worker couldn't open the pages to apply the Collection-page test.

**Batch 2 (SR 11-20) done and merged 2026-09-07.** 19/20 cumulative
companies have New Arrivals, 1/20 absent (Restoration Hardware). 116 leaf
rows, 39 Review rows.

**False-positive pattern found in `merge_new_arrivals.py`'s SEARCH_URL
safety net:** SR 15 Home Centre's 11 rows all got
`LINK LOOKS LIKE A SEARCH PAGE - verify` because their URLs are shaped
`/c/<category>?q=badge.title.en%3ANEW` — a facet-filter query parameter
(Algolia-style `field:value` expression), not a free-text search box. The
worker independently verified real filtering (e.g. Decor: 223 filtered vs.
1300+ unfiltered on the same category). **These are NOT search-result
pages** — treat this specific flag on SR 15 as resolved/confirmed-genuine
when adjudicating, not as an open question. The regex itself (`[?&]q=`
always assumed free-text search) was NOT tightened, since a false positive
here is far cheaper than a missed genuine search page elsewhere — just know
this pattern will recur on any storefront using `q=` for structured facet
filters.

**2 genuine "New Collection"/noindex ambiguity flags this batch** (SR 19
Danube Home UAE): "Bath New Arrivals" and "Office Furniture New Arrivals",
both `noindex,nofollow` pages reusing generic department title/meta with no
New-Arrivals-specific branding, found only via sitemap enumeration — real
uncertainty, not a misclassification.

**Batch 3 (SR 21-30) done and merged 2026-09-07.** 29/30 cumulative
companies have New Arrivals, 1/30 absent (Restoration Hardware only). 170
leaf rows, 44 Review rows. 5 new flags: SR 22 Target Home (3 rows,
qty genuinely unverifiable — redsky API response too large for WebFetch,
but genuine-PLP status independently confirmed via SSR metadata, not just a
tooling gap); SR 25 World Market "New & Trending" (nav's own New Arrivals
link resolves to a page whose H1 says something else and whose count is far
larger than the sum of the clean per-department pages — may commingle
concepts); SR 28 Room & Board "New Arrivals" (destination of the sitewide
banner, but page itself is a 6-section curated editorial layout, no unified
count).

**Batch 4 (SR 31-40) done and merged 2026-09-07.** 39/40 cumulative
companies have New Arrivals, 1/40 absent (Restoration Hardware only, still
the sole absence across all 40 companies to date). 224 leaf rows, 44 Review
rows (no new flags this batch — all 10 companies resolved cleanly).

**Batch 5 (SR 41-50) done and merged 2026-09-08.** 49/50 cumulative
companies have New Arrivals, 1/50 absent (Restoration Hardware only, still
the sole absence across all 50 companies to date). 259 leaf rows, 44 Review
rows (no new flags this batch — every "Collection"-style candidate this
batch resolved cleanly either way: Dunelm's `/category/new` accepted despite
an SEO title of "New Collection - Seasonal Styles" because the nav itself
plainly labels it "New Arrivals" and it's a real filterable PLP; Habitat
UK's "New in" accepted on dual evidence with no ambiguity). Clean hits: Z
Gallerie (512, 8 children, parent page meta description explicitly
self-describes as new-arrivals), Surya (1901, unambiguous "New" nav node),
Nordstrom Home (6515, single undifferentiated listing, no sub-structure),
Bed Bath & Beyond (a uniform "New Arrivals" facet applied across all 10 top
departments, 13014-996), Habitat UK (157), John Lewis Home (6-way hub,
118-360 each, explicitly including Furniture/Bedding/Cushions per the
cross-project-overlap rule), Dunelm (3997; correctly excluded all 10
"New X" department mega-menu tiles as query-filtered re-cuts of the plain
category page, not genuine distinct PLPs), Made.com UK (122, exhaustively
verified by ID-paging), Swoon (34, exhaustively verified item-for-item),
OKA (166 parent + 4 children, children sum 197 > parent 166 — recorded
as-is, both are the site's own numbers).

**Batch 6 (SR 51-60) done and merged 2026-09-08.** 59/60 cumulative
companies have New Arrivals, 1/60 absent (Restoration Hardware only, still
the sole absence across all 60 companies to date). 338 leaf rows, 65 Review
rows. 1 new flag this batch: SR 51 Cox & Cox — two New listings
(`/new/` 179 and `/new/arrivals/` 150) share identical page-1 product IDs
but different totals/H1/title/meta; kept as separate rows per the
no-blind-dedup rule but flagged for the merge step's judgment since the
overlap raises a real possibility they're a near-duplicate concept. SR 54
Schoolhouse's New collection (38) also flagged — confirmed live and real
but unreachable through any current site navigation, found only via
sitemap. Clean hits: Z Gallerie/Surya/etc. pattern continues — The
Citizenry (SR 53) applied the same capped-analytics-value correction as its
Bestsellers row (78 true count via exhaustive enumeration); Williams Sonoma
Home (SR 52) landed mostly clean (135 parent + 10 children) but a few rows
carry MANUAL REVIEW flags where an Akamai block forced API-pattern-matching
instead of a live rendered-header cross-check.

**Batch 7 (SR 61-70) done and merged 2026-09-08.** 69/70 cumulative
companies have New Arrivals, 1/70 absent (Restoration Hardware only, still
the sole absence across all 70 companies to date). 371 leaf rows, 74 Review
rows. SR 63 Serena & Lily came back `partial` — parent "All New Arrivals"
fully verified (141) via one successful Claude-in-Chrome load, but all 7
children are null/flagged after the shared browser session's tab-group
became unstable under multi-worker contention (see [[let-batches-run-to-
completion]] pattern — a tooling-contention gap, not a real access
problem). 1 new ambiguous flag: SR 67 Burrow "Fall Preview" (25, every item
carries a discount badge, unclear if genuinely new stock vs. a seasonal
sale curation). Notable finds: Rowen & Wren (SR 65) distinguished
"Freshly In Stock" (genuine newness signal via its own og:description)
from a lookalike "Available Now" (a fast-delivery filter, not a newness
concept — correctly excluded); Lulu and Georgia (SR 64) found 8 genuine
site-exposed children via a real "bubbles" sub-filter row, while excluding
several orphaned new-* handles reachable only via sitemap/collections.json
with no current nav path; Rejuvenation (SR 62) confirmed via Constructor's
own `groups_max_depth=3` query that 9 room-qualified "New X" pages are a
separate flat merchandising layer (63-93% overlap, not true children of
"All New Arrivals") — correctly excluded rather than nested.

**Batch 8 (SR 71-80) done and merged 2026-09-08.** 77/80 cumulative
companies have New Arrivals, 2/80 absent (Restoration Hardware and now Ferm
Living US — the latter's "News"/"Kids News" collections exist in the
Shopify catalog but currently render a "content currently unavailable"
placeholder, a site-side rollout gap worth a spot recheck later, not a
processing error), 1/80 blocked (SR 79 QVC Home). 399 leaf rows, 75 Review
rows. Clean hits worth noting: Garnet Hill (363 parent + 3 children, sums
match exactly, no flags — a clean contrast to that same company's flagged
Clearance rows); TJ Maxx Home (563, cross-verified against two independent
count sources, exact match); Scully & Scully (194 parent + 7 children,
documented expected overlap where children sum 207 > parent 194); Container
Store Decor (341 parent + 6 children, `/whats-new` confirmed a byte-
identical alias of the canonical URL, not a separate listing).

**Batch 9 (SR 81-90) done and merged 2026-09-08.** 86/90 cumulative
companies have New Arrivals, 2/90 confirmed absent (Restoration Hardware,
Ferm Living US), 2/90 blocked (SR 79 QVC Home, and now SR 82 La Redoute UK
— see below), 430 leaf rows, 78 Review rows. **Fixed a merge-script bug
this batch**, documented fully in
[[bestsellers-clearance-new-arrivals-scaffolded]]: SR 82's na82.json (0
rows, `status: partial`, blocked by a Cloudflare CAPTCHA on every listing
page) was initially merged as "NO NEW ARRIVALS FOUND" — wrong, since the
worker's own notes explicitly say absence wasn't proven (two candidate
"mood" pages exist but couldn't be opened to check). Patched
`ledger_status()` to treat partial+zero-rows as BLOCKED across all three
merge scripts and re-ran; SR 82 now correctly shows blocked, absent count
back to the correct 2. Clean hits worth noting: Marks & Spencer Home ("Just
Arrived", 1021 parent + 8 children, gap between parent and children sum
documented not reconciled); Graham and Green (487 parent + 9 children, sum
exceeds parent — documented as the parent being a curated/capped
cross-department feed, not a strict union); Furniture Village (79, kept
despite page copy mentioning "savings" since it's clearly framed as new
designs, not a promo); Zara Home UK (377, reconciled a tile-count
discrepancy identically across two independent fetches).

**Batch 10 (SR 91-100) done and merged 2026-09-08 — 100/286 milestone.** 95/100
cumulative companies have New Arrivals, 3/100 confirmed absent (Restoration
Hardware, Ferm Living US, House of Hackney — the latter's "New In" nav
links are just a `#/sort:published_at:desc` fragment on the same category,
not a real distinct PLP), 2/100 blocked (SR 79 QVC Home, SR 82 La Redoute
UK). 463 leaf rows, 78 Review rows. Notable finds: AM.PM France (566
parent + 8 children, children sum 76 short of parent — flagged on the row
as likely non-partitioning facets, not an extraction error) despite the
brand having zero Bestsellers/Clearance presence, proving absence in two
categories doesn't predict absence in the third; La Redoute Interieurs FR
(448) found only indirectly after discovering the brand's own "Nouveautes"
nav link is a live site bug pointing to sibling brand AM.PM's New Arrivals
node instead — worth knowing if a future re-check of either brand sees
that link "fixed"; Amara (21 parent + 4 children, children sum 13 doesn't
fully partition 21, both recorded independently per brief guidance);
Conforama FR (11 rows, 1106 parent, children sum 1218 > parent, documented
as expected cross-department overlap).

**Batch 11 (SR 101-110) done and merged 2026-09-08.** 103/110 cumulative
companies have New Arrivals, 5/110 confirmed absent (Restoration Hardware,
Ferm Living US, House of Hackney, Hoeffner, XXXLutz DE — the latter has a
working "Neu" filter facet with real data but no dedicated hub page,
correctly excluded per the standing no-invented-sub-categories rule), 2/110
blocked. 473 leaf rows, 79 Review rows. 1 new ambiguous flag: SR 101 The
Socialite Family "Nouvelles Editions" (28, genuine PLP but an orphan page
found only via sitemap, untranslated French title even on the English
locale — not linked from any nav/footer). Clean hits: KARE (4 rows,
children sum 427 vs parent 430, kept as distinct real nodes rather than
merged); Connox (411, native connox.de storefront used as primary scope,
cross-checked against the connox.com English mirror); IKEA DE (1739,
matching IKEA UK's cross-check pattern exactly); Butlers (202, caught the
same collections.json inflation this site's Bestsellers/Furniture pass
already documented, exhaustion count used instead).

**Batch 12 (SR 111-120) done and merged 2026-09-08.** 113/120 cumulative
companies have New Arrivals, 5/120 confirmed absent, 2/120 blocked. 515
leaf rows, 91 Review rows — a big jump driven mostly by two real
data-quality discoveries this batch, both correctly flagged rather than
silently accepted: fonQ's (SR 111) "Nieuw"/"Nieuw in" collections don't
reliably bound to actually-new items — 5 of 7 children report counts that
equal or EXCEED their full parent department total, all individually
flagged with the specific comparison numbers; Juttu Home (SR 115) runs two
parallel non-identical "New Collection" taxonomies (different backend
category IDs) with mismatched Women/Men counts between them, 2 rows
flagged for adjudication on which is authoritative. SR 113 HKliving came
back `partial` — a plausible "Fresh stock" candidate is real but
dealer-login-gated, correctly null+flagged. Notable edge case: vtwonen's
(SR 112) "Nieuw binnen" listing is genuinely larger than Shopify's
25,000-item products.json pagination cap — even exhaustion-to-completion
isn't achievable here, so qty was correctly left null+flagged rather than
trusting the platform's own unreliable metafield count. Clean hits: Kave
Home (930 parent + 2 children, several themed marketing "New *" selections
correctly excluded as campaigns not recency listings); Zara Home ES (447,
cross-verified two independent ways, matching the GB/DE sibling pattern);
Maisons du Monde BE found two genuinely distinct seasonal listings
(Spring-Summer 1420 + Autumn-Winter 967, 19 total rows) after catching and
avoiding a stale-count bug on client-side SPA transitions.

**Batch 13 (SR 121-130) done and merged 2026-09-08.** 120/130 cumulative
companies have New Arrivals, 8/130 confirmed absent (adds Coincasa,
Denby [dead storefront], Moemax Germany to the running list), 2/130
blocked. 541 leaf rows, 91 Review rows. Clean hits worth noting: Nkuku (7
rows, caught and resolved a 1-unit count discrepancy between a page's own
"See N items" badge and exhaustive product enumeration, trusted the more
directly-verifiable enumerated number); Fenwick Home correctly preferred
the department-scoped "New In" URL over a broader mixed-department
alternative; Castorama France (15 rows, cross-verified against facet-panel
counts); H&M Home IT (567, clean, no flag, matching the UK sibling almost
exactly). No new ambiguous flags this batch for New Arrivals specifically
— the 5 standing Juttu Home "New Collection" flags from batch 12 remain
the only ones on Review from recent batches.

**Batch 14 (SR 131-140) done and merged 2026-09-08.** 129/140 cumulative
companies have New Arrivals, 8/140 confirmed absent (unchanged from batch
13 — all 10 this batch found something), 3/140 blocked (adds SR 134 Leroy
Merlin France, a confirmed IP/ASN-level block — see Bestsellers qa_notes
for the full writeup). 555 leaf rows, 93 Review rows. No new ambiguous
flags this batch. Clean hits worth noting: JYSK Denmark (526 via
"Nyheder," first Danish site, clean); OTTO Home found a genuine tag-based
mechanism (`thema=thmntag_neuheit`, 5 rows, 2 flagged for using a generic
noindex template despite showing real counts); Xenos (239 parent + 2
children, correctly excluded 3 lookalikes including a fragrance product
line and an existing category merely sorted by newest); RoyalDesign found
via a "News" route that the site's own config explicitly maps to "new
arrivals," correctly distinguished from a separate editorial "News" blog
of the same name; IKEA France (712) confirmed department "chips" are
query-param facets not separate PLPs, matching the UK precedent exactly.

**Batch 15 (SR 141-150) done and merged 2026-09-08.** 137/150 cumulative
companies have New Arrivals, 10/150 confirmed absent (adds BHV Marais
Maison, Ferm Living [confirmed twice now — see below]), 3/150 blocked. 567
leaf rows, 94 Review rows. New verify note: Normann Copenhagen's genuine
New Arrivals URL (`/products/news/`) coincidentally matches the PDP-shaped
regex heuristic — confirmed false positive (worker exhaustively verified
via pagination: 33+4=37 exact match), same benign-heuristic-miss pattern
as the standing Home Centre case, informational only. SR 145 Galeries
Lafayette resolved from `partial`/null to `ok`/qty=1144 after the required
tier-3 escalation — see Bestsellers qa_notes for the full writeup. Notable
confirmation: Ferm Living's "content currently unavailable" gap for
Sale/News collections (first found on fermliving.us, SR 73) is now
independently reproduced on the separate fermliving.com/.dk storefront too
— strengthens the read that this is a deliberate brand-wide unlaunched
merchandising tier, not a one-off glitch; worth a recheck across both
domains in a later pass. Clean hits: Sostrene Grene (383 via "Nyheder,"
correctly excluded a stale 301-redirect URL and a seasonal campaign
sub-page); RoyalDesign-style careful editorial-vs-PLP distinction repeated
at Iittala (77, correctly excluded a "Coming Soon" pre-launch teaser as
the functional opposite of New Arrivals) and Finnish Design Shop (807,
first Finnish New Arrivals hit, weekly-refresh copy).

**Batch 16 (SR 151-160) done and merged 2026-09-08.** 146/160 cumulative
companies have New Arrivals, 11/160 confirmed absent, 3/160 blocked. 597
leaf rows, 99 Review rows. **New verify pattern: 3 PDP-shaped false
positives this batch** (Normann Copenhagen, Bloomingville, Muuto — all
using a `/products/news/`-style URL that coincidentally matches the PDP
regex heuristic but are genuine listings, each independently exhaustion-
verified by its worker). Same benign-heuristic-miss class as the standing
Home Centre case; informational only, no action needed, but now a
recognizable pattern specific to this "/products/news/" URL shape on
Danish design-brand storefronts — don't waste time re-investigating it if
it recurs. 1 new ambiguous flag: SR 158 Georg Jensen's "Christmas New
Arrivals" child (64) — a genuine site-exposed child of the New Arrivals
hierarchy, but flagged as a policy question since other passes in this
pipeline conventionally exclude holiday/seasonal content; left in since
this brief has no such exclusion rule, worth a reviewer decision. Clean
hits: Broste Copenhagen (14 rows, correctly excluded a Christmas alias
that summed exactly to already-counted leaves and 2 confirmed-empty
categories); Merci Paris (7 rows, one flagged as a fully-overlapping
curated subset with no nav discoverability); House Doctor (123, correctly
merged a 100%-ID-overlap alias collection rather than double-counting).

**Batch 17 (SR 161-170) done and merged 2026-09-08.** 155/170 cumulative
companies have New Arrivals, 12/170 confirmed absent, 3/170 blocked. 614
leaf rows, 107 Review rows. 3 new ambiguous flags: SR 161 Pols Potten "La
Marzocco" (9, a coffee-machine brand-partnership nav child with no
explicit new-arrivals wording); SR 163 PAN Emirates (634, top items
include "New" as a size-label token, no visible date-added field to
independently confirm recency); SR 169 Tavola's main New Arrivals listing
(3274, flagged since it's ~71% of the entire 4633-product catalog and
functionally close to "whole catalog sorted by newest" rather than a
curated boundary — a genuinely distinct smaller listing at a different URL
was kept clean instead). Same benign PDP-shaped false positive recurred
again on a UAE PAN Emirates search-style URL (see Bestsellers qa_notes for
the full validation writeup). Noon UAE (SR 165) partial for the same
bucketed-count reason documented in Bestsellers qa_notes. Clean hits: Home
R Us UAE (3 rows, minor live-catalog drift between near-simultaneous
fetches documented not treated as an error); IKEA UAE (1231, matching all
IKEA siblings, correctly found the real page lives under a different URL
path than several dead redirect variants); OC Home UAE (466).

**Batch 18 (SR 171-180) done and merged 2026-09-08.** 165/180 cumulative
companies have New Arrivals, 12/180 confirmed absent, 3/180 blocked. 648
leaf rows, 118 Review rows. New verify pattern: 10 "bare Collection-style"
rows now (5 standing from Juttu Home + 5 new from Chattels & More's "New
Collection 2026" department rows) — all correctly on Review already since
the worker's own flags carried through the merge. 1 new flag beyond
Chattels & More: SR 173's own New Collection 2026 Accessories slice
(flagged since only 64% of products carry the site's `is_new` flag vs.
~97-100% elsewhere). Clean hits: Kmart Australia (761, flagged for a
genuine duplicate-menu-placement count mismatch — two nav paths give two
internally-verified-exact totals, 761 vs 757, correctly flagged for merge-
step adjudication rather than silently picking one); Temple & Webster (14
rows); MUJI Japan (640 via a genuine top-nav category, correctly excluded
a zero-product-link editorial lookbook campaign page); Nitori Japan (749,
clean); Aura Living UAE (5 rows, all verified via the site's embedded
payload). David Jones Home (309) and Beacon Lighting (282) both clean,
single-listing companies.

## Batch 18 (SR 181-190) — first APJ/US-warehouse-club batch

First batch to hit Australia, Singapore, and Japan; 0 non-ASCII cells
from both Japanese sites.

Clean hits: IKEA Japan (871, 新商品); Freedom Australia (2712, single
node, slow-hydrating SPA page needed a longer Playwright wait); Castlery
Singapore (9 rows: sitewide 269 + 8 category children summing to 376 >
parent — confirmed genuine multi-category-tag overlap via facet
inspection, not a bug, so not force-reconciled); Country Road Home
(8 rows: parent 196 + 7 department children, confirmed 2 URL aliases of
the parent via identical categoryId before excluding them as duplicates);
Myer Home (9 rows: two distinctly-categoryId'd "New In Home" listings,
3537 and 1739, kept separate for the same reason as its Clearance
counterpart above); Sam's Club (1 row: "New in Kitchen & Dining", 37,
deduped unique product IDs since the site's own displayed count included
non-product ad slots — correctly excluded the broader 270-item parent
node as a mixed roll-up with no clean decor-only subset).

Ambiguous/flagged (Review): House Australia's two seasonal-campaign PLPs
(New Season Autumn Winter 286, New Season Spring Summer 404) — real
counted PLPs but department-scoped seasonal marketing, unclear if they
belong here or to the separate Seasonal project; Francfranc Japan's
"New Items" (7) flagged as an orphan sitemap-only listing with no live
nav path, distinguished from the excluded new_items/new-<dept> family
(each confirmed a 95-100% subset of its base department, not a genuine
curated "recently added" listing).

Costco: see bestsellers qa_notes' Costco writeup — orchestrator follow-up
confirmed the leading candidate /whats-new.html (found via sitemap) still
serves Akamai's challenge wall even via a real interactive browser
(genuinely blocked, not a tooling gap), and the homepage's "What's New"
banner routes to a generic keyword-search page instead, not that URL.
Status upgraded blocked->partial, ledger classification unchanged;
/whats-new.html remains an open lead for a future access-route retry.

## Batch 19 (SR 191-200) — US big-box + Canada, first Etsy marketplace test

Clean hits: Simons Maison (893, single node, confirmed real product
grid/pager not editorial, via a full category-sitemap enumeration);
Sur La Table (9 rows: a 0-qty pure-grouping parent hub linking 8 real
"New in <Dept>" children, 2 redirect aliases correctly folded in);
Structube (1 row, qty=1 — a single current product, parent+child would
have double-counted so only the parent was kept); Kohl's Home (5 rows:
Home-scoped aggregate 3,545 + 4 genuinely distinct department listings).

Clean absence: Etsy US — "Most Recent" is a generic sort applicable to
any category/query, not a distinct New-Arrivals PLP with its own
identity/count; confirmed via a sitewide (not just Home&Living) category
sitemap check.

Flagged (Review): Quince Home hit the same pagination-ceiling issue as
its Bestsellers sibling (verified floor 20 vs. inflated site total 221);
Walmart's Furniture (2022) and Storage (1949) New Arrivals both capped
at "1000+" display and flagged per this company's established
prior-pass convention that capped Walmart counts are unreliable at
scale; JCPenney's Kitchen&Dining (2853) and Home Decor (3661) New
Arrivals rows both flagged for a co-active "View All Brands" chip whose
effect on the count couldn't be confirmed one way or the other; Indigo
Home's "New in Stationery & Gifts" (380) flagged for scope ambiguity —
sample titles are dominantly Home/Lifestyle merchandise despite the
"Stationery" name, likely the Lifestyle department's own listing under
a legacy handle.

## Batch 20 (SR 201-210) — Wayfair-family cluster + luxury/lighting retailers

Clean hits: AllModern (14 rows: main curated page 277 + 13 category
children summing to 663, kept as siblings not parent/child since the
main page is an independently-curated top-picks selection, not an
aggregate — deliberate overlap, not a bug); Birch Lane (166, "All New
Arrivals" child of a pure hub, room-themed curations like "New in
Bathroom" correctly excluded as hand-picked marketing not a real
partition); Joss & Main (11 rows: parent 585 + 10 children summing
exactly, confirmed a true roll-up); Bouclair (467 parent + 10 department
children, exhaustion-verified); Shades of Light (8 rows: 703 parent + 7
family children, one sitemap-only alias correctly not double-counted);
Grandin Road (9 rows: sitewide hub 409 + 8 per-department pages,
explicitly ruled out the seasonal-vs-standing ambiguity flagged in the
task brief — Halloween/Christmas/Seasonal are permanent departments with
the same New Arrivals mechanism as Furniture/Decor here, not one-off
campaigns, so correctly NOT flagged for that reason).

Clean absence: EQ3 (exhaustive full-nav-tree + sitemap check, no New
Arrivals node exists anywhere).

Flagged (Review): Lamps Plus's "New & Trending" (38,641, see bestsellers
qa_notes' writeup); Saks Home's Home-scoped isNew filter (197) flagged
since it's reached via the same filter mechanism as the official Women's
New Arrivals nav link rather than a dedicated Home New Arrivals page;
Grandin Road's Halloween New Arrivals — site's own numberOfProducts field
claims 114 but exhaustive pagination found only 105 distinct products (4
partNumbers duplicated across pages, a pagination/sort-stability bug) —
qty=105 used as the verified figure.

## Batch 21 (SR 211-220) — high-end design/lighting + first India-market companies

**Merge-script bug found and fixed this batch — see bestsellers
qa_notes' full writeup.** SR 214 Terrain's New Arrivals row (413,
exhaustively verified) was being silently pruned because the worker
marked it `is_group:true` with no children submitted (a DataDome block
mid-session prevented opening the 7 real child pages it found). Fixed by
flipping is_group to false; the parent-listing finding is now correctly
in Output/Review instead of vanishing. A companion project-wide scan
found 2 more historical instances of the same pattern in Clearance.xlsx
only (SR 49, SR 55) — see clearance qa_notes.

Clean hits: Design Within Reach (10 rows: parent 478 + 9 department
children, expected cross-department overlap); Hudson Valley Lighting
(10 rows: parent 1680 + 9 children, same overlap pattern); Milton
(5 rows across sitewide + 4 sibling brands); Visual Comfort (6 rows:
sitewide 353 + 5 category pages kept as peers since combined qty exceeds
the sitewide figure, proving they aren't a nested subset).

Clean absence: Pepperfry (exhaustively checked: 9-vertical nav, footer,
full sitemap-index, ~18 URL-shape guesses, banner-tile cross-checks — no
recency-based listing exists anywhere; the marketplace-vs-retailer
scrutiny from Etsy US was applied but Pepperfry's own findings were
genuine site-level pages either way, not per-seller badges).

Flagged (Review): Terrain's restored 413-item row (4-item API/render gap,
same pattern documented for this company in an earlier project pass);
Visual Comfort's two "New and In Stock" pages (142, 113) flagged for
blending "new" with "in stock" availability, a different concept from
pure recency.

## Batch 22 (SR 221-230) — all-India batch, including 3 fashion marketplaces

Clean hits: IKEA India (558, see bestsellers qa_notes' 6-locale-pattern
writeup); H&M Home India (461, needed Claude-in-Chrome tier-3 after
Akamai blocked HTTP+Playwright); Westside Home (600, exact via
products.json pagination); Vaaree (40 rows, all exhaustion-verified
against the site's own "N Products" count).

Clean absences: Myntra, Flipkart, AJIO (all 3 marketplaces — see
bestsellers qa_notes' writeup).

Flagged (Review): FOS Lighting's New Arrivals (homepage-only carousel,
50 distinct links found by manual count but no standalone PLP/no
site-reported total, correctly qty=null rather than guessed); Urban
Ladder's 8 sitemap-only per-room New Arrivals pages (all real listings,
none cross-linked from the hub, each other, or current nav — flagged for
currency/freshness rather than trusted at face value); notably Urban
Ladder's actual nav "New Arrivals" link routes to a themed "Oasis
Collection" marketing page with no product grid at all — correctly
excluded, with the real canonical /collection/new-arrivals (1056) used
instead.

## Batch 23 (SR 231-240) — second all-India batch

Clean hits: Clay Craft India (740, exhaustive enumeration over an
inflated site field); WoodenStreet (29); Fabindia (2 rows, cleanly
scoped to Home/Furniture only, excluding a sitewide listing that mixes
apparel).

Notable: Nykaa Fashion Home needed Claude-in-Chrome tier-3 after Akamai
blocked BOTH HTTP and Playwright entirely (even the plain homepage) —
unlike the 3 marketplaces in batch 22 (Flipkart/Myntra/AJIO, all fully
absent), this one DID turn up 2 genuine New Arrivals listings (11,483
and 3,509) while Bestsellers/Clearance came back absent — a useful
reminder not to assume all marketplaces behave identically.

Flagged (Review): @home by Nilkamal's "New Collections" (14, real PLP
but no on-page confirmation it tracks recency vs. a named range); Ankur
Lighting's "Latest Collection" (2, unlinked from nav, found via sitemap
only); Borosil's New Arrivals rows (same broad/nested-collection pattern
as its Bestsellers — see bestsellers qa_notes); Jainsons Lights (500,
timestamp-based recency couldn't be independently confirmed); Pottery
Barn India's 2 rows (a seasonal-named nav-linked page vs. a larger
unlinked sitemap-only page — genuine ambiguity, human call needed on
which is canonical).

## Batch 24 (SR 241-250) — third all-India batch

Clean hits: Home Centre India (62, the predicted `?q=badge` pattern
reproducing from UAE — see bestsellers qa_notes); Chumbak (403, double-
verified); Ikiru (2767, sitemap-cross-checked); Mason Home (177,
exhaustive count overriding an inflated site field).

Clean absences: Tata CLiQ Luxury Home, Zara Home India (see bestsellers
qa_notes), HomeStop, Meesho.

Flagged (Review): Wonderchef's 2 unlinked/sitemap-only rows (one a
near-superset of its own canonical listing, one department-tagged with
zero overlap); Address Home's 2 unlinked candidates including one with
an evident typo'd handle ("New Arrivalsss") — likely a stale duplicate
from a prior site revision but live and returning real distinct
products, so recorded rather than dropped.

## Batch 25 (SR 251-260) — fourth all-India batch

Clean hits: The Decor Kart (6 rows, parent+5 children); ellementry (111);
West Elm India (184, plus 1 flagged sibling — see below); The White Teak
Company (5 rows, several dead nav-link aliases correctly de-duplicated
via 301-redirect detection); The Bombay Store (2, small but exact);
Whispering Homes (14 rows: nav-listed 7 plus 6 more genuine children
found only via sitemap, 3 verified-empty ones correctly dropped);
Freedom Tree (27); India Circus (74).

Clean absences: Beruru, Good Earth (both thoroughly checked, no
ambiguity).

Flagged (Review): West Elm India's "Spring Summer 2025 Collection" (144)
— its own title says "Shop New Arrivals" but the content is over a year
stale as of this check, a judgment call on whether a dead seasonal
campaign page still counts as a live New Arrivals sub-listing.

## Batch 26 (SR 261-270) — fifth all-India batch

Clean hits: Objectry (51); Oorjaa (6, small orphan but genuine); Sarita
Handa (795 parent + 5 children, no flags); Kapoor E-Illuminations (194);
Nicobar (137, correctly scoped to Home); Jaypore (461, Home-Decor-
filtered, unambiguous — the one clean concept at a company whose
Bestsellers turned out messy); The Artment (5, dated products actually
confirmed genuine recency unlike a similarly-named decoy); Orange Tree
(5 rows: parent+3 children clean); SPIN (2 clean rows, a nav-linked
collection correctly excluded as a marketing-landing reuse with no real
product grid).

Flagged (Review): The Purple Turtles' "Fresh Arrivals" (285, a close
synonym rather than verbatim target term, orphaned from nav but a
genuine subset of the main listing); Orange Tree's second "New Arrivals"-
titled collection (93, sitemap-only, possibly stale/superseded).

## Batch 27 (FINAL — SR 271-285) — UK department stores + last stragglers, PROJECT COMPLETE

**Cross-company duplicate found and fixed — full writeup in bestsellers
qa_notes' Batch 27 section.** SR 82 "La Redoute UK" restored: its
previously-inconclusive `rows: []` (blocked, absence not proven)
replaced with SR 278's 12 verified rows (parent "New In Home" hub + 11
genuine department PLPs, each independently confirmed via its own
"New In `<Dept>`" H1). SR 278 emptied as fully redundant.

**PROCESSING ERROR is now 0 — the full 285-company roster is done.**

Clean hits: The Range (5 rows); Wayfair UK (17 rows, all genuine
distinct curated Event PLPs, confirmed "New Rugs" vs "New-In Rugs" are
NOT aliases); Lakeland (6 rows: parent + 5 department children); ProCook
UK (3 rows: parent + 2 children, tag-filter overlap not an error);
Harrods Home (506); Selfridges Home (275, double-verified); Liberty
London Home (75); The Conran Shop (56, triple-verified); Home Box UAE
(genuinely absent post-Cloudflare-breakthrough, sort-order variant
correctly distinguished from a real filtered listing).

Partial (genuine access gap, not false absence): Argos Home — Akamai
blocked the homepage/mega-menu across all 3 tiers, correctly marked
`partial` rather than a confirmed absence; also documents a
`/list/<any-slug>/` false-positive trap worth remembering for any future
Argos-family retry.

Blocked (Claude-specific robots.txt, new this batch): home24 Germany,
El Corte Inglés Home, Made in Design, Amazon UAE.

Next: PROJECT COMPLETE. No further batches — see memory file for final
totals and the standing Review-sheet backlog.
