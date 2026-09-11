############################################################
# WORKER BRIEF: TEXTILE + STORAGE COMBINED EXTRACTION
############################################################

You are one worker in a batch. You are assigned exactly ONE company. Do the
site research for that company ONCE, then classify every category/subcategory
you find into Textile, Storage, both, or neither. Do not do two separate
research passes.

============================================================
STEP 0 - READ THE FULL RULESETS FIRST
============================================================

Before touching the website, Read these two files IN FULL. They are the
complete, authoritative classification rules - do not skim, do not rely on
this brief's summary alone:

  C:\Users\GyanendraVishwakarma\Web Research Agent\.claude\skills\home-decor-extraction\rules\textile.md
  C:\Users\GyanendraVishwakarma\Web Research Agent\.claude\skills\home-decor-extraction\rules\storage.md

Everything in those two files applies. This brief only adds the shared-pass
mechanics and the output contract.

============================================================
STEP 1 - HARD RULES (apply to both categories)
============================================================

1. HTTP-FIRST ACCESS TIER (updated 2026-08-25 - project-wide, replaces the old
   browser-only rule). Try methods in this order, stop at the first that gives
   you complete, reliable data:
     a. DIRECT HTTP FETCH + HTML PARSING. Use requests / curl_cffi (impersonate
        a real browser when needed) + bs4/lxml to pull the page, sitemap,
        robots.txt, or an embedded JSON blob (__NEXT_DATA__ / __NUXT__ /
        __APOLLO_STATE__) or a category-count API. Parse locally. This is
        genuinely allowed now - do not skip straight to a browser.
     b. PLAYWRIGHT/CDP when the site is client-rendered and (a) can't see the
        real nav/counts (empty SSR shell, JS-built menus, numbers that only
        appear after hydration). `playwright` (Python, sync API) and a
        chromium binary are already installed on this machine - launch
        headless, read the rendered DOM/network responses, close it.
     c. CLAUDE-IN-CHROME (mcp__claude-in-chrome__* tools) ONLY as a last
        resort - genuine ambiguity about the category structure, or an
        anti-bot wall that defeats (a) and (b).
   Do not use screenshots or LLM-driven page reads when the data is
   obtainable deterministically via (a) or (b). Still banned at every tier:
   r.jina.ai, translate.goog, web.archive.org, webcache - those proxy/cache
   the page rather than actually reaching the live site.
   The first-block-stops-you rule (STEP 1 rule 4 below) applies per tier, not
   globally: a block in tier (a) means try tier (b), a block in tier (b) means
   try tier (c), a block in tier (c) means stop for real and report partial.
2. Check robots.txt first (whichever tier you're on). If it names anthropic-ai
   / ClaudeBot / Claude-Web / Claude-User / Claude-SearchBot with a full-site
   Disallow: /, that specifically blocks tier (c) (Claude-in-Chrome) - STOP
   before using a Chrome tab on that site. It does not by itself block plain
   HTTP fetches (tiers a/b) unless the disallow also names your fetch tool's
   user-agent or is a blanket `User-agent: * / Disallow: /`. If it names Claude
   and then Allow: /, that is explicit permission for tier (c) - proceed.
3. qty is the site's own exact number, with an evidence string describing
   exactly where it came from (rendered header text, JSON field path, etc).
   Never estimate, round, infer, aggregate, or copy a parent's/sibling's
   number. null + a "MANUAL REVIEW: <reason>" flag is a correct answer; a
   fabricated number is project-destroying.
4. On the FIRST block (403, DataDome, Akamai, Cloudflare, CAPTCHA,
   "Access Denied", repeated load failure) - stop requesting that host, use
   whatever data you already hold, and write status "partial" or "blocked"
   with a precise failure_reason. Do not sleep/retry/poll waiting for a wall
   to lift. Do not chase the same block via another route.
5. Output text is English only, plain ASCII. Translate any non-English node
   name; do not keep the original in parentheses.
6. No fabrication, no duplicate rows, no quantity aggregation, no URL
   invention, no product-detail/search/View-All/Collection URLs.

============================================================
STEP 2 - ONE SHARED RESEARCH PASS
============================================================

1. Open the company's site in your own new Chrome tab.
2. Build the FULL category tree using the union of: mega-menu navigation,
   category/XML sitemap, and each category page's own sub-category strip.
   A bad slug usually does not 404 - it silently serves a plausible wrong
   number (parent's or site-wide total). Confirm the h1/canonical matches the
   node you requested on every leaf you record.
3. For every node in the tree, decide independently:
   - Does it belong in TEXTILE per rules/textile.md?
   - Does it belong in STORAGE per rules/storage.md?
   A node can belong to one, the other, or neither. It will essentially never
   belong to both (the two rule files define mutually exclusive boundaries -
   e.g. "Fabric Storage Basket" is Storage per storage.md §25, not Textile).
   If a node is Furniture, Lighting, Kitchen & Dining, Wall Decor, Decorative
   Accessories, Bathroom fixtures, or apparel/pet/general-merchandise per
   either ruleset's boundary sections, it belongs in neither array - skip it.
4. Record each qualifying leaf under the correct array (textile_rows /
   storage_rows) with its own grouping-row ancestors per that category's own
   grouping convention (§26/§44 in the respective rule file). A grouping row
   that only leads to leaves in the OTHER category is dropped from this one's
   array (do not emit an orphaned parent).
5. Do not revisit a URL you already read for the other category - one page
   load informs both classification decisions.

============================================================
STEP 3 - OUTPUT CONTRACT
============================================================

Write exactly one file: ts<SR>.json (e.g. ts1.json for SR 1), in this same
directory (pipeline/textile_storage_json_archive/), where <SR> is the SR
number you were assigned from companies.json.

Schema:
{
  "sr": <int>,
  "company": "<name>",
  "brand_site": "<brand_site>",
  "country": "<country>",
  "site_url": "<url>",
  "status": "ok" | "partial" | "blocked" | "error",
  "failure_reason": "<string or null>",
  "notes": "<free text: ACCESS method, TREE method, QTY method, EXCLUDED and why - same style as the Furniture worker notes>",
  "textile_rows": [
    {
      "category": "Textile",
      "sub_category": "<name>",
      "qty": <int or null>,
      "link": "<url or null>",
      "is_group": <bool>,
      "evidence": "<string or null>",
      "flag": "<string or null>",
      "confidence": "HIGH" | "MEDIUM" | "LOW"
    }
  ],
  "storage_rows": [
    {
      "category": "Storage",
      "sub_category": "<name>",
      "qty": <int or null>,
      "link": "<url or null>",
      "is_group": <bool>,
      "evidence": "<string or null>",
      "flag": "<string or null>",
      "confidence": "HIGH" | "MEDIUM" | "LOW"
    }
  ]
}

Grouping rows: is_group=true, qty=null, link=null, evidence=null. Emit each
parent immediately followed by its own children within that array, in
reading order.

If the company has no qualifying Textile nodes, textile_rows = []. Same for
storage_rows. An empty array is a valid, correct answer - do not force a row.

If the site is fully blocked before any tree was built, set status="blocked",
both row arrays to [], and failure_reason describing exactly what happened.

============================================================
STEP 4 - BEFORE YOU FINISH
============================================================

Re-read STEP 0's two rule files' own validation checklists (textile.md §37,
storage.md §45) and self-check your rows against them before writing the
final JSON. Work synchronously in the foreground - do not launch a background
job and end your turn waiting to be notified.
