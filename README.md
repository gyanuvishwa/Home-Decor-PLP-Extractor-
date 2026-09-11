# Home Decor PLP Extraction

## Overview

This project identifies and extracts **Product Listing Pages (PLPs)** —
category/sub-category listing URLs, not individual product pages — from a
shared roster of ~285 home-decor and adjacent retail websites, across a
product taxonomy (Furniture, Lighting, Kitchen & Dining, Wall Decor,
Decorative Home Accessories, Bathroom, Textile, Storage, Pet Care) and a
merchandising-state taxonomy (Bestsellers, New Arrivals, Clearance,
Seasonal/Holiday).

It is implemented as a set of **Claude Code skills** (`.claude/skills/`)
that drive a real browsing/fetching workflow per company, plus a **Python
pipeline** (`pipeline/`) that dispatches work, tracks progress, and merges
per-company JSON results into reviewable Excel workbooks. This is not a
one-shot scraper script — it is an agent-driven extraction workflow with a
human-auditable paper trail (per-company JSON + a `Review` sheet + a
`qa_notes.md` adjudication log per category).

## Objectives

- For every company in the shared roster, find the genuine PLPs a category
  or merchandising state actually has on that specific site — not every
  page that merely mentions the category.
- Record an exact, evidenced product count per PLP wherever the site
  exposes one, rather than an estimate.
- Never silently guess: ambiguous or unverifiable findings are recorded
  with a flag on a `Review` sheet, not dropped or force-included.
- Produce one clean Excel workbook per extraction type with a consistent
  10-column schema, an audit ledger, and a review queue.

## Supported Extraction Types

| Type | Kind | Skill | Output workbook |
|---|---|---|---|
| Furniture | Product taxonomy | `home-decor-extraction` (rule: `furniture.md`) | `Furniture.xlsx` |
| Kitchen & Dining | Product taxonomy | `home-decor-extraction` (rule: `kitchen-and-dining.md`) | `Kitchen_and_Dining.xlsx` |
| Lighting | Product taxonomy | `home-decor-extraction` (rule: `lighting.md`) | `Lighting.xlsx` |
| Wall Decor | Product taxonomy | `home-decor-extraction` (rule: `wall-decor.md`) | `Wall_Decor.xlsx` |
| Decorative Home Accessories | Product taxonomy | `home-decor-extraction` (rule: `decorative-home-accessories.md`) | `Decorative_Home_Accessories.xlsx` |
| Textile | Product taxonomy | `home-decor-extraction` (rule: `textile.md`) | `Textile.xlsx` |
| Storage | Product taxonomy | `home-decor-extraction` (rule: `storage.md`) | `Storage.xlsx` |
| Bathroom | Product taxonomy | `bathroom-extraction` | `Bathroom.xlsx` |
| Pet Care | Product taxonomy | `pet-care-extraction` | `Pet_Care.xlsx` |
| Seasonal / Holiday | Unified multi-holiday | `seasonal-extraction` | `Seasonal.xlsx` |
| Bestsellers | Merchandising state | `bestsellers-extraction` | `Bestsellers.xlsx` |
| New Arrivals | Merchandising state | `new-arrivals-extraction` | `New_Arrivals.xlsx` |
| Clearance | Merchandising state | `clearance-extraction` | `Clearance.xlsx` |

The first five product-taxonomy rows (Furniture, Kitchen & Dining, Lighting,
Wall Decor, Decorative Home Accessories) originated as one combined
`Home_Decor_Extraction` pass over a 327-company list, later split by
category (`pipeline/category_split/`) into the four still-separate
workbooks — Furniture was re-run standalone on the current 286-company
roster. Textile and Storage were extracted in one combined pass
(`pipeline/textile_storage_json_archive/`) and are documented as two rule
modules under the same skill.

## Architecture

