---
name: clearance-extraction
description: Run a Clearance merchandising-PLP extraction over the shared 286-company roster (the same roster and pipeline used for Furniture/Textile/Storage/Pet Care/Seasonal/Bathroom/Bestsellers). Use when the user says "Extract Clearance", asks to continue/resume a Clearance run, or asks to merge/verify the Clearance workbook. Loads the shared decor-extraction core plus the Clearance boundary-rules module.
---

# Clearance Extraction

A new **merchandising-PLP** module on the **existing shared extraction
pipeline** — not a separate scraper, not PDP extraction. This file routes and
wires the module into that pipeline. It does not restate the shared engine;
see `../home-decor-extraction/SKILL.md` for that.

**This is NOT a product-taxonomy category.** Clearance is one of three
sibling *merchandising-state* skills — see
`../bestsellers-extraction/SKILL.md`'s architecture diagram, identical here.
Do not look for tables, lighting, mirrors, furniture, etc. — look for the
listing pages the site itself uses for permanently-marked-down / outlet /
end-of-line merchandising. See §3 and `rules/clearance.md` for the full
boundary, and **read §3.1 (Clearance vs. Sale) especially carefully** — it is
the one genuinely hard judgement call in this skill.

---

## 1. LOAD ORDER

Before running any extraction, read both, in this order:

1. `../home-decor-extraction/rules/_decor-extraction-core.md` — shared
   engine mechanics only (navigation discovery, checkpointing, evidence,
   grouping vs. leaf). Its own product-type inclusion/exclusion list, and its
   ban on "Sale/Clearance" as navigation noise, do not apply here — §3 below
   and `rules/clearance.md` fully replace it for this skill.
2. `rules/clearance.md` (this skill) — the Clearance PLP boundary, and in
   particular the Clearance-vs-Sale test.

Also apply, unmodified, **every hard rule in
`../home-decor-extraction/SKILL.md` §2** and **§6 EFFICIENCY**. Nothing about
Clearance relaxes any of those.

Do not open `rules/furniture.md`, `rules/pet-care.md`, `rules/bestsellers.md`,
`rules/new-arrivals.md`, or any product-taxonomy category module for a
Clearance run.

---

## 2. ENGINE SHAPE

Per-company, site-visit extraction, same shape as Furniture/Pet Care/
Seasonal/Bestsellers. The taxonomy discovered is nearly always flat — do not
manufacture sub-categories that don't exist (rules §6).

**Roster: reuse `pipeline/furniture_json_archive/companies.json` as-is** —
same 286 companies, same SR 1..286, same known SR 286/165 duplicate.

---

## 3. WHAT THIS SKILL IS LOOKING FOR (quick reference — full detail in `rules/clearance.md`)

Genuine PLPs for: Clearance, Clearances, Clearance Sale, Clearance Products,
Clearance Outlet, Outlet, Final Sale, Final Clearance, Last Chance, Last
Chance Products, End of Line, Discontinued (clearance-style) — and
local-language equivalents.

### 3.1 CLEARANCE VS. SALE — READ THIS BEFORE DISPATCHING ANY WORKER

**The single hardest call in this skill.** A page called Sale / Offers /
Deals / Promotions / Discounts / Special Offers is **not** automatically
Clearance. It only counts if the site's OWN taxonomy clearly treats it as
Clearance/Outlet/Final Clearance/Last Chance/End of Line. A generic temporary
promotional sale (seasonal sale, Black Friday, a percent-off campaign) is
excluded by default. **If uncertain, flag for manual review — never guess.**
`merge_clearance.py` enforces a mechanical backstop for this (see §4), but
the worker's own page-content judgement, recorded in `notes`, is what
actually resolves it — see `rules/clearance.md` §3-4 for worked examples.

---

## 4. PIPELINE ARTIFACTS

