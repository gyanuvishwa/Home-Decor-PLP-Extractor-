# New Arrivals — merchandising-PLP boundary rules

Load together with `../home-decor-extraction/rules/_decor-extraction-core.md`
(mechanics only). This module is the complete boundary definition for New
Arrivals; the operational, worker-facing form lives at
`pipeline/new_arrivals_json_archive/NEW_ARRIVALS_BRIEF.md` — deploy that copy
to dispatched workers.

---

## 1. TASK

Not a product-taxonomy category. Find genuine website PLPs representing
newly added products — real listing pages, not editorial or campaign noise.

---

## 2. TARGET TERMS

New Arrivals, New In, New Products, Just In, Just Arrived, Latest Arrivals,
Latest Products, What's New, New This Season, "New Collection" **only when
genuinely a product listing representing new arrivals**, Recently Added,
Newly Added — and equivalent local-language terminology.

---

## 3. COLLECTION PAGES NEED INSPECTION, EVERY TIME

Do not classify based purely on the word "Collection." Determine whether the
page is:

- **A genuine product listing** — browsable products, a count, filter/sort
  like any other category page, and the products are in fact the newest
  additions -> potentially INCLUDE.
- **A marketing/editorial landing page** — hero story, lookbook imagery,
  campaign write-up, no real product grid -> EXCLUDE.

If genuinely uncertain, still record the row with
`"flag": "MANUAL REVIEW: AMBIGUOUS NEW COLLECTION - <what you saw>"` rather
than guessing either way.

---

## 4. WORKED EXAMPLES

| Candidate | Verdict | Why |
|---|---|---|
| `/new-arrivals` — "Showing 1-24 of 47" | INCLUDE | Unambiguous target term, real listing |
| `/new-in` | INCLUDE | Unambiguous target term |
| `/collections/new` — real product grid, sortable, count shown | INCLUDE | Genuine listing despite the generic "new" slug |
| `/new-collection` — actual browsable product grid of recently added SKUs | INCLUDE, note evidence | Site genuinely uses "Collection" to mean this season's new stock |
| `/new-collection` — full-bleed hero images, a brand story, "Discover the Story" CTA, no product grid | EXCLUDE | Editorial/campaign landing page |
| `/summer-collection-2026` — themed lookbook, links out to several unrelated categories | EXCLUDE | Seasonal campaign page, not a new-arrivals listing |
| `/products/linen-throw-88` (page shows a "New" badge) | EXCLUDE | PDP, not a listing — badge is irrelevant |
| `/new-range` — some products, unclear if genuinely "just added" vs. a themed sub-line | FLAG: `MANUAL REVIEW: AMBIGUOUS NEW COLLECTION` | Genuinely uncertain — record, don't guess |

---

## 5. VALIDATION — BOTH MUST HOLD

1. Products are actually listed (a real PLP).
2. The page genuinely represents "recently added to the catalogue" — not a
   themed seasonal campaign, lookbook, or announcement that merely mentions
   new products.

---

## 6. GENUINE SUB-STRUCTURE ONLY

If the site exposes real children (e.g. `New Arrivals > Furniture New
Arrivals / Lighting New Arrivals`), preserve as grouping row + leaves. If
only one undifferentiated listing exists, output just that one row. Never
invent sub-categories.

---

## 7. MULTIPLE PLPS FOR THE SAME CONCEPT

Genuinely different listings -> keep both. True alias of the same listing ->
keep the canonical URL, note the merge decision. Don't dedupe purely because
counts match.

---

## 8. EXCLUDE

New Collection editorial pages (once confirmed non-listing), seasonal
campaign pages, marketing landing pages, blog posts, announcements,
lookbooks, individual products merely labelled "New," search-results pages,
arbitrary date-filter pages.

---

## 9. NAVIGATION / MARKETING — NEVER A NEW ARRIVALS PLP

Shop All, View All, Browse All, Collections (generic), Featured, Best
Sellers, Sale, Offers, Clearance, Outlet, Gift Guides, Blogs, Editorial,
Announcements, Lookbooks, Landing Pages, Search Results.

---

## 10. GROUPING VS. LEAF, ABSENCE PROOF, QTY, LANGUAGE, OUTPUT SHAPE

Identical to the shared core and to the Bestsellers equivalent
(`../../bestsellers-extraction/rules/bestsellers.md` §10) — grouping rows
name-only; qty is the site's own exact number with evidence; a zero-result
search is not proof of absence; output PLP/listing URL only.

---

## 11. CATEGORY / PRODUCT OVERLAP IS EXPECTED

Same product may sit in its normal product-taxonomy category (a separate
project), in Seasonal, and here in New Arrivals simultaneously. Not an
error.

---

## 12. THIS IS PLP-LEVEL EXTRACTION, NOT PDP EXTRACTION

No product-level rows. Open a PDP only to resolve a genuine PLP-boundary
question.

---

## 13. NEVER DUPLICATE THE ENGINE

Same shared architecture as `../../bestsellers-extraction/rules/
bestsellers.md` §13 — this module adds only the New Arrivals classification
boundary.

---

## 14. FINAL DECISION TEST — run for every candidate

1. Is this a real PLP/listing page? No -> exclude.
2. Does it genuinely represent newly added products, not a themed campaign?
   Ambiguous "Collection"-style name with no product grid confirmed -> flag
   for review, don't guess either way.
3. Is it a PDP merely carrying a "New" badge? Yes -> exclude.
4. Can exact qty be established? Yes -> record with evidence. No ->
   `qty: null` + manual-review flag.
5. Is this a true alias of an already-recorded listing? Yes -> keep the
   canonical one only, note why.
