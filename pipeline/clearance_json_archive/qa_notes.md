# Clearance — QA notes / open adjudication items

Log flagged judgement calls here as they arrive during batches, don't batch them
to the end (`.claude/skills/home-decor-extraction/SKILL.md` §5.8).

## Open policy question (block merging any batch that hits this at scale)

**Clearance vs. generic Sale — no blanket rule, judged per site.** Per the
user's explicit spec: a page called Sale/Offers/Deals/Promotions/Discounts/
Special Offers is NOT automatically Clearance. It only counts if the site's
OWN taxonomy clearly treats it as Clearance/Outlet/Final Clearance/Last
Chance/End of Line. `merge_clearance.py` force-flags any sub-category that
matches the generic-sale wording but lacks a strict clearance-family word
(`clearance/outlet/final sale/last chance/end of line/discontinued`) with
`MANUAL REVIEW: GENERIC SALE/OFFERS PAGE, NOT CONFIRMED AS CLEARANCE BY SITE
TAXONOMY`. This is a naming heuristic only — a site can genuinely equate
"Sale" with permanent markdown/outlet merchandising, in which case the
worker's own page inspection (not the name) is what should decide, with the
reasoning recorded in `notes`. Adjudicate each flagged row on its own site
evidence; do not resolve the general policy question by editing the regex to
be looser or stricter without a specific case in front of you.

## Standing safety net (not an open question)

`merge_clearance.py` also force-flags PDP-shaped links, same as the
Bestsellers/New Arrivals siblings — see their qa_notes.md for the caveat.

## Status

**Batch 1 (SR 1-10) done and merged 2026-09-07.** 8/10 companies have
Clearance, 2/10 confirmed absent after real investigation (Restoration
Hardware — RH Outlet confirmed store-only, no online storefront;
Anthropologie Home — only a time-boxed "Sale" family, no clearance
taxonomy). 20 Review rows.

**4 genuine Sale-vs-Clearance ambiguity flags this batch, all worth a human
look:**
- SR 1 Wayfair, `/daily-sales/clearance` (qty 29069): URL/title say
  "Clearance," page's own H1 and tracking metadata say "Open Box." Unclear if
  the site treats these as one merged concept.
- SR 2 West Elm US, `/shop/sale/clearance/` (qty 580): persistent URL + own
  H1/product set/count, but page `<title>` currently ties it to a "Labor Day"
  promo.
- SR 3 Pottery Barn US, nested Sale-page filter (qty 1478, vs. the canonical
  `/shop/sale/all-clearance/` row at 2119): may be a genuinely distinct
  promo-scoped cut or an overlapping filtered view of the same inventory.
- SR 9 Article, `/c/sale` Clearance-tagged facet (qty 107): nav says "Shop
  Clearance" with a genuine "Clearance Sale" facet, but the page itself is a
  combined Sale+Clearance grid currently re-themed as a Labor Day promo, and
  no standalone clearance-only URL exists.

PB Kids US (SR 5) is Akamai-blocked on all 3 access tiers — 13 candidate
clearance sub-pages recorded from sitemap+nav-pattern evidence only, all
`qty: null` + flagged, existence not independently opened/confirmed.

**Batch 2 (SR 11-20) done and merged 2026-09-07.** 13/20 cumulative
companies have Clearance, 7/20 absent after real investigation. 71 leaf
rows, 22 Review rows. 2 new Sale-vs-Clearance flags this batch: SR 13
Bassett "Bedroom Sale & Clearance" (mixed terminology, breadcrumb sits under
generic Sale); SR 19 Danube Home "Clearance Prices" (explicit clearance
name, but nested under the generic Sale branch). Both are genuine per-page
judgment calls, not merge bugs.

**Batch 3 (SR 21-30) done and merged 2026-09-07.** 20/30 cumulative
companies have Clearance, 10/30 absent after real investigation. 122 leaf
rows, 24 Review rows. 2 new Sale-vs-Clearance flags: SR 27 Blu Dot
"Warehouse Sale" (generic-sale-worded, no strict clearance term, force-
flagged by the merge safety net); SR 28 Room & Board "Every Last Yard Event"
(a sustainability-branded discontinued-fabric closeout, not in the site's
own Clearance taxonomy but functionally similar). Notable correct
exclusions this batch worth recording as precedent: Marshalls (off-price
retailer — only counted as Clearance because products carry an EXTRA
markdown layer beyond the everyday "Compare At" price, confirmed by the
worker); One Kings Lane (flash-sale business model — the standing
"Clearance" node was kept separate from the rotating countdown-timer sale
mechanism, which was excluded).

**Batch 4 (SR 31-40) done and merged 2026-09-07.** 24/40 cumulative
companies have Clearance, 16/40 absent after real investigation. 157 leaf
rows, 25 Review rows. 1 new flag: SR 35 Frontgate "Limited Time Only" (a
direct sibling of the confirmed Clearance node under the shared hub, but its
own name signals a temporary promotion). Good precedent from this batch: several premium/design brands (Perigold,
1stDibs, HAY, The Novogratz) confirmed genuinely absent after exhaustive
nav+sitemap checks, distinguishing real absence from under-investigation.

**Batch 5 (SR 41-50) done and merged 2026-09-08.** 34/50 cumulative
companies have Clearance, 16/50 absent after real investigation. 201 leaf
rows, 36 Review rows. 5 new ambiguous-Sale/Clearance flags this batch,
every one carrying a real page-level conflict rather than a name-pattern
guess: SR 43 Nordstrom Home (`/browse/sale/home` H1 literally says
"Clearance" but sits under the sitewide "Sale & Clearance" hub with no
distinct always-on channel); SR 47 Dunelm "Best Value Deals" (728, evergreen
nav size but no permanence/campaign wording either way); SR 48 Made.com UK
(its only live discount facet, "Sale", explicitly marked non-clearance in
the theme's own `saleOrClearance` metadata — Made's actual `/clearance` URLs
all resolve to an empty catch-all, so this was recorded flagged rather than
silently dropped); SR 49 Swoon "Flash SALE" (799, promo copy vs. a
meta_title literally reading "Summer Outlet" — direct signal conflict); SR
50 OKA (9 rows, its entire "Sale" hub — the site has zero pages literally
named Clearance/Outlet/Final Sale/End of Line anywhere in 336 collections,
but permanent nav placement + "gone forever" copy kept it from a clean
exclude). Clean hits: Z Gallerie (278, 7-way split, "SALE" confirmed a
genuinely separate site taxonomy family from "-clearance" URLs so correctly
excluded), Surya (9512, unambiguous "CLEARANCE" nav node with its own CSS
class), Habitat UK (2 genuinely distinct Clearance families verified
non-aliased via product-ID overlap sampling — 535 general + 38
"Clearance Lines at Habitat"), John Lewis Home (80, found via a "Home
Outlet Offers" node distinct from the hub's time-boxed Summer Sale
siblings), Bed Bath & Beyond (1114, genuine on-site Clearance PLP;
correctly excluded a separate `/deals/clearance` hub whose tiles all link
off-domain to overstock.com).

