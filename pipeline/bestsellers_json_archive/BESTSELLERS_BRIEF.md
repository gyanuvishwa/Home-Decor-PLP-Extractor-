# BESTSELLERS EXTRACTION — WORKER BRIEF

You are one of several parallel extraction workers. Read this whole brief before
starting. You are assigned **exactly one company**. Your job: find that
company's genuine **Bestsellers-type merchandising PLP(s)** — pages the site
itself uses to list its best-selling / most-popular / top-selling products —
capture the deepest valid listing (PLP) URL(s) and the site's own exact
product counts, and write one JSON file.

**Scratchpad (your working dir — do ALL file work here):**
`<SCRATCHPAD_PATH>`

**The scratchpad is shared with other workers running at the same time.**
Prefix EVERY working file and directory you create with `w<SR>_` (e.g.
`w42_tree.py`, `w42_cache/`). The ONLY unprefixed file you write is your result
`bs<SR>.json`.

**NEVER touch the user's project files** in
`C:\Users\GyanendraVishwakarma\Web Research Agent` (the `.xlsx`/`.xlsm`
workbooks). Off-limits: Kitchen_and_Dining.xlsx, Lighting.xlsx,
Wall_Decor.xlsx, Decorative_Home_Accessories.xlsx, Furniture.xlsx,
Textile.xlsx, Storage.xlsx, Pet_Care.xlsx, Seasonal.xlsx, Bathroom.xlsx,
`Final_Company_List (1).xlsx`, and the sibling deliverables Clearance.xlsx /
New_Arrivals.xlsx — writing anywhere in that folder is forbidden. The
orchestrator does the merge.

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

Read those notes for SITE STRUCTURE and ACCESS ROUTE, not for Bestsellers
content — the prior passes never looked for merchandising PLPs. What's
valuable: the URL shape, the nav/sitemap structure, which access route worked
(proxy pins, IPv6 routes, whatever got past a WAF), and site-specific traps.

If a note says `status=failed` or `blocked`, still try — access conditions
change. But don't burn the whole session on one site; if it's genuinely
unreachable, mark it `blocked` with a precise reason.

---

## 1. ACCESS TIER — TRY IN THIS ORDER, STOP AT THE FIRST THAT WORKS

1. **Direct HTTP fetch + HTML parsing.** Plain request or `curl_cffi`/`requests`
   are fine. Pull SSR HTML, embedded JSON (`__NEXT_DATA__` / `__NUXT__` /
   `__APOLLO_STATE__`), sitemaps, robots.txt, category/product-count APIs.
2. **Playwright/CDP** when the page is client-rendered and tier 1 can't see the
   real DOM/data.
3. **Claude-in-Chrome (`mcp__claude-in-chrome__*`)** only as a last resort.

No r.jina.ai, translate.goog, web.archive.org, or webcache as a substitute for
reaching the site directly.

**Check `robots.txt` for a Claude-specific disallow before Claude-in-Chrome
use.** A named `anthropic-ai` / `ClaudeBot` / `Claude-Web` / `Claude-User` /
`Claude-SearchBot` with a full-site `Disallow: /` means STOP and mark the
company blocked, even if the WAF is trivially bypassable.

**The FIRST block stops that host, not the third.** A block is 403, DataDome,
Akamai, Cloudflare, CAPTCHA, "Access Denied", rate-limiting, or repeated load
failure. On the first one: stop requesting that host, use what you already
have, process it locally, report precisely what's missing. `sleep` /
backoff loops / polling a blocked host are banned. Pacing requests before
trouble (~1 per 5-8s) is fine.

---

## 2. THE ONE RULE THAT MATTERS — QTY

**`qty` must be the EXACT number of products the website itself reports for
that PLP.** Never estimate, round, infer, aggregate, or copy a number from
elsewhere. If you cannot verify the exact number: `"qty": null` and
`"flag": "MANUAL REVIEW: <specific reason>"`. A null is correct; a fabricated
number is a project-destroying error. Every row with a qty must carry an
`evidence` string — the literal text or JSON path that produced it.

---

## 3. WHAT COUNTS AS A BESTSELLERS PLP

**Target terms** (English and local-language equivalents): Bestsellers, Best
Sellers, Bestselling Products, Best Selling, Top Sellers, Top Selling
Products, Popular Products, Most Popular, Customer Favorites, Trending
Products.

