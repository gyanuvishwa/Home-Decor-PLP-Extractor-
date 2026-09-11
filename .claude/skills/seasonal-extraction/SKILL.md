---
name: seasonal-extraction
description: Run the Seasonal/Holiday category extraction over the shared 286-company roster (the same roster and pipeline used for Furniture/Textile/Storage/Pet Care). One unified pass discovers every genuine seasonal category a company has — Christmas, Diwali, Halloween, and whatever else the site's own taxonomy presents. Use when the user says "Extract Seasonal", asks to continue/resume the Seasonal run, or asks to merge/verify the Seasonal workbook.
---

# Seasonal / Holiday Extraction

A new category on the **existing shared extraction pipeline** — not a
separate scraper, not PDP extraction, not a new workflow. This file routes
and wires the module into that pipeline. It does not restate the shared
engine; see `../home-decor-extraction/SKILL.md` for that.

**This is one unified extraction, not one run per holiday.** A single
worker visit per company discovers and extracts every genuine seasonal/
holiday category that site's own taxonomy presents — there is no
per-occasion routing, no per-occasion workbook, and no per-occasion rules
file. See `rules/seasonal.md` for the full ruleset (received from the user
2026-09-03, transcribed faithfully — do not paraphrase or re-derive it).

---

## 1. ROUTE FIRST

| User says | Load |
|---|---|
| Extract Seasonal / Extract Halloween / Extract Christmas / Extract Diwali / Extract \<any holiday\> | `../home-decor-extraction/rules/_decor-extraction-core.md` + `rules/seasonal.md` |

A request naming one specific holiday (e.g. "extract Christmas") still runs
the same unified Seasonal pass — it does not spin up a Christmas-only
module. The rules module discovers whichever holidays the company actually
has in one visit (`rules/seasonal.md` §10).

Also apply, unmodified, **every hard rule in
`../home-decor-extraction/SKILL.md` §2** (HTTP-first access tier, exact
qty+evidence, robots.txt Claude-disallow check, never touch another
category's workbook, never shift rows — rewrite wholesale, English-only
output) and **§6 EFFICIENCY** (structured data first, checkpoint before
anything expensive, the first-block-stops-you rule, no sleep/backoff
loops). Nothing about Seasonal relaxes any of those.

Do not open `rules/furniture.md`, `rules/textile.md`, `rules/storage.md`,
`../pet-care-extraction/rules/pet-care.md`, or any of the four decor-category
modules for a Seasonal run — cross-loading them is the specific waste this
structure exists to prevent.

---

## 2. ENGINE SHAPE

Per-category, site-visit extraction — the same shape as Furniture/Textile/
Storage/Pet Care, not a re-split of already-captured data. Workers visit
each company's site and extract Seasonal categories only, using the shared
engine (navigation discovery, PLP detection, qty+evidence, checkpointing,
JSON output). One visit covers every holiday the company has; workers do
not revisit the same site once per holiday.

**Roster: reuse `pipeline/furniture_json_archive/companies.json` as-is** —
same 286 companies, same SR 1..286 numbering, the confirmed master roster
underlying the `Output` sheet. Do not regenerate or renumber it.

---

## 3. PIPELINE ARTIFACTS — build from the Pet Care equivalents when the first batch is ready

Not yet built. Model directly on `pipeline/pet_care_json_archive/*`:

| File | Job |
|---|---|
| `pipeline/seasonal_json_archive/companies.json` | roster — verbatim copy of `furniture_json_archive/companies.json`, SR 1..286 |
| `pipeline/seasonal_json_archive/assign.py` | worker assignment block per SR range; `output_file: se<SR>.json` |
| `pipeline/seasonal_json_archive/status.py` | dispatched / done / in-flight / next-up |
| `pipeline/seasonal_json_archive/dispatched.txt` | dispatch ledger |
| `pipeline/seasonal_json_archive/se<SR>.json` | one per completed company, one record per genuine holiday found (rules §19) |
| `pipeline/seasonal_json_archive/merge_seasonal.py` | worker JSON → `Seasonal.xlsx`. Dedup key `(category, sub_category, link)`, per the known Furniture trap. `category` = holiday name, `sub_category` = product type (rules §19) |
| `pipeline/seasonal_json_archive/verify_seasonal.py` | protected-workbook SHA-256 check (every other category workbook: Furniture, Textile, Storage, Pet Care, the four decor workbooks, `Final_Company_List (1).xlsx`) + sheet integrity + 286-row ledger reconciliation + strict whole-file duplicate-URL check (hard `assert`, same as Pet Care — see `../pet-care-extraction/SKILL.md` §7 item 4) |
| `pipeline/seasonal_json_archive/protected_baseline.sha256` | protected-file hashes, taken before the first Seasonal batch runs |
| `pipeline/seasonal_json_archive/qa_notes.md` | open adjudication log |

