---
name: home-decor-extraction
description: Run a category extraction over the company roster - Furniture, Lighting, Kitchen & Dining, Wall Decor, or Decorative Home Accessories. Use when the user says "Extract <category>", asks to continue/resume a category run, or asks to merge, verify or re-split the category workbooks. Loads only the active category's rule module.
---

# Home Decor Extraction — master skill

One skill, one extraction engine, per-category rule modules loaded on demand.
This file is category-agnostic. **Load exactly one category module** from `rules/`
after routing, and never load the others.

> This is a refactor of a working system. The pipeline, scripts, workbooks, state
> and rules described here already exist and are the source of truth. Do not
> rebuild them. If this document ever conflicts with observed working behaviour,
> **the working behaviour wins** — fix this document, not the pipeline.

---

## 1. ROUTE FIRST

| User says | Load |
|---|---|
| Extract Furniture | `rules/furniture.md` |
| Extract Lighting | `rules/_decor-extraction-core.md` + `rules/lighting.md` |
| Extract Kitchen and Dining / Kitchen & Dining / Kitchen + Dining / K&D | `rules/_decor-extraction-core.md` + `rules/kitchen-and-dining.md` |
| Extract Wall Decor (incl. Mirrors, Clocks) | `rules/_decor-extraction-core.md` + `rules/wall-decor.md` |
| Extract Decorative Home Accessories / Decorative Accessories / Decor | `rules/_decor-extraction-core.md` + `rules/decorative-home-accessories.md` |
| Extract Textile | `rules/textile.md` |
| Extract Storage | `rules/storage.md` |

**Anything else — Bathroom, Mirrors-as-its-own-file, or any category not in that
table — is NOT CONFIGURED. STOP and say so.** Do not invent rules, do not
improvise a module, do not reuse a neighbouring category's rules. See §9 for what
is known about the unconfigured ones.

Read only the module(s) the table names. Loading an unrelated category's rules is
the specific waste this structure exists to prevent.

### The two engine shapes are different — know which one you are in

- **Furniture, Textile, Storage** are each a *per-category extraction*: workers
  visit sites and extract that category only. `rules/furniture.md`,
  `rules/textile.md`, `rules/storage.md` are complete, self-contained worker
  briefs. When Textile and Storage are run together as one task (one shared
  research pass per company, classified into both), keep their archives and
  output workbooks separate — see `pipeline/textile_storage_json_archive/`.
- **Lighting / Kitchen & Dining / Wall Decor / Decorative** came from **one shared
  Home Decor extraction pass** that captured all four together, then a
  **classification split** into four workbooks. Their per-category module carries
  the *boundary* rules — what belongs to that category and what must not be dragged
  into it — and `_decor-extraction-core.md` carries the shared extraction scope.
  For these four, re-running the split is usually the right operation, **not**
  re-visiting websites.

Before extracting a decor category, ask which is actually needed: a re-split of
existing validated data, or new site visits. Re-splitting costs no browser calls.

---

## 2. HARD RULES THAT APPLY TO EVERY CATEGORY

1. **HTTP-first access tier (superseded 2026-08-25 — was "browser only").** For
   every target site, try methods in this order and stop at the first one that
   gets you complete, reliable data:
   1. **Direct HTTP fetch + HTML parsing.** Plain request + parse (requests/
      curl_cffi/etc. are fine here — no longer banned). Pull SSR HTML, embedded
      JSON (`__NEXT_DATA__`/`__NUXT__`/`__APOLLO_STATE__`), sitemaps, robots.txt,
      category/product-count APIs. Parse locally; don't re-fetch what you already
      have.
   2. **Playwright/CDP** when the page is client-rendered and step 1 can't see
      the real DOM/data (empty SSR shell, JS-built nav, counts that only appear
      after hydration).
   3. **Claude-in-Chrome (`mcp__claude-in-chrome__*`)** only as a last resort —
      genuine uncertainty about the category structure, anti-bot walls that
      defeat 1 and 2, or anything needing visual/interactive judgement.
   Avoid repeated browser interactions, screenshots, and LLM-driven page reads
   when the same data is obtainable deterministically via 1 or 2. Keep the
   proxy/reader ban: no r.jina.ai, translate.goog, web.archive.org, or webcache
   as a substitute for actually reaching the site.
   Still standing regardless of tier: check `robots.txt` for a Claude-specific
   disallow before Claude-in-Chrome use (rule 3 below); qty must still be the
   site's own exact number with evidence (rule 2 below); first-block-stops-you
   still applies per tier, not globally — a block in tier 1 means try tier 2, a
   block in tier 3 (the last tier) means stop and report partial.
