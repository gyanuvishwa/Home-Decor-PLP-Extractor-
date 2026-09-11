# Bathroom QA notes — open adjudication log

Continued 2026-09-05 from a handoff done on another machine (SR 1-196,
"2026-09-01" checkpoint). The handoff delivered only `Bathroom.xlsx` +
`CHECKPOINT.json` + `SUMMARY.md` + `BATCH_BRIEF.md` + `BATHROOM_RULES.md` —
no per-company worker JSON, and its own pipeline (`bathroom_run/`, `report.py`,
`next_batches.py`, `apply_dedup.py`) does not exist on this machine. This
session rebuilt the missing archive layer (`b<SR>.json` per company, via
`rebuild_archive_from_xlsx.py`) and wired Bathroom into this project's normal
skill/pipeline structure (`.claude/skills/bathroom-extraction/`,
`pipeline/bathroom_json_archive/`) so SR 197-286 can continue the same way
every other category has.

---

## FIXED this session (not just flagged)

1. **Cross-category dedup gap.** The delivered run's "OPTION 1" dedup policy
   (CHECKPOINT.json) only checked new leaves against `Furniture.xlsx`. An
   audit (`build_cross_category_index.py` against all 8 other protected
   workbooks) found **182 leaf URLs** already recorded elsewhere: 120 in
   `Storage.xlsx`, 61 in `Wall_Decor.xlsx`, 1 in `Textile.xlsx`. Fix: extended
   the SAME already-declared policy to the full protected set via
   `cross_category_url_index.json`; `merge_bathroom.py` now routes any hit to
   `review[]` with `ALREADY EXTRACTED IN <file>` instead of `rows[]`, applied
   uniformly to the reconstructed SR 1-196 and every new SR. Nothing in
   Storage/Wall_Decor/Textile was touched — only `Bathroom.xlsx` changed.
   Seasonal.xlsx is deliberately EXCLUDED from the index (it is the one
   category allowed to overlap every other on purpose).
2. **English-only rule violation.** 27 companies (SR 96-99, 103-107, 117,
   119-120, 129-131, 133, 138-142, 145-146, 164, 174, 177, 184 — mostly
   France/Germany/Spain/Denmark/Japan sites) had `category`/`sub_category`
   left in the site's own language, sometimes as "English gloss (native
   original)", sometimes with no gloss at all — 602 affected strings across
   ~462 unique path segments. Fixed by translating every value to English in
   the `b<SR>.json` archive directly (not just the workbook, so it survives
   re-merges); verified via `check_english_only.py`.

## OPEN — needs a run-owner decision, not decided here

1. **Rule-24 residue back-catalogue — RESOLVED 2026-09-05.** All 8 named
   companies re-checked live with product-ID/facet-union proof of
   containment (never guessed): Fenwick +17, Manufactum +80 (5 disclosed as
   scales), Finnish Design Shop +370 (mirror residue correctly NOT added —
   proven to be Wall_Decor-owned), Target AU +30 (10 textile + 12
   beauty/bodycare cross-listings correctly excluded, exact 91-item
   reconciliation), Myer +60 and +17 (two separate parents), Sam's Club +4
   (1 hair towel correctly excluded), JCPenney +572 (largest single
   residue, full facet-union proof). Walmart US: the "~100 no-qty nodes"
   turned out to be the already-accepted (1000+)-cap trade-off, NOT a gap —
   but a genuinely separate coverage gap was found and fixed instead: 8
   missing toilet-seat/bowl subcategories (+3,681 products) that a stale
   sitemap catId had hidden. Net: leaf rows went from 1,307 to 1,377
   (+70 net rows, +~1,730 products) across this pass.
2. **Mirror-subset sweep** (SUMMARY.md item 2): the "record only when proven
   disjoint" decision (2026-09-01) has been applied to SR 176 only; the back
   catalogue (SR 1-175, 177-196) has not been re-tested for mirror/roll-up
   overlap.
