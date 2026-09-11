# Pet Care — category boundary rules

Load with `../../home-decor-extraction/rules/_decor-extraction-core.md` (see
`../SKILL.md` §1). This file defines only the Pet Care category boundary and
classification rules — it does not restate the shared browser/navigation/PLP/
qty/checkpoint/merge/verify engine, and it must not be turned into PDP
extraction: don't crawl PDPs for titles, prices, SKU, materials, dimensions, or
descriptions. A PDP may be opened only to resolve a genuine category ambiguity.

---

## 1. TASK

Extract real Pet Care product-listing/category pages. A valid row:

1. is a genuine PLP/category page,
2. belongs to Pet Care per the rules below,
3. lists products,
4. has a valid category/sub-category name,
5. has its own PLP URL,
6. has an exact site-reported qty where available (shared qty rules).

`WEBSITE → real navigation → Pet Care category tree → Pet Care sub-categories →
valid PLPs → exact qty+evidence → category/sub-category/link → JSON → merge/
reconciliation.`

---

## 2. THE BOUNDARY

Priority order: **primary pet product type > pet purpose > website category >
room/context/marketing name.**

In scope when the products are primarily for: feeding, grooming, cleaning
pets/pet areas, housing, transporting, walking, training, entertaining/
enriching, or otherwise directly supporting pet ownership/care. A pet-related
keyword alone is never sufficient.

---

## 3. TIER 1 — `PET_STRICT` (decisive signal, classify as Pet Care)

A genuine PLP explicitly headed/categorized as one of these is Pet Care:

- **Feeding & drinking** — Pet Feeding, Pet/Dog/Cat Bowls, Pet/Dog/Cat Feeders,
  Automatic Pet Feeders, Pet Water Fountains, Pet Feeding Mats, Pet Food/Treat
  Storage.
- **Beds & sleeping** — Pet/Dog/Cat/Puppy Beds, Pet Mattresses, Pet Cushions,
  Pet Sleeping Mats, Pet Blankets, Dog/Cat/Pet Houses, Pet Tents, Pet Hammocks.
- **Grooming** — Pet/Dog/Cat Grooming, Pet/Dog/Cat Brushes, Pet Combs,
  Deshedding, Pet Nail Care/Clippers, Pet Grooming Kits/Accessories.
- **Hygiene & waste** — Pet Hygiene, Pet/Dog Waste, Cat Litter, Litter
  Boxes/Trays/Scoops/Mats, Pet/Dog Waste Bags, Puppy Pads, Training Pads, Pet
  Diapers.
- **Toys & enrichment** — Pet/Dog/Cat/Puppy Toys, Chew Toys, Pet Balls, Fetch
  Toys, Interactive/Puzzle/Treat Toys, Cat Scratchers, Scratching Posts, Cat
  Trees, Cat Tunnels, Pet Play.
- **Walking & outdoor** — Pet/Dog/Cat Walking, Pet/Dog/Cat Collars, Pet/Dog
  Leashes, Leads, Dog/Pet Harnesses, Retractable Leashes, Pet Walking
  Accessories, Pet ID Tags.
- **Clothing** — Pet/Dog/Cat Clothing, Pet/Dog Coats, Pet Sweaters, Pet
  Raincoats, Pet Shoes/Boots, Pet Bandanas.
- **Travel & transport** — Pet Travel, Pet/Dog/Cat Carriers, Pet Travel
  Bags/Backpacks/Crates, Pet Car Seats, Pet Travel Accessories.
- **Housing & containment** — Pet Housing, Pet/Dog Crates, Pet/Dog Kennels, Pet
  Cages, Pet Pens/Playpens, Pet Gates, Pet Enclosures, Pet Shelters.
- **Training** — Pet/Dog Training, Training Pads/Clickers, Pet/Dog Training
  Accessories.

---

## 4. TIER 2 — `PET_BROAD` (contextual, use only when Tier 1 doesn't already claim it)

Generic branch names (`Accessories`, `Essentials`, `Home`, `Outdoor`, `Care`,
`Lifestyle`) under a clearly pet-specific parent — e.g. `Pets > Accessories`,
`Dogs > Accessories`, `Cats > Essentials`, `Pet Supplies > Accessories`, `Dog
Essentials > Outdoor`, `Cat Essentials > Home`.