**Batch 6 (SR 51-60) done and merged 2026-09-08.** 42/60 cumulative
companies have Clearance, 18/60 absent after real investigation. 259 leaf
rows, 52 Review rows. 8 new ambiguous-Sale/Clearance flags this batch: SR
60 Soho Home (6 rows — the site has no Clearance/Outlet wording anywhere,
only a persistent "Sale" nav item, so its top-level + 5 per-category Sale
pages were all recorded flagged rather than guessed); SR 54 Schoolhouse
"All Sale" (15, description reads "gone for good" — permanent-markdown
language despite the generic name); SR 52 Williams Sonoma Home "Open Box"
(204, permanent-markdown signal from titling but breadcrumb unread before
an Akamai block interrupted verification — file status `partial`). Clean
absences: Cox & Cox (SR 51, only percent-off sale rooms, no clearance
taxonomy anywhere — matches the brief's own worked exclusion example
verbatim) and The White Company (SR 59, plain temporary Sale + two
confirmed-empty Last-Chance nodes). Clean hits worth noting: The Citizenry
(SR 53, Archive Sale 59 + 6 verified children, "final run"/"final batch"
copy = genuine permanent clearance); Pottery Barn Kids UK (SR 58, cleanly
separated a 513-item permanent Clearance branch from a 979-item temporary
Deals branch); West Elm UK (SR 57, 13 rows, correctly separated "Autumn
Sale" and generic "Save 50% or More" from the real Clearance taxonomy
branch); CB2 (SR 56, 9 rows, Clearance pages needed Claude-in-Chrome —
hard 403 at HTTP/Playwright tiers).

**Batch 7 (SR 61-70) done and merged 2026-09-08.** 50/70 cumulative
companies have Clearance, 20/70 absent after real investigation. 290 leaf
rows, 72 Review rows. 4 new ambiguous-Sale/Clearance flags: SR 64 Lulu and
Georgia "Sale" (287, site never uses "Clearance"/"Outlet" anywhere in 845
collections but a per-product "Final Sale" Algolia facet hints at genuine
permanent markdowns mixed in — too mixed to call confidently); SR 67 Burrow
"Labor Day Clearance" (42, flat breadcrumb not nested under the genuine
"Warehouse Sale" taxonomy, homepage banner calls it a seasonal "SALE"); SR
62 Rejuvenation "Vintage"/clearance-sale-vintage (141, mixed
`productPriceType` values, only 48% product-ID overlap with the confirmed
"All Clearance" node, sits as a sibling not a child). SR 63 Serena & Lily
came back `partial` — the site's own main nav literally has a top-level
"Clearance" menu (decisive per the Sale-vs-Clearance test) but every qty is
null/flagged because the product grid needs a browser session token and
Claude-in-Chrome was unstable this session (shared-tab-group contention
from other concurrent workers, not a site block). SR 68 Joybird found a
genuine permanent Clearance taxonomy node (own breadcrumb + heading,
distinct from a separate temporary /sale/ page) that is currently
zero-inventory — correctly dropped rather than emitted as qty:0. Clean
absences: Cox & Cox precedent continues — Heal's had one nav-only
"Clearance" family with a same-condition cross-cutting listing
("Practically Perfect and Perfect Clearance") not itself in nav, kept as
a leaf; The Inside (SR 66) confirmed absent — the only lead was an obvious
sitewide 25%-off promo banner, not ambiguous enough to even flag.

**Batch 8 (SR 71-80) done and merged 2026-09-08.** 56/80 cumulative
companies have Clearance, 23/80 absent, 1/80 blocked (SR 79 QVC Home — 5
real Clearance-taxonomy URLs identified via sitemap, all qty null since the
site is hard-blocked at every tier). 316 leaf rows, 83 Review rows. New
ambiguous flags: SR 74 Garnet Hill (all 5 rows flagged — genuine mixed
signal, breadcrumb/pageHeader say "Sale" throughout while URL
slug/meta say "clearance"); SR 80 HSN Home ("New Markdowns"/"Just Reduced",
2 of 5 rows — read more like recent-price-drop feeds than confirmed
permanent clearance despite nesting under HSN's own Clearance nav). Clean
absences: Urban Outfitters Home (2 candidates opened and excluded outright,
not flagged — one an explicit temporary promo, one a sitewide apparel-led
low-stock page, neither Home-scoped or permanent); Scully & Scully
(thorough 24,365-URL sitemap sweep, zero clearance-taxonomy matches). Clean
hits worth noting: Container Store Decor (907 parent + 9 departments,
correctly dropped a percent-off cross-cut node as a re-slice not a genuine
department); Bloomingdale's Home (39, breadcrumb literally reads "Sale /
Home / Clearance" — decisive under the Sale-vs-Clearance test); TJ Maxx
Home (739, single live-drift discrepancy of 1 item between two independent
count sources, documented not treated as an error).

**Batch 9 (SR 81-90) done and merged 2026-09-08.** 64/90 cumulative
companies have Clearance, 25/90 absent, 1/90 blocked (still SR 79). 360
leaf rows, 105 Review rows (a big jump — see below). Fixed the same
`ledger_status()` partial+zero-rows bug documented in
[[bestsellers-clearance-new-arrivals-scaffolded]] / the Bestsellers
qa_notes; also fixed one non-ASCII "Décor" -> "Decor" in cl82.json before
archiving. SR 82 La Redoute UK's Clearance came back `partial` (9 rows, all
null qty) — a Cloudflare "Country challenge" CAPTCHA blocks every `/pplp/`
listing page, confirmed at all 3 tiers with a rendered screenshot; the
worker correctly refused to solve it and recorded the real, site-confirmed
Clearance taxonomy (found via the reachable `/outlet.aspx` hub) with
null+flagged qty rather than guessing. This is the batch's Review-row
driver: SR 82's 9 rows + Barker and Stonehouse's 17-row Clearance (both
main-site 10 nodes + a genuinely distinct second outlet-microsite domain,
5 more nodes) together account for a large share of the 105 total. Clean
absences: Marks & Spencer Home (sitewide clearance hub has zero Home
category node, confirmed via product-sample check, not just facet
absence). Notable finds: Loaf ("The Loaf Outlet | Clearance", 423 parent +
3 children); Furniture Village (32, children sum to exactly 32, a clean
non-overlapping partition, cross-validated across two independently-
geolocated fetches after the site force-redirected through a geo-IP store
filter); Next Home (513, reached via the site's own `/nextsale` hub's
explicit "CLEARANCE / FURTHER REDUCTIONS" section, distinguished from the
generic upper "SALE" section — the resulting search-style URL triggered
this batch's one "suspect URL" verify note, informational only, same
benign pattern as the standing Home Centre `?q=badge` case).

