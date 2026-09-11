# Skills Overview

Consolidated reference for every Claude skill in `.claude/skills/`. This
document does not replace each skill's own `SKILL.md` — it exists so you can
see how the skills relate to each other and to the shared pipeline without
opening all seven files. For the authoritative rules of any one skill,
always read its own `SKILL.md` and `rules/*.md`.

All skills are discovered by Claude Code from `.claude/skills/<name>/`
(the frontmatter `name:`/`description:` in each `SKILL.md` is what the
harness uses to route a request like "Extract Bathroom" to the right
skill). None of them should be moved out of `.claude/skills/`.

---

## `home-decor-extraction` (core + 7 rule modules)

- **Purpose:** the shared, category-agnostic extraction engine. Handles
  navigation discovery, checkpointing/dispatch conventions, evidence rules,
  and grouping-vs-leaf row semantics that every other product-taxonomy
  category reuses. Loads exactly one rule module per run.
- **Inputs:** the shared company roster (`Final_Company_List (1).xlsx`),
  one of the rule modules under `rules/` selected by the requested
  category.
- **Rule modules (category-specific config, not engine logic):**
  `furniture.md`, `kitchen-and-dining.md`, `lighting.md`, `wall-decor.md`,
  `decorative-home-accessories.md`, `textile.md`, `storage.md`, plus the
  shared `_decor-extraction-core.md` (mechanics, not a category).
- **Output:** `Furniture.xlsx`, `Kitchen_and_Dining.xlsx`, `Lighting.xlsx`,
  `Wall_Decor.xlsx`, `Decorative_Home_Accessories.xlsx`, `Textile.xlsx`,
  `Storage.xlsx` (one per active category).
- **Dependencies:** `pipeline/<category>_json_archive/` (or
  `pipeline/textile_storage_json_archive/` for the combined Textile+Storage
  pass) for dispatch/merge/verify scripts.
- **Failure handling:** blocked sites recorded on the ledger with a
  specific reason; ambiguous PLPs flagged to `Review`, never guessed.
- **Related skills:** `bathroom-extraction` and `pet-care-extraction` are
  siblings that route to this same engine but as their own dedicated
  skills rather than a rule module (they had distinct roster/handoff
  histories).

## `bathroom-extraction`

- **Purpose:** Bathroom category extraction over the shared roster.
- **Inputs:** shared roster; continues a documented cross-machine handoff
  for SR 1-196.
- **Output:** `Bathroom.xlsx`.
- **Dependencies:** `pipeline/bathroom_json_archive/` (`merge_bathroom.py`,
  `verify_bathroom.py`, plus archive-specific tooling like
  `check_english_only.py`, `build_cross_category_index.py`).
- **Related skills:** shares the core engine with `home-decor-extraction`.

## `pet-care-extraction`

- **Purpose:** Pet Care category extraction over the shared roster.
- **Status:** project-complete per its own `SKILL.md` (all 286 roster
  entries processed; SR 286 confirmed duplicate of SR 165, dropped).
- **Output:** `Pet_Care.xlsx`.
- **Dependencies:** `pipeline/pet_care_json_archive/`.
- **Related skills:** shares the core engine with `home-decor-extraction`.

## `seasonal-extraction`

- **Purpose:** one unified pass per company that discovers **every**
  genuine seasonal/holiday category a site's own taxonomy presents
  (Christmas, Diwali, Halloween, Easter, Valentine's Day, Thanksgiving,
  Ramadan/Eid, and whatever else exists) — not one run per holiday.
- **Output:** `Seasonal.xlsx`.
- **Dependencies:** `pipeline/seasonal_json_archive/`
  (`merge_seasonal.py`, `verify_seasonal.py`).
- **Failure handling:** generic gift/promotional/unrelated collection
  pages are excluded unless they satisfy the seasonal rule module's own
  test — not classified as seasonal just for having festive framing.
- **Related skills:** architecturally independent from
  `home-decor-extraction` (own roster/pipeline copy) but follows the same
  engine conventions.

## `bestsellers-extraction`, `new-arrivals-extraction`, `clearance-extraction`

These three are **merchandising-state** siblings — they look for a site's
own "state" pages (what it currently promotes as best-selling / newly
arrived / on clearance), not a product taxonomy — and share one
architecture:

- **Purpose:**
  - `bestsellers-extraction` — genuine Best Sellers / Top Sellers /
    Popular-products pages, never a generic product/category page relabeled.
  - `new-arrivals-extraction` — New Arrivals / New In / Just In / Latest /
    New Collection pages, excluding generic collections that aren't
    genuinely arrivals-labeled by the site.
  - `clearance-extraction` — genuine Clearance / Final Sale / Clearance
    Sale / Sale Clearance pages. **As of 2026-09-11, Outlet and Open Box
    are explicitly excluded**, even when permanently marked down — see
    `clearance-extraction/rules/clearance.md` §1/§3.2.
- **Inputs:** the same shared 286-company roster, copied per archive as
  `companies.json`.
- **Output:** `Bestsellers.xlsx`, `New_Arrivals.xlsx`, `Clearance.xlsx`
  respectively — identical 3-sheet shape (`Output`/`Processing Ledger`/
  `Review`).
- **Dependencies:** `pipeline/bestsellers_json_archive/`,
  `pipeline/new_arrivals_json_archive/`,
  `pipeline/clearance_json_archive/` — each with its own
  `assign.py`/`status.py`/`merge_*.py`/`verify_*.py`.
- **Failure handling:** each has a documented "vs. generic Sale/Offers/
  Deals" ambiguity test; uncertain pages are force-flagged to `Review`
  by the merge script as a mechanical backstop, on top of the worker's
  own page-content judgement.
- **Related skills:** each other (identical architecture, different
  boundary rule), and `home-decor-extraction` for the underlying roster/
  engine conventions they reuse.

---

## Adding a new extraction type

1. Decide whether it's a product-taxonomy category (add a rule module
   under `home-decor-extraction/rules/`) or a new merchandising state /
   distinct-enough workflow (add a new thin skill following the
   `bestsellers-extraction`/`clearance-extraction` shape).
2. Copy the roster convention: a `pipeline/<name>_json_archive/` folder
   with its own `companies.json` (copy of the shared roster),
   `assign.py`, `status.py`, `merge_<name>.py`, `verify_<name>.py`.
3. Write the rule module / skill's boundary rules — what counts, what
   doesn't, and the worked examples for the hardest judgment call (see
   `clearance.md`'s Clearance-vs-Sale test for the pattern to follow).
4. Do not edit `_decor-extraction-core.md` or duplicate its mechanics —
   reuse it.