**Do not treat every occurrence of those generic words as Pet Care.** The parent
hierarchy must actually establish the pet-specific purpose — verify it, don't
infer it from the leaf name alone.

---

## 5. GENERIC PRODUCT TYPES ARE NOT AUTO-INCLUDED

`Beds, Blankets, Cushions, Mats, Baskets, Storage, Containers, Boxes, Toys,
Accessories, Houses, Furniture, Clothing` are not Pet Care by default.
`Home > Blankets` is not Pet Care. `Pets > Blankets` may be. `Pets > Beds` is.
The website hierarchy is the evidence — always check it, never pattern-match the
leaf name alone.

---

## 6. PET-THEMED ≠ PET CARE — EXCLUDE

Do not extract categories merely because they carry dog/cat/animal/paw-print
imagery or motifs. Excludes: Dog Print Cushions, Cat Print Rugs, Animal Print
Blankets, Dog-Themed Wall Art, Cat-Themed Mugs, Pet Lover Gifts, Dog
Illustration Posters, Animal Decorative Accessories, Cat-Themed Stationery.
These are products themed around animals, not made for them.

---

## 7. PET-OWNER PRODUCTS — EXCLUDE

Products primarily for the human owner are not Pet Care by default: Dog/Cat
Lover Gifts, Pet Owner T-Shirts, Pet-Themed Mugs/Stationery, Animal Jewellery,
Dog/Cat-Themed Home Decor/Artwork. Exclude unless the PLP genuinely sits inside
a real Pet Care product branch.

---

## 8. BED / FURNITURE BOUNDARY

Include pet-specific resting/housing products when the site clearly markets them
for pets: Dog/Cat/Pet Beds, Pet Crates/Kennels, Cat/Dog Houses, Pet
Playpens/Enclosures. `Furniture > Beds` is **not** Pet Care just because pets
could use it. `Pets > Dog Beds` is. Never let a generic Furniture category get
claimed by Pet Care.

---

## 9. STORAGE BOUNDARY

Generic storage stays Storage. Include only explicitly pet-specific storage:
Pet Food/Treat/Toy/Supply Storage. `Storage Boxes`, `Baskets`, `Cabinets`,
`Shelving`, `General Organizers` are **not** Pet Care merely because they could
hold pet products — the shared project already keeps future/other categories
separate rather than sweeping them in; follow the same principle.

---

## 10. HYGIENE / CLEANING BOUNDARY

Include pet-specific hygiene/waste: Cat Litter, Litter Boxes/Trays, Pet Waste
Bags, Puppy Pads, Pet Diapers, Pet Hygiene. Do not auto-include generic
`Cleaning`, `Household Cleaning`, `Laundry`, `Bathroom`, `General Waste Bins`
unless explicitly pet-specific.

---

## 11. PET FOOD / CONSUMABLES — NO POLICY YET, DO NOT INVENT ONE

Do not override the shared project's existing treatment of consumables, and do
not infer inclusion just because a site places an item under a Pets section.
**No definitive include/exclude policy exists for pet-care consumables.** Flag:
`MANUAL REVIEW: PET CONSUMABLE — <what>` and log it to `qa_notes.md` (see
`../SKILL.md` §4). Do not decide this yourself.

---

## 12. MEDICAL / VETERINARY — NO POLICY YET, DO NOT INVENT ONE

Pet Medicines, Veterinary Products, Prescription Pet Products, Medical Devices,
Clinical Treatments, Veterinary Equipment: **do not auto-absorb.** Flag:
`MANUAL REVIEW: PET MEDICAL / VETERINARY CATEGORY` and log it to `qa_notes.md`.
Do not decide this yourself.

---

## 13. NAVIGATION / MARKETING — EXCLUDE

Never extract as a category, even inside a Pet section: `Collections, Featured,
Shop All, View All, Browse All, Explore, Discover, New Arrivals, Best Sellers,
Sale, Offers, Clearance, Gifts, Gift Guides, Blogs, Editorial, Lookbooks,
Landing Pages`. Same treatment as the shared core's navigation/marketing
exclusions.

---

## 14. GROUPING VS. LEAF