3. **Compliance findings about prior passes, not this one** (SUMMARY.md item
   3) — flagged against `Furniture.xlsx` sourcing, not Bathroom's own data:
   QVC (`api.qvc.com`, `Disallow: /`), The White Company (a `?q=&page=`
   query-string fetch matching its own Disallow), PAN Emirates
   (`panhome.com`, `Disallow: /`). `Furniture.xlsx` has not been modified —
   this needs the Furniture run owner, not a Bathroom fix.
4. **Anthropologie drift**: US `bathroom-vanities` reads 19 live vs 20 in
   `Furniture.xlsx`. Cosmetic, unresolved.
5. **Bowery Company mis-tagging at product level** (its "Bathroom
   Accessories" node holds a crate and a bag) — recorded with the caveat in
   the SR's own notes, not corrected (would require re-deriving the site's
   own count, not ours to invent).
6. **Shower Curtain Liners (BBB, SR 44)** — filed Textile on parent type but
   ~half the grid is PEVA/plastic with no material sub-node to split it.
7. **Bathroom cleaning inconsistency**: filed Bathroom at Container Store,
   routed out at HSN for the same underlying rule — flagged, not
   reconciled, in the original run.
8. **`do_not_rerun` list carried forward as-is** (do not re-verify):
   - SR 8 McGee & Co. — genuine `ClaudeBot` / `Disallow: /` opt-out.
   - SR 26 HAY US — Cloudflare-managed `ClaudeBot` / `Disallow: /` opt-out.
9. **16 blocked companies carried forward as-is** (see `SUMMARY.md` for the
   full breakdown by cause — bot-manager challenge, robots-forbidden data
   host, egress IP filter, genuine opt-out). Re-verify only if network
   conditions from this machine differ; do not retry SR 8 / SR 26.

## Continuation plan

SR 197-286 (90 companies) via the new `bathroom-extraction` skill +
`pipeline/bathroom_json_archive/`. Same rhythm as Furniture/Pet Care/Seasonal:
one worker per company, write `b<SR>.json` immediately, archive, batch-merge,
`verify_bathroom.py`, log adjudication items here as they arrive.

## MANDATORY FINAL PASSES — run only after all 286 are processed (user instruction, 2026-09-05)

Do NOT run these mid-roster; the completeness check needs the full picture
and a retry pass needs the final blocked-list, not a partial one.

1. **Completeness re-check across ALL 286 (not just the new 90).** For every
   company already marked `BATHROOM FOUND` or `NO BATHROOM FOUND` (SR 1-196
   included), re-verify the nav/sitemap/category-tree walk was actually
   exhaustive — not just "found something, stopped." This subsumes the two
   already-known gaps above (rule-24 residue on ~10 companies, mirror-subset
   sweep applied to SR 176 only) but is broader: check every company, not
   just those two known lists, for a missed Bathroom sub-category.
