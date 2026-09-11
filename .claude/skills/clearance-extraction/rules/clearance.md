# Clearance — merchandising-PLP boundary rules

Load together with `../home-decor-extraction/rules/_decor-extraction-core.md`
(mechanics only). This module is the complete boundary definition for
Clearance; the operational, worker-facing form lives at
`pipeline/clearance_json_archive/CLEARANCE_BRIEF.md` — deploy that copy to
dispatched workers.

---

## 1. TASK

Not a product-taxonomy category. Find genuine website PLPs representing
products the site itself merchandises as permanently-marked-down /
end-of-line — real listing pages, not editorial or promotional noise.

**OUTLET IS NOT CLEARANCE (policy correction, 2026-09-11).** A page whose
own branding, nav label, breadcrumb, or page `<title>`/H1 identifies it as
Outlet — "Outlet", "Outlet Store", "Outlet Products", "Outlet Collection",
"Outlet Sale", "Outlet Deals", a distinct outlet storefront/subdomain (e.g.
`brandoutlet.com`), or any equivalent Outlet merchandising concept — is
**excluded outright**, even if it is permanently-marked-down, end-of-line,
or seconds/returns stock, and even if a worker's prior judgement treated it
as clearance-equivalent. Outlet is judged a distinct merchandising channel
from Clearance for this project, not a synonym or sibling of it. This
applies regardless of how the child listings under an Outlet section are
worded (e.g. `Outlet - Bedroom`, `Furniture Outlet`) — the whole branch is
excluded. See §3.2 for the one hybrid case that survives review.

**OPEN BOX IS NOT CLEARANCE EITHER (policy correction, 2026-09-11).** Same
treatment as Outlet: a page branded "Open Box" / "Open Box Deals" / "Open
Box Returns" / "Open Box Clearance Sale" / any equivalent — previously-
opened, returned, or like-new/cosmetically-marked inventory sold at a
discount — is excluded outright, even when it sits under a site's own
"Clearance"/"Sale" nav umbrella or a worker's judgement calls it permanent-
markdown-equivalent. Open Box is a distinct merchandising concept
(condition-based, not stock-clearance-based) from this project's Clearance
target.

---

## 2. TARGET TERMS