**Batch 10 (SR 91-100) done and merged 2026-09-08 — 100/286 milestone.** 71/100
cumulative companies have Clearance, 28/100 absent, 1/100 blocked (still SR
79). 377 leaf rows, 106 Review rows. 1 new ambiguous flag: SR 96 Maisons du
Monde "Seconde Chance" (376, permanently discounted vs "Neuf" price but
every item is condition-graded used/returned/ex-display stock — closer to
a graded resale channel than genuine new end-of-line, so flagged rather
than guessed either way; its sibling "Braderie" passed cleanly with no
condition facet). Clean absences: AM.PM France (no Soldes/Destockage/Outlet
node anywhere in nav; the only "outlet" lead redirects to La Redoute's
separate apparel-only micro-site with zero AM.PM presence); La Redoute
Interieurs FR (the brand's own "Outlet" tab resolves to a live seasonal
"French Days" promo carousel — page title itself literally confirms it's
the campaign, not permanent clearance). Access note worth flagging: the
laredoute.fr/.co.uk domain family's previously-working WebFetch bypass of
the Cloudflare block no longer works as of this batch — only Claude-in-
Chrome got past it for both AM.PM and La Redoute Interieurs FR this
session; watch for this on any future laredoute.* SR. Clean hits: Conforama
FR ("Destockage", 9 rows, parent cross-checked via seller-facet sum);
Camif ("Destockage" family, 3 rows, breadcrumb-linked parent+children);
Westwing UK ("Last Chance", 1551, double-matched via header+footer count).

**Batch 11 (SR 101-110) done and merged 2026-09-08.** 77/110 cumulative
companies have Clearance, 32/110 absent, 1/110 blocked (still SR 79). 417
leaf rows, 108 Review rows. 2 new ambiguous flags: SR 102 Fleux "Braderie"
(31, nav label literally says clearance wording but on-page copy is an
explicitly dated ~4-week seasonal campaign — textbook default-exclude case
per the brief, so flagged rather than force-excluded); SR 108 Connox (7573,
plain "Sale" label on both locales but the English page's own meta
description mentions "discontinued lines" — a genuine partial permanence
signal). Standout clean exclusion: KARE (SR 109) — the site's own FAQ copy
on its "Sale" page explicitly disclaims being remainder/clearance stock,
the strongest possible negative evidence for the Sale-vs-Clearance test
seen in the project so far. Clean hits: Hoeffner (16 rows via
"Lagerraeumung", filter narrowing independently verified: Sofas 13
filtered vs 1227 unfiltered); XXXLutz DE (23 rows via "Abverkauf",
exhaustion-verified across all 22 leaves); Westwing DE and IKEA DE both
reproduced their UK siblings' exact Clearance patterns ("Last
Chance"/"Letzte Chance"). Clean absences: Zara Home DE (Special Prices page self-describes as Sale,
no permanence language, matching Zara Home UK's identical finding), Butlers
(zero matches across 173 collections, both markdown-adjacent candidates
unambiguously generic/seasonal), The Socialite Family (a prior-pass
"dernieres-pieces" clearance candidate has since been
deleted/unpublished — a useful signal that this site's merchandising pages
churn between passes).

**Batch 12 (SR 111-120) done and merged 2026-09-08.** 82/120 cumulative
companies have Clearance, 37/120 absent, 1/120 blocked (still SR 79). 446
leaf rows, 109 Review rows. 2 new ambiguous flags: SR 116 Maisons du Monde
BE "Voordeel Deals" (114, nav card says "last items/pieces" but the page's
own heading is generic "Bargain Deals" rather than an explicit Outlet/
Clearance label); SR 120 Casa Viva's "Special Price"/ofertas-permanentes
parent (flagged as a rollup grouping row despite strong "permanent offers"
taxonomy-id evidence, since the brief calls for human confirmation on
grouping-row calls). Made.com NL (SR 114) diverged from its own UK
sibling's precedent — UK's Clearance URLs were a dead empty template, but
NL's Next-platform brand facet exposes a small, real, independently
verified "Opruiming" listing (n=2) — a reminder not to assume identical
results across locales even for the same underlying platform issue. Clean
absences: HKliving (B2B/wholesale site, no consumer sale mechanism at
all); Juttu Home (correctly excluded Belgium's legally-named biannual
"Solden" period as temporary, plus a sitewide promo covering most of the
catalog); Kave Home (decisively excluded two seasonally-named "Rebajas"
selections with complete negative evidence, not even flagged ambiguous).
Clean hits: fonQ (10 rows via a genuine "Outlet" structure, every child a
plausible 4-51% subset of its department); Sklum (15 rows, page title
literally "Outlet muebles..."); Casa Viva correctly distinguished its
small "Special Price" clearance concept from a much larger 1029-item
storewide "Rebajas" seasonal sale spanning virtually the whole catalog.

