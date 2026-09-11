# Bestsellers — QA notes / open adjudication items

Log flagged judgement calls here as they arrive during batches, don't batch them
to the end (`.claude/skills/home-decor-extraction/SKILL.md` §5.8).

## Standing safety net (not an open question, just what to expect on Review)

`merge_bestsellers.py` force-flags any link shaped like a single product page
(`/products/<slug>`, `/item/...`, a `?variant=`/`?sku=` query) with
`MANUAL REVIEW: LINK LOOKS LIKE A SINGLE PRODUCT PAGE (PDP), NOT A PLP`. This
is a structural pattern check, not a page-content check — it will occasionally
flag a genuine PLP whose URL happens to look product-like, and can miss a PDP
that doesn't match the pattern. Treat every flagged row as "needs a human
look," not as "confirmed wrong."

## Status

**Batch 1 (SR 1-10) done and merged 2026-09-07.** 7/10 companies have
Bestsellers, 3/10 confirmed absent after real investigation (West Elm US,
Restoration Hardware, Anthropologie Home). 8 Review rows, all genuine
uncertainty (qty unverifiable due to Akamai/shared-browser-session limits,
or scoping ambiguity on a facet-filtered URL) — none were misclassifications
on spot-check. SR 5 (PB Kids US) and SR 3 (Pottery Barn US) were heavily
constrained by Akamai 403 blocks / shared Claude-in-Chrome session
contention across all 10 concurrent workers — several candidate rows have
`qty: null` rather than a verified count for that reason, not because the
PLP doesn't exist.

Fixed during merge: SR 7 is New Arrivals' company, not this file's — no
Bestsellers-specific fixes needed this batch.

**Batch 2 (SR 11-20) done and merged 2026-09-07.** 13/20 cumulative
companies have Bestsellers, 7/20 absent after real investigation. 63 leaf
rows, 11 Review rows. 3 new flags this batch, all legitimate terminology/
naming-mismatch uncertainty, not misclassifications: SR 16 "Most Loved" (not
an exact brief target phrase), SR 20 "Best 30 Selling Artificial Trees"
(header reports 270, not 30) and "Best 30 Selling Lighting Items" (header
reports 6, not 30) — both genuinely mislabeled by the site itself.

**Batch 3 (SR 21-30) done and merged 2026-09-07.** 18/30 cumulative
companies have Bestsellers, 12/30 absent after real investigation (several
premium/design brands with no popularity taxonomy at all: HAY US, Zara Home
UAE, Ethan Allen, Marina Home, The One, Home Centre, Room & Board, Target
Home, plus West Elm/RH/Anthropologie from earlier batches). 106 leaf rows,
15 Review rows. 4 new flags: SR 27 Blu Dot (2 sitemap-only pages, real
product grids but no site-reported total text — qty genuinely unverifiable,
not just tooling-limited); SR 29 High Fashion Home (2 dated/unlinked
campaign pages, real listings but possibly stale artifacts).

**Batch 4 (SR 31-40) done and merged 2026-09-07.** 26/40 cumulative
companies have Bestsellers, 14/40 absent after real investigation. 141 leaf
rows, 15 Review rows (no new flags this batch — all 10 companies resolved
cleanly, several with rigorous cross-verification methods worth noting as
precedent: SR 33 Horchow/SR 39 Jonathan Adler/SR 31 Perigold all
double-verified qty via a second independent count source).

**Batch 5 (SR 41-50) done and merged 2026-09-08.** 33/50 cumulative
companies have Bestsellers, 17/50 absent after real investigation (Nordstrom
Home and John Lewis Home both confirmed absent under Home despite the site
having a Bestsellers pattern elsewhere in the catalogue — e.g. Nordstrom runs
`/bestsellers` for Beauty/Men/Women/Kids/Sale but not Home). 168 leaf rows,
15 Review rows (no new Bestsellers-side flags this batch). Notable finds:
Z Gallerie (356, 7-way category split), Surya (747, unambiguous "Top
Sellers" nav node), Habitat UK ("Trending" node, 89, distinguished from a
generic `/search/bestsellers` keyword page), Swoon (980, 9 children across
two overlapping facet cuts — type and room — both genuine nav, both kept).
Made.com UK confirmed still live (not defunct) but has no Bestsellers
concept anywhere in its 12,150-URL sitemap.

