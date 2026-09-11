# PET CARE EXTRACTION — WORKER BRIEF

You are one of several parallel extraction workers. Read this whole brief before
starting. You are assigned **exactly one company**. Your job: find that
company's **PET CARE** categories/sub-categories, capture the deepest valid
listing (PLP) URLs and the site's own exact product counts, and write one JSON
file.

**Scratchpad (your working dir — do ALL file work here):**
`C:\Users\GYANEN~1\AppData\Local\Temp\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\0775ef29-9010-4d45-a1a8-ce57dffe4abd\scratchpad`

**The scratchpad is shared with ~19 other workers running at the same time.**
Prefix EVERY working file and directory you create with `w<SR>_` (e.g.
`w42_tree.py`, `w42_cache/`). The ONLY unprefixed file you write is your result
`pc<SR>.json`.

**NEVER touch the user's project files** in
`C:\Users\GyanendraVishwakarma\Web Research Agent` (the `.xlsx`/`.xlsm`
workbooks). Eight files there are off-limits — Kitchen_and_Dining.xlsx,
Lighting.xlsx, Wall_Decor.xlsx, Decorative_Home_Accessories.xlsx,
Furniture.xlsx, Textile.xlsx, Storage.xlsx, `Final_Company_List (1).xlsx` —
writing anywhere in that folder is forbidden. The orchestrator does the merge.

**Work synchronously, in the foreground, in this same turn.** Do not launch a
background job and end your turn "waiting to be notified" — the orchestrator
cannot see that and it will silently look like a stall. Finish the company and
write the JSON before you stop.

---

## 0. READ YOUR COMPANY'S ACCESS NOTES FIRST — THIS SAVES YOU AN HOUR

`notes/<SR>.md` in the scratchpad contains the **prior Home-Decor/Furniture
pass** for your exact company: which route reached the site, whether it was
blocked and by what, the URL shape, and category URLs that were **verified
working**. Read it before your first fetch.

**Read those notes for SITE STRUCTURE and ACCESS ROUTE, not for Pet Care
content.** The prior passes deliberately excluded Pet Care (they were doing
Furniture/Lighting/Wall Decor/Decorative/Kitchen & Dining/Textile/Storage), so
an empty or absent Pet Care mention there means nothing about whether Pet Care
exists on the site. What's valuable: the URL shape, the nav/sitemap structure,
which access route worked (proxy pins, IPv6 routes, whatever got past a WAF),
and site-specific traps.

If a note says `status=failed` or `blocked`, still try — access conditions
change, and tier 1/2 below may succeed where an older pass didn't. But don't
burn the whole session on one site; if it's genuinely unreachable, mark it
`blocked` with a precise reason.

---

## 1. ACCESS TIER — TRY IN THIS ORDER, STOP AT THE FIRST THAT WORKS

1. **Direct HTTP fetch + HTML parsing.** Plain request or `curl_cffi`/`requests`
   (Bash/Python) are fine. Pull SSR HTML, embedded JSON (`__NEXT_DATA__` /
   `__NUXT__` / `__APOLLO_STATE__`), sitemaps, robots.txt, category/product-count
   APIs. Parse locally; don't re-fetch what you already have.
2. **Playwright/CDP** when the page is client-rendered and tier 1 can't see the
   real DOM/data.
3. **Claude-in-Chrome (`mcp__claude-in-chrome__*`)** only as a last resort —
   genuine uncertainty about category structure, an anti-bot wall that defeats
   1 and 2, or something needing visual/interactive judgement.

No r.jina.ai, translate.goog, web.archive.org, or webcache as a substitute for
reaching the site directly.

**Check `robots.txt` for a Claude-specific disallow before Claude-in-Chrome
use.** A named `anthropic-ai` / `ClaudeBot` / `Claude-Web` / `Claude-User` /
`Claude-SearchBot` with a full-site `Disallow: /` means STOP and mark the
company blocked, even if the WAF is trivially bypassable. Some sites name
Claude and then `Allow: /` — that's explicit permission, not a block.

**The FIRST block stops that host, not the third.** A block is 403, DataDome,
Akamai, Cloudflare, CAPTCHA, "Access Denied", rate-limiting, or repeated load
failure. On the first one: stop requesting that host, use what you already
have, process it locally, and report precisely what's missing. `sleep` /
`time.sleep()` / backoff loops / polling a blocked host are banned. Pacing
requests before trouble (~1 per 5-8s) is fine.

---

## 2. THE ONE RULE THAT MATTERS — QTY

**`qty` must be the EXACT number of products the website itself reports for
that sub-category URL.**

- NEVER estimate, approximate, round, infer, aggregate, average, sum children,
  or copy a qty from a parent or sibling category.
- If you cannot verify the exact number, set `"qty": null` and
  `"flag": "MANUAL REVIEW: <specific reason>"`. A null is a **correct** answer.
  A made-up number is a project-destroying error.
- Every row with a qty must carry an `evidence` string: the literal text or
  JSON path that produced it (e.g. `"listing header 'Showing 1-24 of 186'"`,
  or `"__NEXT_DATA__:props.pageProps.search.numFound=186"`). A qty without
  evidence is nulled at merge.
- Storefront count APIs are often inflated (Shopify `products_count`, Magento
  `categoryList.product_count`). Prefer the rendered "N items" header unless
  you've confirmed the structured count is exact.

Accuracy beats coverage. Beats speed. Always.

---

## 3. WHAT COUNTS AS PET CARE — THE BOUNDARY