2. **`qty` is the site's own exact number, with an `evidence` string.** Never
   estimate, round, infer, aggregate, or copy a parent's number. `null` + a
   `MANUAL REVIEW: <reason>` flag is a correct answer; a fabricated number is
   project-destroying. Any qty lacking evidence is nulled at merge.
3. **Check `robots.txt` for a Claude-specific disallow** before extracting. A named
   `anthropic-ai` / `ClaudeBot` / `Claude-Web` / `Claude-User` / `Claude-SearchBot`
   with a full-site `Disallow: /` means STOP and mark the company blocked — even if
   the WAF is trivially bypassable. Several sites name Claude and then `Allow: /`;
   that is explicit permission, the opposite of a block.
4. **Never write to another category's workbook.** A Furniture run must not touch
   `Kitchen_and_Dining.xlsx`, `Lighting.xlsx`, `Wall_Decor.xlsx` or
   `Decorative_Home_Accessories.xlsx`. SHA-256 baselines for all four plus the
   source workbook live at
   `pipeline/furniture_json_archive/protected_baseline.sha256` and are re-checked by
   `verify_furniture.py`. Run it after any batch.
5. **Never shift rows in these sheets.** `openpyxl`'s `delete_rows` corrupts cells
   here. Edit in memory, rewrite the sheet wholesale, and diff against a backup.
   Check for `~$` lock files first — these workbooks are often open in Excel.
6. **Output text is English only**, plain ASCII. Translate site node names; do not
   keep the original in parentheses. `merge_final.py` enforces this itself.

---

## 3. THE EXISTING ENGINE — REUSE IT, DO NOT REBUILD IT

Durable pipeline root: `pipeline/`. Nothing here should be re-implemented.

**Furniture run** — `pipeline/furniture_json_archive/`
| File | Job |
|---|---|
| `FURNITURE_BRIEF.md` | worker brief — same content as `rules/furniture.md` (§5) |
| `companies.json` | the 286-company roster for this run |
| `assign.py` | prints a worker's assignment block for an SR range |
| `status.py` | dispatched / done / in-flight / next-up |
| `dispatched.txt` | dispatch ledger |
| `f<SR>.json` | one per completed company — the output contract |
| `merge_furniture.py` | worker JSON → `Furniture.xlsx` |
| `verify_furniture.py` | protected-file check + sheet integrity + ledger |
| `qa_notes.md` | open adjudication items carried across sessions |
| `notes/<SR>.md` | the prior Home-Decor pass for that company |

**Home Decor run** — `pipeline/`
`BRIEF.md` (worker brief), `merge.py` → batch workbook, `merge_final.py` → the
`Output` sheet of `Final_Company_List (1).xlsx`, `json_archive/c<SR>.json` (329
archived worker outputs), plus pre-merge checks `_verify.py`, `_dupkey.py`,
`_roomscan.py`, `_summary.py`. Run the checks every time.

**Category split** — `pipeline/category_split/`
`parse.py` → `classify.py` → `assign.py` → `build_files.py` → `reconcile.py`.
This is the code that produced the four category workbooks. `classify.py` is the
executable source of truth behind the four decor modules in `rules/`; those modules
document it, they do not replace it. To re-split, run these — do not hand-classify.