**Batch 13 (SR 121-130) done and merged 2026-09-08.** 89/130 cumulative
companies have Clearance, 40/130 absent, 1/130 blocked (still SR 79). 476
leaf rows, 118 Review rows. 2 new ambiguous flags: SR 128 Nkuku "Sale" (36,
generic promo label but H1 says "The Home Archive" — genuine unresolved
permanence signal); SR 126 Anthropologie UK (9 rows — the entire site
never uses clearance/outlet/final-sale language anywhere despite a
persistent multi-level "Sale" taxonomy, so every row recorded per the
brief's ambiguity guidance rather than guessed). Denby (SR 124) confirmed
genuinely absent for the most extreme possible reason — the whole
storefront is dead (company in administration since 31 March 2026, every
URL serves a static legal notice). Clean hits worth noting: Pooky (400 via
"Last chance," classified Clearance despite a "/sale" URL slug because the
nav label and og:description both explicitly frame it as permanent
end-of-line stock); Coincasa (7 rows via a genuine but currently
nav-unlinked "Outlet" section — still live and sitemap-indexed, flagged
for reviewer awareness); Moemax Germany found a genuine but structurally
different Clearance concept from its XXXLutz-group sibling ("Filialschnaeppchen"/
Branch Bargains, 1041, vs. XXXLutz's "Abverkauf" hub) — a reminder that
even same-group siblings shouldn't be assumed to share the same
merchandising structure; Castorama France (13 rows via "Destockage
massif," on-page copy explicitly confirms permanent markdown "in the limit
of stock per store").

**Batch 14 (SR 131-140) done and merged 2026-09-08.** 95/140 cumulative
companies have Clearance, 43/140 absent, 2/140 blocked (SR 79, SR 134
Leroy Merlin France — see Bestsellers qa_notes for the full access-block
writeup). 486 leaf rows, 121 Review rows. 2 new ambiguous flags: SR 132
DEPOT "Sale" (782, generic heading but some items carry a "permanently
cheaper" badge — sub-department children not individually opened since
the parent is itself unresolved); SR 138 Mango Outlet's "Descuentos
especiales" (23, "rebajas" wording could be a temporary extra-discount
promo despite sitting inside the Outlet site's permanent nav). Clean hits
worth noting: JYSK Denmark (372 via "Outlet," on-page copy explicitly says
"discontinued items... while stock lasts" — first Danish site, went
cleanly); H&M Home France found a decisive "Last Chance" signal
(`sale:"oldSale"` internal flag, standing node across every department) —
cleaner than either the UK sibling's ambiguous finding or the IT sibling's
total absence; IKEA France correctly distinguished "Offres Outlet"/Last
Chance (86, genuine discontinuation signal) from a "Prix baisse" everyday-
low-price campaign (423, no discontinuation signal) and confirmed France
never uses the regulated "Soldes" term in nav at all. Clean absences:
RoyalDesign (Outlet is only a per-product badge, not a filterable
listing); Nordic Nest (both candidates cleanly excluded as generic
temporary promos, one explicitly grouped with Black Friday/Cyber Monday);
Xenos (the only outlet-redirect page explicitly refreshes biweekly with
new flyer offers — unambiguous rotating-promo language).

**Batch 15 (SR 141-150) done and merged 2026-09-08.** 100/150 cumulative
companies have Clearance, 48/150 absent, 2/150 blocked. 495 leaf rows, 123
Review rows. 2 new flags: SR 149 Seletti ("Sales"/last-chance URL slug but
generic label, no permanence language — 134); SR 142 Sostrene Grene
"Sidste chance" (qty left null+flagged since it's a personalized
algorithmic feed with no site-reported total, not a real access failure).
SR 145 Galeries Lafayette resolved from `partial`/null to `ok`/qty=3 after
a required tier-3 (Claude-in-Chrome) escalation the worker initially
skipped — see Bestsellers qa_notes for the full writeup; watch for workers
that report `partial` with an unexercised tier 3 in their own narrative.
Clean absences worth noting: BHV Marais Maison (the one candidate,
"Soldes," is a currently-empty statutory French sale-period page,
correctly dropped rather than kept at qty:0); Zara Home France made it
another consistent no-Clearance locale (temporary-discount copy, matching
UK/DE/ES exactly). Clean hits: Monoprix Maison (5 rows via a genuine
sitewide "Outlet" branch, correctly dropped an empty "Derniere chance"
node); Finnish Design Shop (667 via "Outlet," first Finnish Clearance hit,
on-page copy explicitly says "discontinued... while stocks last");
Iittala's Clearance taxonomy is real but all 4 pages currently show "THE
CAMPAIGN HAS ENDED" with zero products — correctly dropped, not kept.

**Batch 16 (SR 151-160) done and merged 2026-09-08.** 104/160 cumulative
companies have Clearance, 54/160 absent, 2/160 blocked. 512 leaf rows, 130
Review rows. 2 new ambiguous flags: SR 155 Manufactum "Sale" (459, meta
copy genuinely ambiguous between rolling clearance and generic discount);
SR 152 Broste Copenhagen "Mid Season Sale" (74, mixes clearance language
"discontinued designs" with dated %-off campaign signals). Notable "Udsalg
trap" catch: SR 158 Georg Jensen found live `/udsalg/*` listing pages but
every one is explicitly titled/dated "Summer Sale 2026" with an expiry —
exactly the danger the brief warns about for Danish sites, correctly
excluded rather than assumed-clearance from the URL wording alone. Real-
but-currently-empty findings (dropped per the zero-product rule, not kept
at qty:0, each fully documented): AmbienteDirect's "Outlet" node (genuine
separate taxonomy from Sale, proving the site does distinguish them, but 0
products); Bloomingville's B2B Outlet page (real, login-gated, 0 products
publicly); House Doctor's 3 named Sale collections (all confirmed empty).
Clean hits: Merci Paris (10 rows via "Derniere chance," clearly
distinguished from France's dated "Soldes"); Dille & Kamille (93 via
"/discounts/," reached after the network-egress workaround, strong
on-page permanence signal despite a non-obvious page title).

**Batch 17 (SR 161-170) done and merged 2026-09-08.** 113/170 cumulative
companies have Clearance, 55/170 absent, 2/170 blocked. 531 leaf rows, 138
Review rows. 3 new ambiguous flags, all UAE-region "sale wording without
confirmed permanence" cases: SR 167 OC Home's "DSS Final Sale" (177,
correctly recognized DSS = Dubai Summer Surprises, an annual regional
seasonal campaign, despite the "Final Sale" wording); SR 170 Tanagra's
"Last Chance Exclusives" (616, every sampled product shows zero actual
discount — scarcity marketing vs. genuine clearance, a real judgment
call). Notable regional pattern: UAE retailers frequently use
"Sale"/"Final Sale"/"Last Chance" language for campaigns tied to named
seasonal events (DSS = Dubai Summer Surprises) rather than permanent
markdown concepts — worth extra scrutiny on any UAE "sale" page before
accepting the wording at face value. Clean hits: Home R Us UAE (435 via
"Last Chance," kept unflagged despite mixed "Sale" title wording since
it's a standalone permanent nav category — judgment call documented, not
force-flagged); IKEA UAE (874, matching all IKEA siblings); Crate & Barrel
UAE (9 rows, careful parent/child dedup check confirmed near-identical
product sets, avoided double-counting); Serax (5 rows via a genuine
evergreen "Archive Sale" program, correctly distinguished from Black
Friday promo collections via ongoing publish-date rotation). Clean
absences: Pols Potten (6+ sale-adjacent candidates individually checked
and excluded as dated/orphaned/non-permanent).

**Batch 18 (SR 171-180) done and merged 2026-09-08.** 122/180 cumulative
companies have Clearance, 56/180 absent, 2/180 blocked. 614 leaf rows, 159
Review rows — a big jump this batch, mostly UAE ambiguous-wording cases
and Chattels & More's flagged rows. 3 new ambiguous flags beyond Chattels
& More (see Bestsellers qa_notes for that company's full writeup): SR 172
The Bowery Company (228, careful investigation found page chrome says
generic "Sale" but 100% of sampled product badges literally read
"Clearance sale" — genuine tension, correctly flagged); SR 178 Target
Australia's Clearance came back `partial` — parent verified (811) but all
11 confirmed-genuine child categories got Akamai-blocked mid-session,
correctly recorded null+flagged rather than dropped since their existence
is independently confirmed (candidate for a later retry from a different
session/IP); SR 180 David Jones found a genuine site-defined
"clearance_flag" facet (1572) distinct from a much larger generic Sale
listing, verified live via Playwright, but no bookmarkable filtered URL
exists so it links to the parent page with an explanatory flag. Clean
hits: Beacon Lighting (12 rows, confirmed permanent-markdown taxonomy via
breadcrumbs); Temple & Webster (15 rows, correctly distinguished a 35,492-
item generic Sale roll-up from the genuine 1,893-item badged Clearance
node); Kmart Australia (1413, unambiguous top-level nav tab); Nitori Japan
(36 rows via a genuine regionally-partitioned Outlet concept for
returned/repaired stock, one zero-qty category correctly dropped); MUJI
Japan's "Mottainai Ichi"/No-Waste Market (57, a culturally-specific
permanent outlet program, correctly distinguished from the generic "SALE"
page). Clean absences: Aura Living UAE (decisively excluded a real "Sale"
section after specifically checking for DSS-style campaign wording and
finding none).

## Batch 18 (SR 181-190) — first APJ/US-warehouse-club batch

