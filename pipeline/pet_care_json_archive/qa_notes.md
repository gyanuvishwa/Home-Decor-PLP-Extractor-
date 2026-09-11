# Pet Care — QA notes / open adjudication items

Log flagged judgement calls here as they arrive during batches, don't batch them
to the end (`.claude/skills/home-decor-extraction/SKILL.md` §5.8).

## Open policy questions (block merging any batch that hits these)

1. **Pet food / consumables — no include/exclude policy exists.**
   `rules/pet-care.md` §11 explicitly defers this rather than inventing a rule.
   `merge_pet_care.py` force-flags any sub-category matching food/treats/snacks/
   chews/supplements/vitamins/nutrition as
   `MANUAL REVIEW: PET CONSUMABLE - no include/exclude policy yet` and routes it
   to the Review sheet. Needs an explicit decision (include as Pet Care? exclude
   entirely? a separate future category, the same way Bathroom is held out of
   Home Decor?) before those rows are treated as final.

2. **Medical / veterinary categories — no inclusion rule exists.**
   `rules/pet-care.md` §12, same treatment. `merge_pet_care.py` force-flags
   medicine/veterinary/prescription/clinical/dewormer/flea-tick matches as
   `MANUAL REVIEW: PET MEDICAL / VETERINARY CATEGORY - no inclusion rule yet`.
   Needs an explicit decision before those rows are treated as final.

## Batch-specific items

### Batch 1 (SR 1-20), dispatched and merged 2026-09-02

- **SR 1 Wayfair — "Dog Food Storage & Treat Jars" (qty 457) is flagged as the
  open pet-consumable question (#1 above).** Otherwise clean: 48 rows total (44
  leaf + 4 grouping — Dog Beds, Cat Trees/Perches/Scratchers, Litter Boxes, Bird
  Cages), all qty+evidence. Worker flagged that 3 of the 4 grouping calls (Cat
  Trees/Perches/Scratchers, Litter Boxes, Bird Cages) were inferred by naming
  analogy to the one verified case (Dog Beds), not individually re-confirmed —
  worth a spot check next session.
- **SR 2 West Elm — RESOLVED 2026-09-02.** Redo worker re-verified qty=22 for
  Dog Accessories via a fully compliant tier-1 route (West Elm's own
  Constructor.io browse API, `ac.cnstrc.com`, reached with `curl_cffi`
  `impersonate=safari15_5` — direct HTTP, no proxy). Flag cleared, no longer on
  the Review sheet. The second row ("Kids Dog Shop",
  `/shop/kids-baby/kids-dog-shop/`) was also resolved: confirmed via the same
  compliant route to be dog-themed kids room decor (breadcrumb "Baby & Kids
  Inspiration > Dog Lover" — bedding, wall art, furniture, lamps with dog
  motifs), correctly excluded per the pet-themed-not-pet-care rule and removed
  from `rows` entirely rather than left as an open flag.
- **SR 7 Anthropologie — no direct PLP URL.** Found "Pet Accessories" (qty 75)
  only as a product-type facet count on the aggregate `/home-catalog` page; the
  host blocked every attempt to construct a direct filtered-category URL, then
  blocked further requests entirely. Row is flagged and points at the
  aggregate page rather than a dedicated PLP. Needs a follow-up pass to find
  the real deep link, or a decision to accept the aggregate-page link as-is.
- **SR 8 McGee & Co. — blocked, not attempted.** `robots.txt` names
  `ClaudeBot` with a full-site `Disallow: /`. Per the hard rule this is a
  correct stop, not a gap to fill differently — do not retry with a different
  route.
- **Clean finds (no open items):** SR 3 Pottery Barn (Storage > Pet Beds &
  Accessories, qty 20), SR 14 Ashley Furniture (Pet > Pet Beds, dog crates,
  qty 4), SR 15 Home Centre (Furniture > Outdoor > Pet Care, qty 30), SR 19
  Danube Home (DIY & Tools > Home Utility > Pet Accessories, qty 38).
- **Confirmed absence (0 rows, real investigation each time — not
  unsearched):** SR 4, 5, 6, 9, 10, 11, 12, 13, 16, 17, 18, 20.
- Next batch should start at SR 21.

### Batch 2 (SR 21-40), dispatched 2026-09-02 — merge pending (Pet_Care.xlsx was open in Excel)

- **SR 22 Target — the big one.** 31 rows (2 grouping — Dog Supplies, Cat
  Supplies — + 29 leaves), all qty+evidence, every genuine Pets-department
  category walked via the site's own `__NEXT_DATA__` taxonomy tree. 9 rows hit
  the two open policy gaps and are correctly self-flagged by the worker before
  merge even ran: Dog/Cat Food, Dog/Cat Treats, Dog Vitamins & Supplements
  (consumable); Dog/Cat Flea & Tick Treatment, Cat Health & Grooming, Pet
  Health & Wellness (medical/vet). Access: redsky API for most counts, hit a
  PerimeterX rate block partway through and correctly escalated to
  Claude-in-Chrome (tier 3, compliant) for the rest rather than retrying the
  blocked host. 132 tool calls, ~20 min — the heaviest single-company effort
  so far.
- **SR 40 Aerin — borderline access-tier question.** Confirmed absence (0
  rows), but reached via `api.allorigins.win`, a CORS-proxy not literally named
  in the banned list (`r.jina.ai`/`translate.goog`/`web.archive.org`/webcache)
  but functionally the same category — "a substitute for reaching the site
  directly" through a third party. Unlike the SR2 case, nothing numeric is at
  stake (it's a null/absence result backed by 3 independent checks: sitemap
  keyword grep, full mega-menu enumeration, and cross-check against the prior
  Home-Decor pass's already-established catalog), so not treated as a redo
  candidate. **Open question: should `api.allorigins.win` (and similar
  CORS-proxy services) be added to the explicit ban list in
  `rules/pet-care.md` and `PET_CARE_BRIEF.md`, the same as r.jina.ai?** A
  prior Home-Decor pass apparently used this route too, so it may predate the
  current ban policy rather than being a new violation — needs a decision
  before the next batch, not a retro-fix of this one.
- **SR 24 Marshalls — "Pet" department, qty 226**, cross-verified three ways
  (rendered header, embedded nav JSON, and confirming zero further children in
  the site's own navigation hierarchy). Correctly deduplicated the New
  Arrivals/Clearance "Pet" filter variants against the base node.
- **SR 33 Horchow (now redirects to Neiman Marcus) — "Pet Beds &
  Accessories", qty 26**, dual-verified (rendered header + embedded JSON).
- **SR 21 Zara Home UAE — clean "Pets Collection"**, 5 sub-categories (Toys,
  Beds, Food Bowls, Washing and Brushing, Collars and Leashes), all
  qty+evidence via the site's own category-grid API.
- **SR 23 At Home — 4 categories** (Pet Beds, Food Bowls & Mats, Pet Food
  Canisters, Furniture Covers & Blankets), all qty+evidence via the SFRA
  storefront's unchallenged refinebar endpoint.
- **SR 26 HAY US — single "Dogs" leaf, qty 10.**
- **SR 36 The Company Store — 3 small categories** (Pet Pajamas, Pet Towels,
  Pet Bedding), qty 1-2 each, correctly deduped a marketing-page overlap.
- **Confirmed absence (0 rows, real investigation each time):** SR 25 World
  Market, SR 27 Blu Dot, SR 28 Room & Board, SR 29 High Fashion Home, SR 30
  One Kings Lane, SR 31 Perigold, SR 32 1stDibs, SR 34 Ballard Designs, SR 35
  Frontgate (96 tool calls — thorough dig into orphaned legacy pet-product
  pages despite the site historically selling pet furniture), SR 37 The
  Novogratz, SR 38 Caitlin Wilson, SR 39 Jonathan Adler.
- Next batch should start at SR 41.

### Merge script fix, 2026-09-02 (applies retroactively to both batches)

**`CONSUMABLE_FLAG` in `merge_pet_care.py`/`verify_pet_care.py` was over-matching
on feeding equipment.** The regex matched the literal word "food"/"treat"
anywhere in a sub-category name, which wrongly force-flagged genuine Tier 1
includes — "Food Bowls" (Zara Home), "Dog/Cat Bowls & Food Storage" (Target),
"Food Bowls & Mats" / "Pet Food Canisters" (At Home), "Dog Food Storage & Treat
Jars" (Wayfair) — as if they were the consumable-policy-gap items, when
`rules/pet-care.md`'s own Tier 1 list explicitly includes "Pet Food Storage"
and "Pet Treat Storage" as ordinary feeding-equipment categories, no policy
question involved. Added `FEEDING_EQUIPMENT_OVERRIDE` (bowls/storage/
canisters/mats/jars/containers/dishes/feeders) as a negative match — a
food/treat word combined with a container word is no longer flagged. Fixed in
both scripts, re-merged: review rows dropped from 15 to 9, all correctly the
genuine open-policy items (Dog/Cat Food, Dog/Cat Treats, Dog Vitamins &
Supplements, Dog/Cat Flea & Tick Treatment) plus SR22's two self-flagged
ambiguous buckets (Cat Health & Grooming, Pet Health & Wellness).

### SR 7 Anthropologie — RESOLVED 2026-09-02

Redo worker found the real filtered-PLP URL:
`https://www.anthropologie.com/home-catalog?attributionProductType=Pet+Accessories`
— discovered via the site's own embedded `urbnInitialPiniaState` JSON (not a
guessed query param) and confirmed by clicking the live UI filter and reading
`window.location.href`. Verified server-rendered with qty still 75, matching
the original figure exactly. Link updated, flag cleared, no longer on Review.

### Batch 3 (SR 41-60), dispatched, merged, verified and content-spot-checked 2026-09-02

- **SR 46 John Lewis Home — the big one.** 15 rows (1 group + 14 leaves) under
  `Home & Garden > Hobbies & Interests > Pet Care`, all 14 leaf quantities
  summing exactly to the hub's reported 207 total (proof it's a complete,
  mutually-exclusive facet split, not a guess). One correctly-flagged
  consumable ("Treats", qty 8 — treat gift sets/advent calendars).
