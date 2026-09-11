---
name: bathroom-extraction
description: Run the Bathroom category extraction over the shared 286-company roster (the same roster and pipeline used for Furniture/Textile/Storage/Pet Care/Seasonal). Use when the user says "Extract Bathroom", asks to continue/resume the Bathroom run, or asks to merge/verify the Bathroom workbook.
---

# Bathroom Extraction

A new category module on the **existing shared extraction pipeline** — not a
separate scraper, not PDP extraction. This file routes and wires the module
into that pipeline. It does not restate the shared engine; see
`../home-decor-extraction/SKILL.md` for that.

> **CONTINUING A CROSS-MACHINE HANDOFF.** SR 1-196 (of 286) were extracted on
> a different machine and delivered 2026-09-05 as a merged `Bathroom.xlsx` +
> `CHECKPOINT.json`/`SUMMARY.md`/`BATCH_BRIEF.md` — no per-company worker
> JSON, and that machine's own pipeline (`bathroom_run/`, `report.py`,
> `next_batches.py`) does not exist here. This session rebuilt the missing
> `b<SR>.json` archive layer from the workbook
> (`pipeline/bathroom_json_archive/rebuild_archive_from_xlsx.py`) and found +
> fixed two real defects in the handoff — see
> `pipeline/bathroom_json_archive/qa_notes.md` **"FIXED this session"** for
> exactly what changed (a cross-category dedup gap against
> Storage/Wall_Decor/Textile, and 27 companies with non-English
> category/sub_category text). Read that file's **"OPEN"** section before
> touching the back-catalogue (SR 1-196) again — several items there are
> explicitly deferred to the run owner, not yours to decide.
>
> **139 companies have real Bathroom, 41 confirmed absent, 16 blocked, 90
> still pending (SR 197-286).** Continue from SR 197 using the engine below.

---

## 1. LOAD ORDER

Before running any extraction, read:

1. `rules/bathroom.md` (this skill) — the full Bathroom classification
   ruleset (authoritative, user-supplied 2026-09-05) plus the
   cross-category dedup addendum at its end.

This category does not use `_decor-extraction-core.md` — `rules/bathroom.md`
is self-contained, the same shape as `pet-care.md`.

Also apply, unmodified, **every hard rule in
`../home-decor-extraction/SKILL.md` §2** (HTTP-first access tier, exact
qty+evidence, robots.txt Claude-disallow check, never touch another
category's workbook, never shift rows — rewrite wholesale, English-only
output) and **§6 EFFICIENCY** (structured data first, checkpoint before
anything expensive, the first-block-stops-you rule, no sleep/backoff loops).
Nothing about Bathroom relaxes any of those.

Do not open `rules/furniture.md`, `rules/textile.md`, `rules/storage.md`,
any of the four decor-category modules, `pet-care.md` or `seasonal.md` for a
Bathroom run — cross-loading them is the specific waste this structure
exists to prevent.

---

## 2. ENGINE SHAPE

**Per-category, site-visit extraction** — the same shape as
Furniture/Textile/Storage/Pet Care, not a re-split of already-captured data.
Workers visit each company's site and extract Bathroom categories only.

**Roster: reuse `pipeline/furniture_json_archive/companies.json` as-is**,
copied verbatim into `pipeline/bathroom_json_archive/companies.json` — same
286 companies, same SR 1..286 numbering. Do not regenerate or renumber it.

---

## 3. PIPELINE ARTIFACTS

| File | Job |
|---|---|
| `pipeline/bathroom_json_archive/companies.json` | roster — verbatim copy of `furniture_json_archive/companies.json`, SR 1..286 |
| `pipeline/bathroom_json_archive/assign.py` | prints a worker's assignment block for an SR range; `output_file: b<SR>.json` |
| `pipeline/bathroom_json_archive/status.py` | dispatched / done / in-flight / next-up, scanning `b*.json` |
| `pipeline/bathroom_json_archive/dispatched.txt` | dispatch ledger — SR 1-196 pre-seeded as done (the handoff), append new SRs as batches go out |
| `pipeline/bathroom_json_archive/b<SR>.json` | one per completed company — `{status, failure_reason, notes, rows[], review[]}`. `review[]` is an EXTRA field vs. the pc/f/se contract (explicit routed-out / already-extracted / empty-node entries) — carry it forward, `merge_bathroom.py` reads it directly instead of deriving everything from a `flag` string. |
| `pipeline/bathroom_json_archive/rebuild_archive_from_xlsx.py` | one-time reconstruction script that produced the SR 1-196 `b<SR>.json` files from the handoff workbook. Do not re-run against a hand-edited `Bathroom.xlsx` — it will overwrite manual fixes; edit `b<SR>.json` directly instead. |
| `pipeline/bathroom_json_archive/build_cross_category_index.py` | rebuilds `cross_category_url_index.json` (leaf URL -> owning workbook) from Furniture/Textile/Storage/Lighting/Wall_Decor/Kitchen_and_Dining/Decorative_Home_Accessories/Pet_Care. Re-run whenever one of those workbooks changes, before the next Bathroom merge. Seasonal is deliberately excluded (it overlaps every category on purpose). |
| `pipeline/bathroom_json_archive/merge_bathroom.py` | worker JSON -> `Bathroom.xlsx`. Dedup key `(category, sub_category, link)` within a company, plus the cross-category index check (moves a hit to `review[]`, never `rows[]`) — see `rules/bathroom.md`'s dedup addendum. |
| `pipeline/bathroom_json_archive/verify_bathroom.py` | protected-workbook SHA-256 check (10 files, see below) + sheet integrity + 286-row ledger reconciliation + strict whole-file duplicate-URL check + cross-category contamination check (must be zero) + non-ASCII check (must be zero) |
| `pipeline/bathroom_json_archive/check_english_only.py` | scans every `b<SR>.json` directly for non-ASCII `category`/`sub_category` text — run after any translation fix |
| `pipeline/bathroom_json_archive/protected_baseline.sha256` | the 10 protected files' hashes as of 2026-09-05, before any new Bathroom batch ran |
| `pipeline/bathroom_json_archive/qa_notes.md` | open adjudication log — read before touching SR 1-196 |