**Add `Seasonal.xlsx` to every other category's protected-baseline file**
once created, so no other run can write to it either.

---

## 4. OPEN ADJUDICATION — LOG TO `qa_notes.md`, DON'T INVENT

The rules module resolves most boundary questions explicitly (unlike Pet
Care's two deferred policy questions, Seasonal's ruleset was given complete
and specific). Still flag rather than decide:

- A candidate that looks seasonal but isn't clearly one of §3's named
  holidays or vocabulary and isn't obviously a marketing page either
  (`rules/seasonal.md` §4/§6) — genuine ambiguity, not a clean exclude.
- A "Festive"/generic seasonal label whose actual holiday association can't
  be pinned down from site context (rules §3, the Diwali/Festive
  ambiguity called out explicitly by the user).
- Anything that doesn't fit `rules/seasonal.md` as written — a new kind of
  boundary case, not just a new example of an existing one.

---

## 5. OUTPUT

One workbook: `Seasonal.xlsx`, project root. Same sheet layout as every
other category workbook — re-derive it before any structural edit, per
`../home-decor-extraction/SKILL.md` §8: `Maisons | Company name | Brand Site
| Country | site URL | Category | Sub-Category | Type | qty | link`.
`Category` = the holiday/festival name (Christmas, Diwali, Halloween, …);
`Sub-Category` = the specific product type under it, faithful to the site's
own taxonomy (rules §19). Grouping rows: `fill FFFFF2CC + bold + blank qty +
blank link`, name only. Header fill `FFD9E1F2`. Copy resolved `font`/
`fill`/`border`/`alignment`/`number_format`/`protection`, never
`cell._style` (raises `IndexError` on save).

---

## 6. TRAPS SPECIFIC TO THIS CATEGORY

- **Seasonal products in a normal category ≠ a Seasonal category.** A
  Christmas ornament sitting inside `Decorative Accessories` doesn't make
  that category Seasonal (rules §5–§6).
- **No exclusivity against other categories — this is the one category
  that deliberately overlaps.** Unlike Furniture/Textile/Storage/Pet Care's
  "don't steal a record another category owns" discipline, a genuine
  seasonal PLP (e.g. `Christmas Lighting`) belongs in `Seasonal.xlsx` even
  though the same products would also sit in `Lighting.xlsx`. Do not drop a
  seasonal row to avoid overlap, and do not edit any other category's
  workbook to "correct" it (rules §7).
- **One pass finds every holiday a company has — don't assume a single
  "Seasonal" root node.** Some sites nest everything under one `Holiday
  Shop`/`Festivals` branch, some scatter top-level nav items with no shared
  parent (rules §10).
- **"Collection" in the name is not an automatic exclude** — inspect
  whether the page is a real PLP or a landing page either way (rules §4).
- **A zero-result internal search is not proof a holiday is absent** —
  same trap as every other category (`../home-decor-extraction/SKILL.md`
  §7); check navigation/mega-menu/sitemap before recording `NO_SEASONAL`
  (rules §12).

---

## 7. VERIFY BEFORE REPORTING A MERGE DONE — MANDATORY

Same discipline as every prior category (see
`../pet-care-extraction/SKILL.md` §7 for the concrete history of why this
matters — two real classification bugs shipped clean through automated
verification there).

1. Read every Review-sheet row against `rules/seasonal.md` — does it match
   a worked example, or is it a false-positive flag on a real include?
2. Any regex/keyword logic written or edited in `merge_seasonal.py` or
   `verify_seasonal.py` this session gets extra scrutiny before being
   trusted at scale — test it against the rules module's own examples.
3. Only report "merged and verified" after both the structural check
   (`verify_seasonal.py`) and this content spot-check pass.
4. `verify_seasonal.py` must always pass its strict whole-file
   duplicate-URL check — hard failure, not a warning, every merge.