- **SR 47 Dunelm — 7 rows** (1 group + 6 leaves: Pet Bowls 72, Dog Supplies
  761, Dog Beds 292, Dog Leads/Collars/Harnesses 83, Cat Supplies 167, Cat
  Beds 88), every qty dual-verified against two independent count sources.
- **SR 52 Williams Sonoma Home — edge case, correctly handled.** "Pet Food
  Storage & Supplies" (qty 15) contains a container word ("Storage"), so the
  merge script's `FEEDING_EQUIPMENT_OVERRIDE` would not have force-flagged it
  — but the worker inspected the actual 15 products and found real consumables
  mixed in (dog treats, a treat maker), and set its own
  `MANUAL REVIEW: PET CONSUMABLE` flag in the JSON. That flag is worker-set,
  not merge-script-derived, so it survived the override correctly — this is
  the exact "check which rule the rules doc actually resolves it to, don't
  trust first-match regex behavior" case SKILL.md §7 now calls out explicitly.
- **SR 43 Nordstrom Home — qty correctly left null.** Found "Pet Accessories"
  but two live renders returned different totals (835 vs 854) and the listing
  showed contamination with a non-pet product; a bot-wall then blocked further
  verification. Flagged `MANUAL REVIEW: unstable/unverifiable qty` rather than
  guessing — this is not a consumable/medical policy item, just an honest gap.
- **SR 51 Cox & Cox — 1 product.** "Pet" (Round Rattan Pet House), qty 1.
  Correctly dropped a zero-product Pet Beds page and a marketing "Gifts for
  Pets" landing page.
- **SR 55 Crate & Barrel — 1 category.** "Pet Accessories", qty 19,
  dual-verified; correctly excluded "pet-friendly upholstery" (fabric
  treatment, not a pet product) and "Petrie" (unrelated collection name).
- **Two workers self-caught and fixed process mistakes mid-run**: SR42 (Surya)
  and SR44 (Bed Bath & Beyond) each briefly wrote a stray temp file into the
  protected `pipeline/pet_care_json_archive` directory instead of the
  scratchpad, caught it themselves, deleted it, and continued correctly — no
  action needed, noting for pattern-awareness only.
- **Confirmed absence (0 rows, real investigation each time):** SR 41 Z
  Gallerie, SR 42 Surya, SR 45 Habitat UK, SR 48 Made.com UK (now a Next plc
  storefront, confirmed live-but-empty via soft-404 taxonomy check), SR 49
  Swoon, SR 50 OKA, SR 53 The Citizenry, SR 54 Schoolhouse, SR 56 CB2 US
  (roster's own name field literally reads "US" — cosmetic roster quirk, not
  an extraction issue), SR 57 West Elm UK (unlike West Elm US, genuinely no
  pet line), SR 58 Pottery Barn Kids UK (same Peter Rabbit false-positive
  pattern as PB Kids US, correctly excluded), SR 59 The White Company (the
  seasonal dog range noted in the dispatch prompt is not currently live), SR
  60 Soho Home.

**Content spot-check performed before reporting this batch done** (per
[[verify-merge-flags-before-reporting-done]] / SKILL.md §7): read all 12
Review-sheet rows individually against the rules module's Tier 1/§11/§12
examples — all 9 from batches 1-2 plus 3 new ones (Nordstrom's qty flag,
John Lewis's Treats, Williams Sonoma's mixed-consumable leaf) are genuine, no
false positives. Cross-checked all 8 leaf rows across all 3 batches whose
name matches both a consumable word and a container word — confirmed all 8
are legitimate feeding-equipment categories correctly left unflagged.

### Batch 4 (SR 61-80), dispatched, merged, verified and content-spot-checked 2026-09-02

- **SR 69 Macy's Home — the big one.** 25 rows (2 grouping — Dog Supplies, Cat
  Supplies — + 23 leaves) across Dog/Cat/Small Animal & Bird departments.
  153 tool calls, ~20 minutes: Akamai blocked every route until Claude-in-Chrome,
  found the real hub via a homepage footer link (not the roster's own `id=22672`
  URL, which dead-ends), correctly merged one true cross-species duplicate
  (Dog/Cat "Carriers & Crates" resolved to the identical listing), backfilled
  Tier-1 categories (Toys, Litter, Waste) missing from the pill-nav via
  species-scoped facet PLPs, cross-validated every qty via
  `ceil(totalResults/resultsPerPage) == numberOfPages`. 4 correctly-flagged
  open-policy rows (Dog/Cat Food & Treats, Dog/Cat Health & Wellness).
- **SR 70 Lowe's Home Decor — real department, unverifiable qty.** Found
  "Animal & Pet Care" (14 sub-categories, embedded in `__PRELOADED_STATE__`
  taxonomy JSON) but every `/pl/` listing page was Akamai-blocked across 6
  impersonation profiles + Playwright — all 14 rows correctly carry `qty: null`
  rather than a guess. Excluded "Livestock Supplies" (farm animals, not
  companion pets). 2 of the 14 also carry a consumable flag (Toys & Treats,
  Vitamins & Supplements).
- **SR 77 Bloomingdale's — 9 rows** (1 group "The Pet Shop" + 8 leaves: Beds,
  Bowls, Carrier, Collars & Leashes, Pet Clothing, Toys, Other, Treats),
  164-item hub found via footer nav; 2 of 8 facet counts cross-verified
  against live filter headers.
- **SR 78 Container Store — "Pet Accessories", qty 40**, triple-verified
  (facet count + selectedFilters count + product-id array length); all 40
  product names confirmed genuinely pet-specific.
