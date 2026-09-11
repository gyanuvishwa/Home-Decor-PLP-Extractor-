# CLEARANCE EXTRACTION — WORKER BRIEF

You are one of several parallel extraction workers. Read this whole brief before
starting. You are assigned **exactly one company**. Your job: find that
company's genuine **Clearance-type merchandising PLP(s)** — pages the site
itself uses to list permanently-marked-down / end-of-line products —
capture the deepest valid listing (PLP) URL(s) and the site's own exact
product counts, and write one JSON file.

**POLICY: OUTLET IS NOT CLEARANCE.** Do not record any page branded Outlet
by the site (nav label, breadcrumb, page `<title>`/H1, or a separate outlet
storefront/subdomain) — "Outlet", "Outlet Store", "Outlet Products",
"Outlet Collection", "Outlet Sale", "Outlet Deals", or any equivalent, in
any language. This holds even if the stock is permanently marked down,
seconds, returns, or end-of-line — Outlet is judged a separate
merchandising channel from Clearance for this project, full stop. See §3
below.

**POLICY: OPEN BOX IS NOT CLEARANCE EITHER.** Do not record any page
branded "Open Box" — "Open Box", "Open Box Deals", "Open Box Returns",
"Open Box Clearance Sale", or any equivalent (previously-opened/returned/
like-new condition-based discount inventory). Same hard-exclude treatment
as Outlet, even if the page sits under the site's own Clearance/Sale nav.

**Scratchpad (your working dir — do ALL file work here):**
`<SCRATCHPAD_PATH>`

**The scratchpad is shared with other workers running at the same time.**
Prefix EVERY working file and directory you create with `w<SR>_` (e.g.
`w42_tree.py`, `w42_cache/`). The ONLY unprefixed file you write is your result
`cl<SR>.json`.

**NEVER touch the user's project files** in
`C:\Users\GyanendraVishwakarma\Web Research Agent` (the `.xlsx`/`.xlsm`
workbooks). Off-limits: Kitchen_and_Dining.xlsx, Lighting.xlsx,
Wall_Decor.xlsx, Decorative_Home_Accessories.xlsx, Furniture.xlsx,
Textile.xlsx, Storage.xlsx, Pet_Care.xlsx, Seasonal.xlsx, Bathroom.xlsx,
`Final_Company_List (1).xlsx`, and the sibling deliverables Bestsellers.xlsx /
New_Arrivals.xlsx — writing anywhere in that folder is forbidden. The
orchestrator does the merge.

**Work synchronously, in the foreground, in this same turn.** Do not launch a
background job and end your turn "waiting to be notified." Finish the company
and write the JSON before you stop.

---

## 0. READ YOUR COMPANY'S ACCESS NOTES FIRST — THIS SAVES YOU AN HOUR

`notes/<SR>.md` in the scratchpad contains the **prior Home-Decor/Furniture
pass** for your exact company: access route, blocks, verified URL shape.
Read it before your first fetch — for site structure and access route only,
not for Clearance content (the prior passes never looked for it).

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

## 3. WHAT COUNTS AS A CLEARANCE PLP