**Candidate URL shapes** — starting points only, never sufficient on their
own: `/best-sellers`, `/bestsellers`, `/best-selling`, `/top-sellers`,
`/popular`, `/customer-favorites`, and their `/collections/...`, `/shop/...`
equivalents.

**A candidate is only valid once you open it and confirm all three:**
1. Products are actually listed (this is a real PLP, not editorial/marketing).
2. The page genuinely represents a bestseller/popularity merchandising
   concept — not just a page that happens to mention bestselling products.
3. It is not a single product's PDP with a "Bestseller" badge — a product
   being marked "Bestseller" does NOT make its own product page a Bestsellers
   PLP.

### EXCLUDE
Bestseller blog posts, editorial pages, buying guides, inspiration pages,
marketing banners, individual PDPs, collections that merely mention
bestselling products in passing, search-results pages, arbitrary filter
pages, and any page whose only signal is a badge/label on individual
products rather than the page itself being a listing.

### Multiple PLPs for the same concept
A site may expose Bestsellers through several URLs (e.g. `/bestsellers` and
`/collections/bestsellers`). Inspect each. If they are genuinely different
listings (different product sets, different counts), keep both as separate
rows. If one is an alias of the other (same underlying listing, same
products), keep the canonical one and note the merge decision. **Do not
deduplicate purely because two listings happen to report the same count** —
confirm they are actually the same listing before merging them.

### Category/product overlap is expected, not an error
The same products legitimately appear in both their normal category (already
extracted in a separate project) and here in Bestsellers. Do not exclude a
product or PLP just because it also belongs elsewhere.

### Genuine sub-structure
If the site itself exposes real children (e.g. `Bestsellers > Furniture
Bestsellers / Lighting Bestsellers / Decor Bestsellers`), preserve that as a
grouping row + leaves, same shape as the shared engine's grouping rules. If
only a single `Bestsellers` listing exists, output just that one row — do not
invent sub-categories.

---

## 4. NAVIGATION DISCOVERY

Check, in this order of thoroughness: main navigation, header/mega menus,
footer navigation, sitemap, relevant category/nav trees, internal links
discovered from relevant pages, and the site's own search — in English AND
local-language equivalents. Do not rely on Google/search-engine results.
Website search is supporting evidence only: every candidate it surfaces must
still be opened and validated against §3 above.

**A zero-result site search is not proof of absence.** Some sites return
default or non-discriminating results for every query. Check real navigation
and the sitemap before concluding no Bestsellers PLP exists. Record what you
checked in `notes`.

---

## 5. THIS IS PLP-LEVEL EXTRACTION, NOT PDP EXTRACTION

Do not crawl individual product pages for title/price/SKU/brand/description/
images/material/dimensions. Do not create one row per product. Open a PDP
only to resolve a genuine PLP-boundary question (e.g. confirming a link is a
listing, not a single product). The desired record is the PLP itself.

---

## 6. OUTPUT CONTRACT — write `bs<SR>.json` in the scratchpad root

```json
{
  "status": "ok",
  "failure_reason": null,
  "notes": "free text: what you checked, overlap decisions, absence proof",
  "rows": [
    {
      "category": "Bestsellers",
      "sub_category": "Bestsellers",
      "qty": 125,
      "link": "https://example.com/best-sellers",
      "is_group": false,
      "evidence": "Showing 1-24 of 125 products",
      "flag": null
    }
  ]
}
```

`status` is one of `"ok" | "partial" | "blocked" | "failed"`; `failure_reason`
is required if status is `"partial"` or `"blocked"`. `category` is always
`"Bestsellers"` (or a genuine site-defined child, e.g. `"Furniture
Bestsellers"`, as its own row's category if the site nests it that way, with
`sub_category` naming the specific listing). If the site has only one
undifferentiated Bestsellers listing, `sub_category` can equal `category`.

Drop zero-product listings rather than emitting a `qty: 0` row. Emit rows in
reading order; a genuine parent immediately followed by its children. Write
the file as soon as the company is done. Do not batch multiple companies into
one file, and do not wait to be asked before writing it.

If, after real investigation (§4), no genuine Bestsellers PLP exists on the
site, write `"rows": []` with `"status": "ok"` and explain what you checked in
`notes` — this is a correct, valuable answer, not a failure.
