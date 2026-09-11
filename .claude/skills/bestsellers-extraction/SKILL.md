---
name: bestsellers-extraction
description: Run a Bestsellers merchandising-PLP extraction over the shared 286-company roster (the same roster and pipeline used for Furniture/Textile/Storage/Pet Care/Seasonal/Bathroom). Use when the user says "Extract Bestsellers", asks to continue/resume a Bestsellers run, or asks to merge/verify the Bestsellers workbook. Loads the shared decor-extraction core plus the Bestsellers boundary-rules module.
---

# Bestsellers Extraction

A new **merchandising-PLP** module on the **existing shared extraction
pipeline** — not a separate scraper, not PDP extraction. This file routes and
wires the module into that pipeline. It does not restate the shared engine;
see `../home-decor-extraction/SKILL.md` for that.

**This is NOT a product-taxonomy category** the way Furniture/Lighting/Pet
Care are. Bestsellers, Clearance and New Arrivals are three separate
*merchandising states* — pages a site uses to list its best-selling /
permanently-marked-down / newest products, regardless of product type. Do not
look for tables, lighting, mirrors, furniture, bathroom fixtures, etc. — look
for the listing pages themselves. See §3 below and
`rules/bestsellers.md` for the full boundary.

> **Architecture — one engine, three thin sibling skills:**
> ```text
> SHARED PLP EXTRACTION CORE
>         |
>         +-- bestsellers-extraction   <- this skill
>         +-- clearance-extraction
>         +-- new-arrivals-extraction
> ```
> Each has its own roster copy, its own `b?<SR>.json` contract, its own
> merge/verify script, its own workbook, and its own checkpoint/dispatch
> ledger. A failure or a paused run in one must never block or reset another —
> see §7. Do not combine their JSON, their Excel files, or their
> checkpoints.

---

## 1. LOAD ORDER

Before running any extraction, read both, in this order:

1. `../home-decor-extraction/rules/_decor-extraction-core.md` — shared
   engine mechanics (navigation discovery, checkpointing, evidence, grouping
   vs. leaf). Read it for *mechanics only* — its own inclusion/exclusion list
   (product-type categories) does not apply here; §3 below and
   `rules/bestsellers.md` fully replace it for this skill. Note in particular
   that the core's own "NEVER EXTRACT (navigation/marketing)" list bans
   "Best Sellers" — that ban is for the *product-category* extractions
   (Furniture, Lighting, etc.), where a Bestsellers page is correctly
   excluded as non-taxonomic noise. It does not apply here, where Bestsellers
   pages are the entire target.
2. `rules/bestsellers.md` (this skill) — the Bestsellers PLP boundary and
   classification rules.

Also apply, unmodified, **every hard rule in
`../home-decor-extraction/SKILL.md` §2** (HTTP-first access tier, exact
qty+evidence, robots.txt Claude-disallow check, never touch another
category's/skill's workbook, never shift rows — rewrite wholesale,
English-only output) and **§6 EFFICIENCY** (structured data first, checkpoint
before anything expensive, the first-block-stops-you rule, no sleep/backoff
loops). Nothing about Bestsellers relaxes any of those.

Do not open `rules/furniture.md`, `rules/pet-care.md`, `rules/clearance.md`,
`rules/new-arrivals.md`, or any product-taxonomy category module for a
Bestsellers run — the classification target is entirely different and
cross-loading them is the specific waste this structure exists to prevent.

---

## 2. ENGINE SHAPE

This is a **per-company, site-visit extraction**, same shape as Furniture/
Pet Care/Seasonal — workers visit each company's site and extract Bestsellers
merchandising PLPs only, using the shared engine (navigation discovery, PLP
detection, qty+evidence, checkpointing, JSON output). The one structural
difference: the taxonomy discovered is nearly always flat (one or a handful
of listing pages), not a deep category tree — do not manufacture
sub-categories that don't exist (rules §7).

**Roster: reuse `pipeline/furniture_json_archive/companies.json` as-is** —
same 286 companies, same SR 1..286 numbering, same known SR 286/165 duplicate
("Noon UAE") already resolved identically for Pet Care/Seasonal/Bathroom. Do
not regenerate or renumber it.

---

## 3. WHAT THIS SKILL IS LOOKING FOR (quick reference — full detail in `rules/bestsellers.md`)

Genuine PLPs for: Bestsellers, Best Sellers, Bestselling Products, Best
Selling, Top Sellers, Top Selling Products, Popular Products, Most Popular,
Customer Favorites, Trending Products — and local-language equivalents. A
candidate URL (`/best-sellers`, `/bestsellers`, `/collections/best-sellers`,
etc.) is never sufficient alone; open and confirm it's a real listing, not
editorial/marketing, and not a PDP carrying a "Bestseller" badge.

---

## 4. PIPELINE ARTIFACTS (modeled on the Pet Care / Seasonal / Bathroom equivalents)