First batch to hit Australia, Singapore, and Japan (see bestsellers
qa_notes for the full market-mix list); 0 non-ASCII cells from both
Japanese sites.

Clean hits: IKEA Japan (897, Last Chance, double-confirmed via ARIA count
text + JSON totalCount, filter query param proven client-side only so the
canonical unfiltered URL was used); House Australia (734, own metaTitle
literally "SALE: HOMEWARES CLEARANCE SALE"); Castlery Singapore (183,
"while stocks last" permanence language); Country Road Home (43, on a
dedicated outlet.countryroad.com.au subdomain, correctly distinguished
from a "MID SEASon sale" temporary promo on the main site); Myer Home
(10 rows: an 8-department "Home Clearance" hierarchy summing to 488, PLUS
a second, distinctly-categoryId'd "Home Clearance" listing at 321 reached
via a different nav path — kept as separate rows since counts genuinely
differ, not an alias).

Ambiguous/flagged (Review): Freedom Australia's "Sales & Clearance" hub
(525) flagged because its 8 clean clearance children only sum to 401 —
confirmed the 124-unit gap is non-clearance Sale inventory bleeding into
the hub (e.g. Sofas, which has no dedicated clearance child page); the 8
children themselves stayed unflagged since each has an unambiguous
clearance-taxonomy URL/title. HipVan: 4 rows flagged (Display Pieces
Up to 80% Off/As-Is Home Office/2 Warehouse Sale pages) — all real PLPs
with exact counts but titled "Sale"/"As-is"/"Warehouse Sale" rather than
literally "Clearance", each judgment individually reasoned rather than
uniformly included/excluded. Francfranc Japan's BAZAR (391) flagged
despite living under an "Outlet Products" nav heading — its own blog
mentions BAZAR-exclusive new SKUs, an exclusive-SKU wrinkle worth human
judgement.

Sam's Club: found the site's real Clearance PLP (246, stable across 6
fetches) but excluded it — its own Product Type facet is
apparel/electronics/grocery-dominated with only 1 incidental
furniture-tagged item, failing this project's home/decor scope test.

Costco: see bestsellers qa_notes' Costco writeup — orchestrator follow-up
found the "While Supplies Last" nav entry (Costco's closest analogue to a
clearance concept, COSTID-tagged so a genuine backend campaign, not
literal free-text search) but it has no dedicated bookmarkable
department-scoped URL — a keyword-search view over the whole catalogue
(121 results, Furniture:1/Home & Kitchen:18 facets) with no way to isolate
a clean home-decor subset. Recorded as no confirmed rows rather than
guessing a number; status upgraded blocked->partial, ledger classification
unchanged.

## Batch 19 (SR 191-200) — US big-box + Canada, first Etsy marketplace test

Clean hits: Sur La Table (147, permanent `Sale > Clearance` taxonomy node
despite the `/sale/` URL path, 3 redirect aliases correctly folded in);
Indigo Home (229, "Lifestyle & Gifts" clearance child, unambiguous since
nav explicitly names the section Clearance — no recurrence of the
duplicate-link defect flagged for this exact company in an earlier
category project, confirmed by checking all 3 sibling workbooks'
SR200 rows have distinct links); Kohl's Home (5 rows via Claude-in-Chrome
tier 3 after Akamai blocked HTTP+Playwright: hub + 3 department children
summing correctly, 1 thin facet-combo row flagged for volatility).

Clean absence: Structube's "Sale" (990 products) correctly excluded as a
generic percent-off promo with no permanence wording — textbook exclude,
not flagged.

Flagged (Review): Structube's "Open Box" (22) — GraphQL total_count says
140 but the rendered storefront only shows 22, likely regional
availability filtering; Walmart's "All Home Clearance" facet proven
non-functional (capped count statistically identical to the unfiltered
Home baseline, i.e. the facet isn't actually restricting anything) but
kept as a row since it's genuinely site-labelled Clearance; JCPenney's
"Home Closeouts" (194) flagged since the site's own label is "Closeout"
not literally "Clearance" — included per the brief's Outlet/End-of-Line
equivalence but flagged for human confirmation; Sur La Table's Clearance
header (147) vs. its own pagination footer (148) off by 1, unresolved
without product-level inspection.

Simons Maison: found `home-decor/sale--sale-6770` (80) but excluded
entirely (not even flagged) — grepped the whole page for permanence
language (final sale/last chance/end of line/discontinued/permanent) and
found none; it's mechanically identical to the site's "New" filter
family, present in every department including apparel.

## Batch 20 (SR 201-210) — Wayfair-family cluster + luxury/lighting retailers

Clean hits: Bouclair (177, nav-confirmed "Clearance" child of "Sale",
1 alias merged); Grandin Road (207, unambiguous outlet/clearance wording,
8 department children kept as leaves, 1 alias merged); Joss & Main
(252 "Closeout" — see bestsellers qa_notes' Wayfair-family
search-redirect-discovery writeup, applicable here).

Clean absences: Birch Lane and AllModern both genuinely absent (though
see the Birch Lane recheck flag in bestsellers qa_notes — not tried with
the search-redirect trick yet); Saks Home (thoroughly checked: 95-item
"Designer Sale" page has zero permanence/outlet wording, and a "clearance"
site-search returning 12,007 non-discriminating results confirmed no
dedicated taxonomy exists — genuinely absent, not even flagged as
ambiguous).

Flagged (Review): EQ3's "Spring Clearance Sale" (19) — explicit
"Clearance" in the H1/slug but nested among clearly-temporary campaigns
under an isPromo:true node; Lamps Plus's "Open Box" (8,401) — site nav
treats it as a Clearance sibling not child, flagged for human
adjudication on scope; Lumens' "Open Box Returns" (715) and "Warehouse
Sale" (5,114) — the latter's visible copy reads as temporary but its own
meta-keywords tag literally says "End Of the Year Clearance Sale"; Shades
of Light: 3 small sitemap-only "Sale"-named listings (3/2/2 items) all
flagged for generic naming + no live nav link, one auto-flagged by the
merge script's own Sale-vs-Clearance rule despite living under a
"Mirrors Clearance" category label (sub-category text alone drives that
rule, a known/accepted merge-script behavior, not a new bug).

## Batch 21 (SR 211-220) — high-end design/lighting + first India-market companies

**Merge-script bug found and fixed this batch — see bestsellers
qa_notes' full writeup.** Two historical rows silently missing from
Clearance.xlsx since their original batches now restored: **SR 49
Swoon's "Flash SALE" (799)** and **SR 55 Crate & Barrel US's "Kids
Clearance" (466)**. Both were genuine, already-extracted, already-
archived findings — this was a display bug in the merge, not a
re-extraction. Root cause: a lone/last leaf row mislabeled
`is_group:true` gets pruned as an orphan grouping row. Also fixed SR 214
Terrain's New Arrivals row (see new_arrivals qa_notes) with the same
pattern. Recommend a periodic full-archive is_group-orphan scan going
forward, not just spot-checking the current batch.

Clean hits: Hudson Valley Lighting (2358, strong "Outlet Sale" on-page
evidence); Design Within Reach (457, explicit "Clearance: Up to 50% Off"
H1); Milton (43, unambiguous "Clearance Sale" H1); Pepperfry (71, H1
"Last Chance to Buy" — correctly distinguished from a same-named decoy
category page with zero clearance vocabulary); Visual Comfort (8 rows:
Last Call + Open Box + 5 room children, 14 seasonal-campaign pages
correctly excluded).

Flagged (Review): 2Modern's "On Sale" (9335), Lightology's "Overstock"
(1042), Visual Comfort's "Last Look" (440, trade-exclusive staging list),
Cello World's "Sale" (52, sitemap-only, no permanence wording), Terrain's
"Sale - Garden" (24, same reasoning as its now-restored "Sale (All Sale)"
parent row — backend flags indicate genuine permanent markdown despite
generic "Sale" naming).

## Batch 22 (SR 221-230) — all-India batch, including 3 fashion marketplaces

Clean hits: IKEA India (67, "Last chance" — see bestsellers qa_notes'
6-locale-pattern writeup); FOS Lighting (142, distinctly nav-labeled red
"Clearance" separate from generic Sale, triple-cross-checked); Urban
Ladder (189, "Deal Zone > Clearance Sale" breadcrumb); Nestasia (3 clean
rows: 112/11/44, confirmed genuinely distinct via near-zero product-ID
overlap between them).

Clean absences: Myntra, Flipkart, AJIO (all 3 marketplaces genuinely
absent — see bestsellers qa_notes); Westside Home (existing Sale-Home
collection currently 0 products, correctly dropped not reported stale);
Vaaree (the only "clearance"-named URL actually resolves to an unrelated
rugs-brand page — a decoy, correctly excluded); H&M Home India (only
candidate's own page heading is literally "UPTO 70% OFF", the brief's
textbook example of generic-promo-to-exclude).

Flagged (Review): Nestasia's 4th Clearance listing ("Exclusive/End of
Season", 1570) — title says Clearance but on-page H1 says "End of Season
Sale", and its size dwarfs the other 3 genuine clearance listings
(112/11/44 vs 1570), suggesting a broad seasonal event rather than
targeted clearance stock.

## Batch 23 (SR 231-240) — second all-India batch

Clean hits: Jainsons Lights (428, explicit "stock clearance Scheme"
wording, exhaustive count overriding inflated raw field); Pottery Barn
India (3 clean rows: parent 16 + 2 non-overlapping department children,
9+7=16 confirming real sub-structure).

Clean absences: Clay Craft India, Ankur Lighting, @home by Nilkamal,
Borosil, Pure Home + Living, Nykaa Fashion Home — all confirmed via the
Sale-vs-Clearance test (generic percent-off/seasonal campaigns with zero
permanence signal, or zero clearance-taxonomy nodes anywhere in the
catalogue).

Flagged (Review): WoodenStreet's "Furniture Sale" (117, breadcrumb says
Sale but SEO title says Clearance); Fabindia's 2 rows (864, 7 — a
permanent standing nav section sibling to New Arrivals, but the word
"Clearance" never appears anywhere on the site); Pottery Barn India's
"Open Box & Outlet Deals" (5, outlet-style content but nested under the
generic Sale nav branch rather than Clearance).