- **SR 80 HSN Home — "Pet Supplies", 11 rows, 253 total items**, every qty
  backed by a page-header string matching the site's own facet count; worker
  explicitly avoided `translate.goog` even though a prior Home-Decor pass on
  this same company had used it — the access-tier ban is holding across
  sessions, not just within this one.
- **SR 61 Heal's, SR 62 Rejuvenation, SR 71 TJ Maxx, SR 78 Container Store —
  smaller finds**, all with dual/triple-verified qty. Note SR 62's "Pet
  Accessories" is a single wall-mounted dog-wash faucet — a borderline
  plumbing-fixture judgment call the worker flagged in `notes` (kept as
  grooming/hygiene per the site's own pet-specific category naming; not
  force-flagged since it's a scope judgment, not a consumable/medical policy
  gap).
- **SR 72 Urban Outfitters — correctly 0 rows**, unlike sibling Anthropologie
  (SR7, real 75-item facet): UO's only pet-labeled slug returns
  `totalRecordCount: 0`, correctly dropped per the zero-product rule.
- **Confirmed absence (0 rows, real investigation each time):** SR 63 Serena &
  Lily, SR 64 Lulu and Georgia, SR 65 Rowen & Wren, SR 66 The Inside, SR 67
  Burrow, SR 73 Ferm Living US, SR 74 Garnet Hill Home, SR 75 Scully & Scully
  (correctly excluded pet figurines + "Dog/Cat Lover Gift Ideas" buckets), SR
  76 Safavieh Home.
- **SR 68 Joybird — 1 row.** "Pet Beds" (qty 1); correctly merged a
  style-facet duplicate (`/modern/pet-beds/`) into the same row and excluded 2
  editorial pet-friendly-fabric marketing pages.