A genuine parent Pet Care node with real child categories (e.g. `Pet Care >
Feeding / Grooming / Beds / Toys / Walking`) is a grouping row per the shared
output contract — name only, `qty: null`, `link: null`, children as leaves
immediately following in reading order. Never double-count parent and child
quantities.

---

## 15. OVERLAPPING PLPs

Same URL, or same underlying listing with identical count/facet breakdown from
two nav nodes → one row, per the shared overlap rule; explain the merge decision
in `notes`. Genuinely different PLPs → keep both.

---

## 16–17. QTY

Use the shared qty method and priority (displayed total → structured/API count
→ full enumeration only when actually reaching the end). Record the exact
number with evidence (`"Showing 1-24 of 186"`, `"186 products"`, `"186 items"`).
Never estimate, round, infer, sum children, or reuse a parent/site-wide number.

Before accepting: confirm the number belongs to that specific PLP, confirm it
varies sensibly between categories, reject a constant site-wide figure, watch
for display caps, don't use a parent total for a child, check pagination
consistency, and account for variant/out-of-stock counting quirks. If exact qty
can't be established: `qty: null`, `flag: MANUAL REVIEW: <reason>` — never
fabricate.

---

## 18. ABSENCE PROOF

A zero-result site search is not proof Pet Care is absent — some sites return
default or non-discriminating search results (see the shared trap in
`../../home-decor-extraction/SKILL.md` §7). Check: real navigation, mega menu,
relevant category tree, sitemap/category structure, relevant English/local-
language slugs, and only then use internal search as supporting evidence. Record
what was checked in `notes`.

---

## 19. LANGUAGE

Normalize non-English categories to English while preserving the site's actual
meaning. Do not invent an English category the site's taxonomy doesn't support;
keep sub-category wording faithful to the source.

---

## 20–21. OUTPUT SHAPE

PLP/category URL only — never substitute individual PDP links. For every valid
leaf: `category, sub_category, qty, link, is_group, evidence, flag` per the
shared output contract (see `../SKILL.md` §5).

---

## 22. ZERO-PRODUCT PLPs

Follow the shared Home Decor workflow's existing behavior (drop zero-product
categories) — do not invent a different rule for this category.

---

## 23. NEVER DUPLICATE THE ENGINE

Browser automation, navigation discovery, PLP detection, qty extraction,
evidence handling, checkpointing, JSON generation, merge, reconciliation,
verification, logging — all shared. This module adds only the Pet Care
classification boundary.

```
SHARED EXTRACTION CORE
        |
        +-- Kitchen & Dining / Lighting / Wall Decor / Decorative Home
        |   Accessories / Furniture / Textile / Storage rules
        |
        +-- Pet Care rules  <- this module
```

---

## 24. DO NOT STEAL FROM OTHER CATEGORIES

Do not absorb records that belong to Furniture, Storage, Bathroom, Kitchen &
Dining, Lighting, Wall Decor, Home Decor, or Textiles unless the site's own
taxonomy **and** the pet-specific purpose both clearly establish Pet Care
ownership. If another category is the stronger owner, leave the record there —
the shared project deliberately preserves boundaries and leaves unassigned
records unassigned rather than guessing.

---

## 25. FINAL DECISION TEST — run for every candidate

1. Is this a real PLP/category page? No → exclude.
2. Does the site's taxonomy clearly place it in a Pet/Pet Care branch? No →
   keep investigating (don't exclude on this alone).
3. Are the products primarily for pets/pet care? No → exclude.
4. Is another existing category the clearly stronger owner? Yes → don't steal
   it.
5. Is this a marketing/navigation page? Yes → exclude.
6. Can exact qty be established? Yes → record with evidence. No → `qty: null` +
   manual-review flag.

---

## 26. STANDARD

For every company: discover the real Pet Care taxonomy, inspect the relevant
PLPs, distinguish grouping nodes from leaves, capture exact qty with evidence,
avoid duplicate listing URLs, exclude marketing/navigation and pet-themed
(non-care) categories, respect other categories' boundaries, record absence only
after real investigation, write the company JSON immediately on completion.

Optimize for correct taxonomy + complete relevant PLP coverage + exact qty +
zero unjustified cross-category leakage — not for row count.
