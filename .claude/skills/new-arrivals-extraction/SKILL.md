---
name: new-arrivals-extraction
description: Run a New Arrivals merchandising-PLP extraction over the shared 286-company roster (the same roster and pipeline used for Furniture/Textile/Storage/Pet Care/Seasonal/Bathroom/Bestsellers/Clearance). Use when the user says "Extract New Arrivals", asks to continue/resume a New Arrivals run, or asks to merge/verify the New Arrivals workbook. Loads the shared decor-extraction core plus the New Arrivals boundary-rules module.
---

# New Arrivals Extraction

A new **merchandising-PLP** module on the **existing shared extraction
pipeline** — not a separate scraper, not PDP extraction. This file routes and
wires the module into that pipeline. It does not restate the shared engine;
see `../home-decor-extraction/SKILL.md` for that.

**This is NOT a product-taxonomy category.** New Arrivals is one of three
sibling *merchandising-state* skills — see
`../bestsellers-extraction/SKILL.md`'s architecture diagram, identical here.
Do not look for tables, lighting, mirrors, furniture, etc. — look for the
listing pages the site itself uses for newly added products. See §3 and
`rules/new-arrivals.md` for the full boundary, and **read §3.1 ("Collection"
pages) especially carefully** — it is the one genuinely hard judgement call
in this skill.

---

## 1. LOAD ORDER

Before running any extraction, read both, in this order:

1. `../home-decor-extraction/rules/_decor-extraction-core.md` — shared
   engine mechanics only. Its own product-type list and its ban on "New
   Arrivals" as navigation noise do not apply here — §3 below and
   `rules/new-arrivals.md` fully replace it for this skill.
2. `rules/new-arrivals.md` (this skill) — the New Arrivals PLP boundary, and
   in particular the Collection-page test.

Also apply, unmodified, **every hard rule in
`../home-decor-extraction/SKILL.md` §2** and **§6 EFFICIENCY**. Nothing about
New Arrivals relaxes any of those.

Do not open `rules/furniture.md`, `rules/pet-care.md`, `rules/bestsellers.md`,
`rules/clearance.md`, or any product-taxonomy category module for a New
Arrivals run.

---

## 2. ENGINE SHAPE

Per-company, site-visit extraction, same shape as Furniture/Pet Care/
Seasonal/Bestsellers/Clearance. The taxonomy discovered is nearly always
flat — do not manufacture sub-categories that don't exist (rules §6).

**Roster: reuse `pipeline/furniture_json_archive/companies.json` as-is** —
same 286 companies, same SR 1..286, same known SR 286/165 duplicate.

---

## 3. WHAT THIS SKILL IS LOOKING FOR (quick reference — full detail in `rules/new-arrivals.md`)

Genuine PLPs for: New Arrivals, New In, New Products, Just In, Just Arrived,
Latest Arrivals, Latest Products, What's New, New This Season, "New
Collection" **only when genuinely a product listing**, Recently Added,
Newly Added — and local-language equivalents.

### 3.1 "COLLECTION" PAGES NEED INSPECTION, EVERY TIME

Do not classify a page as New Arrivals purely because it's called "New
Collection" / "New Season" / "New Range." Determine whether it's a genuine
product listing (browsable products, a count, filter/sort like any other
category page) or a marketing/editorial landing page (hero story, lookbook
imagery, campaign write-up, no real product grid). If genuinely uncertain,
flag for manual review rather than guessing. `merge_new_arrivals.py` enforces
a mechanical backstop for this (see §4), but the worker's own page-content
judgement is what actually resolves it — see `rules/new-arrivals.md` §3-4
for worked examples.

---

## 4. PIPELINE ARTIFACTS