2. **Retry every blocked company after the full 286 are done** — the
   original 16 (`SUMMARY.md`'s breakdown by cause) plus every new block
   picked up during SR 197-286 (already includes SR 199 Etsy US — DataDome
   site-wide wall, all 5 curl_cffi profiles 403'd, confirmed NOT a robots
   opt-out). **Exception — never retry:** SR 8 McGee & Co. and SR 26 HAY US
   (genuine `ClaudeBot`/`Disallow: /` opt-outs, re-verified 2026-09-01).
   Retry everything else once, using whatever access tier (HTTP tiers, then
   escalate per `home-decor-extraction/SKILL.md` §2 rule 1) is available at
   that time — network/bot-wall conditions can differ session to session.

## RETRY PASS RESULTS (2026-09-05, after full 286 completion)

Retried 18 of 27 blocked (excluded the then-known 9 genuine ClaudeBot
opt-outs: SR 8, 26, 215, 227, 251, 281, 282, 283, 285) plus SR 205
(partial, not blocked, but genuinely unresolved). Claude-in-Chrome was
available this session and cleared several bot-manager challenges the
original handoff had no tool to defeat.

**Newly resolved (blocked -> ok/partial):** SR 79 QVC Home (2 leaves), SR 116
Maisons du Monde BE (7 leaves, HTTP-only via utm trick, no browser needed),
SR 205 Lamps Plus (1 leaf, resolved from partial), SR 245 Meesho Home &
Kitchen (2 leaves, upgraded blocked->partial).

**IMPORTANT — newly discovered GENUINE robots opt-out, add to the
never-retry list:** SR 169 Tavola UAE. The original block was a Cloudflare
challenge the prior run couldn't get past to even READ robots.txt. This
retry's browser tier defeated Cloudflare and found `ClaudeBot: Disallow: /`
+ `Claude-Web: Disallow: /` underneath — a real opt-out that had been
hidden by the access block, not a separate finding. The tree glimpsed
before hitting robots.txt was correctly discarded, not recorded. **Never
retry SR 169** — same footing as SR 8/26/215/227/251/281/282/283/285.

**SR 153 Dille & Kamille — re-checked again 2026-09-05 per explicit user
request ("no urls are opening, fix it").** Fresh test across all 4 permitted
tiers (direct HTTP, curl_cffi 3 profiles, Claude-in-Chrome real browser
session) confirmed the exact same genuine network-level block: the site's
only IP (83.143.184.156, no AAAA record at all) refuses every connection
from this workstation. Project memory notes `r.jina.ai` fixed this identical
problem in an earlier (2026-09-04) session, but that is the same banned
proxy category enforced strictly elsewhere this session (caught and
corrected two workers for using Wayback/translate.goog under similar
"direct access failed" pressure). Asked the user explicitly whether to
authorize a narrow one-company exception; **user chose to keep it blocked,
no exception** — consistent with the standing rule. Do not retry again
without a materially different signal (e.g., a report the site is back up).

**Reconfirmed still-blocked (all 3 tiers exhausted again, no further
retry needed unless conditions change materially):** SR 134 Leroy Merlin
France (IP/ASN-level CDN deny, real browser session included), SR 144 BHV
Marais Maison (Cloudflare invisible challenge never resolved even via a
real browser), SR 153 Dille & Kamille (network-level unreachable on every
tier, including the browser's separate network path), SR 163 PAN Emirates
(robots.txt confirmed blanket `Disallow: /` on the live host, or 520
unreadable on the alternate — never retry, same footing as a Claude-named
opt-out), SR 189 Costco US (Akamai holds on all 3 tiers; original 18-node
tree preserved).

**Ledger accuracy fix (post-retry):** `merge_bathroom.py`'s `ledger_status()`
was mapping any 0-row company to "NO BATHROOM FOUND" regardless of whether
`status` was `"ok"` (a genuine confirmed absence, rule 36) or `"partial"`
(access prevented verifying a real, substantial recovered tree — SR 70
Lowe's, 26 review entries; SR 145 Galeries Lafayette, 28 review entries).
Added a distinct `"PARTIAL - UNRESOLVED (see review)"` ledger status so
these two are never mistaken for a confirmed absence. SR 199 Etsy US
correctly stays "NO BATHROOM FOUND" despite real candidates existing,
because every one is either already-owned elsewhere or has no recordable
exact qty (capped at "1,000+") — that is the intended, correct outcome per
this project's dedup/no-estimate conventions, not a gap.

**Genuine shared-tool contention observed, no data corruption resulted:**
SR 145 Galeries Lafayette's retry hit 3 hijacked-tab navigations mid-load
during a period of high concurrent Claude-in-Chrome usage; correctly
detected via page-identity mismatch and discarded, original 28-node
tree/notes preserved unchanged. See the "CONFIRMED RISK" note above.

## New-batch flagged items (SR 197-212, 2026-09-05) — needs adjudication, not decided here

- **SR 206 Bouclair** — "Bathroom Wall Decor" (qty 3) is majority wall art,
  candidate for Wall Decor, but not yet in `cross_category_url_index.json`
  (Wall_Decor.xlsx may not have a matching URL) — needs a human check before
  it's recorded anywhere. "Bathroom Decor" (qty 117) is a mixed
  merchandising collection spanning Storage/Textile/genuine-Bathroom with no
  site subcategorization — flagged MIXED, not guessed.
- **SR 204 EQ3** — the only Bathroom-tagged URL (qty 10) mixes in 1 Textile
  item (shower curtain) and 3 general-furniture items (stools) with no way
  to split by URL; qty kept at the site's own exact figure per the
  quantity rule, with the composition caveat flagged for whoever reviews it.
- **SR 205 Lamps Plus** — partial: catalog layer is Akamai-walled, so
  "Bathroom Vanities" is a real nav node with an unverifiable qty (in
  review, not rows). Retry in the blocked/partial sweep after SR 286.
- New blocked additions to the retry list: **SR 197 Home Depot** (Akamai,
  robots clean) and **SR 199 Etsy US** (DataDome, robots clean).

## Batch SR 213-252 notes (2026-09-05)

- Two workers (SR 197 Home Depot's first attempt, SR 226 IKEA India's first
  attempt) launched a background crawl job and ended their turn waiting on
  it instead of working synchronously — both stopped and redone correctly.
  One worker (SR 197's first attempt) briefly used web.archive.org before
  being caught and corrected. Watch for this pattern in future batches.
- **Verified false positive**: `verify_bathroom.py`'s suspect-URL check
  flags Tata CLiQ Luxury Home's (SR 241) category URLs
  (`...?page=0&q=:relevance:category:LSH1416100103...`) as search-like
  because of the bare regex on `q=`. Confirmed live (HTTP 200, real category
  content) — this is Tata CLiQ's own category-facet URL encoding, not a
  text search. `merge_bathroom.py` does not have the pet_care-style
  "LINK LOOKS LIKE A SEARCH PAGE" soft-flag `verify_bathroom.py` does; if
  ever added, give it an allowance for `q=:relevance:category:` shaped
  values so it doesn't false-flag this and any similarly-encoded site.
- New blocked additions: **SR 215 Design Within Reach** (genuine ClaudeBot
  `Disallow: /` opt-out — never retry, like SR 8/SR 26), **SR 227 Nestasia**
  (genuine ClaudeBot `Disallow: /` opt-out — never retry), **SR 251 The
  Decor Kart** (genuine ClaudeBot `Disallow: /` opt-out — never retry),
  **SR 245 Meesho Home & Kitchen** (Akamai, all 3 access tiers genuinely
  exhausted including Claude-in-Chrome — retry candidate), **SR 242 Zara
  Home India** (self-inflicted Akamai block from an oversized store-id scan
  — retry candidate, 5 genuine bathroom nodes already confirmed to exist,
  just need quantities).
- **CONFIRMED RISK: shared Claude-in-Chrome tab contention under high concurrency.**
  When ~18-20 workers run simultaneously and several fall back to the browser
  tier, they can share one browser extension session — SR 145's retry saw 3
  navigation attempts hijacked mid-load to unrelated companies' sites
  (bhv.fr, bloomingdales.com, templeandwebster.com.au, etsy.com — all other
  concurrent workers in the same batch). No bad data resulted here because
  the worker checks page identity (h1/breadcrumb/canonical) before trusting
  content, per the project's own mandatory node-identity rule — a hijacked
  tab shows the WRONG company's content, which that check catches. Still,
  keep future large concurrent batches under closer watch when many are
  likely to need the browser tier at once (bot-walled retries especially);
  consider smaller batch sizes for retry-heavy dispatches specifically.
- **SR 220 Pepperfry** and **SR 223 AJIO Home**: minor audit-trail gaps
  found and partly fixed — Pepperfry's silent mirror-dedup omission was
  corrected directly in `b220.json`; AJIO's four clear-cut Textile
  exclusions are documented in `notes` prose only, not separate `review[]`
  rows (not fixed — no concrete qty/URL was captured for them, so adding a
  row would require fabricating one; low priority, no correctness impact).