## Batch 24 (SR 241-250) — third all-India batch

Clean hit: Mason Home (19, "Last Chance"/"Final Call" nav item with
outlet/limited-stock framing, exhaustive count overriding an inflated
site field).

Clean absences: Tata CLiQ Luxury Home, Zara Home India (see bestsellers
qa_notes' /ww/-catalogue writeup), Home Centre India (only an internal
CMS slug/analytics ID says "Clearance" — never customer-visible, so
correctly treated as absent not ambiguous), HomeStop, Meesho, Address
Home (confirmed via a discriminating-search test), Chumbak, Ikiru — all
via thorough Sale-vs-Clearance testing, no permanence signal found.

Flagged (Review): Wonderchef's 2 rows (a "Renewed" recommerce program
and an "EOL Product Sale" — both conceptually outlet/end-of-line but
neither uses the literal brief wording, and both are sitemap-only/
unlinked from nav).

## Batch 25 (SR 251-260) — fourth all-India batch

Clean hit: Whispering Homes (2 rows, both with explicit "Clearance Sale"
in their own title tags — a clean example of the Sale-vs-Clearance test
working as intended).

Clean absences: ellementry, West Elm India (see bestsellers qa_notes'
franchise-platform writeup), The White Teak Company, The Bombay Store,
Beruru (predictive-search API returned empty collections for every
clearance-family term, a stronger absence signal than usual), Good Earth
— all confirmed with zero ambiguity, no flags needed on any of them.

Flagged (Review): The Decor Kart's entire 6-child "On Sale" family
(15-416 each) all flagged uniformly — no permanence/outlet wording
anywhere across 639 collections checked; Freedom Tree's "Deep Discounts"
(231) — page itself says only "Deep Discounts" but the nav copy linking
to it literally says "Last Chance-Upto 50% off", a genuine wording
conflict between two site surfaces; India Circus's clearance-sale.html
(153) — URL slug says clearance but every live surface (breadcrumb, nav
label, title tag) currently badges it "Monsoon Sale"/"End of Season
Sale", a clear seasonal-seasonal-campaign signal despite the permanent-
sounding URL.

## Batch 26 (SR 261-270) — fifth all-India batch

Clean hit: Sarita Handa's "The Final Few" (438 parent + 8 children) — a
genuinely permanent end-of-line concept with explicit "won't return"
copy, no flag needed; the strongest, cleanest Clearance example found in
the India-market run so far.

Clean absences: Oorjaa, The Purple Turtles, Orange Tree, Nicobar, Jaypore
(all thoroughly checked, generic seasonal Sale campaigns correctly
excluded, no permanence signal anywhere).

Flagged (Review): 4 companies each contributed exactly one ambiguous row
this batch, all following the same shape — Objectry's persistent-but-
plain "Sale" (32), Kapoor E-Illuminations' page says plain "Sale" but
nav anchor text says "Clearance Sale" (94), The Artment's page says
"Clearance" but its only on-site link is a "Flat 33% Off" promo banner
(21), SPIN's "Stock Sale" (19, distinct from its clean "Outlet" row) —
each a genuine wording/placement conflict between different site
surfaces rather than a clear-cut call either way.

## Batch 27 (FINAL — SR 271-285) — UK department stores + last stragglers, PROJECT COMPLETE

**Cross-company duplicate found and fixed — full writeup in bestsellers
qa_notes' Batch 27 section.** SR 82 "La Redoute UK" restored/corrected:
removed 4 out-of-scope fashion Clearance rows (Women's/Men's/Kids'/
Knitwear — a scoping mistake from an earlier session), replaced its
null/blocked home rows with SR 278's verified data (parent "Final
Clearance" hub at /outlet.aspx + Furniture Outlet clean + 3 flagged
Sale-worded home leaves). SR 278 emptied as fully redundant. This is
the reason `verify_clearance.py`'s strict duplicate-URL check failed
before the fix and passes clean after it.

