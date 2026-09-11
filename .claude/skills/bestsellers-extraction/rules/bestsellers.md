# Bestsellers — merchandising-PLP boundary rules

Load together with `../home-decor-extraction/rules/_decor-extraction-core.md`
(mechanics only — its own product-type inclusion/exclusion list does not
apply to this skill). This module is the complete boundary definition for
Bestsellers; the operational, worker-facing form of the same rules lives at
`pipeline/bestsellers_json_archive/BESTSELLERS_BRIEF.md` — deploy that copy
to dispatched workers, not this file directly.

---

## 1. TASK

Not a product-taxonomy category. Find genuine website PLPs representing the
company's own **Bestsellers / popularity merchandising concept** — real
listing pages the site uses to surface its best-selling products — and
capture their exact product counts with evidence. Do not look for product
types (tables, lighting, mirrors, furniture, bathroom, wall decor, etc.).

---

## 2. TARGET TERMS

Bestsellers, Best Sellers, Bestselling Products, Best Selling, Top Sellers,
Top Selling Products, Popular Products, Most Popular, Customer Favorites,
Trending Products — and equivalent local-language terminology.

---

## 3. CANDIDATE URL SHAPES — STARTING POINTS ONLY

```text
/best-sellers
/bestsellers
/best-selling
/top-sellers
/popular
/customer-favorites
```

...and their `/collections/...`, `/shop/...` equivalents. **The URL alone
never establishes validity.** Open the page.

---

## 4. VALIDATION — ALL THREE MUST HOLD

1. Products are actually listed.
2. The page represents a bestseller/popularity merchandising concept.
3. It is not merely an editorial/marketing page, and not an individual PDP
   carrying a "Bestseller" badge.

---

## 5. EXCLUDE

Bestseller blog posts, editorial pages, buying guides, inspiration pages,
marketing banners, individual PDPs, collections that merely mention
bestselling products in passing, search-results pages, arbitrary filter
pages, and any page whose only "Bestseller" signal is a badge/label on
individual products. **A product marked "Bestseller" does NOT make its own
product page a Bestsellers PLP.**

---

## 6. GENUINE SUB-STRUCTURE ONLY

If the site itself exposes real children (e.g. `Bestsellers > Furniture
Bestsellers / Lighting Bestsellers / Decor Bestsellers`), preserve that as a
grouping row + leaves — same shape as the shared engine. If only a single
`Bestsellers` listing exists (the common case), output just that one row.
**Never invent sub-categories that don't exist** just to look more thorough.

---

## 7. MULTIPLE PLPS FOR THE SAME CONCEPT

A site may expose Bestsellers through several URLs (e.g. `/bestsellers` and
`/collections/bestsellers`). Inspect each:
- Genuinely different listings (different product sets/counts) -> keep both,
  as separate rows.
- True alias of the same underlying listing -> keep the canonical URL, note
  the merge decision in `notes`.

**Do not deduplicate purely because two listings happen to report equal
counts** — confirm they're actually the same listing first.

---

## 8. WORKED EXAMPLES (final-decision test applied)

| Candidate | Verdict | Why |
|---|---|---|
| `/best-sellers` — grid of 125 products, "Showing 1-24 of 125" | INCLUDE | Real PLP, genuine bestseller concept, header count |
| `/collections/best-sellers-furniture` (a child under Bestsellers nav) | INCLUDE as sub-row | Genuine site-defined sub-structure |
| `/blog/our-top-10-bestsellers-this-year` | EXCLUDE | Editorial blog post, not a PLP |
| `/products/velvet-sofa-123` (badge says "Bestseller") | EXCLUDE | PDP, not a listing — badge is irrelevant |
| `/collections/trending` — hero banner + 3 curated looks, no product grid/count | EXCLUDE | Marketing landing page, not a real listing |
| `/search?q=bestseller` | EXCLUDE | Search-results page, not a merchandising PLP |
| `/popular` returning "0 results" every time regardless of the page checked | Investigate further before concluding absence | Could be a non-discriminating search/filter default — verify via nav/sitemap first |

---

## 9. NAVIGATION / MARKETING — NEVER A BESTSELLERS PLP EVEN IF DISCOVERED WHILE LOOKING FOR ONE

Shop All, View All, Browse All, Collections (generic), Featured, New
Arrivals, Sale, Offers, Clearance, Gift Guides, Blogs, Editorial, Lookbooks,
Landing Pages, Search Results. (Note the inversion from the shared decor
core: there, "Best Sellers" itself is on this banned list because it's
noise relative to a product-type taxonomy. Here, Bestsellers is the target —
only the surrounding marketing/nav noise is banned.)

---

## 10. GROUPING VS. LEAF, ABSENCE PROOF, QTY, LANGUAGE, OUTPUT SHAPE

All identical to the shared core and to Pet Care's equivalent sections
(`../../pet-care-extraction/rules/pet-care.md` §14, §16-21) — grouping rows
carry name only (`qty: null`, `link: null`); qty is the site's own exact
number with evidence, never estimated; a zero-result search is not proof of
absence — check real navigation, mega menu, sitemap, and local-language
equivalents first; normalize output to plain ASCII English while keeping the
site's actual meaning; output is PLP/listing URL only, never a PDP link.

Zero-product listings are dropped, not emitted as `qty: 0` rows, matching
this skill's roster (Furniture-derived), which follows that convention.

---

## 11. CATEGORY / PRODUCT OVERLAP IS EXPECTED

A product may legitimately appear in its normal product-taxonomy category
(a separate, already-completed project) AND in Bestsellers. This is not an
error and must never trigger cross-file deduplication or exclusion.

---

## 12. THIS IS PLP-LEVEL EXTRACTION, NOT PDP EXTRACTION

Do not crawl individual product pages for title/price/SKU/brand/description/
images/material/dimensions. Do not create one row per product. Open a PDP
only to resolve a genuine PLP-boundary question.

---

## 13. NEVER DUPLICATE THE ENGINE

Browser automation, navigation discovery, PLP detection, qty extraction,
evidence handling, checkpointing, JSON generation, merge, reconciliation,
verification, logging — all shared. This module adds only the Bestsellers
classification boundary.

```text
SHARED PLP EXTRACTION CORE
        |
        +-- Bestsellers rules  <- this module
        +-- Clearance rules
        +-- New Arrivals rules
```

---

## 14. FINAL DECISION TEST — run for every candidate

1. Is this a real PLP/listing page? No -> exclude.
2. Does it represent the site's own bestseller/popularity merchandising
   concept? No -> keep investigating (don't exclude on this alone).
3. Is it merely editorial/marketing, or a PDP with a badge? Yes -> exclude.
4. Can exact qty be established? Yes -> record with evidence. No ->
   `qty: null` + manual-review flag.
5. Is this a true alias of an already-recorded listing? Yes -> keep the
   canonical one only, note why.