```text
Company roster (Final_Company_List (1).xlsx, shared across all 13 types)
 ↓
Per-company site visit (direct HTTP → Playwright/CDP → Claude-in-Chrome,
 in that order, stopping at the first tier that works)
 ↓
Navigation / navbar discovery (header, mega-menus, footer, sitemap, site
 search — never relying on Google)
 ↓
Category discovery (product-taxonomy categories, or merchandising-state
 pages, per the active skill's rule module)
 ↓
Subcategory discovery (only where the site genuinely exposes real
 sub-listings — never invented)
 ↓
PLP detection & validation (must be a real listing page, not a PDP, not a
 marketing/editorial page, not a coupon page)
 ↓
Deduplication (exact-link dedup within a company; cross-company duplicate
 URLs are a hard verification failure)
 ↓
Per-company JSON result (`<archive>/<prefix><SR>.json`)
 ↓
merge_<category>.py → Excel workbook (Output / Processing Ledger / Review)
 ↓
verify_<category>.py → structural + content reconciliation (hard asserts)
```

## Skills Architecture

All skills live under `.claude/skills/` (the location Claude Code itself
discovers and loads skills from — do not move these into a generic
top-level `skills/` folder, it would stop them from being usable as Claude
Code skills).

- **`home-decor-extraction`** — the master/core skill. Category-agnostic
  engine: navigation discovery, checkpointing, evidence rules, grouping-vs-
  leaf handling. Loads exactly one rule module from `rules/` per run
  (`furniture.md`, `kitchen-and-dining.md`, `lighting.md`, `wall-decor.md`,
  `decorative-home-accessories.md`, `textile.md`, `storage.md`), plus the
  shared mechanics in `rules/_decor-extraction-core.md`.
- **`bathroom-extraction`**, **`pet-care-extraction`** — category-specific
  skills that route to the same core engine and add their own boundary
  rules, for categories that needed a dedicated skill rather than a rule
  module (each had a distinct roster history / cross-machine handoff).
- **`seasonal-extraction`** — one unified pass per company that discovers
  every genuine seasonal/holiday category a site's own taxonomy presents
  (Christmas, Diwali, Halloween, Easter, Valentine's Day, Thanksgiving,
  Ramadan/Eid, etc.) in a single visit, rather than one run per holiday.
- **`bestsellers-extraction`**, **`new-arrivals-extraction`**,
  **`clearance-extraction`** — the three **merchandising-state** skills.
  These are siblings sharing an architecture: they look for the site's own
  Bestsellers/New Arrivals/Clearance merchandising pages, not product
  categories, and each layers a distinct boundary-rules module on the same
  shared core mechanics.

Every skill's `SKILL.md` documents: what it is (vs. what it is not),
routing/load order, the roster it shares, the pipeline artifacts it owns,
and pointers to its `rules/*.md` boundary definition. See
[`docs/SKILLS_OVERVIEW.md`](docs/SKILLS_OVERVIEW.md) for a consolidated
per-skill reference table (purpose, inputs, outputs, dependencies, related
skills) without duplicating each skill's own documentation.

## Extraction Rules