**Content spot-check performed before reporting this batch done** (per
[[verify-merge-flags-before-reporting-done]] / SKILL.md §7): read all 33
Review-sheet rows individually against the rules module's examples — all
genuine (13 consumable, 2 medical, 1 qty-unstable, 14 Lowe's
qty-Akamai-blocked, plus SR52/SR62's worker-set judgment-call flags), zero
false positives. Cross-checked all 9 leaf rows across all 4 batches matching
both a consumable and container word — all 9 confirmed legitimate
feeding-equipment categories, correctly unflagged.

**⚠️ Protected-file note, not caused by this pipeline:** `verify_pet_care.py`
flagged `Kitchen_and_Dining.xlsx`, `Lighting.xlsx`, and `Textile.xlsx` as
MODIFIED against the baseline. Checked: `merge_pet_care.py` only ever writes
to `Pet_Care.xlsx` (confirmed in source — no code path touches those files),
and file mtimes show all 3 were modified today (2026-09-02, ~11:32-11:36),
with `~$Furniture.xlsx`/`~$Lighting.xlsx`/`~$Textile.xlsx` lock files present
— strongly indicating the user's own concurrent Excel activity on those
workbooks, unrelated to the Pet Care batch. Flagged to the user directly;
`protected_baseline.sha256` was deliberately NOT auto-updated — that's the
user's call, not something to silently correct.

### Batch 5 (SR 81-100), dispatched, merged, verified and content-spot-checked 2026-09-02

First batch to include non-English (French) companies — SR96-100. All French
workers were explicitly instructed to normalize category names to English
while preserving the site's actual taxonomy (no invented English categories).

- **SR 92 IKEA UK — "Pet products" hub**, 3 rows (1 group + Cats 11, Dogs 13),
  triple-verified. Worker independently found the LURVIG line (mentioned in
  the dispatch note) has been superseded by UTSÄDD — didn't take the note at
  face value, investigated and corrected it.
- **SR 96 Maisons du Monde FR — 5 rows**, well-translated to English (Boîtes
  à croquettes → Pet Food Storage Boxes, Gamelles → Pet Bowls, Arbre à chat →
  Cat Trees/Scratchers). Parent "Animalerie" page's own count (98) doesn't
  match its children's sum (664) — a real site catalog quirk, not a filter
  artifact — so correctly kept as a pure grouping row (`qty: null`) rather
  than reconciled or guessed, per the shared "parent totals are not always
  supersets of children" rule.
- **SR 90 Zara Home UK — 6 rows**, mirroring Zara Home UAE's (SR21) taxonomy
  structure but with independently verified, genuinely different per-country
  quantities (not copied).
- **SR 83 Next Home — "Pet Accessories", qty 135.** Extremely thorough: probed
  23 guessed sub-category slugs to confirm the category is flat (all
  soft-404'd), correctly excluded a Gifts-department recipient filter.
- **SR 93 Rockett St George — 2 rows.** Correctly rejected the "Animal
  Magic/Animal Lights" pet-themed decor collections exactly as flagged in the
  dispatch note, and caught a dead "For Pets" gift-guide redirect.
- **Smaller finds, all dual/triple-verified:** SR 82 La Redoute UK ("Pet
  Shop", qty 41), SR 86 Loaf ("Dog Beds", qty 2 — correctly excluded a
  punny-named human mattress), SR 88 Oliver Bonas ("Pet Accessories", qty 32),
  SR 91 Westwing UK ("Pet Supplies", qty 30), SR 95 Amara ("Cat & Dog
  Accessories", qty 37).
- **Confirmed absence (0 rows, real investigation each time):** SR 81 Graham
  and Green (found genuine pet SKUs with no dedicated PLP, correctly excluded),
  SR 84 M&S Home, SR 85 Barker and Stonehouse, SR 87 Furniture Village, SR 89
  H&M Home UK (a genuine "Dog Clothes & Accessories" node exists but sits under
  H&M's general fashion department, out of this company's scope), SR 94 House
  of Hackney, SR 97 AM.PM France, SR 98 La Redoute Interieurs FR (correctly
  scoped separately from sibling SR82), SR 99 Conforama FR (traced a
  discontinued "Animalerie" department — dead CMS tile, 404 URLs), SR 100
  Camif (correctly flagged its own site search as non-discriminating rather
  than using it as absence proof).

**Content spot-check performed before reporting this batch done** (per
[[verify-merge-flags-before-reporting-done]] / SKILL.md §7): all 33
Review-sheet rows are byte-identical to the pre-batch-5 set — batch 5's finds
introduced zero new flags. Cross-checked the full 100-company dataset for
container+consumable rows: 11 total (2 new from this batch — Zara UK's "Food
Bowls", Maisons du Monde's "Pet Food Storage Boxes"), all confirmed legitimate
equipment, correctly unflagged.

### Batch 6 (SR 101-120), dispatched, merged, verified and content-spot-checked 2026-09-02

First fully non-English batch — France (SR101-102), Germany (SR103-110),
Netherlands (SR111-114), Belgium (SR115-116), Spain (SR117-120). All workers
normalized category names to English while preserving the site's real
taxonomy; no issues.

- **Cross-market comparison pattern worked well this batch** — several
  companies in this roster have sibling entries in other countries, and every
  worker independently re-verified rather than copying:
  - **Zara Home**: now 4 markets done (UAE/SR21, UK/SR90, DE/SR106, ES/SR117),
    same shared Inditex taxonomy IDs, each with genuinely different qty. ES
    uniquely included "Customisation" as a real leaf (4 genuinely pet-specific
    products, zero overlap with other categories) where UAE excluded the same
    node (non-pet items there) — flagged by the worker for cross-market
    consistency review, not a bug.
  - **IKEA**: DE (SR107) independently found its own DE-specific slug
    (`haustierprodukte`, not a copy of UK's `pet-products`) and confirmed the
    same shared category IDs/platform as UK (SR92).
  - **Westwing**: DE (SR103, qty 154) vs UK (SR91, qty 30) — same single-leaf
    "Pet Supplies" pattern, correctly independent numbers.
  - **Maisons du Monde**: BE (SR116, 3 sub-categories, exact rollup) vs FR
    (SR96, 5 sub-categories, mismatched rollup) — smaller taxonomy in BE,
    independently verified, not copied.
- **SR 105 XXXLutz DE — 6 rows.** Small pet-furniture-only assortment (Dog
  Cushions/Sofas/Beds, Pet Accessories, Cat Trees), all pagination-exhaustion
  verified.
- **SR 108 Connox — 5 rows.** Escalated to Playwright after direct HTTP only
  saw an empty React mount (unlike the prior Home-Decor pass on this company,
  which nulled every qty) — got real rendered counts this time. Correctly
  caught the parent hub's own count not matching its children's sum
  (cross-listing) and left the group qty null rather than reconcile.
- **SR 111 fonQ — 5 rows**, very thorough (42 tool calls): 3 leaves have no
  separately crawlable URL, so qty came from an embedded exhaustive facet JSON
  instead (4 facet values summing exactly to the parent's 32) — flagged
  `MANUAL REVIEW` per row for the missing-URL reason, `link: null` rather than
  fabricated. Correctly excluded wild-bird/bat nest boxes filed under the
  Garden department, not Pet Supplies.
- **SR 112 vtwonen — 6 rows.** Exact rollup verified via product-ID overlap
  (85 = sum of 5 children, 100% overlap). One row ("Birdhouses & Feeding
  Spots") self-flagged as genuinely ambiguous — wild garden birds vs. owned
  pet birds — a real scope judgment call, not a policy-gap item.
- **SR 120 Casa Viva — 1 row.** "Mascotas", qty 1, dual-verified.
- **Confirmed absence (0 rows, real investigation each time):** SR 101 The
  Socialite Family, SR 102 Fleux, SR 104 Hoeffner (traced pet-adjacent SKUs
  found via search back to their breadcrumbs — all sit under generic non-pet
  categories, correctly didn't invent a category), SR 109 KARE, SR 110
  Butlers, SR 113 HKliving, SR 114 Made.com NL (same defunct-Made.com pattern
  as the UK sibling, traced through a domain redirect to Next Retail), SR 115
  Juttu Home (sharp exclusion of pet-themed gift items), SR 119 Sklum.

**Content spot-check performed before reporting this batch done** (per
[[verify-merge-flags-before-reporting-done]] / SKILL.md §7): read all 38
Review-sheet rows — the 5 new ones (fonQ ×3, vtwonen, Zara Home ES) are all
legitimate worker-set judgment-call flags, not regex false positives.
Cross-checked the full 120-company dataset for container+consumable rows: 14
total (3 new — Connox, Maisons du Monde BE, Zara Home ES, all "Food Bowls"
variants), all confirmed legitimate equipment, correctly unflagged.

### Strict whole-file duplicate-URL check added 2026-09-02 (user request)

The user explicitly asked: "also check for duplicate urls in whole file
strictly in every merge." `verify_pet_care.py` now has a hard `assert` (not a
warning) that no link is ever assigned to more than one *different* company —
distinct from the pre-existing "same link twice in one company" check (a
same-company repeat can legitimately happen via nav overlap between two
categories on one site; a cross-company repeat never can — each URL belongs
to exactly one company's domain, so a repeat there means a real bug). Run
retroactively against all 120 companies through batch 6: **zero violations**.
This check is now permanent and mandatory — see SKILL.md §7 item 4. Any
future edit to `verify_pet_care.py` must keep it, and it must be run (current
version, not a stale cached copy) before any batch is reported merged.

### Batch 7 (SR 121-140) — Italy, UK, Germany, France, Denmark, Netherlands,
Sweden, Spain — dispatched, merged and verified 2026-09-02

20 workers. 1 worker (SR 123, H&M Home IT) stopped mid-task without writing
its output file — resumed via `SendMessage` to finish the in-progress check;
it completed cleanly on resume (genuine absence, full mega-menu + 30-shard
sitemap sweep). All 20 `pc<SR>.json` files present before archiving.

Sibling/cross-market companies, all independently re-verified rather than
reused: Westwing IT (SR 121, vs. other Westwing markets already in the
roster), Anthropologie UK (SR 126 — confirmed a genuinely distinct `/en-gb/`
storefront from SR 7's US site, 18 products vs. 75 for the same facet name,
not a copy), H&M Home IT (SR 123) vs. H&M Home France (SR 139, independently
16 products each), IKEA France (SR 140, vs. other IKEA markets — cats
confirmed discontinued in FR, dogs qty=1).

Absent (confirmed via real investigation, not default site-search):
Coincasa (SR 122, the one pet category page has zero live products, verified
against a working control category), Denby (SR 124, has Pet Bowls only — 2
sibling "gift" collections correctly excluded as duplicates/marketing),
Pooky (SR 127), Nkuku (SR 128, 4 pet-named Shopify collections all
genuinely 0 products despite inflated `products_count`), Nordic Nest
(SR 136), RoyalDesign (SR 137, correctly discarded a false-absence site
search returning ~32k "results"), Mango Home (SR 138), DEPOT (SR 132, one
pet category page exists with 0 products).

Blocked: Leroy Merlin France (SR 134) — confirmed a network/edge-level 403
across all 3 access tiers including a real Claude-in-Chrome browser session,
not a bot-fingerprint block; per this brief's rules, `web.archive.org` is not
an allowed substitute, so no Wayback reconstruction was attempted. That's now
2 blocked companies total (with McGee & Co. from batch 1).

Found: Westwing IT (154), Fenwick Home (3 rows, +MANUAL REVIEW for an
18-product gap between the parent total and its two named children — flagged
rather than guessed), Anthropologie UK (18), Mömax Germany (16), Castorama
France (29 rows across 5 species — several MANUAL REVIEW flags for
wild-garden/poultry/livestock content mixed into pet categories at the PLP
level, and for farm-animal/poultry housing that the rules module has no
policy on at all, same treatment as the two existing open policy gaps),
OTTO Home (93 rows across 7 species), JYSK Denmark (4 rows, cross-verified
via 3 independent count signals), Xenos (1 row), H&M Home France (16),
IKEA France (2 rows).

**Bug found and fixed during the mandatory content spot-check (SKILL.md §7):**
`merge_pet_care.py`'s `CONSUMABLE_FLAG` force-flagged OTTO Home's "Chew Toys"
(SR 131) as `MANUAL REVIEW: PET CONSUMABLE`, but `rules/pet-care.md` §14
explicitly lists "Chew Toys" and "Interactive/Puzzle/Treat Toys" under Tier 1
"Toys & enrichment" as ordinary, no-review-needed includes — the exact same
failure mode as the earlier "Food Bowls" bug (a food/treat/chew *adjective*
describing a toy, not a separate consumable item). Fixed by adding a
`TOY_QUALIFIER_PHRASE` strip step in both `merge_pet_care.py` and
`verify_pet_care.py`: strip any `<chew|treat|puzzle|interactive|fetch>
toy(s)` phrase out of the sub-category name before testing for a consumable
match. Verified against known good/bad cases: "Chew Toys" and
"Interactive/Puzzle/Treat Toys" now correctly clear; "Toys & Treats", "Pet
Toys & Treats", "Dog Food & Treats" (treats listed as a *separate* item, not
describing a toy) correctly stay flagged. Re-ran merge+verify after the fix —
review rows dropped from 54 to 53, only the one false positive removed, zero
new false negatives (checked every remaining Review row and every Output row
containing "Toy" by hand). See
[[verify-merge-flags-before-reporting-done]] for the generalized lesson.

### Batch 8 (SR 141-160) — France, Denmark, Finland, Italy, Netherlands,
Germany — dispatched, merged and verified 2026-09-02

20 workers, mostly Scandinavian/French design and lifestyle brands. Zara Home
France (SR 146) is the roster's 5th Zara Home market — independently
re-derived, 6 sub-categories cross-verified twice against the site's own
API with zero drift.

**A banned-proxy violation was caught and corrected:** SR 153 (Dille &
Kamille) initially used `r.jina.ai` — explicitly banned at every access
tier — after direct fetch timed out (this workstation's known-intermittent
IPv4 egress to that host, see [[ipv4-egress-dead-use-ipv6-proxy]]). Resumed
the same worker and told it to redo through a compliant route rather than
accept the banned-proxy result. It exhausted all 3 tiers properly this
time — 6 curl_cffi TLS profiles, confirmed no AAAA record exists (so no IPv6
route was possible), Playwright/CDP, and Claude-in-Chrome — and hit genuine
TCP-level connection failures on every one (not a WAF/bot-block, which would
succeed at TCP and fail at HTTP). Correctly changed its own status from "ok"
to "blocked" and dropped the unverifiable "Dog Baskets qty=5" finding rather
than keep a number that only ever came from the banned proxy. That's now 4
blocked companies total (McGee & Co., Leroy Merlin France, BHV Marais Maison,
Dille & Kamille). Re-check Dille & Kamille's `Home > Baskets > Dog baskets`
page first once this host's egress recovers.

BHV Marais Maison (SR 144) is also blocked — a site-wide Cloudflare
challenge confirmed unresolvable across direct HTTP, the prior pass's
8-profile curl_cffi + proxy sweep, and this session's own Claude-in-Chrome
attempt (browser sat on the challenge page, never resolved).

Absent (confirmed via real investigation): Iittala, &Tradition, Muuto, House
Doctor, Ferm Living, Normann Copenhagen, Galeries Lafayette Maison, Broste
Copenhagen, Merci Paris, Georg Jensen — 10 Scandinavian/French design brands
with genuinely no pet product line, each proven via full nav/sitemap
enumeration (not default site-search results).

Found: Monoprix Maison (5 rows), Sostrene Grene (1), Finnish Design Shop
(3 rows), Zara Home France (7 rows), Seletti (1, a pet-themed
Toiletpaper-collab furniture line correctly excluded), AmbienteDirect (1),
Bloomingville (1, with a live-vs-schema qty discrepancy correctly flagged
rather than guessed), Manufactum (1, with a non-pet-specific brush correctly
filtered out of the count).

**Content spot-check performed before reporting this batch done:** both new
Review flags (Monoprix's mixed pet/non-pet "Other Accessories" node,
Bloomingville's live-vs-JSON-LD qty conflict) are genuine judgment calls, not
regex false positives. Reverse-checked every Output row in this range for
container/consumable/toy overlaps — Zara Home France's "Food Bowls"
correctly stayed unflagged (equipment override still working).

### Batch 9 (SR 161-180) — Netherlands, Belgium, UAE cluster, Japan, Australia
— dispatched, merged and verified 2026-09-02

20 workers, first batch reaching outside Europe/US: UAE (10 companies),
Japan (MUJI, Nitori), Australia (Beacon Lighting, Kmart, Target AU, Temple &
Webster, David Jones). Two workers stopped mid-task without writing output
and needed resuming: SR 165 (Noon UAE) twice — first a genuine API server
error cutting off the agent mid-response, then a second silent stall waiting
on a background fetch; both times resumed via `SendMessage` rather than
redispatched from scratch, and it completed cleanly the second resume.

3 more blocked companies this batch, all confirmed via all 3 access tiers
including a real Claude-in-Chrome session, none via a banned proxy: PAN
Emirates UAE and Tavola UAE (both persistent Cloudflare Turnstile that never
resolved even in a real browser — Tavola's prior Home-Decor pass had used
`translate.goog` to get through, correctly not reused here since it's
banned). BHV Marais Maison from batch 8 is the same class of block. That's
now 6 blocked companies total (batch 8 also had Leroy Merlin France and
Dille & Kamille — see their notes above).

IKEA UAE (SR 164) is this roster's 3rd IKEA market — independently
re-derived (Cats=12, Dogs=12), genuinely different from both other markets
already extracted (one had cats discontinued, qty=1 dog; this one has both
categories live at 12 each).

Absent (confirmed via real investigation): Pols Potten, Serax, OC Home UAE,
Home R Us UAE, Chattels & More, Aura Living UAE, Tanagra, The Bowery
Company, Beacon Lighting — 9 companies with genuinely no pet product line,
each proven via full nav/sitemap enumeration. Crate & Barrel UAE is a
notable near-miss: 2 real pet-bowl SKUs exist buried in a generic "Home
Accents" catch-all with no dedicated pet category/PLP anywhere — correctly
not reported as a row per the boundary rule (a generic branch needs a
pet-specific parent node, which doesn't exist here).

Found: MUJI Japan (4 rows, a nav-hidden Pet Supplies subtree discovered
through a product breadcrumb, not the visible menu — exhaustiveness
cross-checked two ways), Nitori Japan (14 rows across 13 categories, the
single biggest simple find this project — exhaustion-checked via
pagination), Kmart Australia (23 rows across Dog/Cat/Fish/Pet Tech/Pet
Wellness, qty cross-verified against a second backend API endpoint per
leaf), Target Australia (15 rows, 445 total products, double
cross-verified), Temple & Webster (13 rows, 872 total, reached via a real
Claude-in-Chrome session after a Cloudflare challenge that auto-resolved —
no banned proxy needed), David Jones Home (7 rows, 3 of them null-qty behind
an hCaptcha that was correctly never solved, one behind a genuine app error
unrelated to bot-detection), Noon UAE (175 rows across 155 leaf categories —
by far the largest single company this project has seen; status "partial"
since 99 of 155 leaves only expose a rounded/threshold count like "300+"
with no exact figure anywhere in the page, correctly left `qty: null` +
flagged rather than estimated).

**Content spot-check performed before reporting this batch done:** all 173
Review rows across the batch's 5 flagged companies read individually or by
systematic sampling (Noon UAE's 108 rows broken down: 8 genuine consumable
flags, 8 genuine medical flags, 92 genuine null-qty flags — sampled all 92
sub-category names, all real aquarium/reptile/grooming/housing equipment,
no nav/marketing leakage). Reverse-checked every Output row across SR
161-180 containing "toy"/"bowl"/"food"/"treat"/"chew" — every equipment row
(Dog/Cat Bowls, Pet Toys, Bowls & Feeders, etc.) correctly stayed unflagged;
the two bare "Food" hits were grouping-row headers, not data. Zero false
positives or wrongly-suppressed rows found.

### Batch 10 (SR 181-200) — Singapore, Japan, Australia continued, USA/Canada
mass retailers — dispatched, merged and verified 2026-09-02

20 workers, including several of the largest mass-market retailers in the
roster: Costco, Sam's Club, Walmart, The Home Depot, Etsy. All 5 have real,
substantial Pet departments. IKEA Japan (SR 184) is this roster's 4th IKEA
market — Cats=9/Dogs=9, again genuinely distinct from all 3 other markets.

**A third occurrence of the `CONSUMABLE_FLAG` over-match bug was caught and
fixed:** "Pet Food Scoops" (JCPenney, batch 9's SR 195) got force-flagged as
a consumable, but `rules/pet-care.md` §hygiene explicitly lists
"Litter Boxes/Trays/Scoops/Mats" as Tier 1 hygiene equipment — a scoop is a
utensil, not the food itself, same failure class as "Food Bowls" (batch 1-2)
and "Chew Toys" (batch 7). Fixed by adding `scoops?` to
`FEEDING_EQUIPMENT_OVERRIDE` in both `merge_pet_care.py` and
`verify_pet_care.py`. Verified against known-good/known-bad cases before
re-running; review rows dropped from 284 to 283, only the one false positive
removed. **This regex pair has now needed a real bugfix three times** —
treat it as permanently high-risk on every future edit, not "fixed now."

Two workers stalled mid-task without writing output again (SR 199 Etsy US,
resumed once and completed cleanly) — same recovery pattern as batches 7 and
9, resumed via `SendMessage` rather than redispatched.

The livestock/farm-animal boundary question (first surfaced at Castorama
France in batch 7) recurred at Walmart (Cattle, Chicken Coops), The Home
Depot (Chicken Coops, Tanks/Waterers/Feeders, Chicken Runs, Horse Supplies),
and Sam's Club — all correctly flagged for review rather than each worker
inventing its own answer, consistent treatment across companies.

Absent (confirmed via real investigation): Castlery Singapore, Francfranc
Japan, Structube, Simons Maison, Sur La Table (batch 9's carry-over company),
Indigo Home — each proven via full nav/sitemap enumeration, not default
site-search. Found with real Pet Care: Freedom Australia, HipVan, House
Australia, IKEA Japan, Country Road Home, Myer Home, Costco US, Sam's Club,
Quince Home, Walmart US, Kohl's Home, The Home Depot, Etsy US, JCPenney Home
(carried over from batch 9's notes) — a notably higher hit rate than most
prior batches, driven by the mass-retailer cluster (Costco/Sam's
Club/Walmart/Home Depot/Etsy all have real, substantial Pet departments).

**Content spot-check performed before reporting this batch done:** all 283
Review rows checked — Walmart's 81 broken down by flag type (34 consumable,
4 medical, 3 farm/livestock, 5 mixed-species-hub, 35 null-qty equipment, all
genuine), remaining companies' 40 rows read individually. Reverse-checked
every Output row across SR 181-200 containing
toy/bowl/food/treat/chew/scoop/feeder — all equipment rows correctly stayed
unflagged; the "Dog Food"/"Cat Food"/etc. hits with no flag turned out to be
grouping-row headers (qty/link null by design), not leaf data, confirmed by
inspection. Zero new false positives beyond the one bug already fixed above.

### Batch 11 (SR 201-220) — Wayfair-family + boutique furniture/lighting,
Canada, India — dispatched, merged and verified 2026-09-02

20 workers: 3 Wayfair-family siblings (AllModern, Birch Lane, Joss & Main —
each independently re-derived, not assumed shared with Wayfair itself or
each other), a cluster of lighting-only specialists (Lamps Plus, Lumens,
Shades of Light, 2Modern, Lightology, Hudson Valley Lighting, Visual
Comfort), and this roster's first 3 India-market companies (Cello World,
Milton, Pepperfry).

Design Within Reach (SR 215) is blocked for a new reason — an explicit
`User-agent: ClaudeBot / Disallow: /` in robots.txt, correctly halted before
any fetch attempt per the hard rule, distinct from every other block in this
project so far (which were all WAF/Cloudflare-type, not a named
robots.txt directive). That's now 7 blocked companies total.

No false-absence traps or classifier bugs this batch — clean run. Notably
several PET-plastic-material false positives were correctly filtered (Cello
World's `pet-container`/`pet-storage-jar`, Milton's `pet-pp-bottles`/
`pet-jars`) — the recurring "PET the polymer" vs "pet the animal" ambiguity
handled correctly every time it's come up across this project.

Absent (confirmed via real investigation): Birch Lane, Joss & Main, EQ3,
Bouclair, Saks Home, Shades of Light, Grandin Road, 2Modern, Design Public,
Lightology, Terrain, Hudson Valley Lighting, Visual Comfort, Cello World,
Milton — 15 companies, the highest absent-count batch yet (lighting-only
retailers structurally don't carry pet products). Two access escalations to
a real Claude-in-Chrome session both cleared cleanly with no CAPTCHA solved
(Saks Home's DataDome challenge, Joss & Main's PerimeterX block).

Found: AllModern (5 rows, careful reconciliation catching a stale/orphaned
duplicate sitemap entry), Lamps Plus (1 row, qty unverifiable after an
Akamai block — flagged not guessed), Lumens (1 row, qty=15 cross-verified
via 4 independent signals), Pepperfry (4 rows, found via a nested sitemap
invisible to the top-level index).

**Content spot-check performed before reporting this batch done:** the one
new Review row (Lamps Plus qty-unverified) read and confirmed genuine.
Reverse-checked every Output row across SR 201-220 containing
toy/bowl/food/treat/chew/scoop/feeder/jar — both hits (AllModern's "Pet
Bowls + Feeders" and "Pet Food Storage + Treat Jars") correctly stayed
unflagged. Zero new false positives, zero regressions from the batch 10 fix.

### Batch 12 (SR 221-240) — all India-market companies — dispatched, merged
and verified 2026-09-02

20 workers, the roster's first all-single-country batch: 5 large
marketplaces/general retailers (Flipkart, Myntra, AJIO, Westside, Fabindia)
plus 3 sibling companies (IKEA India — 5th independently-verified IKEA
market, Cats=5/Dogs=6; H&M Home India — 3rd H&M Home market; Pottery Barn
India, independent of the US original).

Two very large finds: **Flipkart** (161 rows across 9 species groups — Birds,
Cats, Dogs, Fish, Grooming, Health, Horse, Large Animals, Small Animals) —
status "partial", every qty correctly left null because the site's own
product-count facet was proven to fluctuate between fetches on a 3x re-fetch
test (9475/9474/9422 for an identical URL), not certifiable as exact per the
qty/evidence rule. **Myntra Home** (35 rows, 1685 products across 34
categories) — the worker caught and avoided a real trap: short "SEO" URL
slugs like `/pet-bed` return plausible-looking pages whose product counts
don't match the real in-category facet (82 vs. the verified 1 for "Pet
Beds") — these are catalog-wide search landing pages, not real categories,
and were correctly excluded as a count source.

Several sharp exclusion calls this batch, each independently investigated
rather than trusting a promising-sounding category name: Fabindia's "Dog
Toy" turned out to be a dog-*shaped* plush toy for children (pet-themed, not
pet-use); Westside Home's "Pet Accessories & Essentials" collection turned
out to be entirely bath towels/laundry organizers despite deceptive SEO
metadata; WoodenStreet's "pet houses" was unsubstantiated marketing prose
with no real category/listing behind it; AJIO's 5 "pet"-named collections
were all non-discriminating catch-alls or off-nav orphan pages, correctly
excluded.

Absent (confirmed via real investigation): AJIO Home, FOS Lighting, Nestasia,
Westside Home, WoodenStreet, @home by Nilkamal, Clay Craft India, Ankur
Lighting, Borosil, Fabindia, Jainsons Lights, Nykaa Fashion Home (reached via
Claude-in-Chrome after Akamai blocked automated tiers, correctly avoided the
now-banned `translate.goog` route the prior pass had used), Pottery Barn
India, Pure Home + Living, H&M Home India — 15 companies.

Found: Flipkart, Myntra Home, IKEA India, Urban Ladder (1 row, Pet Beds
qty=18) — 4 companies with real Pet Care this batch.

**Content spot-check performed before reporting this batch done:** all 152
new Review rows (Flipkart's) categorized and sampled — 23 consumable, 4
medical, 125 null-qty equipment, all genuine, no nav/marketing leakage in
the equipment sample. Reverse-checked every Output row across SR 221-240
containing toy/bowl/food/treat/chew/scoop/feeder/jar — all 3 hits (Myntra's
Pet Toys/Bowls/Feeders) correctly stayed unflagged. Zero new false
positives, zero regressions.

### Batch 13 (SR 241-260) — all India-market companies — dispatched, merged
and verified 2026-09-02

20 workers, second all-India batch. Two sibling companies: West Elm India
(independently absent, distinct conclusion from West Elm US's real Pet Care
finding) and Zara Home India (its 6th market in this roster) — the latter
surfaced a genuinely new edge case (see below).

**Zara Home India (SR 242) — a new kind of ambiguity, correctly flagged
rather than resolved.** The India storefront (served through Zara Home's
shared "ww" Rest-of-World catalogue) has zero discoverable path to Pet
Care through any real navigation, sitemap, or breadcrumb — but the worker
found real, live pet products (22 items: harnesses, bandanas, beds,
blankets, toys) by reusing a categoryId harvested from the UAE market's own
nav against the India-served catalogue's grid API, which unexpectedly
returned content. Individual product pages are genuinely live (200). This
is a new question this project hasn't hit before: does an API-reachable-
but-unnavigable category count as "present" on a storefront? The worker
correctly recorded it with qty=22 and a MANUAL REVIEW flag rather than
picking an answer — this is a policy question for a human, alongside the
existing consumable/medical/livestock ones.

**Meesho (SR 245) — a large marketplace with a platform-wide qty
limitation.** 21 rows (1 group + 20 leaves: Collars, Clothes/Grooming,
Food/Treats, Aquarium, Toys, Bowls, Beds/Furniture, Houses/Kennels, Litter,
Carriers, Training, Health — per-species splits for Dog/Cat). Every qty is
null because the site's SSR payload always ships `totalProductsCount:0`
(real counts load via client-side XHR, and the facet/search endpoints are
robots.txt-disallowed) — same limitation the prior Home-Decor pass on this
site already documented. A WAF block after ~2 successful fetches meant
several sub-category titles are slug-derived rather than independently
confirmed — correctly flagged as such rather than presented with false
confidence. Two possible-overlap pairs (Clothes & Grooming vs. per-species
Apparel; Health Supplies for Pets vs. Pet Health) flagged for merge-time
adjudication rather than silently deduped or silently kept as duplicates.

Absent (confirmed via real investigation): Tata CLiQ Luxury Home, Home
Centre India, HomeStop, Wonderchef, Address Home, Chumbak, Ikiru, Mason
Home, The Decor Kart, Whispering Homes, ellementry, West Elm India, The
White Teak Company, The Bombay Store, Beruru, Good Earth, India Circus (one
pet category found but corroborated as genuinely zero-product/delisted) —
17 companies.

Found: Zara Home India (1 row, flagged reachability ambiguity), Meesho (21
rows, all null-qty per platform limitation), Freedom Tree (1 row, Dog Toys
qty=13, verified via a full 1933-product catalog sweep).

**Content spot-check performed before reporting this batch done:** both
new-Review companies' rows read individually (21 total) — all genuine
judgment calls (unreachability, slug-unconfirmed titles, qty-unattainable,
overlap-for-adjudication), zero regex false positives. Reverse-checked
every Output row across SR 241-260 containing
toy/bowl/food/treat/chew/scoop/feeder/jar — the one hit (Freedom Tree's
"Dog Toys") correctly stayed unflagged.

### Batch 14 (SR 261-280) — remaining India + new UK cluster — dispatched,
merged and verified 2026-09-02

20 workers: 10 remaining India companies plus a new UK cluster (10
companies), including Wayfair UK (a Wayfair-family sibling that, unlike
AllModern/Birch Lane/Joss & Main, turned out to have a real, substantial
Pets department — confirming the "always re-verify, never assume sibling
parity" discipline pays off in both directions).

**A consistency gap was caught and fixed:** Wayfair UK's "Chicken Coops,
Chicken Runs & Houses" (qty 281) and "Chicken Coop Accessories" (qty 302)
were merged unflagged, but the identical livestock/farm-animal boundary
question had been consistently flagged at Castorama France, Walmart, Home
Depot, and Sam's Club in earlier batches. This worker simply didn't apply
that flag — not a regex bug, a worker-judgment inconsistency caught during
the routine content spot-check. Fixed by editing `pc272.json` directly to
add the `FARM ANIMAL / LIVESTOCK` flag to both rows (citing the 4 prior
companies as precedent) and re-merging. Review rows went from 492 to 494;
re-verified clean. Worth remembering: the "flag consistently, never let one
worker decide" discipline needs an active check at merge time too, not just
trust that every worker independently arrives at the same judgment call.

The Range (SR 271) was the largest UK find and the most heavily flagged:
119 rows, 31 of them on Review (mostly the per-species Food/Treats and
Healthcare/Supplements split, all genuine consumable/medical flags per the
two existing open policy gaps) — sampled the full 31-row set individually,
zero false positives.

Absent (confirmed via real investigation): Objectry, Oorjaa, Sarita Handa,
The Purple Turtles, Kapoor E-Illuminations, Jaypore, The Artment, Orange
Tree, SPIN, ProCook, Liberty London Home, La Redoute Interiors UK (the LRI
brand-filter entity specifically — the general site does carry third-party
pet brands), The Conran Shop — 13 companies.

Found: Lakeland (2 rows, careful product-level filtering dropped a
misfiled human-food item and 4 non-pet cleaning products from mixed
collections), Nicobar (1 row, Dog Sweaters qty=3, cross-verified via 3
independent URLs), Argos Home (25 rows across Dogs/Cats/Fish&SmallPets,
wild-bird garden supplies correctly excluded), Harrods Home (6 rows, a
duplicate-listing merge and a mistagged-SKU flag both caught), Selfridges
Home (1 row, qty=267), The Range (119 rows, the batch's largest find),
Wayfair UK (44 rows, including the chicken-coop fix above).

**Content spot-check performed before reporting this batch done:** all 35
new Review rows across the 4 flagged companies read (Lakeland ×1, Argos
×1, Harrods ×2, The Range's full 31-row set) — all genuine, zero false
positives. Reverse-checked every Output row across SR 261-280 containing
toy/bowl/food/treat/chew/scoop/feeder/jar — all equipment rows correctly
unflagged, "Food & Treats" hits were grouping-row headers not leaf data
(same pattern as Noon UAE/Walmart in earlier batches). The one real issue
found (Wayfair UK's chicken-coop flag gap) is fixed above.

### Final batch (SR 281-286) — dispatched, merged and verified 2026-09-02
— PROJECT COMPLETE, 286/286

6 companies, the last of the roster. Notable:

- **SR 165 = SR 286, both "Noon UAE"** — the master roster lists this
  company twice (identical name/brand_site/URL), the exact same duplicate
  already resolved for this exact company in the sibling Furniture project
  (`furniture_json_archive/qa_notes.md`, user decision 2026-08-24: keep
  SR 165 canonical, clear SR 286). Initially applied the identical
  resolution here without re-dispatching a worker: SR 165 (batch 9, 175
  rows) stayed canonical, SR 286 was written directly as `rows: []` with
  notes explaining why. **Updated 2026-09-02 per explicit user instruction**
  ("sr 286 and 165 are same companies so just removed one of them if
  exist in file"): SR 286 is now dropped entirely, not just cleared — it
  no longer appears in the Output, Processing Ledger, or Review sheets at
  all. Implemented as a permanent, idempotent fix in `merge_pet_care.py`
  (`KNOWN_ROSTER_DUPLICATES = {286: 165}`, filtered out of `blocks` before
  the ledger is built) and `verify_pet_care.py` (ledger-count assert
  changed from a hardcoded 286 to `286 - len(KNOWN_ROSTER_DUPLICATES)` =
  285, plus a new assert that no known-duplicate SR is present in the
  ledger) — so this stays fixed on every future re-merge, not just this
  one. **The Processing Ledger is now intentionally 285 rows, not 286** —
  this is expected and correct, not a regression; do not "fix" it back to
  286 without checking this note first.
- **4 of the 6 companies hit an explicit Claude-specific robots.txt
  disallow** — home24 Germany (3rd time this exact domain has hit this in
  this project), Made in Design (confirmed unchanged from the prior
  Home-Decor pass), El Corte Inglés Home, and Amazon UAE (4 separate named
  Claude directives). All correctly stopped before any extraction attempt,
  per the hard rule — no bypass considered. That brings the project total
  to **11 blocked companies** (was 7 after batch 14; +4 here, no new
  Cloudflare/WAF-type blocks this batch, all robots.txt policy stops).
- **Home Box UAE** (1 real find, 3 rows: Pets group + Pet Accessories 13 +
  Pet Costumes 4) reached via a legitimate Claude-in-Chrome session after
  Cloudflare blocked tiers 1-2 — cleared automatically, no CAPTCHA solved.

**Content spot-check performed before reporting the project done:** zero
new Review rows this batch (Home Box UAE's 3 rows all had clean exact
counts, no flags needed) — reverse-checked anyway for
toy/bowl/food/treat/chew/scoop/feeder/jar overlaps, none found. Clean
close to the project.

## PROJECT COMPLETE — final numbers (2026-09-02, updated after the SR 286
## duplicate-removal fix)

All 286 roster entries processed (285 unique companies — SR 286 is a
confirmed duplicate of SR 165, dropped entirely per explicit user
instruction, see the note above). `Pet_Care.xlsx`:
- **1546 data rows** (1248 leaf + 186 grouping + separators)
- **112 companies with real Pet Care**
- **162 confirmed absent** (each via real nav/sitemap/catalog investigation,
  never a bare site-search null result)
- **11 blocked**: McGee & Co., Leroy Merlin France, BHV Marais Maison, PAN
  Emirates UAE, Tavola UAE, Dille & Kamille, Design Within Reach, home24
  Germany, Made in Design, El Corte Inglés Home, Amazon UAE
- **494 review rows**, every one content-spot-checked against
  `rules/pet-care.md`'s own worked examples across all 15 batches — zero
  known false positives remaining (3 real `CONSUMABLE_FLAG` bugs were
  found and fixed along the way: "Food Bowls" batch 1-2, "Chew Toys"
  batch 7, "Pet Food Scoops" batch 10; one consistency gap was found and
  fixed: Wayfair UK's chicken-coop livestock flag, batch 14)
- **Zero cross-company duplicate URLs** (strict check, added mid-project
  at the user's request, passing on every merge since)
- **Processing Ledger reconciles to exactly 285** (286 master-roster
  entries minus the 1 confirmed duplicate, SR 286) — this is the correct,
  intentional total after the fix above, not 286

Three open policy questions remain for a human decision, never resolved by
this pipeline itself (flagged consistently wherever they appeared):
1. Pet food/consumables — no include/exclude policy (rules §11)
2. Medical/veterinary categories — no inclusion rule (rules §12)
3. Livestock/farm-animal boundary — surfaced at Castorama France, Walmart,
   Home Depot, Sam's Club, Wayfair UK — no policy exists
4. (New, singular case) Zara Home India's API-reachable-but-unnavigable
   category — does that count as "present" on a storefront?

See `SKILL.md` §4 for the adjudication log. No further batches to
dispatch — this file's per-batch structure ends here.

### Post-completion fix: SR 111 fonQ missing links (2026-09-02)

User spotted 3 leaf rows with `qty` but no `link`: Pet Cushions (7), Pet
Baskets/Beds (2), Feeding & Drinking Bowls (11). Root cause (already
documented in the worker's original evidence/flag, not a merge bug):
fonQ's `?type_product=` filter parameter isn't applied server-side, so
these 3 facet values have no separately crawlable URL — the worker
correctly derived qty from an embedded exhaustive facet JSON on the
parent category page (`fonq.nl/collections/dierenmeubels-accessoires`,
verified the 4 facet values there sum exactly to the page's own
`nbResults=32`) and left `link` null rather than fabricate one.

At the user's request, backfilled the parent category page's own URL as
a fallback link for all 3 rows (edited `pc111.json` directly, re-ran
merge+verify). The flag text was updated to make clear it's an
*unfiltered parent-page* link, not the exact filtered view. Two of the
three rows also picked up the standard "shares a link with another row
in this company" flag as a side effect (all 3 now share the same parent
URL) — this is correct/expected, not a bug, since they genuinely do share
that link and it's already explained by the primary flag. Re-verified
clean afterward: STRICT cross-company duplicate check still 0 (this is a
same-company share, a different and non-fatal check), ledger still 285,
review rows still 494 (only content changed, not count).

If this pattern recurs elsewhere (a qty-verified facet value with no
crawlable filter URL), the same fallback — link to the parent page,
flag it explicitly as unfiltered — is the reusable resolution.

**Update same day:** the user then manually edited the live `Pet_Care.xlsx`
directly, replacing the 3 parent-page fallback links with the real
`?type_product=<slug>` filtered URLs (using the exact slugs already
present in the worker's own facet-JSON evidence: `dierenkussen`,
`dierenmand`, `voer-en-of-drinkbak`) and asked for a check. A fresh HTTP
fetch of those URLs showed the site's own embedded facet JSON marking the
corresponding facet value `"selected":false` even with the query param
present — i.e. a plain HTTP GET does not show the filter applied
server-side, matching the original worker's finding exactly. Reported
this to the user with the evidence; **the user confirmed the URLs work
correctly when opened in an actual browser** (client-side JS applies the
query param on page load, which a raw fetch can't observe) and asked to
keep them as-is. Deferring to the user's live-browser confirmation over
the raw-fetch check.

`pc111.json` was updated to match the user's chosen URLs (link + flag
text revised to note the browser-confirmed-vs-raw-fetch discrepancy) so
the JSON archive stays in sync with the live workbook — the live
`Pet_Care.xlsx` was NOT re-merged immediately after this JSON edit alone,
to avoid rewriting the whole workbook and risking any other manual edits
the user may have made outside this conversation's visibility. (It WAS
re-merged shortly after, together with the SR 124 Denby fix below — see
that entry for confirmation both fixes survived the same re-merge.)

### Post-completion fix: SR 124 Denby now closed/in administration
(2026-09-02)

User reported the SR 124 Denby "Pet Bowls" URL (qty=18, extracted earlier
the same session) "showing closed" when opened in a browser. Verified via
both a plain HTTP fetch (raw HTML contains "administrat[ion]" text at
byte offset ~173835) and a real Claude-in-Chrome browser session
(screenshot confirmed a literal "CLOSED" graphic plus a full legal
notice) — denbypottery.com now serves this notice sitewide, not just on
the pet-bowls collection page. Root cause: Denby Retail Limited and
related Denby Group entities entered administration (UK insolvency) on
31 March 2026; site operation transferred to a new entity, Denby Home
Pottery Limited, on 4 June 2026. This is a genuine business-closure
event, not a technical/bot block, a caching artifact, or an access-tier
issue — no product listing, navigation, or storefront content is
currently reachable on this domain by any means.

Corrected `pc124.json`: `status` changed from `"ok"` to `"blocked"`,
`rows` cleared to `[]`, the original qty=18 finding preserved in `notes`
for historical reference only (explicitly marked "must NOT be treated as
current"), with a pointer that if the new owner relaunches the storefront
this SR should be **re-extracted fresh**, not reverted to the old
finding (a new operator may carry a completely different catalog).
Re-merged (together with the SR 111 fonQ fix above — both confirmed
present after this merge) and re-verified clean: ledger still 285, zero
cross-company duplicate URLs, review rows still 494. Company counts
shifted correctly: PET CARE FOUND 112→111, BLOCKED 11→12.

**Lesson for any future re-run of this pipeline (or a sibling category
project sharing this roster):** a company's site can change state
*during* a session, not just between sessions — the original SR 124
extraction and this correction happened the same day. A clean, confident
extraction at time T is not a permanent guarantee; if a user reports a
link behaving unexpectedly, always re-check live rather than assuming the
archived JSON is still accurate, even for very recently extracted rows.