**Before writing any script, search `pipeline/` first.** Merging, validation,
reconciliation, Excel edits, duplicate detection, progress tracking and manifest
building all already exist. Do not write a second one.

### Known script traps — do not rediscover these
- `merge_final.py`'s `BATCH` constant is a hardcoded `range()`. Bump it by hand
  when the roster grows or the merge silently truncates at the old ceiling.
- `merge_final.py`'s `SCRATCH` and `_dupkey.py`'s `S` are hardcoded session paths.
  Re-point them at the current scratchpad before running.
- `merge_furniture.py`'s dedup key must be `(category, sub_category, link)`, never
  `(category, sub_category)`. Name-only ate 22 real rows.
- `merge_furniture.py`'s `NOT_FURNITURE` safety net needs `FURNITURE_OVERRIDE`
  entries for bare `vanity`, `crib/cot/cotbed/changing table`, `coat stand/rack`.
  **Always read the `DROPPED non-furniture` lines after a merge** — that is the
  false-positive channel.
- `englishify.py` is pointed at the old frozen workbook. Do not run it against
  `Final_Company_List (1).xlsx` without re-pointing it.
- A merge rebuilds its sheet from whatever worker JSON it finds. Never re-run a
  merge with an incomplete JSON set, and always diff against a backup.

---

## 4. STATE, CACHE AND PROGRESS — PRESERVE, NEVER RESET

Completion is tracked **per company per category**, and already is: each category
run has its own archive directory and its own file naming, so a company being done
in one category says nothing about another.

| Category | Completion marker | Roster |
|---|---|---|
| Furniture | `pipeline/furniture_json_archive/f<SR>.json` | `companies.json` (SR 1..286) |
| Home Decor (the four decor categories) | `pipeline/json_archive/c<SR>.json` | master roster, 327 S.N. |

That separation *is* the category-specific cache and the category-specific progress
tracking. Do not build a new one on top of it.

- **SR numbering differs between runs.** The Furniture roster is SR 1..286 from the
  `Output` sheet; the Home Decor archive is keyed by the master list's S.N. (327
  entries). `c<SR>.json` and `f<SR>.json` are **not** the same company for the same
  number. Map by company name / brand site, never by number.
- **Never mark completed work pending, never delete an archive, never reset the
  dispatch ledger.** A missing `f<SR>.json` mid-run legitimately shows as
  `PROCESSING ERROR` in the ledger — that is the correct mid-flight state, not a
  defect.
- **Archive after every batch.** Copy new `f<SR>.json` / `c<SR>.json` back into
  `pipeline/…_json_archive/` immediately. The scratchpad is session-temp and does
  not survive.
- **Resuming in a new session:** the previous session's scratchpad usually still
  exists on disk at
  `%TEMP%\claude\C--Users-GyanendraVishwakarma-Web-Research-Agent\<old-session-id>\scratchpad`
  and can be read and copied from. Recover `notes/` from there rather than
  regenerating it — regenerating from `json_archive/c*.json` is the fallback.
  Then copy the pipeline scripts into the current scratchpad and re-point the
  hardcoded path constants.

---

## 5. RUNNING A BATCH

1. **Read the state before doing anything.** `python status.py` (Furniture) or the
   archive listing. Never re-derive it from memory or from this document.
2. **Sync the brief.** Copy the active `rules/<category>.md` into the working
   scratchpad under the filename the workers expect (`FURNITURE_BRIEF.md` for
   Furniture) and update the scratchpad path inside it. Workers must read the same
   text at the same path they always have — `rules/<category>.md` is the source,
   the scratchpad copy is the deployment.
3. **Generate `notes/<SR>.md`** for the batch before dispatching. It gives each
   worker the prior pass for its own company — URL shape, category tree, verified
   URLs. Biggest single accelerator; do it first.