Priority: **PRIMARY PET PRODUCT TYPE > PET PURPOSE > WEBSITE CATEGORY >
ROOM/CONTEXT/MARKETING NAME.**

In scope when products are primarily for: feeding, grooming, cleaning
pets/pet areas, housing, transporting, walking, training, entertaining/
enriching, or otherwise directly supporting pet ownership/care. A pet-related
keyword alone is never enough.

### Tier 1 — decisive signal, include

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
- **Housing & containment** — Pet Housing, Pet/Dog Crates, Pet/Dog Kennels,
  Pet Cages, Pet Pens/Playpens, Pet Gates, Pet Enclosures, Pet Shelters.
- **Training** — Pet/Dog Training, Training Pads/Clickers, Pet/Dog Training
  Accessories.

### Tier 2 — contextual, only when Tier 1 doesn't already claim it

Generic branch names (`Accessories`, `Essentials`, `Home`, `Outdoor`, `Care`,
`Lifestyle`) under a **clearly pet-specific parent** — e.g. `Pets >
Accessories`, `Dogs > Accessories`, `Cats > Essentials`. Verify the parent
hierarchy actually establishes the pet-specific purpose; don't infer it from
the leaf name alone.

### EXCLUDE

- **Generic product types are not auto-included.** `Beds, Blankets, Cushions,
  Mats, Baskets, Storage, Containers, Boxes, Toys, Accessories, Houses,
  Furniture, Clothing` need a pet-specific parent branch. `Home > Blankets` and
  `Furniture > Beds` are NOT Pet Care. `Pets > Blankets` / `Pets > Beds` ARE.
- **Pet-themed ≠ Pet Care.** Dog-print cushions, cat-illustration mugs,
  animal-pattern rugs, pet lover gifts, dog/cat-themed wall art or stationery
  — these are themed around animals, not made for them. Exclude.
- **Pet-owner products** (T-shirts, mugs, jewellery for the human) — exclude
  unless the PLP genuinely sits inside a real Pet Care branch.
- **Generic storage/cleaning stay in their own category.** Only explicitly
  pet-specific storage/hygiene counts (Pet Food Storage, Cat Litter, Pet Waste
  Bags). `Storage Boxes`, `Baskets`, `Cleaning`, `Laundry`, `Bathroom` are not
  Pet Care by default.
- **Navigation/marketing pages are never a category**, even inside a Pet
  section: Collections, Featured, Shop All, View All, Browse All, Explore,
  Discover, New Arrivals, Best Sellers, Sale, Offers, Clearance, Gifts, Gift
  Guides, Blogs, Editorial, Lookbooks, Landing Pages.
- **Don't steal from other categories.** If Furniture, Storage, Bathroom,
  Kitchen & Dining, Lighting, Wall Decor, or Textiles is the clearly stronger
  owner, leave the record there.

### Flag, don't decide — two open policy gaps

- **Pet food / consumables** — no include/exclude policy exists yet. If you
  find a genuine pet-food/treat/supplement category, still record it (don't
  silently drop it) with `"flag": "MANUAL REVIEW: PET CONSUMABLE - <what>"`.
- **Medical / veterinary categories** (medicines, prescription products,
  clinical treatments, vet equipment) — no inclusion rule exists yet. Record
  with `"flag": "MANUAL REVIEW: PET MEDICAL / VETERINARY CATEGORY - <what>"`.

Don't invent a policy for either. The merge step also force-flags anything
that looks like either case, so it's not fatal if you miss one — but flagging
it yourself means better `evidence`/context in the flag text.

---

## 4. GROUPING VS. LEAF, OVERLAPS, ABSENCE PROOF

- A genuine parent node with real child categories (e.g. `Pet Care > Feeding /
  Grooming / Beds / Toys / Walking`) is a **grouping row**: `is_group: true`,
  `qty: null`, `link: null`. Its children are the leaves, immediately
  following in reading order. Never double-count parent and child quantities.
- Same URL, or same underlying listing with identical count/facet breakdown
  from two nav nodes → one row; explain the merge in `notes`. Genuinely
  different PLPs → keep both.
- **A zero-result site search is not proof of absence.** Some sites return
  default/non-discriminating results for every query. Check real navigation,
  mega menu, category tree, and sitemap before concluding Pet Care is absent.
  Record what you checked in `notes`.
- Drop zero-product categories (don't emit a row for them).
- This is PLP/category extraction, **not PDP extraction**. Don't crawl
  individual product pages for titles/prices/SKU/materials/dimensions. Open a
  PDP only to resolve a genuine category ambiguity.

---

## 5. OUTPUT CONTRACT — write `pc<SR>.json` in the scratchpad root

```json
{
  "status": "ok",              // "ok" | "partial" | "blocked" | "failed"
  "failure_reason": null,      // required if status is "partial" or "blocked"
  "notes": "free text: what you checked, overlap decisions, absence proof",
  "rows": [
    {
      "category": "Pet Care",
      "sub_category": "Dog Beds",
      "qty": 186,
      "link": "https://example.com/dog-beds",
      "is_group": false,
      "evidence": "listing header 'Showing 1-24 of 186'",
      "flag": null
    },
    {
      "category": "Pet Care",
      "sub_category": "Feeding",
      "qty": null,
      "link": null,
      "is_group": true,
      "evidence": null,
      "flag": null
    }
  ]
}
```

Emit rows in reading order, each parent immediately followed by its children.
`category` is the top-level Pet Care grouping as the site (or your own
sensible grouping) names it; `sub_category` is the actual leaf/branch name.

Write the file as soon as the company is done. Do not batch multiple
companies into one file, and do not wait to be asked before writing it.