`PROTECTED` set for `verify_bathroom.py` / the baseline file: `Furniture.xlsx`,
`Textile.xlsx`, `Storage.xlsx`, `Lighting.xlsx`, `Wall_Decor.xlsx`,
`Kitchen_and_Dining.xlsx`, `Decorative_Home_Accessories.xlsx`, `Pet_Care.xlsx`,
`Seasonal.xlsx`, `Final_Company_List (1).xlsx`.

**Add `Bathroom.xlsx` to every other category's protected-baseline file**
once convenient, so no other run can write to it either (currently
one-directional).

---

## 4. OPEN ADJUDICATION — READ `qa_notes.md` FIRST, DON'T RE-DECIDE

`rules/bathroom.md` resolves almost all boundary questions explicitly. The
open items are inherited from the handoff, not new judgement calls — see
`pipeline/bathroom_json_archive/qa_notes.md`'s **"OPEN"** section for the
full list (rule-24 residue back-catalogue, mirror-subset sweep, prior-pass
compliance findings against `Furniture.xlsx`, an Anthropologie count drift,
a couple of named single-company caveats, and the do-not-rerun / blocked
lists). None of these are yours to resolve solo — log anything new the same
way, don't silently decide.

---

## 5. OUTPUT

One workbook: `Bathroom.xlsx`, project root. Same sheet layout as every other
category workbook — re-derive it before any structural edit, per
`../home-decor-extraction/SKILL.md` §8: `Maisons | Company name | Brand Site
| Country | site URL | Category | Sub-Category | Type | qty | link`.
Grouping rows: `fill FFFFF2CC + bold + blank qty + blank link`, name only.
Header fill `FFD9E1F2`. Copy resolved `font`/`fill`/`border`/`alignment`/
`number_format`/`protection`, never `cell._style` (raises `IndexError` on
save).

---

## 6. TRAPS SPECIFIC TO THIS CATEGORY (proven on the SR 1-196 pass — see `BATCH_BRIEF.md` if it's still in your Downloads for the full detail)

- **"Mirror" and "tumbler" are false-positive magnets.** Mirror-*finish*
  serveware, mirror-*dial* watches, drinking tumblers, mirror-polished
  cutlery have all been wrongly flagged as Bathroom candidates on this run —
  open the node and judge the actual products (rule 29).
- **Lighting brands can still have a real Bathroom node** (Pooky, Beacon
  Lighting both had genuine bathroom-mirror listings) — don't treat "this is
  a lighting company" as proof of absence.
- **A department literally named "Bathroom" can hold zero Bathroom
  products** (Chattels & More's "Bathroom" department is robes/towels/
  slippers only — all Textile).
- **Count traps are the same family as every other category**: JSON-LD caps
  (100), silent pagination caps, sentinel totals, colourway counts
  masquerading as product counts, `?page=` being ignored and re-serving page
  1. Never trust a single source without the enumeration-to-exhaustion or
  multi-page cross-check this project already requires everywhere.
- **Cross-category duplication is a real, proven failure mode on this very
  run** — see §3/`rules/bathroom.md`'s dedup addendum. Run the index check,
  don't assume OPTION 1 against Furniture alone is enough.
- **Robots directives are per-host and per-group** — an API host, sitemap
  host or country subdomain needs its own check; a parent domain's
  permission never extends to another host. A literal "Claude" string is
  not automatically a directive (check it sits under an actual
  `User-agent:` line for a Claude agent).

---

## 7. VERIFY BEFORE REPORTING A MERGE DONE — MANDATORY

Same discipline as every prior category (`../pet-care-extraction/SKILL.md`
§7 has the concrete history of why this matters).

1. Read every new Review-sheet row against `rules/bathroom.md` — does it
   match a worked example, or is it a false-positive flag on a real include?
2. Any regex/keyword logic touched in `merge_bathroom.py` or
   `verify_bathroom.py` this session gets extra scrutiny before being
   trusted at scale.
3. Only report "merged and verified" after both the structural check
   (`verify_bathroom.py`) and this content spot-check pass.
4. `verify_bathroom.py` must always pass its strict whole-file duplicate-URL
   check AND its cross-category contamination check AND its non-ASCII
   check — hard failures, not warnings, every merge.