| File | Job |
|---|---|
| `pipeline/clearance_json_archive/companies.json` | roster — verbatim copy of `furniture_json_archive/companies.json`, SR 1..286 |
| `pipeline/clearance_json_archive/CLEARANCE_BRIEF.md` | worker brief — operational form of `rules/clearance.md`, with the full Clearance-vs-Sale test spelled out. Deploy a copy to the scratchpad before dispatching. |
| `pipeline/clearance_json_archive/assign.py` | prints a worker's assignment block; `output_file: cl<SR>.json` |
| `pipeline/clearance_json_archive/status.py` | dispatched / done / in-flight / next-up, scanning `cl*.json` |
| `pipeline/clearance_json_archive/dispatched.txt` | dispatch ledger — starts empty |
| `pipeline/clearance_json_archive/cl<SR>.json` | one per completed company |
| `pipeline/clearance_json_archive/merge_clearance.py` | worker JSON -> `Clearance.xlsx`. Dedup key `(category, sub_category, link)`. Drops navigation/marketing nodes (BANNED — deliberately does NOT ban "clearance/outlet/final sale/last chance/end of line", those are the target, and deliberately does NOT ban generic "sale/offers/deals/promotions/discounts" either, since the mechanical backstop below handles those instead of an outright drop). **Force-flags any sub-category matching generic-sale wording that lacks a strict clearance-family word** as `MANUAL REVIEW: GENERIC SALE/OFFERS PAGE, NOT CONFIRMED AS CLEARANCE BY SITE TAXONOMY` — this is a name-pattern backstop, not a substitute for the worker's own page-content judgement (`pipeline/clearance_json_archive/qa_notes.md` has the full caveat). Also force-flags PDP-shaped links, same as the sibling skills. |
| `pipeline/clearance_json_archive/verify_clearance.py` | protected-workbook SHA-256 check (all 10 prior category workbooks + `Final_Company_List (1).xlsx` + siblings Bestsellers.xlsx/New_Arrivals.xlsx) + sheet integrity + 285-row ledger reconciliation + strict whole-file duplicate-URL check + a cross-check that every generic-sale-worded, non-strict sub-category actually landed on Review. |
| `pipeline/clearance_json_archive/protected_baseline.sha256` | protected files' hashes as of 2026-09-07, before any Clearance batch ran |
| `pipeline/clearance_json_archive/qa_notes.md` | open adjudication log, including the standing Clearance-vs-Sale policy note — read it before merging any batch that hits ambiguous rows |

---

## 5. OPEN ADJUDICATION — LOG TO `qa_notes.md`, DON'T RESOLVE UNILATERALLY

**Clearance vs. generic Sale has no blanket rule** — it is judged per site,
per the worker's page-content evidence, not by keyword alone. When a batch
produces `MANUAL REVIEW: GENERIC SALE/OFFERS PAGE...` rows, do not silently
decide either way at merge time; log each one with its specific evidence to
`qa_notes.md` for adjudication, the same discipline every other category's
open policy questions follow (see Pet Care's consumable/medical gaps for the
precedent).

---

## 6. OUTPUT

One workbook: `Clearance.xlsx`, project root. Same sheet layout/contract as
`../home-decor-extraction/SKILL.md` §8. Most companies will produce a small
number of leaf rows (often exactly one) — that is the expected shape.

---

## 7. TRAPS SPECIFIC TO THIS SKILL

- **The Sale-vs-Clearance line is the whole game here** — see §3.1. Get this
  wrong at scale and the deliverable is useless; when in doubt, flag.
- **Coupon pages and discount-code landing pages with no product grid are not
  PLPs at all** — exclude outright, don't even flag them as ambiguous
  Clearance candidates.
- **Black Friday / seasonal promotion pages are excluded by default** even
  if heavily discounted — they're temporary campaigns, not the site's
  standing clearance/outlet merchandising.
- **Site search returning 0 is not proof of absence** — same trap as every
  other category. Enumerate nav + sitemap first.
- **Multiple URLs, one underlying listing** — don't dedupe on matching counts
  alone; confirm they're the same listing first.
- **Category/product overlap with the product-taxonomy workbooks is
  expected**, not a defect.

---

## 8. INDEPENDENT CHECKPOINTS

Same as `../bestsellers-extraction/SKILL.md` §7 — Bestsellers/Clearance/New
Arrivals each track completion independently. A block in one says nothing
about the others; never reset this skill's ledger because a sibling hit a
problem.

---

## 9. VERIFY BEFORE REPORTING A MERGE DONE — MANDATORY

**A clean `merge_clearance.py` + `verify_clearance.py` exit does not mean the
merge is correct.** Before reporting any merge as done:

1. Read every row on the Review sheet — especially every
   `GENERIC SALE/OFFERS PAGE` flag — and check it against
   `rules/clearance.md` §4's worked examples and the worker's own `notes`
   evidence, not just the regex match.
2. If you edited `CLEARANCE_STRICT`/`GENERIC_SALE` or any other regex in
   `merge_clearance.py`/`verify_clearance.py` this session, treat that as
   reason for extra scrutiny before trusting it at scale.
3. Only report a batch "merged and verified" after both the structural check
   and this content spot-check pass.
4. **`verify_clearance.py` must always pass its strict whole-file
   duplicate-URL check** — a hard `assert`, not optional.