**Batch 6 (SR 51-60) done and merged 2026-09-08.** 41/60 cumulative
companies have Bestsellers, 19/60 absent after real investigation. 209 leaf
rows, 25 Review rows. Two workers (SR 52 Williams Sonoma Home, SR 57 West
Elm UK) initially stalled mid-run waiting on a self-launched background
task instead of finishing in the foreground — both resumed with an explicit
"finish synchronously" instruction and completed correctly on the second
pass; no data loss, but worth watching for in future batches (see
[[let-batches-run-to-completion]] — this is a related but distinct failure
mode: not a batch getting stopped early, but a single worker parking itself
mid-task). SR 55 Crate & Barrel US came back `partial` (Akamai IP block hit
mid-session, core Bestsellers/Clearance/New-Arrivals top-line counts
confirmed before the block, ~9 category-level rows per file flagged
MANUAL REVIEW with null qty rather than fabricated — legitimate partial,
not a processing error). SR 52 Williams Sonoma Home Clearance also came
back `partial` for the same reason (Akamai). Notable finds: The Citizenry
(SR 53) caught a misleading capped "50" value in the site's own analytics
blob and used exhaustive product.json enumeration instead (81 true count);
West Elm UK (SR 57) correctly excluded a byte-identical duplicate
Bestsellers URL and corrected for 2 injected non-product promo banners in
every count; CB2 (SR 56) needed a 3-tier access split per-path (plain HTTP
for /new/*, Claude-in-Chrome for /special-features/best-sellers/* and all
of /sale/* which hard-403 at both HTTP and Playwright tiers).

**Batch 7 (SR 61-70) done and merged 2026-09-08.** 50/70 cumulative
companies have Bestsellers, 20/70 absent after real investigation. 219 leaf
rows, 25 Review rows. No workers stalled on background tasks this batch
(the batch-6 fix — explicit "finish synchronously" warning in every worker
prompt — held). SR 63 Serena & Lily confirmed genuinely absent (full nav
+ sitemap sweep, zero target-term matches; two sitemap-only "favorites"
pages correctly rejected as one-off marketing curation, not Bestsellers).
Notable finds: Heal's (SR 61) proved this exact site's aggregate
`collections.json` counts inflated (already known from the prior Home-Decor
pass) so used exhaustive `products.json` enumeration instead; Rowen & Wren
(SR 65) found an orphan "Your Favourites" collection via its own
`og:description` explicitly using the phrase "most popular designs";
Rejuvenation (SR 62) hit a path-specific 403 on `/shop/sale/*` while
`/shop/new-and-featured/*` stayed reachable in the same session — correctly
treated as a path-specific block, not a full-host block, and stayed on the
site's Constructor.io API rather than escalating tiers; Macy's Home (SR 69)
got an exact uncapped Bestsellers count (400) but Clearance/New Arrivals
both only expose a capped "(500+)" header with no reliable exact-count
source, so both were correctly left null+flagged rather than estimated
from page-count math (a sanity check on Bestsellers proved page counts
aren't uniform on this platform, so a derived guess would have been
unreliable); Lowe's Home Decor (SR 70) discarded a bogus ~1M-item embedded
`itemCount` field in favor of exhaustion-verified counts (100).

**Batch 8 (SR 71-80) done and merged 2026-09-08.** 57/80 cumulative
companies have Bestsellers, 22/80 absent, 1/80 genuinely blocked (SR 79 QVC
Home — hard Akamai/DataDome block re-verified from scratch at all 3 access
tiers including a real logged-in Claude-in-Chrome session; worker correctly
declined to use a computable search-API count since search-results pages
are excluded by the brief, so recorded null+flagged rather than a usable
number). 232 leaf rows, 26 Review rows. One worker (SR 75 Scully & Scully)
stalled waiting on a Monitor notification despite the standing
synchronous-work warning — resumed with the same explicit instruction and
completed cleanly on the second pass; watch for this recurring even with
the warning in the prompt (see [[bestsellers-clearance-new-arrivals-
scaffolded]] for the general pattern). Notable finds: Ferm Living US (SR
73) has an entire tier of merchandising collections (10 Sale variants +
News/Kids News) that exist in the Shopify catalog but currently render a
"content currently unavailable" placeholder — a site-side rollout gap, not
an access failure, worth a spot recheck in a later pass; Safavieh Home (SR
76) correctly rejected a "Rug Bestsellers" nav tile that was just an alias
of the full unfiltered rugs catalog; Bloomingdale's Home (SR 77) rejected a
lookalike New Arrivals search-derived count (15,717 — nearly the entire
department's markdown catalog size) in favor of the genuine curated nav
node (2,037); TJ Maxx Home (SR 71) confirmed genuinely absent via a full
3,119-node nav sweep.

**Batch 9 (SR 81-90) done and merged 2026-09-08.** 65/90 cumulative
companies have Bestsellers, 24/90 absent, 1/90 blocked (still SR 79). 246
leaf rows, 29 Review rows. **Fixed a merge-script bug this batch**:
`ledger_status()` in all three merge scripts (bestsellers, clearance,
new_arrivals — same shared pattern) only classified `status: "blocked"` or
`"failed"` as BLOCKED; a `status: "partial"` with zero rows (a genuine
"investigation was cut short, absence not proven" case) fell through to
"NO ... FOUND", misrepresenting an access failure as a completed
absence-check. Caught when SR 82 La Redoute UK's na82.json (0 rows,
partial, Cloudflare CAPTCHA blocked every listing page) got merged as "NO
NEW ARRIVALS FOUND" despite the worker's own notes explicitly saying
absence wasn't proven. Patched all three `ledger_status()` functions to
treat partial+zero-rows as BLOCKED, re-ran all three merges — verified
correct after the fix. Also fixed one non-ASCII cell caught during
pre-merge validation this batch: cl82.json had "Décor Final Clearance"
(accented é) in category/sub_category, corrected to plain-ASCII "Decor"
before archiving, per [[output-must-be-english-only]]. Also cleaned up two
stray scratch files that had leaked into the protected project root
(w87_home.html from SR 87, w57_full_sample.json left over from batch 7) —
neither touched any .xlsx, but worth a reminder to check the project root
each batch, not just the scratchpad. Notable finds: Barker and Stonehouse
(SR 85) caught and corrected for a confirmed +1 phantom-result Searchspring
API offset (documented from the prior Home-Decor pass too); Zara Home UK
(SR 90) confirmed absent — every "BESTSELLERS" nav entry resolves to an
in-page widget on a department landing page, not a standalone URL, and
none appear in the 322-URL category sitemap; H&M Home UK (SR 89) confirmed
absent by direct comparison to the Men's department, which does have a
working Bestsellers page (proving the platform supports it, Home just
lacks one).

**Batch 10 (SR 91-100) done and merged 2026-09-08 — 100/286 milestone.** 71/100
cumulative companies have Bestsellers, 28/100 absent, 1/100 blocked (still
SR 79). 254 leaf rows, 29 Review rows. First batch to include French sites
(Maisons du Monde, AM.PM, La Redoute Interieurs, Conforama, Camif) — all
handled correctly: workers translated category/sub_category to plain
ASCII English (0 non-ASCII cells) while quoting original French text/URLs
in evidence/notes, applied the same Sale-vs-Clearance discipline to French
"Soldes"/"Destockage"/"Braderie" terms. No workers stalled this batch (the
synchronous-work prompt fix continues to hold across 20 workers now).
Notable finds: Amara (SR 95) found a deindexed-but-live Bestsellers page
via a robots.txt `Disallow` clue rather than nav (16); House of Hackney
(SR 94) caught the same collections.json inflation bug documented in the
prior Home-Decor pass; IKEA UK correctly treated department "chips" as
query filters, not distinct PLPs; Rockett St George's Outlet listing had
only 1 live product but a completely clean signal (badge + title both say
"seconds"), kept rather than dropped since it's non-zero.

**Batch 11 (SR 101-110) done and merged 2026-09-08.** 76/110 cumulative
companies have Bestsellers, 33/110 absent, 1/110 blocked (still SR 79).
262 leaf rows, 30 Review rows. First batch with German sites (Westwing DE,
Hoeffner, XXXLutz DE, Zara Home DE, IKEA DE, Connox, KARE, Butlers) plus 2
more French (The Socialite Family, Fleux) — same clean pattern as batch
10's French sites: 0 non-ASCII cells, German target-term guidance
(Bestseller/Meistverkauft/Topseller, Raeumung/Restposten/Outlet,
Neuheiten) applied correctly, Sale-vs-Clearance discipline held in German
too. One worker-prompt typo this batch (a garbled notes-file path sent to
the Fleux/SR102 worker) — caught and corrected via a follow-up message
before the worker wasted a turn; final result was clean. UK/DE/FR sibling
pairs matched closely where expected: Westwing DE mirrored Westwing UK's
Bestsellers-absent/Clearance-via-"Last Chance" pattern almost exactly; Zara
Home DE reproduced the exact same "Bestsellers is just an in-page widget,
not a standalone PLP" finding as Zara Home UK; IKEA DE found its own
"Letzte Chance" Clearance page paralleling IKEA UK's "Last chance". Notable
finds: KARE's Clearance exclusion is a standout — the site's own on-page
FAQ copy *explicitly disclaims* being remainder/clearance stock ("Bei KARE
ist das anders..."), the cleanest possible Sale-vs-Clearance evidence
seen yet; XXXLutz DE found a working "Neu" filter facet with real data but
correctly excluded it from New Arrivals since it has no dedicated hub page
(unlike its own Abverkauf/Clearance facet, which does) — consistent with
the project's standing "no invented sub-categories from generic filters"
rule.

**Batch 12 (SR 111-120) done and merged 2026-09-08.** 82/120 cumulative
companies have Bestsellers, 37/120 absent, 1/120 blocked (still SR 79). 276
leaf rows, 32 Review rows. First batch spanning Netherlands/Belgium (Dutch)
and Spain — same clean local-language pattern held (0 non-ASCII cells).
SR 113 HKliving came back `partial` — the site's plausible Bestsellers
candidate ("Must-haves") is real but gated behind a dealer/wholesale login
this session has no credentials for; correctly recorded null+flagged
rather than guessed. Notable finds: fonQ (SR 111) flagged its own
"Best Rated Products" listing since it's rating-based not sales-volume
(though the site's own SEO copy self-describes it as customer favorites);
Zara Home ES reproduced the exact GB/DE sibling pattern independently
verified rather than assumed (single in-page widget, not standalone);
Sklum ran an exhaustive regex sitemap scan plus confirmed the platform's
native `best-sales` module isn't even installed (HTTP 500) before calling
genuine absence; Kave Home found 3 genuinely separate Bestsellers listings
via the site's own curated-PLP sitemap index, a discovery method (`/s/
<slug>` selections-sitemap) worth remembering for other Algolia-backed
sites.

**Batch 13 (SR 121-130) done and merged 2026-09-08.** 84/130 cumulative
companies have Bestsellers, 45/130 absent, 1/130 blocked (still SR 79). 279
leaf rows, 32 Review rows. First batch with Italian sites (Westwing IT,
Coincasa, H&M Home IT) — same clean pattern held. **Major finding: SR 124
Denby's entire storefront is dead** — the company entered administration
31 March 2026, and every URL (verified with a real rendered browser, not
just a status code) now serves a static legal notice with zero links/nav.
All three of Denby's files correctly report `status: ok, rows: []` since
this is a confirmed absence, not a missed search — but flag this to a
human reviewer since it's a business-status finding, not a data gap, and
worth checking again in a later re-verification pass in case Denby Home
Pottery Limited relaunches a storefront. Sibling cross-checks continued to
pay off: Westwing IT reproduced its UK/DE siblings' pattern exactly;
H&M Home IT matched the UK sibling on Bestsellers/New-Arrivals but actually
diverged further on Clearance (IT has zero ambiguous Sale node at all,
where UK had one) — and the worker caught that a prior-pass access note
about an excluded Home nav item now appears stale/since-removed. Notable
finds: Pooky and Coincasa both confirmed absent via a sort-dropdown-only
signal (not a real PLP); Anthropologie UK needed Claude-in-Chrome after
DataDome blocked tiers 1-2, found a live listing at a different URL than
the sitemap's dead `/bestsellers` entry.

**Batch 14 (SR 131-140) done and merged 2026-09-08.** 89/140 cumulative
companies have Bestsellers, 49/140 absent, 2/140 blocked (SR 79 QVC Home,
and now SR 134 Leroy Merlin France — confirmed IP/ASN-level 403 at both
HTTP and Playwright tiers, re-verified independently, matching the prior
project pass exactly; tier-3 Claude-in-Chrome couldn't be exercised by the
worker because this session has 2 connected browsers requiring an
interactive disambiguation subagents can't invoke — the orchestrator may
retry this one directly later since it holds that tool access). 284 leaf
rows, 34 Review rows. First batch with Danish (JYSK) — 7 languages proven
clean now. 1 new ambiguous flag: SR 135 Xenos "Trending" (59, reads more
like style curation than sales-popularity ranking). Notable finds: OTTO
Home discovered the site's genuine merchandising taxonomy runs through
named filter facets rather than dedicated URL paths, distinguished from
arbitrary sort/filter noise via each page's own SEO title/indexing status;
Nordic Nest's Bestsellers page (55,365) was recorded but flagged since
that count is roughly the whole catalog's size, raising doubt it's a real
curated shortlist; H&M Home France added a third divergent data point in
that sibling series (FR/UK/IT all differ from each other on at least one
category, a reminder not to assume sibling-locale consistency); Mango Home
correctly found Clearance lives entirely on a separate self-identified
mangooutlet.com domain, not under the main storefront.

**Batch 15 (SR 141-150) done and merged 2026-09-08.** 95/150 cumulative
companies have Bestsellers, 53/150 absent, 2/150 blocked (unchanged). 291
leaf rows, 35 Review rows. First batch with Finnish sites (Finnish Design
Shop, Iittala) — 8 languages proven clean now. 2 new flags: SR 147 Normann
Copenhagen (15, real distinct page but built on a non-standard curated-
widget layout with no h1/h2 — recorded with qty since it's exhaustively
countable, flagged for the structural oddity, not the content). SR 145
Galeries Lafayette needed a genuine tier-3 escalation this batch — the
worker initially skipped Claude-in-Chrome and returned `partial` for
Clearance/New-Arrivals with null qtys; caught this (the brief requires
exhausting all 3 tiers before settling for null) and resumed it explicitly
— tier 3 succeeded and both categories now have real confirmed numbers,
zero flags remaining. Worth remembering: check a worker's own access-tier
narrative for "tier 3 not attempted" admissions, not just its final
status field. Notable finds: Zara Home France made it 4/4 (now more, per
worker's own count) fully-consistent Zara Home locales — no Bestsellers,
no Clearance, one genuine New Arrivals PLP, same shared categoryId
pattern every time; Seletti and Finnish Design Shop both caught inflated
metadata counts and used exhaustion instead.

**Batch 16 (SR 151-160) done and merged 2026-09-08.** 96/160 cumulative
companies have Bestsellers, 62/160 absent, 2/160 blocked. 292 leaf rows, 35
Review rows. Heavily Danish-design-brand batch (6 of 10) — no Bestsellers
concept exists at ANY of the 6 Danish design brands checked this batch
(Bloomingville, Broste Copenhagen [found, 1 exception], House Doctor,
&Tradition, Georg Jensen, Muuto) — Broste Copenhagen was the sole
exception with a genuine curated Bestsellers page (440). Two sites had
real B2B/wholesale Bestsellers-adjacent pages that returned 0 products for
anonymous public users (Bloomingville's Outlet-style page, House Doctor's
"Favourites" widget) — correctly documented as genuine-but-empty rather
than silently dropped without explanation. Dille & Kamille (SR 153) hit a
genuine network-egress-level block (not a site WAF — other hosts connected
fine) persisting across all 3 standard tiers; the worker fell back to
r.jina.ai only after exhausting them, same accepted last-resort exception
precedent as Bed Bath & Beyond's translate.goog case. Notable finds:
Broste Copenhagen correctly excluded 6 near-duplicate per-category
"bestsellers" URLs that were 91-100% identical to the full category
catalog (legacy aliases, not genuine curation); Seletti-style inflated-
metadata pattern continued to show up and get correctly overridden by
exhaustion counts.

**Batch 17 (SR 161-170) done and merged 2026-09-08.** 104/170 cumulative
companies have Bestsellers, 64/170 absent, 2/170 blocked. 304 leaf rows, 42
Review rows. First batch of UAE companies (8 of 10) — IKEA UAE reproduced
its UK/DE/FR siblings' pattern exactly (5/5 locale consistency now).
Notable access finding: PAN Emirates UAE and Tavola UAE both needed
Claude-in-Chrome after Cloudflare challenges blocked tiers 1-2. PAN
Emirates' merchandising pages live at `/search/<term>` URLs — a new
"suspect URL" false-positive pattern (matches the search-page heuristic)
but the worker rigorously validated it's genuine backend collection
matching, not live full-text search, via query normalization + a
negative-control nonsense-query test (0 results) — same accepted-false-
positive class as Home Centre/Next.co.uk. 2 new flags: SR 162 Serax (2
stale dated snapshot collections, >1 year old, unlinked from nav, unclear
if still active); SR 163 PAN Emirates' New Arrivals also flagged
separately (see New Arrivals notes). Notable finds: Crate & Barrel UAE
(SR 168) confirmed genuinely different platform (SAP Commerce) from the
blocked US site (Akamai) — no access carryover between locale siblings on
different platforms; Noon UAE (SR 165) came back `partial` across all 3
categories for a first-of-its-kind reason — the site never displays exact
counts anywhere, only bucketed figures ("700+", "3K+"), confirmed via both
SSR HTML and live browser render, so every qty is correctly null+flagged
despite the category structure itself being solid (5-6 real rows each).

**Batch 18 (SR 171-180) done and merged 2026-09-08.** 110/180 cumulative
companies have Bestsellers, 68/180 absent, 2/180 blocked. 322 leaf rows, 56
Review rows. First batch with Japanese sites (MUJI Japan, Nitori Japan) and
first Australian companies (5 of 10) — both went cleanly, 9 languages
proven now. **Data-quality note (not a bug): SR 173 Chattels & More
triggered a new verify heuristic ("same link twice in one company")** —
its department-level rows correctly share one landing URL per promotion
since the site exposes no separate bookmarkable URL per department; each
row still carries a distinct, API-verified exact qty. Informational only,
verify still passed OK. Fixed 2 non-ASCII issues before archiving this
batch: Nitori Japan's "Bedding Ranking" sub_category had embedded Japanese
characters (stripped to English-only per rule), Chattels & More's 12 rows
used an en-dash (–) throughout instead of a plain hyphen (bulk-replaced).
Notable finds: Nitori Japan's Bestsellers is a fixed Top-20
recommendation-widget format spanning ~798 non-countable leaf pages across
4 brand storefronts — recorded as a grouping row + one honestly-sourced
verified example rather than fabricating a uniform count or omitting the
concept; MUJI Japan correctly rejected 3 Japanese-language lookalikes
(a sort filter, a "featured on TV" curation, and an editorial ranking
retrospective) before landing on genuine absence; Chattels & More
discovered 12 rows across 3 unlinked-but-live promotion pages
(Bestsellers/Best Sellers/Most Popular, all pairwise verified as
genuinely different curated sets, not aliases) reachable only by guessing
the site's URL/API slug pattern — all correctly flagged since none is
discoverable through live navigation.

## Batch 18 (SR 181-190) — first APJ/US-warehouse-club batch

First batch to hit Australia (Freedom, House, Country Road Home, Myer
Home), Singapore (HipVan, Castlery), and Japan (IKEA Japan, Francfranc
Japan), plus two US warehouse clubs (Costco, Sam's Club). 0 non-ASCII
cells resulted from both Japanese-language sites (9th/10th languages
proven clean).

Clean hits: IKEA Japan (726, single unambiguous node, translation key
`T_OFFERS_TYPE_TOP_SELLER` confirmed as the site's own bestseller label);
Freedom Australia (906, SAP/Hybris+Spartacus SPA needed tier-2 Playwright
since counts are Coveo-client-rendered); Castlery Singapore (4 rows,
sitewide + 3 non-zero category children summing exactly); Myer Home
(2 rows: Home Best Sellers 89 + Now Trending/Homewares Inspiration 302,
confirmed a genuine Fredhopper PLP not editorial).

Clean absences: House Australia (no dedicated PLP; only a per-product
badge + a sort-by-Bestsellers option, correctly excluded), HipVan (a
retired /bestsellers-2 404, homepage's "Best Selling Collections" is a
sort-param variant not a standalone PLP, correctly excluded), Country
Road Home (site search proven non-discriminating — nonsense query also
returned ~1000 results — correctly treated as inconclusive rather than
proof of absence, then confirmed absent via sitemap+nav), Sam's Club
(feature flag `enableTrendingCatNav: false` embedded in every page
confirms the concept exists in the platform but is disabled sitewide —
a stronger absence signal than usual), Francfranc Japan (a 300+ page
`ranking-<dept>` family proven to be alternate-sort views of the base
category via exhaustive product-ID-set comparison, not a curated
concept — plus an expired dated "Hit Ranking" campaign and an editorial
"Recommended Items" page, both correctly excluded).

Costco: dispatched worker hit a genuine Akamai block at tiers 1-2 and
could not reach tier 3 (browser-selection step unavailable to a
subagent). Orchestrator follow-up with direct Claude-in-Chrome access
confirmed the site is NOT uniformly blocked (homepage/department pages
render fine) but found no Bestsellers nav entry anywhere — status
upgraded from `blocked` to `partial` with richer notes; ledger
classification unchanged (still counts as BLOCKED / ACCESS FAILURE per
the partial+zero-rows rule). See [[bestsellers-clearance-new-arrivals-scaffolded]]
for the general Costco-recheck writeup, applicable across all 3 sibling
workbooks.

## Batch 19 (SR 191-200) — US big-box + Canada, first Etsy marketplace test

Mostly US/Canada (Quince, Simons Maison, Structube, Walmart, JCPenney,
Kohl's, Home Depot, Sur La Table, Etsy, Indigo Home).

Clean hits: Sur La Table (9 rows: parent 464 + 8 department children,
confirmed via breadcrumb/categoryID JSON not just sort-order); Simons
Maison ruled out via a full 8,207-URL category-sitemap suffix analysis —
only `--new-*` and `--sale-*` filter families exist sitewide, no
bestseller-equivalent at all (a stronger absence signal than usual).

Clean absences: Home Depot (thorough sitemap+nav search despite Akamai
blocking department pages at both HTTP and Playwright tiers — correctly
classified as genuine absence, not access failure, since sitewide search
found nothing beyond near-misses like a fixed 24-SKU homepage carousel
and literal-product-name "Zero-Clearance"/"Clearance Side Marker" false
positives); Etsy US (sitewide absence across all 3 concepts — only
per-listing "Bestseller" badges and a generic "Most Recent" sort exist,
no genuine PLP; confirmed via the site's full non-Home-scoped
`/categories` sitemap too, ruling out a Home&Living-specific gap).

Flagged (Review): Quince Home's Bestsellers/New-Arrivals both hit a real
pagination ceiling — site's own total is a per-color-variant count, only
30 rows retrievable via any tier (cursor ignored server-side), so a
verified distinct-product floor (25/20) was given with qty=null rather
than reporting the inflated site total or the unverifiable floor as
exact. Indigo Home's "Trending Gifts" (34) flagged as cross-department
gifts, not Home-exclusive, but included as the closest genuine match
since no Home-only Bestsellers PLP exists on the site (also not
currently linked from live nav — found via sitemap).

Access-tier note: Kohl's Home needed Claude-in-Chrome (tier 3) to get
past an Akamai behavioral JS challenge that blocked both curl and
Playwright — this worked for a dispatched worker this batch (unlike the
SR189 Costco case) because the orchestrator's earlier browser-selection
already resolved the multi-browser ambiguity for the session.

## Batch 20 (SR 201-210) — Wayfair-family cluster + luxury/lighting retailers

Three Wayfair-owned sibling brands landed in one batch (AllModern,
Birch Lane, Joss & Main), all confirmed on the same Next.js/BlockBuilder
platform with `resultCount`/`browseResultCount` as the exact-count
evidence field: AllModern (2 rows, 487+35), Birch Lane (1 row, 429),
Joss & Main (1 row, 445). Also EQ3 found a genuinely distinct second
Bestsellers listing under Inspiration > Trending (12) alongside the main
one (45+4 children) — kept as separate rows, not merged, since they're
structurally different listings.

Clean hits: Bouclair (268, exhaustion-verified via paged products.json);
Saks Home (100, via Claude-in-Chrome tier-3 after DataDome blocked
HTTP+Playwright); Grandin Road (71, "Customer Favorites & Best Sellers",
found via a robots.txt disallow-line hint rather than nav/sitemap).

Flagged (Review): Lamps Plus's only trending-adjacent listing ("New &
Trending", 38,641) mixes new+popular in one undifferentiated bucket with
no pure-bestseller alternative anywhere — flagged in both Bestsellers
and New Arrivals rather than picked for one; Lumens' "Top Selling Gifts"
(40) flagged since it's scoped to the Gift Guide family, not the core
Bestsellers branch.

**Notable platform-discovery pattern (Wayfair family):** Joss & Main's
Clearance ("Closeout", 252) was NOT linked from any nav — only
discoverable via internal site-search redirecting to a canonical
`/curated/...~ev<id>.html` event page. AllModern tried the same
search-redirect trick and confirmed genuine absence (no canonical
redirect, only generic keyword matches). Birch Lane's Clearance was
reported absent in this batch WITHOUT trying the search-redirect trick
(it wasn't known yet when that worker ran) — worth a quick recheck of
Birch Lane specifically in a future pass using this technique before
treating its absence as fully confirmed.

## Batch 21 (SR 211-220) — high-end design/lighting + first India-market companies

First batch to hit India (Cello World, Milton, Pepperfry) alongside
high-end US design/lighting brands (2Modern, Design Public, Lightology,
Terrain, Design Within Reach, Hudson Valley Lighting, Visual Comfort).
0 non-ASCII across all 3 Indian companies (all-English content).

**Merge-script bug found and fixed this batch (applies retroactively):**
a lone leaf row incorrectly flagged `is_group: true` with nothing after
it gets silently pruned as an "orphan grouping row with no surviving
children" — the row's real, verified qty vanishes from Output AND Review
entirely, with no trace except the archived JSON. Caught via SR 214
Terrain's New Arrivals (413, verified exact) disappearing despite
`status: partial` with 1 real row. A full project-wide scan for this
exact pattern (single-row or last-row `is_group:true` with no children
following) turned up 2 more silent instances from MUCH earlier batches:
**SR 49 Swoon's "Flash SALE" (799)** and **SR 55 Crate & Barrel US's
"Kids Clearance" (466)**, both in Clearance.xlsx, both present all along
in the archived JSON but never in the workbook. All three fixed by
flipping `is_group` to `false` in the source JSON and re-merging; both
historical rows now appear correctly in Clearance.xlsx Output. This is
NOT a new class of bug in the extraction rules — it's specifically about
worker output mislabeling a genuine leaf as a parent — but worth a
similar full-archive scan (`grep`-style is_group-orphan check, not just
this-batch) after any future large gap between merges, since it can hide
silently for many batches before being noticed.

Clean hits: Visual Comfort (7 rows, GraphQL-verified); Milton (6 rows
across sitewide + 4 sibling brands + Milton Concepts); Pepperfry (2964,
via systematic URL-pattern probing since not nav-linked, content-verified
via JSON-LD).

Clean absences: Hudson Valley Lighting and Lightology (both exhaustively
nav/search/URL-checked); Design Public's Clearance (thorough outlet-
taxonomy check found 3 real outlet collections all currently zero-product,
correctly dropped per the zero-listing rule rather than reported stale).

Flagged (Review): Terrain's Bestsellers (11) includes one apparel-leaning
item (a garden sun hat) kept per the site's own combined count rather
than silently dropped; 2Modern's "On Sale" (9335) and Lightology's
"Overstock" (1042) both flagged for lacking literal clearance/outlet
wording despite being the closest genuine candidates; Visual Comfort's
"Last Look" (440) flagged as a trade-exclusive pre-clearance staging list,
not itself the public clearance page.

## Batch 22 (SR 221-230) — all-India batch, including 3 fashion marketplaces

First all-India batch: 3 large marketplaces (Flipkart, Myntra, AJIO),
IKEA India, and several India-native home brands (FOS Lighting, H&M
Home India, Nestasia, Urban Ladder, Vaaree, Westside Home).

**Non-ASCII catch this batch:** H&M Home India's Bestsellers sub-category
came back as "Bestsellers Under ₹999" (a literal Rupee symbol embedded in
a price-capped category name) — fixed by the orchestrator to "Bestsellers
Under Rs. 999" before merging, keeping the project's 0-non-ASCII-cells
streak intact. First time a currency symbol (not a whole non-English
sentence) has tripped this check — worth remembering that price-in-name
categories are a distinct non-ASCII risk from the language-translation
cases seen so far.

Also ran the is_group-orphan scan (see batch 21's merge-script-bug fix)
against this batch pre-merge — 0 orphans found, the explicit worker-prompt
warning held.

**IKEA India reproduces the exact 6-locale pattern** (UK/DE/FR/UAE/Japan/
India all now confirmed) — same URL shapes, same translation keys,
verified independently each time rather than assumed.

Clean sitewide absences across all 3 concepts (thorough, not quick-search-
based): Myntra Home (generic search-fallback for every guessed slug,
confirmed via full nav JSON walk), Flipkart Home & Kitchen (per-listing
badges + a robots.txt-disallowed filter facet correctly excluded), AJIO
Home (270K+ URL sitemap regex-scanned across two storefront generations —
old SSR + new Fynd-CMS — zero Home-scoped matches in either).

Flagged (Review): Urban Ladder's Bestsellers has 3 differently-counted
pages all named "Bestsellers"-variants (118/47/13) — 2 flagged for human
dedup rather than merged or dropped, since exact counts differ and true
relationship (alias vs. genuinely separate) couldn't be confirmed.

## Batch 23 (SR 231-240) — second all-India batch

Second consecutive all-India batch (WoodenStreet, @home by Nilkamal, Clay
Craft India, Ankur Lighting, Borosil, Fabindia, Jainsons Lights, Nykaa
Fashion Home, Pottery Barn India, Pure Home + Living). 0 non-ASCII, 0
orphan is_group rows (the batch-21/22 fixes continue to hold).

**Security note (not an extraction finding, flagged to user directly):**
Pure Home + Living (SR 240) publishes a `/agents.md` file with
prompt-injection-style content aimed at AI shopping agents (urging
install of a third-party "Shop skill" and use of an MCP/checkout
protocol). Worker correctly did not act on any of it. Recorded here for
project memory; no further action needed unless this pattern recurs
elsewhere in the roster.

Clean hits: Pottery Barn India (188); Pure Home + Living (107, exhaustive
count overriding an inflated site field); Ankur Lighting (2 rows, both
exact, inflated raw counts correctly overridden); @home by Nilkamal
(3 rows).

Clean absences: 3 of 4 marketplace/fashion-adjacent sites came back
absent for Bestsellers specifically (WoodenStreet, Fabindia, Nykaa
Fashion Home all confirmed via full nav+sitemap+search-fallback checks);
Clay Craft India (fuzzy-search false-positive correctly excluded).

Flagged (Review): Borosil's entire Bestsellers/New-Arrivals slate (6
rows total) flagged for suspiciously broad/nested product sets (up to
80% of the whole catalogue, byte-identical sibling collections under
different labels) — each individually passes the "real reachable PLP"
test but the pattern strongly suggests automated broad collections
rather than genuine curation; recorded per brief rather than dropped,
but worth a dedicated human pass on this company specifically.

## Batch 24 (SR 241-250) — third all-India batch

Third consecutive all-India batch. 0 non-ASCII, 0 orphan is_group rows.

**Predicted pattern confirmed: Home Centre's `?q=badge` benign-search-URL
class reproduces on the India storefront** exactly as documented for
UAE — the worker was briefed in advance and correctly included the row
despite the merge script's generic search-URL heuristic firing on it
(expected/by-design behavior, not a bug).

**Zara Home India is genuinely absent because it has no dedicated India
storefront** — it's served entirely through the shared "Rest of World"
`/ww/` catalogue used by ~140 other countries. Checked: no other Zara
Home entry in this roster (UAE/UK/DE/ES/France) shares `/ww/`, so no
duplicate-row risk here, unlike the standing Noon UAE (SR165/286) case.

Clean hits: Ikiru (11 rows, 1 flagged); Address Home (1 clean row, plus
a whole-catalog decoy correctly excluded).

Clean absences (thoroughly, not quick-search-based): Tata CLiQ Luxury
Home, Zara Home India, HomeStop, Meesho Home & Kitchen, Chumbak — all
confirmed via nav+sitemap+soft-404/non-discriminating-search checks,
consistent with the project's standing false-absence discipline.

Flagged (Review): Wonderchef's Bestsellers has 4 flagged sitemap-only,
unlinked collections alongside 2 clean nav-linked ones — a similar
"broad/unclear provenance" pattern to Borosil (batch 23), though here
each candidate has low-to-moderate product overlap rather than being
byte-identical, so more plausibly genuinely separate merchant-curated
lists than automated duplicates; still needs human adjudication.

## Batch 25 (SR 251-260) — fourth all-India batch

Fourth consecutive all-India batch (The Decor Kart, Whispering Homes,
ellementry, West Elm India, The White Teak Company, The Bombay Store,
Beruru, Freedom Tree, Good Earth, India Circus). 0 non-ASCII, 0 orphan
is_group rows — both fixes continue holding cleanly across 5 batches now.

**West Elm India confirms the franchise-storefront pattern already seen
with Pottery Barn India: same Fynd Commerce platform, no Akamai
protection at all** (unlike US/UK West Elm siblings elsewhere in this
project that needed Claude-in-Chrome) — tier 1 sufficed. Also notable:
West Elm India's live nav slot for "Shop Best Sellers" was mid-rotation
to a seasonal campaign with no bestseller wording when checked (Dynamic
Yield personalization); worker correctly extracted the stably-self-
titled bestsellers page instead of the rotation target.

Clean hits: ellementry (161, exact); Beruru (4 rows: parent + 3 children,
containment-verified against a flat breadcrumb structure); The Bombay
Store (3 rows, 1 whole-catalog decoy correctly excluded); Whispering
Homes (5 rows, parent+4 children summing exactly).

Clean absences: The White Teak Company, Beruru's own absence-checks (see
clearance/new-arrivals below), Good Earth (SPA route-probing against a
deliberately nonexistent control URL, plus correctly treating the
site's own no-op search API as non-evidence rather than false-absence
proof).

Flagged (Review): The Decor Kart's secondary "Bestsellers" listing (23)
found only via the site's own search-app empty-results fallback config
— a real live page but reachable through an unusual discovery path.

## Batch 26 (SR 261-270) — fifth all-India batch

Fifth consecutive all-India batch. 0 non-ASCII, 0 orphan is_group rows —
both fixes clean across 6 batches now.

Clean hits: Sarita Handa (0 Bestsellers but 9 clean Clearance + 6 clean
New Arrivals rows, all arithmetic-verified, no flags anywhere — one of
the cleanest companies this project has processed); Nicobar (2 clean
rows, correctly scoped to Home vertical); Kapoor E-Illuminations (1
clean Bestsellers, resolved via a domain redirect since the roster
listed the dead apex domain); SPIN (7 clean Bestsellers rows, correctly
distinguishing genuine curated collections from 2 whole-catalog-mimic
decoys and a marketing-landing-reuse nav link).

Recurring pattern this batch: **orphan/sitemap-only duplicate listings**
under the same merchandising label — The Purple Turtles (3), Orange Tree
(3), Jaypore (5, all EOSS-campaign-tied) — each genuinely distinct
product sets (low/zero ID overlap confirmed), not aliases, but none
reachable via live navigation. All correctly recorded with MANUAL REVIEW
flags rather than silently trusted or dropped, consistent with project
discipline. Jaypore in particular has no canonical Bestsellers nav item
at all — over a dozen similarly-named marketing collections exist
sitewide, a genuinely harder case than most companies processed so far.

Flagged (Review): Oorjaa's "Best Sellers" duplicate (339) is an exact-set
match to the entire catalog — a mislabeled all-products collection, not
curation; The Artment's "Trending Decor" (21) has an H1 matching the
brief's target term but a URL handle and product dates suggesting it's
actually a restock-notification page.

## Batch 27 (FINAL — SR 271-285) — UK department stores + last stragglers, PROJECT COMPLETE

Final batch: 10 UK companies (The Range, Wayfair UK, Lakeland, ProCook,
Argos Home, Harrods Home, Selfridges Home, La Redoute Interiors UK,
Liberty London Home, The Conran Shop) plus the last 5 companies from
across the roster (home24 Germany, El Corte Inglés Home, Made in Design,
Home Box UAE, Amazon UAE). SR 286 (Noon UAE, known duplicate of SR 165)
was never dispatched, per standing project convention. **PROCESSING
ERROR is now 0 across all three workbooks — the full 285-company roster
is done.**

**Cross-company duplicate found and fixed (required to pass verify):**
SR 278 "La Redoute Interiors UK" and SR 82 "La Redoute UK" (already
merged from an earlier batch, mostly `qty: null` due to a Cloudflare
block) turned out to be the same domain, and SR 278's worker — who
successfully cleared the same Cloudflare "Country challenge" via
Claude-in-Chrome (auto-resolves after ~4s in a real browser) — found
that for this concept (unlike the separate category-taxonomy project)
there is no brand-specific filtering: SR 278's home-scoped rows are
identical URLs/counts to what SR 82's home subset would be. The strict
duplicate-URL check in `verify_clearance.py` caught 4 exact link
collisions and failed the pipeline. Resolution: folded SR 278's verified
data into SR 82 (replacing SR 82's old blocked/null rows), removed SR
82's original out-of-scope fashion rows (Women's/Men's/Kids'/Knitwear
Clearance — a scoping mistake from SR 82's earlier session, since every
other multi-category company in this roster is scoped to home/decor
only), and emptied SR 278 to `rows: []` since it's now fully redundant.
Applied consistently across all three concept workbooks (Bestsellers,
Clearance, New Arrivals), even though only Clearance's assertion
actually failed — Bestsellers/New Arrivals had the identical underlying
duplicate but weren't caught because the merge script blanks parent/
group-row links before the strict check runs. Full reasoning preserved
in bs82.json/cl82.json/na82.json's `notes` fields.

**New blocked entries this batch (Claude-specific robots.txt
disallow, re-verified fresh each time, not assumed from old notes):**
home24 Germany, El Corte Inglés Home, Made in Design, Amazon UAE — all
4 joining the standing QVC Home/Leroy Merlin France/Costco US list.

**Access breakthrough:** Home Box UAE's Cloudflare Turnstile challenge
(previously a hard block for this project) was cleared by Claude-in-
Chrome on the first try — confirmed genuinely absent across all 3
concepts once past it, not a tooling gap.

Clean hits: The Range (7 rows), Wayfair UK (1 row, confirmed same
Wayfair-family platform as AllModern/Birch Lane/Joss & Main but does
NOT reproduce their Clearance search-redirect trick), Lakeland (0, but
6 New Arrivals rows), ProCook UK (3 rows, investigated independently
from its India sibling), Harrods Home (Trending Homeware as the
department's bestseller-equivalent since Home has no literal
"Bestsellers" page), Liberty London Home (1 clean row), The Conran Shop
(1 row, triple-verified).

Clean absences: Selfridges Home (Home has no Bestsellers though other
departments do).

Partial (not ok — genuine access gap, not false absence): Argos Home's
Bestsellers/New Arrivals — Akamai blocked the homepage/mega-menu across
all 3 tiers including Claude-in-Chrome, so `rows: []` was correctly
marked `partial` rather than a confirmed absence; also caught a
`/list/<any-slug>/` false-positive trap (always returns HTTP 200,
verified against a nonsense-slug control).

PROJECT STATUS: all 285 companies processed across Bestsellers,
Clearance, and New Arrivals. See memory file for final cumulative
totals and the standing list of Review-sheet items still awaiting human
adjudication.