| File | Job |
|---|---|
| `pipeline/new_arrivals_json_archive/companies.json` | roster — verbatim copy of `furniture_json_archive/companies.json`, SR 1..286 |
| `pipeline/new_arrivals_json_archive/NEW_ARRIVALS_BRIEF.md` | worker brief — operational form of `rules/new-arrivals.md`, with the full Collection-page test spelled out. Deploy a copy to the scratchpad before dispatching. |
| `pipeline/new_arrivals_json_archive/assign.py` | prints a worker's assignment block; `output_file: na<SR>.json` |
| `pipeline/new_arrivals_json_archive/status.py` | dispatched / done / in-flight / next-up, scanning `na*.json` |
| `pipeline/new_arrivals_json_archive/dispatched.txt` | dispatch ledger — starts empty |
| `pipeline/new_arrivals_json_archive/na<SR>.json` | one per completed company |
| `pipeline/new_arrivals_json_archive/merge_new_arrivals.py` | worker JSON -> `New_Arrivals.xlsx`. Dedup key `(category, sub_category, link)`. Drops navigation/marketing nodes (BANNED — deliberately does NOT ban "new arrivals/new in/just in/latest/what's new/recently added", those are the target). **Force-flags any bare "New Collection"/"New Season"/"New Range" name lacking an unambiguous New Arrivals signal word** as `MANUAL REVIEW: 'COLLECTION'-STYLE NAME WITHOUT A CLEAR NEW-ARRIVALS SIGNAL` — a name-pattern backstop, not a substitute for the worker's own page-content judgement (`pipeline/new_arrivals_json_archive/qa_notes.md` has the full caveat). Also force-flags PDP-shaped links, same as the sibling skills. |
| `pipeline/new_arrivals_json_archive/verify_new_arrivals.py` | protected-workbook SHA-256 check (all 10 prior category workbooks + `Final_Company_List (1).xlsx` + siblings Bestsellers.xlsx/Clearance.xlsx) + sheet integrity + 285-row ledger reconciliation + strict whole-file duplicate-URL check + a cross-check that every ambiguous Collection-style sub-category actually landed on Review. |
| `pipeline/new_arrivals_json_archive/protected_baseline.sha256` | protected files' hashes as of 2026-09-07, before any New Arrivals batch ran |
| `pipeline/new_arrivals_json_archive/qa_notes.md` | open adjudication log, including the standing Collection-page policy note |

---

## 5. OPEN ADJUDICATION — LOG TO `qa_notes.md`, DON'T RESOLVE UNILATERALLY

**"New Collection" ambiguity has no blanket rule** — judged per site, per the
worker's page-content evidence, not by keyword alone. Log flagged rows with
their specific evidence to `qa_notes.md` for adjudication rather than
deciding either way at merge time.

---

## 6. OUTPUT

One workbook: `New_Arrivals.xlsx`, project root. Same sheet layout/contract
as `../home-decor-extraction/SKILL.md` §8. Most companies will produce a
small number of leaf rows (often exactly one) — that is the expected shape.

---

## 7. TRAPS SPECIFIC TO THIS SKILL

- **The Collection-page ambiguity is the whole game here** — see §3.1.
- **A PDP's own "New" badge is never a New Arrivals PLP** — same PDP trap as
  Bestsellers' "Bestseller" badge.
- **Seasonal campaign pages and lookbooks are excluded by default** even if
  they showcase genuinely new products — they're editorial, not a listing.
- **Site search returning 0 is not proof of absence** — enumerate nav +
  sitemap first.
- **Multiple URLs, one underlying listing** — don't dedupe on matching counts
  alone; confirm they're the same listing first.
- **Category/product overlap with the product-taxonomy workbooks and with
  the Seasonal workbook is expected**, not a defect — a genuinely new
  Christmas product can appear in both Seasonal and here.

---

## 8. INDEPENDENT CHECKPOINTS

Same as `../bestsellers-extraction/SKILL.md` §7 — Bestsellers/Clearance/New
Arrivals each track completion independently. A block in one says nothing
about the others; never reset this skill's ledger because a sibling hit a
problem.

---

## 9. VERIFY BEFORE REPORTING A MERGE DONE — MANDATORY

**A clean `merge_new_arrivals.py` + `verify_new_arrivals.py` exit does not
mean the merge is correct.** Before reporting any merge as done:

1. Read every row on the Review sheet — especially every `'COLLECTION'-STYLE
   NAME` flag — and check it against `rules/new-arrivals.md` §4's worked
   examples and the worker's own `notes` evidence, not just the regex match.
2. If you edited `NEW_ARRIVALS_STRICT`/`AMBIGUOUS_COLLECTION` or any other
   regex in `merge_new_arrivals.py`/`verify_new_arrivals.py` this session,
   treat that as reason for extra scrutiny before trusting it at scale.
3. Only report a batch "merged and verified" after both the structural check
   and this content spot-check pass.
4. **`verify_new_arrivals.py` must always pass its strict whole-file
   duplicate-URL check** — a hard `assert`, not optional.