| File | Job |
|---|---|
| `pipeline/bestsellers_json_archive/companies.json` | roster — verbatim copy of `furniture_json_archive/companies.json`, SR 1..286. Do not edit; do not renumber. |
| `pipeline/bestsellers_json_archive/BESTSELLERS_BRIEF.md` | worker brief — same content as `rules/bestsellers.md`, operational form. Deploy a copy to the scratchpad before dispatching, same as every prior category. |
| `pipeline/bestsellers_json_archive/assign.py` | prints a worker's assignment block for an SR range; `output_file: bs<SR>.json` |
| `pipeline/bestsellers_json_archive/status.py` | dispatched / done / in-flight / next-up, scanning `bs*.json` |
| `pipeline/bestsellers_json_archive/dispatched.txt` | dispatch ledger — starts empty |
| `pipeline/bestsellers_json_archive/bs<SR>.json` | one per completed company — the output contract |
| `pipeline/bestsellers_json_archive/merge_bestsellers.py` | worker JSON -> `Bestsellers.xlsx` (`Output`/`Processing Ledger`/`Review` sheets). Dedup key `(category, sub_category, link)`. Drops navigation/marketing nodes it can independently recognize as never-a-Bestsellers-PLP (BANNED — deliberately does NOT ban "best sellers/top sellers/popular/trending/customer favorites", those are the target). Force-flags any link shaped like a single product page (`/products/<slug>`, `?variant=`, `?sku=`) as `MANUAL REVIEW: LINK LOOKS LIKE A SINGLE PRODUCT PAGE (PDP), NOT A PLP` — a structural safety net, not a page-content check; treat every flag as "needs a look," not "confirmed wrong" (`pipeline/bestsellers_json_archive/qa_notes.md`). |
| `pipeline/bestsellers_json_archive/verify_bestsellers.py` | protected-workbook SHA-256 check (all 10 prior category workbooks + `Final_Company_List (1).xlsx` + the two sibling merchandising workbooks Clearance.xlsx/New_Arrivals.xlsx) + sheet integrity + 285-row ledger reconciliation (286 roster minus the known SR 286/165 duplicate) + a strict whole-file duplicate-URL check (any link used by >1 company is a hard `assert` failure) + a cross-check that every PDP-shaped link actually landed on Review. |
| `pipeline/bestsellers_json_archive/protected_baseline.sha256` | the protected files' hashes as of 2026-09-07, before any Bestsellers batch ran |
| `pipeline/bestsellers_json_archive/qa_notes.md` | open adjudication log — the live per-batch source of truth |

**Add `Bestsellers.xlsx` to the sibling skills' protected-baseline files once
it exists** (they already list it in their `PROTECTED` array — just re-hash
and append to their `protected_baseline.sha256` after the first real merge),
so a Clearance/New Arrivals run can't accidentally write to it either.

---

## 5. OUTPUT

One workbook: `Bestsellers.xlsx`, project root. Same sheet layout as the
other category workbooks — re-derive it before any structural edit, per the
shared contract in `../home-decor-extraction/SKILL.md` §8: `Maisons |
Company name | Brand Site | Country | site URL | Category | Sub-Category |
Type | qty | link`. Grouping rows (only when the site genuinely nests
Bestsellers by department): `fill FFFFF2CC + bold + blank qty + blank link`,
name only. Header fill `FFD9E1F2`. Copy resolved
`font`/`fill`/`border`/`alignment`/`number_format`/`protection`, never
`cell._style` (raises `IndexError` on save).

Most companies will produce exactly one leaf row (`category` = `sub_category`
= `"Bestsellers"`) — that is the expected shape, not a sign of under-
extraction. Do not manufacture sub-rows to look more thorough.

---

## 6. TRAPS SPECIFIC TO THIS SKILL

- **A "Bestseller" badge on a PDP is not a Bestsellers PLP.** The most common
  false positive: a worker follows a product carousel or a badge link and
  lands on a single product page. `merge_bestsellers.py`'s `PDP_LIKE` net
  catches the common URL shapes; it does not replace opening the page.
- **Don't confuse "Popular"/"Trending" with any popularity-adjacent page.**
  A "Trending Now" editorial blog post is not the same as a "Trending
  Products" listing page — open it and check for an actual product grid.
- **Site search returning 0 is not proof of absence** — same trap as every
  other category (`../home-decor-extraction/SKILL.md` §7). Enumerate nav +
  sitemap before concluding a site has no Bestsellers PLP.
- **Multiple URLs, one underlying listing.** `/bestsellers` and
  `/collections/bestsellers` are often the exact same page. Confirm before
  merging two rows into one — don't dedupe on "the counts happen to match"
  alone (rules §5).
- **Category/product overlap with the separately-extracted product-taxonomy
  workbooks is expected**, not a defect — never cross-reference or exclude
  based on what's already in Furniture.xlsx etc.

---

## 7. INDEPENDENT CHECKPOINTS — DO NOT LET A SIBLING'S FAILURE BLOCK THIS SKILL

Bestsellers/Clearance/New Arrivals each track completion independently via
their own `*_json_archive/` directory and their own dispatch ledger. A
company being `BLOCKED` in Clearance says nothing about its Bestsellers or
New Arrivals status, and vice versa. Process the full 286-company roster for
this skill regardless of how the other two are progressing. Never reset this
skill's `dispatched.txt` or delete an archived `bs<SR>.json` because a
sibling skill hit a problem.

---

## 8. VERIFY BEFORE REPORTING A MERGE DONE — MANDATORY

**A clean `merge_bestsellers.py` + `verify_bestsellers.py` exit does not mean
the merge is correct.** `verify_bestsellers.py` checks structure (dedup,
ledger count, protected files, non-ASCII, URL shape, PDP-shape cross-check) —
it does not check that individual PLP-vs-marketing/PDP judgement calls were
actually right. Before reporting any merge as done:

1. Read every row on the Review sheet — not just the summary counts — and
   ask "does this actually match a worked example in `rules/bestsellers.md`
   §8?" for each one.
2. If you wrote or edited any regex/keyword logic in `merge_bestsellers.py`
   or `verify_bestsellers.py` in this session, treat that as reason for
   *extra* scrutiny — test it against the rules module's own examples before
   trusting it at scale, the same discipline `merge_pet_care.py`'s force-flag
   pair already required.
3. Only report a batch "merged and verified" after both the structural check
   and this content spot-check pass.
4. **`verify_bestsellers.py` must always pass its strict whole-file
   duplicate-URL check** — a hard `assert`, not optional.