4. **Dispatch, cap 20 concurrent workers.** One worker = one company. Dispatch
   exactly one replacement per completion notification. `status.py`'s in-flight
   count under-reports, because a worker writes its JSON slightly before it exits.
5. **Each worker gets its own browser tab** and must never touch a tab it did not
   create. Helper files are prefixed `w<SR>_`; the only unprefixed file a worker
   writes is its result JSON.
6. **Check the result file immediately after every completion notification**, even
   a normal-sounding one. Known failure mode: a worker launches a background job
   and ends its turn "waiting to be notified" — the orchestrator cannot see it, so
   it silently stops with a missing or stale file. If that happens, `SendMessage`
   the same agent with an instruction to work synchronously in the foreground.
7. **Archive, then merge, then verify.** Copy results to the archive, run the
   merge, read its dropped-row messages, run `verify_furniture.py` / `_verify.py`.
8. **Log adjudication items to `qa_notes.md` as they arrive**, don't batch them to
   the end. Flag, never silently decide.

---

## 6. EFFICIENCY — MANDATORY

Accuracy first, always. But re-verifying an established fact is prohibited.

- **Structured data first, browser second.** If the answer is already in SSR HTML,
  embedded JSON (`__NEXT_DATA__` / `__NUXT__` / `__APOLLO_STATE__`), a captured API
  response, or data already extracted — parse it locally with Python. Pull the
  dataset once, then work offline.
- **Extract once → filter deterministically → verify only exceptions.** If a
  listing has 94 products and 3 titles look furniture-ish, inspect 3, not 94.
  Report the split (`total / clear / candidate / needs-verification`) and open only
  the last group. Keyword scans generate candidates; they never classify.
- **Checkpoint before anything expensive** (`w<SR>_checkpoint.json`): URL, counts,
  pagination status, item IDs, titles, candidates, verified, remaining, rate-limit
  status. On resume, read it and continue from the last incomplete phase. Never
  rediscover a site from scratch.
- **HARD BLOCK RULE — the FIRST block stops the target, not the third.** A block is
  403, DataDome, Akamai, Cloudflare, CAPTCHA, "Access Denied", a rate-limit
  response, or repeated load failure. On the first one: stop requesting that host,
  save the checkpoint, use the data already held, process it locally, and report
  precisely what is still missing. **`sleep` / `time.sleep()` / cooldown timers /
  backoff loops / polling a blocked host are banned** — a command whose only purpose
  is to wait for a website is not productive work. Pacing requests *before* trouble
  (~1 per 5-8s) is fine and encouraged; waiting for a wall to lift is not. Write
  `status: "partial"` with a `failure_reason` naming exactly what is unverified. An
  honest partial with a precise gap tops up in minutes; a burned hour does not.
  Do not chase the same block via another route.
- **Before each browser call ask what NEW information it produces.** If you already
  have it, skip the call. Two independent confirmations are enough; a third is
  waste. Do not push large page dumps through context when a local parse can reduce
  them to a small table first.
- **Use scripts for deterministic work.** Excel edits, merging, dedup, reconciliation
  and counting are script jobs. Reserve the model for interpretation and judgement.

---

## 7. TRAPS PROVEN ACROSS RUNS — CHECK THESE

- **The nav under-reports the tree.** Take the union of mega-menu **and** category
  sitemap **and** each category page's own sub-category strip. Real countable
  categories have been found sitemap-only on four companies in a single batch.