**PROCESSING ERROR is now 0 — the full 285-company roster is done.**

Clean hits: The Range (2 rows, thin current stock but genuine); The
Conran Shop (3 rows: parent + 2 children, clean Clearance-vs-Sale pass);
Argos Home (2 rows: 1841 + 299, using the company's established
2-department stand-in convention from its earlier category-pass);
ProCook UK (1 row, unambiguous).

Clean absences: Wayfair UK (does not reproduce the Wayfair-family
search-redirect trick seen at Joss & Main); Lakeland; Harrods Home
(confidently absent, storewide sale correctly excluded); Selfridges
Home; Liberty London Home (structurally proven via a disabled feature
flag); Home Box UAE (post-Cloudflare-breakthrough, genuinely absent).

Blocked (Claude-specific robots.txt, new this batch): home24 Germany,
El Corte Inglés Home, Made in Design, Amazon UAE.

Next: PROJECT COMPLETE. No further batches — see memory file for final
totals and the standing Review-sheet backlog.

## POLICY CORRECTION 2026-09-11 — Outlet is no longer treated as Clearance

**User-directed correction, retroactive cleanup of the full archive.**
Every prior batch above treated "Outlet"/"Clearance Outlet" as a valid
target term (per the original brief) and several clean hits/flags above
reference that ("Sklum, page title literally 'Outlet muebles'", "fonQ, 10
rows via a genuine 'Outlet' structure", "JYSK Denmark (372 via 'Outlet')",
"Country Road Home ... on a dedicated outlet.countryroad.com.au subdomain",
"IKEA France correctly distinguished 'Offres Outlet'/Last Chance", "Loaf
('The Loaf Outlet | Clearance')", "Coincasa ... via a genuine ... 'Outlet'
section", "Nitori Japan (36 rows via a genuine ... Outlet concept)",
"Francfranc Japan's BAZAR ... living under an 'Outlet Products' nav
heading", "Hudson Valley Lighting (2358, strong 'Outlet Sale' on-page
evidence)", "Lamps Plus's 'Open Box' ... its own <title> says 'Outlet
Deals'", "Monoprix Maison (5 rows via a genuine sitewide 'Outlet' branch)").
**As of this correction, all of those are excluded.** `rules/clearance.md`
§1/§2/§3.2, `CLEARANCE_BRIEF.md`, `merge_clearance.py` (new `OUTLET_BAN`
hard-drop) and `verify_clearance.py` (new `OUTLET_LEAKED` assertion) were
all updated so future batches apply this from the start.

**Removal criterion applied:** a row is dropped if the page's own branding
— its `<title>`, H1, breadcrumb/nav label, or a distinct outlet storefront/
subdomain — identifies it as Outlet, regardless of how clearance-like the
underlying stock is (permanent markdown / seconds / returns / end-of-line
does not save it). A row is KEPT if its own on-page name is genuinely
Clearance-family (Clearance, Clearance Sale, Final Clearance, Last Chance,
End of Line) even when the URL path happens to contain `/outlet/` or a
sibling umbrella nav label mixes both words — see §3.2's hybrid-department
rule (Crate & Barrel UAE / Frontgate / Grandin Road / Blu Dot precedents
below).

**117 rows dropped across 26 companies (first pass, sub_category itself
said "Outlet"):** SR2 West Elm US (1: Open Box Outlet Deals); SR14 Ashley
Furniture (8: Outlet + 7 dept children); SR20 Bloomr (6, company now
0 rows); SR46 John Lewis (1: Home Outlet Offers, now 0 rows); SR47 Dunelm
(1: Returns Outlet, 7 genuine Clearance rows kept); SR52 Williams Sonoma
(1: Outlet - Dining & Bar, Open Box row kept); SR62 Rejuvenation (1: Open
Box Outlet Deals, 2 rows kept); SR82 La Redoute UK (1: Furniture Outlet
child, parent Final Clearance + 3 Sale-flagged children kept); SR85 Barker
and Stonehouse (6: the separate "Store Clearance (Outlet Stores)"
microsite grouping, main-site 11-row Clearance kept intact); SR86 Loaf (4,
title 'The Loaf Outlet | Clearance | Loaf', now 0 rows); SR93 Rockett St
George (1, title 'Rockett St George Outlet', now 0 rows); SR95 Amara (1,
nav item + title 'Shop All Outlet at Amara', now 0 rows); SR111 fonQ (10,
now 0 rows); SR119 Sklum (15, title 'Outlet muebles...', now 0 rows —
**borderline, see below**); SR122 Coin.it (7, now 0 rows); SR138 Mango
Outlet (2, separate outlet storefront, now 0 rows); SR141 Monoprix (5, now
0 rows); SR143 Finnish Design Shop (1, now 0 rows); SR145 Galeries
Lafayette (1, now 0 rows); SR152 Broste Copenhagen (1, Archive Sale +
Mid Season Sale rows kept); SR174 MUJI (1, 'Mottainai Ichi
(Outlet/Returned-Goods Market)', now 0 rows); SR177 Nitori Japan (36, now
0 rows); SR187 Francfranc Japan (1: Outlet row; BAZAR removed separately
below); SR239 Pottery Barn India (1: Open Box & Outlet Deals, 3 genuine
Clearance rows kept); SR270 SPIN (1: Outlet, Stock Sale kept); SR280 The
Conran Shop (3, now 0 rows).

**9 more rows dropped (second pass, caught by reading page-title/H1/
subdomain evidence — the sub_category text alone didn't say "outlet"):**
SR49 Swoon "Flash SALE" (799, own meta_title 'Summer Outlet | Swoon');
SR133 JYSK Denmark "Clearance" (372, worker's own notes: "H1 'Outlet'" —
company's only row, now 0); SR140 IKEA France "Clearance" (86, own H1
'Offres Outlet', own `<title>` 'Offres outlet: fins de serie...' — company's
only row, now 0); SR186 Country Road "Clearance" (43, hosted on the
separate outlet.countryroad.com.au subdomain — company's only row, now 0);
SR187 Francfranc Japan "BAZAR" (391, grouped by the site's own
category-accordion tree directly under its 'アウトレット商品'/"Outlet
Products" heading — company now 0 rows total after both SR187 removals);
SR205 Lamps Plus "Open Box" (8401, own `<title>` 'Open Box Lighting -
Outlet Deals').

**Total: 126 rows removed across 27 companies.** `merge_clearance.py`'s new
`OUTLET_BAN` regex now drops any future row whose own sub_category/category
text contains "outlet" automatically; the second-pass cases (title/H1 says
Outlet but the row's own name doesn't) remain something only a worker's own
page-content reading, not a regex, can catch — flag those explicitly in
`notes`/`flag` going forward per the updated brief.

**Hybrid "Clearance & Outlet" departments — kept, per §3.2, not removed:**
these all have an umbrella nav/SEO label mixing both words, but every
individual leaf listing's own H1/breadcrumb/API-slug is cleanly
Clearance-branded, so the leaves survive: SR168 Crate & Barrel UAE (parent
row 'Clearance & Outlet' auto-dropped by `OUTLET_BAN`, all 8 genuine
`*-clearance-*`-slugged children kept intact); SR27 Blu Dot (SEO `<title>`
suffix '... - Clearance & Outlet | Blu Dot' appears on every Sale-family
page uniformly, but the actual collection names are 'Last Chance'/'Last
Chance - <dept>'/'Warehouse Sale', none outlet-branded — kept as-is); SR35
Frontgate (every URL sits under `/sale/outlet/...` but every page's own H1
override is genuinely '<Dept> Clearance' — kept as-is); SR210 Grandin Road
(URL slug `/grand-finale-outlet/` but the site's own nav entry/API
categoryName is 'Clearance'/'Final Clearance' — kept as-is, matches the
existing Batch-20 "unambiguous outlet/clearance wording" note above, which
in hindsight undersold that this is genuinely Clearance-branded on-page,
not Outlet).

**Borderline calls flagged here for human reconsideration, not resolved
unilaterally beyond the call already made:**
- **SR119 Sklum** — removed (15 rows, ~4160 products). Its own page
  `<title>` is 'Outlet muebles | Precios bajos en muebles - SKLUM' and body
  copy repeatedly self-describes as 'el outlet de muebles online', which is
  why it was removed under the same rule as SR86/93/95/133/140/186/205 (own
  title/H1 says Outlet). But unlike those, its **on-page H1 is 'Special
  Price'**, not 'Outlet', and its 14 child rows are all named 'Special
  Price <dept>' with zero outlet wording of their own — structurally closer
  to the SR168/SR27/SR35/SR210 hybrid pattern that was kept. If a reviewer
  judges the H1 ('Special Price') should control over the `<title>` tag
  here (the same way it did for those four), this entire company's 15 rows
  should be restored.
- **SR55 Crate & Barrel US "Kids Clearance" row (466 products)** — KEPT,
  not removed, but flagged here as genuinely mixed: its own H1 is 'Up to
  60% off Kids Clearance & Outlet' and `<title>` ends '...Home Decor Outlet
  | Crate & Kids' — Outlet is explicitly co-equal in the page's own
  branding, and there is no separable pure-Clearance-only subset of this
  single 466-count listing (unlike SR168/27/35/210 where the outlet wording
  lived only at an umbrella level above cleanly-Clearance-named leaves).
  The other 10 Crate & Barrel Clearance rows in the same company (Furniture
  Clearance, Outdoor Clearance, etc.) are cleanly Clearance-only with no
  outlet mention. A reviewer may reasonably decide this one row should be
  dropped or split out.

Re-merged and re-verified after both passes: `merge_clearance.py` ->
`Output` 869 rows / 646 leaf / 64 grouping / 158 companies-with-rows,
`Processing Ledger` 285 rows (157 CLEARANCE FOUND / 121 NO CLEARANCE FOUND
/ 7 BLOCKED, 0 PROCESSING ERROR), `Review` 191 rows. `verify_clearance.py`
-> OK: 0 cross-company duplicate URLs, 0 nav/marketing leaks, 0
Outlet-branded leaks, all 12 pre-existing protected workbooks + Final
Company List unchanged, Bestsellers.xlsx/New_Arrivals.xlsx untouched.

## POLICY CORRECTION 2026-09-11 PASS 3 — Open Box removed too, SR217 link rot fixed

**User directive: Open Box is not Clearance either — same hard-exclude
treatment as Outlet.** `rules/clearance.md` §1/§2, `CLEARANCE_BRIEF.md`,
`merge_clearance.py` (new `OPEN_BOX_BAN` hard-drop) and
`verify_clearance.py` (new `OPEN_BOX_LEAKED` assertion) all updated.

**8 rows dropped across 5 companies:** SR52 Williams Sonoma Home ("Open
Box", 204 — company's only row, now 0 rows; its worker status was already
`partial`/Akamai-blocked before this qty was removed, so its ledger status
correctly reads BLOCKED/ACCESS FAILURE now, not NO CLEARANCE FOUND — the
underlying investigation was genuinely never completed); SR193 Structube
("Open Box", 22 — company's only row, now 0); SR208 Lumens ("Open Box
Returns", 715 — "Warehouse Sale" (5114) kept, already separately flagged
ambiguous Sale/Clearance); SR217 Visual Comfort (6 rows: "Open Box" parent
+ Ceiling/Floor/Outdoor/Table/Wall children, 917/236/12/31/51/249); SR252
Whispering Homes ("Open Box Clearance Sale", 25 — "Clearance Sale (40% Off)"
(245) kept).

**SR217 Visual Comfort — link-rot fix (user-reported "links not working"):**
the site was restructured since original extraction; every old
`https://www.visualcomfort.com/us/c/sale/*` URL now 404s. Verified against
the live site (2026-09-11):
- `Open Box` and its 5 department children — removed per the Open Box
  policy above regardless of link status.
- `Last Look` — its new-site path `/sale/last-look/` also 404s, and the
  current `/sale/` hub's own on-page copy no longer mentions "Last Look"
  anywhere (only "Last Call and Open Box sales are final") — genuinely
  discontinued by the site, not just a broken link. Dropped entirely.
- `Last Call` — kept. Confirmed live at a new URL,
  `https://www.visualcomfort.com/sale/last-call/` (200 OK, H1 "Last Call",
  meta description "Save up to 70% off Last Call styles!"). Link corrected
  to this URL. The old qty (417) could not be re-verified against the new
  page — it's now a client-rendered SPA with no server-rendered product
  count in the raw HTML (the category id 22986 seen in the markup is not a
  product count) — so qty was nulled and the row flagged
  `MANUAL REVIEW: LINK ROT` pending a live re-check (would need Playwright
  to render the SPA and read the actual count).

SR217 now has exactly 1 row (down from 8), all with a corrected link.

Re-merged and re-verified after this pass: `Output` 856 rows / 636 leaf /
63 grouping / 156 companies-with-rows, `Processing Ledger` 285 rows (155
CLEARANCE FOUND / 122 NO CLEARANCE FOUND / 8 BLOCKED, 0 PROCESSING ERROR),
`Review` 188 rows. `verify_clearance.py` -> OK: 0 cross-company duplicate
URLs, 0 nav/marketing leaks, 0 Outlet-branded leaks, 0 Open-Box leaks, all
12 protected workbooks unchanged.

**SR122 Coincasa/Coin.it language question (user-reported):** already
resolved as a side effect of the Outlet cleanup above — SR122's only
findings were 7 Italian-named Outlet rows (`Outlet Casa`, `Tavola e Cucina
Outlet`, etc.), all removed in PASS 1/2. SR122 now has 0 Output rows (its
genuine "SALDI" page was already correctly excluded as a generic seasonal
sale in the original pass, per the ledger note) — no Italian text remains
anywhere in Output for this company; `verify_clearance.py`'s non-ASCII-cell
check confirms 0 for the whole workbook.