Clearance, Clearances, Clearance Sale, Clearance Products, Final Sale, Final
Clearance, Last Chance, Last Chance Products, End of Line, Discontinued
(when merchandised clearance-style) — and equivalent local-language
terminology. **"Outlet" and "Clearance Outlet" are explicitly NOT target
terms** — see §1 and §3.2. **Neither is "Open Box" in any form** ("Open Box
Deals", "Open Box Returns", "Open Box Clearance Sale") — see §1.

---

## 3. CLEARANCE VS. SALE — THE CENTRAL DISTINCTION

Do NOT automatically include every Sale/Offers/Deals/Promotions/Discounts/
Special Offers page as Clearance.

**Inspect the page and the site's own taxonomy.**

- If the site clearly treats the page as **Clearance / Final Clearance /
  Last Chance / End of Line** -> qualifies.
- If the site clearly treats the page as **Outlet** in any form (own
  branding, nav label, breadcrumb, page `<title>`/H1, or a distinct outlet
  storefront/subdomain) -> **excluded per §1**, regardless of how
  clearance-like the underlying stock is.
- If it is a **generic temporary promotional sale** -> do NOT automatically
  include it as Clearance.
- **If uncertain -> flag for manual review rather than guessing.**

Signals that a "Sale" page is actually clearance-equivalent: on-page copy
describing permanent markdowns / discontinued stock / limited final
quantities; a breadcrumb or nav label that says Clearance even if the URL
slug says `/sale`; the listing persisting unchanged across visits/weeks
rather than rotating with a campaign calendar. Signals it's a generic
promotion: tied to a named campaign (Black Friday, a seasonal sale, a
percent-off code), explicitly time-boxed copy ("ends Sunday"), or it's the
storewide discount mechanism rather than a specific stock category.

---

## 3.2 OUTLET vs. HYBRID "CLEARANCE & OUTLET" DEPARTMENTS

Some sites bundle Clearance and Outlet under one umbrella nav label (e.g. a
department breadcrumb literally reading "Clearance & Outlet") while the
actual child listings underneath are individually Clearance-branded (URL
slugs / API category codes / page titles all say "clearance", none say
"outlet"). In that specific shape — the outlet wording appears ONLY at the
umbrella/department level, never on any actual leaf listing — keep the
Clearance-branded leaves and don't let the umbrella's label taint them.
Log the call to `qa_notes.md` either way so it's auditable.

If instead the page's OWN `<title>`/H1/nav item is itself branded "Outlet"
(even if "Clearance" appears elsewhere in the title, e.g. `"The Outlet |
Clearance | Brand"`), that page is Outlet, not Clearance — exclude it per
§1, do not keep it on the strength of the word "Clearance" appearing
alongside "Outlet" in the same title.

---

## 4. WORKED EXAMPLES

| Candidate | Verdict | Why |
|---|---|---|
| `/clearance` — "84 items", breadcrumb "Home > Clearance" | INCLUDE | Strict clearance term, real listing |
| `/outlet` — permanent outlet-store style section, own nav label "Outlet" | EXCLUDE (per §1 policy correction) | Outlet is its own merchandising channel, not Clearance, regardless of permanence |
| `/sale` — "Clearance Sale - final reductions on discontinued styles" copy, same listing every visit | INCLUDE, note evidence | Generic-sounding URL, but page content clearly establishes clearance-equivalent meaning |
| `/sale` — "Summer Sale - 20% off everything, ends August 31" | EXCLUDE | Time-boxed storewide promotion, not clearance |
| `/black-friday` | EXCLUDE | Named campaign |
| `/offers` — mixed bag of temporary discounts and a genuine "shop discontinued styles" sub-link | Investigate the sub-link specifically; the parent `/offers` page itself stays EXCLUDE unless it's a real listing | Don't credit a marketing hub page for content that actually lives one level deeper |
| `/deals` — no clear signal either way, page has a product grid | FLAG: `MANUAL REVIEW: AMBIGUOUS SALE/CLEARANCE` | Genuinely uncertain — record, don't guess |
| `/coupon-codes` | EXCLUDE, not even a candidate | Not a product listing at all |

---

## 5. VALIDATION — BOTH MUST HOLD

1. Products are actually listed (a real PLP).
2. The site's own taxonomy treats it as Clearance/Outlet-style merchandising,
   per §3.

---

## 6. GENUINE SUB-STRUCTURE ONLY

If the site exposes real children (e.g. `Clearance > Furniture Clearance /
Lighting Clearance`), preserve as grouping row + leaves. If only one
undifferentiated listing exists, output just that one row. Never invent
sub-categories.

---

## 7. MULTIPLE PLPS FOR THE SAME CONCEPT

Genuinely different listings -> keep both. True alias of the same listing ->
keep the canonical URL, note the merge decision. Don't dedupe purely because
counts match.

---

## 8. EXCLUDE

Individual PDPs with a clearance badge, promotional banners, sale articles,
discount landing pages with no product grid, coupon pages, generic offers
pages with no clearance signal, Black Friday promotions, seasonal
promotions, marketing/editorial pages, and **any Outlet-branded page or
section (see §1/§3.2), no matter how clearance-like the stock is** — unless
the page is a genuine PLP the site's own taxonomy treats as Clearance per
§3.

---

## 9. NAVIGATION / MARKETING — NEVER A CLEARANCE PLP

Shop All, View All, Browse All, Collections (generic), Featured, New
Arrivals, Best Sellers, Gift Guides, Coupons/Promo Codes, Blogs, Editorial,
Lookbooks, Landing Pages, Black Friday, Search Results.

---

## 10. GROUPING VS. LEAF, ABSENCE PROOF, QTY, LANGUAGE, OUTPUT SHAPE

Identical to the shared core and to the Bestsellers equivalent
(`../../bestsellers-extraction/rules/bestsellers.md` §10) — grouping rows
name-only; qty is the site's own exact number with evidence; a zero-result
search is not proof of absence; output PLP/listing URL only.

---

## 11. CATEGORY / PRODUCT OVERLAP IS EXPECTED

Same product may sit in its normal product-taxonomy category (a separate
project) and here in Clearance. Not an error.

---

## 12. THIS IS PLP-LEVEL EXTRACTION, NOT PDP EXTRACTION

No product-level rows. Open a PDP only to resolve a genuine PLP-boundary
question.

---

## 13. NEVER DUPLICATE THE ENGINE

Same shared architecture as `../../bestsellers-extraction/rules/
bestsellers.md` §13 — this module adds only the Clearance classification
boundary.

---

## 14. FINAL DECISION TEST — run for every candidate

1. Is this a real PLP/listing page? No -> exclude.
2. Is this page itself branded Outlet (§1/§3.2)? Yes -> exclude, full stop
   — do not proceed to step 3 for this candidate.
3. Does the site's own taxonomy establish it as Clearance-equivalent (§3)?
   Yes -> include. No, but generic-sale-shaped -> flag for review, don't
   guess either way.
4. Is it a coupon/discount-code page with no listing? Yes -> exclude, not
   even a candidate.
5. Can exact qty be established? Yes -> record with evidence. No ->
   `qty: null` + manual-review flag.
6. Is this a true alias of an already-recorded listing? Yes -> keep the
   canonical one only, note why.