- **A bad slug usually does not 404** — it serves a plausible wrong number (the
  parent's total, or the site-wide total). Confirm HTTP 200 **and** that the
  h1/canonical is the node you asked for, on every leaf.
- **Node identity comes from the slug, never the display label.** Two different
  categories can render an identical localised label.
- **Storefront count APIs are often inflated** — Shopify `products_count` (wrong on
  6/6 stores), Magento `categoryList.product_count`, Constructor on Williams-Sonoma
  properties. Prefer the rendered header. Some structured counts are exact under
  check (Target redsky, TJX/Marshalls Endeca, 1stDibs, Perigold, Neiman Marcus);
  say in `evidence` which you used and why.
- **`qty` is an in-stock snapshot** on stock-gated storefronts — the header counts
  purchasable products, not the published catalogue. Record the header per the qty
  rule anyway, but say so if a node reads implausibly low.
- **Parent totals are not always supersets of children** — products get multi-tagged.
  "Parent ≥ children" is **not** a validity test here; do not add it to a verifier.
- **A site search returning 0 is not proof of absence.** Run a discrimination check
  (query something the site definitely does not sell and something it definitely
  does); if the counts do not differ, enumerate and title-scan instead.
- **Don't count product tiles by counting hrefs** — non-ASCII slugs undercount,
  carousels overcount, prefetch overcounts. Use a structured product-ID field, and
  treat the PLP's own item list as the only authority for "is this product in this
  grid".

---

## 8. OUTPUT

Each category has one workbook in the project root. A run writes only its own.

`Furniture.xlsx` · `Kitchen_and_Dining.xlsx` · `Lighting.xlsx` · `Wall_Decor.xlsx` ·
`Decorative_Home_Accessories.xlsx`, plus the source `Final_Company_List (1).xlsx`
(`Output` sheet) and `Unassigned_Records_Report.csv`.

Sheet layout — re-derive before any structural edit, do not assume:
`Maisons | Company name | Brand Site | Country | site URL | Category | Sub-Category | Type | qty | link`.
A company block starts on a row with `Maisons` set in col A; blank rows separate
blocks, and that banner row is also the first Category section's first row.
Col F (Category) is sparse — non-empty only on a section's first row. Col G is a
two-level tree: a grouping row is `fill FFFFF2CC + bold + blank qty + blank link`,
its leaves follow un-highlighted. Header fill is `FFD9E1F2`.

Grouping rows carry name only — `qty: null`, `link: null`. Emit rows in reading
order, each parent immediately followed by its children.

Copying `cell._style` between workbooks raises `IndexError` on save — copy the
resolved `font`/`fill`/`border`/`alignment`/`number_format`/`protection` instead.

---

## 9. NOT CONFIGURED — STOP IF ASKED

- **Mirrors** is deliberately **not** its own category. Mirrors and clocks belong to
  Wall Decor, never to Lighting and never to a file of their own. Asked for a
  Mirrors extraction, say this and offer Wall Decor.
- **Bathroom is now configured as its own skill**, `bathroom-extraction`
  (`../bathroom-extraction/SKILL.md` + `rules/bathroom.md` there — not in
  this skill's own `rules/` directory, which still carries only the
  original placeholder). Route "Extract Bathroom" / "continue Bathroom" to
  that skill, the same way Pet Care and Seasonal live outside this table.
  SR 1-196 were done on another machine and handed off 2026-09-05; SR
  197-286 are in progress. See `pipeline/bathroom_json_archive/qa_notes.md`
  for open items before touching the back-catalogue.
- **Textile and Storage are now configured** (`rules/textile.md`,
  `rules/storage.md`, filled 2026-08-24) — route to them normally, do not treat
  them as deferred.
- **Bestsellers / Clearance / New Arrivals are now configured**, each as its
  own skill (`../bestsellers-extraction/SKILL.md`, `../clearance-extraction/
  SKILL.md`, `../new-arrivals-extraction/SKILL.md`), the same way Bathroom,
  Pet Care and Seasonal live outside this table. **These are NOT
  product-taxonomy categories** — they are merchandising-PLP extractions
  (the site's own Bestsellers/Clearance/New Arrivals listing pages, whatever
  product type they contain), built 2026-09-07, scaffolded but not yet run
  (no batches dispatched). Route "Extract Bestsellers" / "Extract Clearance"
  / "Extract New Arrivals" to those skills, not here.

If asked for Mirrors as its own file: stop, say it is not configured — Mirrors
stays inside Wall Decor, see above.
