---
name: pet-care-extraction
description: Run a Pet Care category extraction over the shared 286-company roster (the same roster and pipeline used for Furniture/Textile/Storage). Use when the user says "Extract Pet Care", asks to continue/resume a Pet Care run, or asks to merge/verify the Pet Care workbook. Loads the shared decor-extraction core plus the Pet Care boundary-rules module.
---

# Pet Care Extraction

A new category module on the **existing shared extraction pipeline** — not a
separate scraper, not PDP extraction. This file routes and wires the module into
that pipeline. It does not restate the shared engine; see
`../home-decor-extraction/SKILL.md` for that.

> **PROJECT COMPLETE — all 286 roster entries processed, merged and
> verified** (2026-09-02, 15 batches). 285 unique companies (SR 286 is a
> confirmed duplicate of SR 165 "Noon UAE" — **dropped entirely** from the
> workbook per explicit user instruction, not just cleared; see the
> `KNOWN_ROSTER_DUPLICATES` constant in `merge_pet_care.py` and
> `verify_pet_care.py`). Final numbers (post-completion fixes included):
> **111 companies have real Pet Care, 162 confirmed absent, 12 blocked**,
> 494 review rows (all content-spot-checked, zero known false positives
> remaining), zero cross-company duplicate URLs, **Processing Ledger
> reconciles to exactly 285** (not 286 — that's correct and intentional
> after the duplicate-removal fix, don't treat a 285-row ledger as a bug).
> **Two post-completion corrections were made after the user spot-checked
> the live file**: SR 111 fonQ's 3 no-crawlable-URL facet rows got a
> user-confirmed working filter URL (kept over this project's own raw-fetch
> check, which the user verified in a real browser); SR 124 Denby moved
> from "PET CARE FOUND" to "BLOCKED" after the user reported its URL
> "showing closed" — the company entered UK administration
> (insolvency) and the entire site now serves a static closure notice, a
> genuine same-day business-state change, not a bot block or stale cache.
> If more spot-check corrections come in, keep following this pattern:
> verify independently (HTTP fetch + real browser when they disagree),
> edit the source `pc<SR>.json`, re-merge, re-verify. `verify_pet_care.py`
> runs a **strict whole-file duplicate-URL check** (§7 item 4) — mandatory
> on every merge, kept passing on every merge since it was added. The
> `CONSUMABLE_FLAG` / `FEEDING_EQUIPMENT_OVERRIDE` pair needed **3 real
> bugfixes** over the project ("Food Bowls" batch 1-2, "Chew Toys" batch 7,
> "Pet Food Scoops" batch 10) — if this pipeline is ever re-run or
> extended, treat that regex pair as permanently high-risk and re-test
> against known-good/known-bad examples on any edit. One consistency gap
> was also caught and fixed (Wayfair UK's missed livestock flag, batch
> 14). See `pipeline/pet_care_json_archive/qa_notes.md`'s final "PROJECT
> COMPLETE" section for the complete final tally and the open-questions
> list (§4 below) that still needs a human decision. **No further batches
> to dispatch.**

---

## 1. LOAD ORDER

Before running any extraction, read both, in this order:

1. `../home-decor-extraction/rules/_decor-extraction-core.md` — the shared
   boundary-classification core (navigation discovery, PLP detection, grouping vs.
   leaf rows, overlap handling).
2. `rules/pet-care.md` (this skill) — the Pet Care category boundary and
   classification rules. It defines scope only; it assumes the core and the
   engine below.

Also apply, unmodified, **every hard rule in
`../home-decor-extraction/SKILL.md` §2** (HTTP-first access tier, exact
qty+evidence, robots.txt Claude-disallow check, never touch another category's
workbook, never shift rows — rewrite wholesale, English-only output) and **§6
EFFICIENCY** (structured data first, checkpoint before anything expensive, the
first-block-stops-you rule, no sleep/backoff loops). Nothing about Pet Care
relaxes any of those.

Do not open `rules/furniture.md`, `rules/textile.md`, `rules/storage.md`, or any
of the four decor-category modules for a Pet Care run — the classification
boundaries differ and cross-loading them is the specific waste this structure
exists to prevent.

---

## 2. ENGINE SHAPE

This is a **per-category, site-visit extraction** — the same shape as
Furniture/Textile/Storage, not a re-split of already-captured data. Workers visit
each company's site and extract Pet Care categories only, using the shared engine
(navigation discovery, PLP detection, qty+evidence, checkpointing, JSON output).

**Roster: reuse `pipeline/furniture_json_archive/companies.json` as-is** — same
286 companies, same SR 1..286 numbering, confirmed by the user as the same master
roster underlying the `Output` sheet. Do not regenerate or renumber it for Pet
Care.

---

## 3. PIPELINE ARTIFACTS (built 2026-09-02, modeled on the Furniture equivalents)

| File | Job |
|---|---|
| `pipeline/pet_care_json_archive/companies.json` | roster — verbatim copy of `furniture_json_archive/companies.json`, SR 1..286. Do not edit; do not renumber. |
| `pipeline/pet_care_json_archive/assign.py` | prints a worker's assignment block for an SR range; `output_file: pc<SR>.json` |
| `pipeline/pet_care_json_archive/status.py` | dispatched / done / in-flight / next-up, scanning `pc*.json` |
| `pipeline/pet_care_json_archive/dispatched.txt` | dispatch ledger — starts empty |
| `pipeline/pet_care_json_archive/pc<SR>.json` | one per completed company — the output contract, same shape as `f<SR>.json` |
| `pipeline/pet_care_json_archive/merge_pet_care.py` | worker JSON → `Pet_Care.xlsx` (`Output`/`Processing Ledger`/`Review` sheets). Dedup key is `(category, sub_category, link)`, per the known Furniture trap. Trusts the worker's Pet Care classification — unlike `merge_furniture.py`'s exclusion-based `NOT_FURNITURE` net, there is no executable classifier to check against, so this only nets nav/marketing nodes (§13 of the rules module) plus two **forced** review flags: any sub-category matching food/treats/chews/supplements/vitamins/nutrition gets `MANUAL REVIEW: PET CONSUMABLE`, and any matching medicine/veterinary/prescription/clinical/dewormer/flea-tick gets `MANUAL REVIEW: PET MEDICAL / VETERINARY CATEGORY` — both per §4 below, regardless of whether the worker already flagged them. Two negative-match overrides suppress the consumable flag: `FEEDING_EQUIPMENT_OVERRIDE` (bowls/storage/canisters/mats/jars/containers/dishes/feeders/**scoops**, scoops added batch 10) — "Food Bowls"/"Pet Food Storage"/"Treat Jars"/"Pet Food Scoops" are Tier 1 equipment includes, not the consumable itself — and `TOY_QUALIFIER_PHRASE` (added batch 7), which strips a `<chew|treat|puzzle|interactive|fetch> toy(s)` phrase before testing — "Chew Toys"/"Interactive/Puzzle/Treat Toys" are Tier 1 toys (rules §14), not the consumable, while "Toys & Treats"/"Pet Toys & Treats" (treats as a *separate* listed item) correctly still flag. **Both overrides exist because of real bugs, now 3 of them** (see §7) — if you touch `CONSUMABLE_FLAG`, `MEDICAL_FLAG`, or either override again, re-verify against §7 before trusting it at scale. |
| `pipeline/pet_care_json_archive/verify_pet_care.py` | protected-workbook SHA-256 check (`Kitchen_and_Dining.xlsx`, `Lighting.xlsx`, `Wall_Decor.xlsx`, `Decorative_Home_Accessories.xlsx`, `Furniture.xlsx`, `Textile.xlsx`, `Storage.xlsx`, `Final_Company_List (1).xlsx`) + sheet integrity + 286-row ledger reconciliation + a cross-check that every consumable/medical-looking sub-category actually landed on the Review sheet + a **strict whole-file duplicate-URL check** (added 2026-09-02 at the user's request): any link used by more than one *different* company is a hard failure (`assert`), not just a warning — a URL belongs to exactly one company's domain, so a cross-company repeat means a copy-paste/wrong-company-assigned bug. Distinct from the pre-existing "same link twice in one company" check (a same-company repeat can legitimately happen via nav overlap; a cross-company repeat never can). Run clean against all 120 companies through batch 6 — zero violations. |
| `pipeline/pet_care_json_archive/protected_baseline.sha256` | the 8 protected files' hashes as of 2026-09-02, before any Pet Care batch ran |
| `pipeline/pet_care_json_archive/qa_notes.md` | open adjudication log — the live per-batch source of truth |

**Add `Pet_Care.xlsx` to the OTHER categories' protected-baseline files once
convenient**, so a Furniture/Textile/Storage/decor run can't write to it
either (currently one-directional: Pet Care protects the other seven, they
don't yet know to protect it back).

---

## 4. OPEN ADJUDICATION ITEMS — LOG THESE TO `qa_notes.md` FIRST

The boundary rules in `rules/pet-care.md` explicitly defer two policy questions
rather than inventing an answer. Do not resolve them yourself:

- **Pet Food / Consumables (§11 of the rules module).** No definitive
  include/exclude policy exists yet for pet-care consumables. Flag each
  candidate `MANUAL REVIEW: PET CONSUMABLE — <what>` rather than deciding.
- **Medical / Veterinary categories (§12).** No inclusion rule exists. Flag
  `MANUAL REVIEW: PET MEDICAL / VETERINARY CATEGORY` rather than absorbing or
  dropping them.

Get an explicit decision on both before merging a batch that contains them, the
same way Furniture's `qa_notes.md` carries open judgement calls across sessions.

A third open question surfaced in batch 13: **API-reachable-but-unnavigable
categories.** Zara Home India (SR 242) has real, live pet products with zero
discoverable path through the storefront's own navigation, sitemap, or
breadcrumbs — the worker only found them by reusing another market's
categoryId against the API. Flagged as `MANUAL REVIEW`, not resolved. If
this recurs, log it the same way as the two above rather than deciding
per-worker whether "API-reachable" counts as "present."

---

## 5. OUTPUT

One workbook: `Pet_Care.xlsx`, project root. Same sheet layout as the other
category workbooks — re-derive it before any structural edit, per the shared
contract in `../home-decor-extraction/SKILL.md` §8:
`Maisons | Company name | Brand Site | Country | site URL | Category |
Sub-Category | Type | qty | link`. Grouping rows: `fill FFFFF2CC + bold + blank
qty + blank link`, name only. Header fill `FFD9E1F2`. Copy resolved
`font`/`fill`/`border`/`alignment`/`number_format`/`protection`, never
`cell._style` (raises `IndexError` on save).

---

## 6. TRAPS SPECIFIC TO THIS CATEGORY

- **Pet-themed ≠ Pet Care.** A dog-print cushion or cat-illustration mug is
  themed around animals, not made for them — exclude (rules §6–§7).
- **Generic product types (beds, storage, toys, clothing, furniture) are not
  Pet Care by default.** Only the pet-specific branch counts — `Pets > Beds` is
  in scope, `Home > Blankets` and `Furniture > Beds` are not (rules §5, §8, §9).
- **Do not steal from Furniture/Storage/Bathroom/Kitchen & Dining/Lighting/Wall
  Decor/Textiles.** If another category is the clearly stronger owner, leave the
  record there (rules §24).
- **Tier 2 (`PET_BROAD`) needs real hierarchy evidence**, not just a loose noun
  like Accessories/Essentials/Home/Outdoor/Care/Lifestyle sitting under a Pets
  node — confirm the parent branch is actually pet-specific (rules §4).
  Also see the general trap in `../home-decor-extraction/SKILL.md` §7 about site
  search returning 0 not being proof of absence — it applies here too (rules
  §18).

---

## 7. VERIFY BEFORE REPORTING A MERGE DONE — MANDATORY

**A clean `merge_pet_care.py` + `verify_pet_care.py` exit does not mean the
merge is correct.** `verify_pet_care.py` checks structure (dedup, ledger count,
protected files, non-ASCII, URL shape) — it does not check that the
classification/flagging logic itself is *right*. That gap already bit this
project twice: `CONSUMABLE_FLAG` matched the bare word "food"/"treat" anywhere,
so it force-flagged Tier 1 feeding-equipment categories ("Food Bowls", "Dog
Food Storage", "Pet Food Canisters") as if they were the open consumable-policy
question (batch 1-2), and then again in batch 7 with "Chew Toys" (a Tier 1
toy, not a consumable). Both bugs shipped in the same session they were
written, and `verify` reported a clean OK the whole time — the first wasn't
caught until the user read the Review sheet themselves; the second was
caught only because the spot-check discipline below was already in place.

**Before reporting any merge as done, every time:**

1. Read every row on the Review sheet — not just the summary counts — and ask
   "does this actually match a worked example in `rules/pet-care.md`?" for
   each one. A flag that fires on a Tier 1 include (§3 of the rules module) is
   a bug, not a correct catch.
2. If you wrote or edited any regex/keyword logic in `merge_pet_care.py` or
   `verify_pet_care.py` in this session, treat that as reason for *extra*
   scrutiny, not less — test it against the rules module's own listed examples
   before trusting it at scale, the same discipline `merge_furniture.py`'s
   `NOT_FURNITURE`/`FURNITURE_OVERRIDE` pair already required.
3. Only report a batch "merged and verified" after both the structural check
   (`verify_pet_care.py`) and this content spot-check pass.
4. **`verify_pet_care.py` must always pass its strict whole-file duplicate-URL
   check** (the same link assigned to two different companies) — this is a
   hard `assert`, not optional. Added 2026-09-02 at the user's explicit
   request ("check for duplicate urls in whole file strictly in every
   merge"). Do not weaken it to a warning, do not skip it, and do not merge
   without running the current `verify_pet_care.py` (an old cached copy
   without this check does not count).
