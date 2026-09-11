# NEW ARRIVALS EXTRACTION — WORKER BRIEF

You are one of several parallel extraction workers. Read this whole brief before
starting. You are assigned **exactly one company**. Your job: find that
company's genuine **New Arrivals-type merchandising PLP(s)** — pages the site
itself uses to list newly added products — capture the deepest valid listing
(PLP) URL(s) and the site's own exact product counts, and write one JSON file.

**Scratchpad (your working dir — do ALL file work here):**
`<SCRATCHPAD_PATH>`

**The scratchpad is shared with other workers running at the same time.**
Prefix EVERY working file and directory you create with `w<SR>_` (e.g.
`w42_tree.py`, `w42_cache/`). The ONLY unprefixed file you write is your result
`na<SR>.json`.

**NEVER touch the user's project files** in
`C:\Users\GyanendraVishwakarma\Web Research Agent` (the `.xlsx`/`.xlsm`
workbooks). Off-limits: Kitchen_and_Dining.xlsx, Lighting.xlsx,
Wall_Decor.xlsx, Decorative_Home_Accessories.xlsx, Furniture.xlsx,
Textile.xlsx, Storage.xlsx, Pet_Care.xlsx, Seasonal.xlsx, Bathroom.xlsx,
`Final_Company_List (1).xlsx`, and the sibling deliverables Bestsellers.xlsx /
Clearance.xlsx — writing anywhere in that folder is forbidden. The
orchestrator does the merge.

**Work synchronously, in the foreground, in this same turn.** Do not launch a
background job and end your turn "waiting to be notified." Finish the company
and write the JSON before you stop.

---

## 0. READ YOUR COMPANY'S ACCESS NOTES FIRST — THIS SAVES YOU AN HOUR

`notes/<SR>.md` in the scratchpad contains the **prior Home-Decor/Furniture
pass** for your exact company: access route, blocks, verified URL shape.
Read it before your first fetch — for site structure and access route only,
not for New Arrivals content (the prior passes never looked for it).

If a note says `status=failed` or `blocked`, still try — access conditions
change. But don't burn the whole session on one site; if genuinely
unreachable, mark it `blocked` with a precise reason.

---

## 1. ACCESS TIER — TRY IN THIS ORDER, STOP AT THE FIRST THAT WORKS

1. **Direct HTTP fetch + HTML parsing.** Plain request or `curl_cffi`/`requests`
   are fine. Pull SSR HTML, embedded JSON, sitemaps, robots.txt, category/
   product-count APIs.
2. **Playwright/CDP** when tier 1 can't see the real DOM/data.
3. **Claude-in-Chrome** only as a last resort.

No r.jina.ai, translate.goog, web.archive.org, or webcache as a substitute.

**Check `robots.txt` for a Claude-specific disallow before Claude-in-Chrome
use** — a full-site `Disallow: /` named at Claude means STOP, mark blocked.

**The FIRST block stops that host, not the third.** 403/DataDome/Akamai/
Cloudflare/CAPTCHA/"Access Denied"/rate-limiting = stop, use what you have,
report precisely what's missing. No sleep/backoff loops.

---

## 2. THE ONE RULE THAT MATTERS — QTY

**`qty` must be the EXACT number of products the website itself reports.**
Never estimate, round, infer, or aggregate. If you cannot verify the exact
number: `"qty": null` and `"flag": "MANUAL REVIEW: <specific reason>"`. Every
row with a qty must carry an `evidence` string.

---

## 3. WHAT COUNTS AS A NEW ARRIVALS PLP

**Target terms** (English and local-language equivalents): New Arrivals, New
In, New Products, Just In, Just Arrived, Latest Arrivals, Latest Products,
What's New, New This Season, Recently Added, Newly Added, and "New
Collection" **only when it is genuinely a product listing representing new
arrivals** (see below).

**A candidate is only valid once you open it and confirm:**
1. Products are actually listed (a real PLP, not a marketing/editorial page).
2. The page genuinely represents "recently added to the catalogue" — not a
   themed seasonal campaign, lookbook, or announcement that merely mentions
   new products.

### "COLLECTION" PAGES NEED INSPECTION, EVERY TIME

Do not classify a page as New Arrivals purely because it's called "New
Collection" / "New Season" / "New Range." Open it and determine which of
these it actually is:

- **A genuine product listing** (a real PLP: browsable products, a count,
  filtering/sorting like any other category page) → likely a valid New
  Arrivals PLP if the products are in fact the newest additions. Record it.
- **A marketing/editorial landing page** (a themed hero story, lookbook
  imagery, a campaign write-up, no real product grid) → exclude.

**If you genuinely cannot tell, still record the row but set
`"flag": "MANUAL REVIEW: AMBIGUOUS NEW COLLECTION - <what you saw>"`.** The
merge step also force-flags any bare "Collection"-style name lacking a clear
New Arrivals signal word, so it's not fatal if you miss one — but your own
flag with real page evidence is far more useful than the merge's blind
name-pattern net.

### EXCLUDE
New Collection editorial pages (once confirmed non-listing), seasonal
campaign pages, marketing landing pages, blog posts, announcements,
lookbooks, individual products merely labelled "New" (a PDP's own "New"
badge does NOT make that PDP a New Arrivals PLP), search-results pages,
arbitrary date-filter pages.

### Multiple PLPs / genuine sub-structure
Same rule as the shared engine: genuinely different listings → keep both;
true aliases of the same listing → keep the canonical one, note the merge
decision. If the site exposes real children (e.g. `New Arrivals > Furniture
New Arrivals / Lighting New Arrivals`), preserve as grouping row + leaves.
Don't invent sub-categories that don't exist.

### Category/product overlap is expected
The same products may legitimately sit in their normal category (a separate
project) and here in New Arrivals. That is not an error.

---

## 4. NAVIGATION DISCOVERY

Check: main navigation, header/mega menus, footer navigation, sitemap,
relevant category/nav trees, internal links from relevant pages, and the
site's own search — English AND local-language equivalents. Don't rely on
Google. Search is supporting evidence only — every candidate must still be
opened and validated against §3.

**A zero-result site search is not proof of absence.** Check real navigation
and sitemap before concluding no New Arrivals PLP exists. Record what you
checked in `notes`.

---

## 5. THIS IS PLP-LEVEL EXTRACTION, NOT PDP EXTRACTION

No product-level rows (title/price/SKU/brand/description/images/material/
dimensions). Open a PDP only to resolve a genuine PLP-boundary question.

---

## 6. OUTPUT CONTRACT — write `na<SR>.json` in the scratchpad root

```json
{
  "status": "ok",
  "failure_reason": null,
  "notes": "free text: what you checked, Collection-page reasoning, absence proof",
  "rows": [
    {
      "category": "New Arrivals",
      "sub_category": "New Arrivals",
      "qty": 47,
      "link": "https://example.com/new-arrivals",
      "is_group": false,
      "evidence": "47 products",
      "flag": null
    }
  ]
}
```

`status` is one of `"ok" | "partial" | "blocked" | "failed"`; `failure_reason`
required if `"partial"`/`"blocked"`. `category` is always `"New Arrivals"` (or
a genuine site-defined child, e.g. `"Furniture New Arrivals"`); `sub_category`
names the specific listing, and can equal `category` if there is only one
undifferentiated listing.

Drop zero-product listings. Emit rows in reading order, parent immediately
followed by children. Write the file as soon as the company is done — do not
batch, do not wait to be asked.

If, after real investigation, no genuine New Arrivals PLP exists, write
`"rows": []` with `"status": "ok"` and explain what you checked in `notes` —
a correct, valuable answer.