Enforced across every skill (see `rules/_decor-extraction-core.md` and each
category's own rule module for the full detail):

- Extract only PLPs genuinely relevant to the active category/state — not
  every page that happens to mention it.
- Prefer leaf/sub-category PLPs when a site exposes real sub-structure;
  never invent sub-categories that don't exist.
- Don't add a parent-category URL on top of valid, non-overlapping child
  URLs that already cover it.
- Navigation/marketing nodes (Shop All, View All, Collections, Featured,
  Gift Guides, Coupons, Blogs, Black Friday, Search Results, etc.) are never
  a genuine PLP, even if discovered while looking for one.
- A URL that resolves to a single product page (PDP), not a listing, is
  force-flagged for review, never silently included.
- Exact-duplicate URLs within one company are dropped; the **same URL used
  by more than one company** is a hard verification failure
  (`verify_*.py` asserts on it).
- Redirects/canonical URLs are followed to the real destination before
  recording.
- Pagination and infinite scroll are exhausted (or cross-checked via a
  site's own count API) before recording an exact `qty` — a zero-result
  site search is explicitly **not** treated as proof a category is absent;
  nav + sitemap are checked too.
- Blocked/inaccessible sites are recorded on the `Processing Ledger` as
  `BLOCKED / ACCESS FAILURE` with the specific reason (Claude-specific
  `robots.txt` disallow, WAF/Akamai/Cloudflare block, etc.) — never silently
  treated as "no PLP found."
- A `qty` that cannot be verified exactly is recorded as `null` with a
  `MANUAL REVIEW` flag, never estimated or guessed.
- **Merchandising-state boundary calls, corrected 2026-09-11:** Outlet is
  **not** Clearance (a page branded Outlet by its own title/H1/nav/
  subdomain is excluded outright, even if the stock is permanently marked
  down), and Open Box is **not** Clearance either, under the same rule —
  see `.claude/skills/clearance-extraction/rules/clearance.md` §1/§3.2 and
  `pipeline/clearance_json_archive/qa_notes.md`'s 2026-09-11 entries for the
  full worked reasoning and the companies affected.
- Bestsellers must be the site's own Best Sellers/Top Sellers/Popular
  merchandising page, not a generic product/category page relabeled.
- New Arrivals recognizes "New In", "Just In", "Latest", "New Collection"
  as equivalents, but excludes generic collection pages that aren't
  genuinely new-arrivals-labeled by the site.

## Category Rules

Category-specific inclusion/exclusion logic is deliberately kept out of the
shared engine (`rules/_decor-extraction-core.md`) and lives in one rule
module per category/state instead:

```text
.claude/skills/home-decor-extraction/rules/
  ├── _decor-extraction-core.md      (shared engine — reusable, not category-specific)
  ├── furniture.md
  ├── kitchen-and-dining.md
  ├── lighting.md
  ├── wall-decor.md
  ├── decorative-home-accessories.md
  ├── textile.md
  └── storage.md

.claude/skills/bathroom-extraction/rules/       (bathroom boundary)
.claude/skills/pet-care-extraction/rules/       (pet-care boundary)
.claude/skills/seasonal-extraction/rules/       (per-holiday keyword sets)
.claude/skills/bestsellers-extraction/rules/    (bestsellers boundary)
.claude/skills/new-arrivals-extraction/rules/   (new-arrivals boundary)
.claude/skills/clearance-extraction/rules/      (clearance boundary, incl. the
                                                  Outlet/Open-Box exclusions)
```

This means adding a new category or merchandising state means adding a new
rule module (and, if the roster/pipeline shape genuinely differs, a new
thin routing skill) — not editing the shared engine.

## Output Format

Every `merge_<category>.py` writes one workbook with the same 3-sheet
shape:

**`Output`** (10 columns, one row per PLP; a blank row separates
companies; a same-color-filled row marks a grouping/parent category):

| Column | Field |
|---|---|
| A | Maisons (SR — roster serial number) |
| B | Company name |
| C | Brand Site |
| D | Country |
| E | site URL |
| F | Category |
| G | Sub-Category |
| H | Type (`"category"` marker on a company's first row) |
| I | qty (exact product count, or blank if unverified) |
| J | link (the PLP URL) |

**`Processing Ledger`** — one row per roster company (285, after dropping
one known duplicate roster entry): Maisons, Company, Country, Website,
`<Type> Found` (YES/NO), record count, Status
(`<TYPE> FOUND` / `NO <TYPE> FOUND` / `BLOCKED / ACCESS FAILURE` /
`PROCESSING ERROR`), and a Notes column carrying the access/investigation
summary.

**`Review`** — every leaf row with a null `qty`, a manual-review flag
(ambiguous classification, PDP-shaped link, shared-link collision, search-
URL-as-link, etc.), for human adjudication before being trusted as final.

## Installation

- **Python 3.12+** with `openpyxl` (Excel read/write) — the only hard
  dependency the merge/verify scripts import. Some category archives also
  used `requests`, `beautifulsoup4`, `lxml`, `curl_cffi` (TLS-impersonating
  HTTP client), and `playwright` (+ `playwright install chromium`) during
  extraction; install what a given script imports before running it.
- **Claude Code CLI**, with this repository's `.claude/skills/` available
  to it (skills are auto-discovered from `.claude/skills/` in the working
  directory).
- No Node/JS runtime is required for the pipeline itself.

```bash
pip install openpyxl requests beautifulsoup4 lxml curl_cffi playwright
python -m playwright install chromium
```

## Configuration

- **`.env.example`** — copy to `.env` for any secrets you introduce later.
  As audited, **no script currently reads an environment variable**; there
  are no required secrets to run the merge/verify pipeline.
- **Known hardcoded path** (see "Limitations"): every
  `pipeline/*_json_archive/merge_*.py` and `verify_*.py` sets
  `PROJ = r"C:\Users\GyanendraVishwakarma\Web Research Agent"` at the top of
  the file. If you run this pipeline from a different machine/path, update
  that constant in the script(s) you intend to run.
- **`Final_Company_List (1).xlsx`** is the shared 286-row company roster
  (`Output` sheet: SR, Company name, Brand Site, Country, site URL) every
  category/state skill reads from — it is the one input every workflow has
  in common.

## Usage

Each category has an identical three-step pipeline: **dispatch → extract
(agent) → merge/verify**. Commands below use Clearance as the concrete
example; substitute the category's own archive folder and script names
(see the table under "Supported Extraction Types").

```bash
# 1. Check progress / what's left to dispatch
python pipeline/clearance_json_archive/status.py

# 2. Print one worker's assignment (company + brief), then dispatch that
#    company to a Claude Code agent running the clearance-extraction skill
python pipeline/clearance_json_archive/assign.py <SR>

# 3. After a batch of companies has produced cl<SR>.json result files,
#    rebuild the workbook from everything on disk (idempotent)
python pipeline/clearance_json_archive/merge_clearance.py

# 4. Verify the rebuilt workbook (protected-file hashes, ledger
#    reconciliation, strict duplicate-URL check, content sanity checks)
python pipeline/clearance_json_archive/verify_clearance.py
```

In an interactive Claude Code session, the equivalent is simply asking for
the category by name, e.g. **"Extract Clearance"**, **"resume the Bathroom
run"**, or **"merge and verify Bestsellers"** — the relevant skill in
`.claude/skills/` is loaded automatically per its `description` frontmatter.

## Claude / Browser Requirements

- **Claude Code CLI** — the harness these skills are written for
  (`.claude/skills/*/SKILL.md`, standard skill frontmatter/routing).
- **Access-tier order, enforced by every skill's brief:** (1) direct HTTP
  fetch (`requests`/`curl_cffi`), (2) Playwright/CDP when tier 1 can't see
  the real DOM/data, (3) Claude-in-Chrome only as a last resort. Proxy
  URLs (`r.jina.ai`, `translate.goog`, `web.archive.org`, webcache) are
  explicitly banned as a substitute for a real fetch.
- **`robots.txt` is checked for a Claude-specific disallow** before any
  Claude-in-Chrome browser use; a site-wide disallow targeting Claude means
  stop and record `BLOCKED / ACCESS FAILURE`, not bypass it.
- No MCP connectors or external agent-browser tooling are required by the
  pipeline scripts themselves; they are plain Python + openpyxl.

## Workflow Examples

1. **Standard category extraction (e.g. Lighting):** ask "Extract Lighting"
   → `home-decor-extraction` skill routes to `rules/lighting.md` → dispatch
   via `pipeline/lighting_json_archive` conventions → merge into
   `Lighting.xlsx`.
2. **Furniture extraction:** "Extract Furniture" →
   `pipeline/furniture_json_archive/{assign,status,merge_furniture,
   verify_furniture}.py` → `Furniture.xlsx`.
3. **Bathroom extraction:** "Extract Bathroom" / "resume the Bathroom run"
   → `bathroom-extraction` skill → `pipeline/bathroom_json_archive/` →
   `Bathroom.xlsx`.
4. **Seasonal extraction:** "Extract Seasonal" → `seasonal-extraction`
   skill, one unified per-company pass across every genuine holiday
   category → `pipeline/seasonal_json_archive/` → `Seasonal.xlsx`.
5. **Bestsellers extraction:** "Extract Bestsellers" →
   `bestsellers-extraction` skill → `pipeline/bestsellers_json_archive/` →
   `Bestsellers.xlsx`.
6. **New Arrivals extraction:** "Extract New Arrivals" →
   `new-arrivals-extraction` skill → `pipeline/new_arrivals_json_archive/`
   → `New_Arrivals.xlsx`.
7. **Clearance extraction:** "Extract Clearance" / "merge and verify
   Clearance" → `clearance-extraction` skill →
   `pipeline/clearance_json_archive/` → `Clearance.xlsx`.

## Error Handling

- **Blocked websites** — recorded on `Processing Ledger` as
  `BLOCKED / ACCESS FAILURE` with the exact cause (robots.txt disallow,
  named WAF/bot-management product, HTTP status) in Notes; never
  reclassified as "no category found."
- **Missing categories** — a real, thorough check that finds nothing is
  `NO <TYPE> FOUND`; this is distinct from a check that was cut short
  (`BLOCKED`) — `merge_*.py`'s `ledger_status()` deliberately does not
  conflate a `partial` investigation with zero rows into a false
  "confirmed absent."
- **Invalid PLPs** — PDP-shaped links and nav/marketing nodes are dropped
  or force-flagged by the merge script itself as a mechanical backstop,
  independent of what a worker submitted.
- **Redirects** — the destination the redirect resolves to is what gets
  recorded, not the original requested URL.
- **Pagination failures** — if an exact total can't be established (e.g. a
  client-rendered SPA with no server-side count), `qty` is nulled and the
  row is flagged for manual review rather than estimated.
- **Browser failures** — a host-specific block stops that host's
  extraction attempt (no retry/backoff loop against a block); the specific
  failure is recorded, not silently swallowed.
- **Duplicate URLs** — exact duplicates within a company are dropped at
  merge time; the same URL claimed by two different companies is a hard
  `verify_*.py` assertion failure that blocks calling the merge "done."
- **Partial extraction** — a company whose investigation was interrupted
  (e.g. `status: partial` in its JSON) is distinguished on the ledger from
  one that was fully checked and found to have nothing.

## Data Quality

- `verify_<category>.py` re-derives every check independently from the
  written workbook (not from in-memory merge state): sheet structure,
  ledger row count against the roster minus known duplicates, exact
  duplicate-record detection, strict cross-company duplicate-URL assertion,
  non-ASCII (non-English) cell detection, PDP-shaped-link detection, and a
  protected-workbook SHA-256 check confirming the merge never touched any
  *other* category's `.xlsx`.
- A clean `merge_*.py` + `verify_*.py` exit is **not** treated as
  sufficient on its own — every skill's brief requires a manual content
  spot-check of the `Review` sheet (especially generic-Sale-vs-Clearance
  and Outlet-vs-Clearance flags) against the rule module's worked examples
  before a batch is reported as done.
- Output category/sub-category text is enforced English-only; non-ASCII
  cells are a verify-time finding, not silently accepted.

## Repository Structure

```text
Web Research Agent/                         (repo root)
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docs/
│   └── SKILLS_OVERVIEW.md
├── .claude/
│   └── skills/
│       ├── home-decor-extraction/          (core engine + 7 category rule modules)
│       ├── bathroom-extraction/
│       ├── pet-care-extraction/
│       ├── seasonal-extraction/
│       ├── bestsellers-extraction/
│       ├── new-arrivals-extraction/
│       └── clearance-extraction/
├── pipeline/
│   ├── json_archive/                       (original combined Home Decor pass)
│   ├── category_split/                     (splits Home Decor output into 4 category files)
│   ├── furniture_json_archive/
│   ├── textile_storage_json_archive/
│   ├── bathroom_json_archive/
│   ├── pet_care_json_archive/
│   ├── seasonal_json_archive/
│   ├── bestsellers_json_archive/
│   ├── new_arrivals_json_archive/
│   ├── clearance_json_archive/
│   └── final_list_batch_sn*/               (original 327-company roster batches)
├── Final_Company_List (1).xlsx             (shared company roster — the one common input)
├── Furniture.xlsx
├── Kitchen_and_Dining.xlsx
├── Lighting.xlsx
├── Wall_Decor.xlsx
├── Decorative_Home_Accessories.xlsx
├── Textile.xlsx
├── Storage.xlsx
├── Bathroom.xlsx
├── Pet_Care.xlsx
├── Seasonal.xlsx
├── Bestsellers.xlsx
├── New_Arrivals.xlsx
└── Clearance.xlsx
```

Each `pipeline/*_json_archive/` folder is self-contained: its own
`companies.json` (roster copy), `assign.py`/`status.py` (dispatch/progress),
`merge_<category>.py`/`verify_<category>.py`, a worker brief (`*_BRIEF.md`),
a `qa_notes.md` adjudication log, and the per-company result JSON files
(`<prefix><SR>.json`) that are the actual raw extraction evidence behind
every row in the corresponding `.xlsx`.

This existing structure is preserved as-is rather than reorganized into a
generic `scripts/`/`input/`/`output/` split: the scripts resolve paths
relative to their own file location and to the hardcoded project root (see
"Limitations"), so moving them would require rewriting every script's path
logic for no functional benefit.

Not committed to this repository (see `.gitignore`): raw scraping cache
(HTML/XML dumps, `.pkl` snapshots — one exceeds GitHub's 100MB file limit),
ad hoc root-level research scratch files from past sessions, Excel lock
files, editor/OS files, Python/venv cache directories, and
`.claude/settings.local.json` (machine-specific local permissions/paths).
Non-primary workbooks at the project root (an early combined batch export,
a performance-test workbook, an unassigned-records report, and two
non-canonical company-list spreadsheets) are also excluded — the canonical
roster is `Final_Company_List (1).xlsx`.

## Limitations

- **Hardcoded absolute path.** Every `merge_*.py`/`verify_*.py` hardcodes
  `PROJ = r"C:\Users\GyanendraVishwakarma\Web Research Agent"`. The
  pipeline is not portable out of the box — see "Configuration."
- **Windows-oriented.** Examples and some scripts assume a Windows
  filesystem/PowerShell environment (e.g. Excel `~$*.xlsx` lock-file
  checks before writing).
- **No automated test suite.** Correctness is enforced by each
  `verify_*.py`'s structural/content assertions plus a documented manual
  Review-sheet spot-check, not by unit tests.
- **Uneven per-archive tooling.** Some archives (e.g.
  `textile_storage_json_archive`, `seasonal_json_archive`) accumulated many
  one-off debug scripts (`sr202_*.py`, `pw_test*.py`, etc.) during
  extraction that were never cleaned up into reusable utilities; they are
  kept for provenance but are not a stable API.
- **Two categories share one skill without their own dedicated skill
  folder.** Textile and Storage are rule modules under
  `home-decor-extraction/rules/`, not standalone skills — this mirrors how
  they were actually run (one combined extraction pass), not a gap.
- **`Review` sheet findings are not self-resolving.** Ambiguous
  classification calls (e.g. is a "Sale" page really Clearance?) are
  recorded, not decided, by the automated pipeline — they require the
  human adjudication documented in each category's `qa_notes.md`.
- **No CI/CD.** Verification is run manually per batch, not on every
  commit.

## Future Improvements

- Externalize the hardcoded project root into an environment variable or a
  small shared `config.py`, without touching each script's other logic.
- Add a lightweight automated test (e.g. a synthetic 2-3-company roster and
  fixture JSON) so `merge_*.py`/`verify_*.py` changes can be checked without
  a full live batch.
- Consolidate the ad hoc per-archive debug scripts (`textile_storage`,
  `seasonal`) into the same `assign.py`/`status.py`/`merge_*.py`/
  `verify_*.py` shape the other archives already use.
- Give Textile and Storage their own thin routing skills (mirroring
  Bathroom/Pet Care) if they are ever run as fully independent workflows
  again, rather than only as `home-decor-extraction` rule modules.
- Add a CI check that runs every category's `verify_*.py` against its
  current `pipeline/*_json_archive/` and workbook on each push.