**Target terms** (English and local-language equivalents): Clearance,
Clearances, Clearance Sale, Clearance Products, Final Sale, Final Clearance,
Last Chance, Last Chance Products, End of Line, Discontinued (when
merchandised as a clearance-style listing). **"Outlet" / "Clearance Outlet"
is explicitly NOT a target term — see the policy note at the top of this
brief. Neither is "Open Box" in any form ("Open Box Deals", "Open Box
Returns", "Open Box Clearance Sale") — same treatment, hard exclude.**

**A candidate is only valid once you open it and confirm:**
1. Products are actually listed (a real PLP, not editorial/marketing/coupon
   page).
2. The page is not itself branded Outlet (own `<title>`/H1/nav label, or a
   separate outlet storefront/subdomain) — if it is, exclude it, do not
   proceed to check 3.
3. The site's OWN taxonomy treats this page as clearance-style
   merchandising — not a temporary promotional campaign, and not Outlet.

**Hybrid "Clearance & Outlet" departments:** if a site bundles both under one
umbrella nav label but the individual child listings are each independently
Clearance-branded (URL slug / API category code / page title all say
"clearance", none say "outlet"), keep the Clearance-branded children and
ignore the umbrella's mixed name. If instead the specific page itself is
titled/labeled Outlet (even alongside the word Clearance, e.g. `"The Outlet
| Clearance | Brand"`), that page is Outlet — exclude it.

### CLEARANCE VS. SALE — THE CRITICAL DISTINCTION

This is the single most important judgment call in this brief. A page called
**Sale / Offers / Deals / Promotions / Discounts / Special Offers** should
**NOT** be automatically classified as Clearance.

- If the website's own taxonomy clearly treats the page as **Clearance /
  Final Clearance / Last Chance / End of Line** (and it is NOT itself
  branded Outlet), it qualifies — record it and say in `notes` what told
  you so (page heading, breadcrumb, nav label, on-page copy describing it
  as permanent markdown stock).
- If it is a **generic temporary promotional sale** (seasonal sale, Black
  Friday, a percent-off campaign with no permanence signal), do **not**
  include it as Clearance.
- **If uncertain, still record the row but set
  `"flag": "MANUAL REVIEW: AMBIGUOUS SALE/CLEARANCE - <what you saw and why
  you're unsure>"`** rather than guessing either way. The merge step also
  force-flags any generic-sale-worded row that lacks a strict clearance word,
  so it's not fatal if you miss one — but your own flag with real page
  evidence is far more useful than the merge's blind name-pattern net.

### EXCLUDE
Individual PDPs with a clearance badge, promotional banners, sale articles,
discount landing pages with no products listed, coupon pages, generic offers
pages, Black Friday promotion pages, seasonal promotion pages, marketing/
editorial pages, and **any Outlet-branded page or section** — unless the
actual page is a genuine PLP that the site's own taxonomy treats as
Clearance (not Outlet) per the test above.

### Multiple PLPs / genuine sub-structure
Same rule as the shared engine: different URLs that are genuinely different
listings → keep both; true aliases of the same listing → keep the canonical
one and note the merge. If the site exposes real children (e.g. `Clearance >
Furniture Clearance / Lighting Clearance`), preserve as grouping row +
leaves. Don't invent sub-categories that don't exist.

### Category/product overlap is expected
The same products may legitimately sit in their normal category (a separate
project) and here in Clearance. That is not an error.

---

## 4. NAVIGATION DISCOVERY

Check: main navigation, header/mega menus, footer navigation, sitemap,
relevant category/nav trees, internal links from relevant pages, and the
site's own search — English AND local-language equivalents. Don't rely on
Google. Search is supporting evidence only — every candidate must still be
opened and validated against §3.

**A zero-result site search is not proof of absence.** Check real navigation
and sitemap before concluding no Clearance PLP exists. Record what you
checked in `notes`.

---

## 5. THIS IS PLP-LEVEL EXTRACTION, NOT PDP EXTRACTION

No product-level rows (title/price/SKU/brand/description/images/material/
dimensions). Open a PDP only to resolve a genuine PLP-boundary question.

---

## 6. OUTPUT CONTRACT — write `cl<SR>.json` in the scratchpad root

```json
{
  "status": "ok",
  "failure_reason": null,
  "notes": "free text: what you checked, Sale-vs-Clearance reasoning, absence proof",
  "rows": [
    {
      "category": "Clearance",
      "sub_category": "Clearance",
      "qty": 84,
      "link": "https://example.com/clearance",
      "is_group": false,
      "evidence": "84 products",
      "flag": null
    }
  ]
}
```

`status` is one of `"ok" | "partial" | "blocked" | "failed"`; `failure_reason`
required if `"partial"`/`"blocked"`. `category` is always `"Clearance"` (or a
genuine site-defined child, e.g. `"Furniture Clearance"`); `sub_category`
names the specific listing, and can equal `category` if there is only one
undifferentiated listing.

Drop zero-product listings. Emit rows in reading order, parent immediately
followed by children. Write the file as soon as the company is done — do not
batch, do not wait to be asked.

If, after real investigation, no genuine Clearance PLP exists (and nothing
ambiguous was found either), write `"rows": []` with `"status": "ok"` and
explain what you checked in `notes` — a correct, valuable answer.
