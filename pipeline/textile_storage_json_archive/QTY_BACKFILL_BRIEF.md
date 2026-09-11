############################################################
# WORKER BRIEF: QTY BACKFILL FOR PARTIAL COMPANIES
############################################################

You are backfilling missing quantities for ONE company whose Textile+Storage
extraction already ran and produced a real, correct category tree — but some
leaf rows have qty=null with a "MANUAL REVIEW" flag because every access
tier was blocked (Akamai/PerimeterX/DataDome/Imperva) at the time, INCLUDING
Claude-in-Chrome, which was disconnected for that whole research stretch.

Claude-in-Chrome is now reliably connected. Your job: revisit ONLY the
specific null-qty rows you are given below, read each one's live product
count via Claude-in-Chrome, and update the existing ts<SR>.json file in
place with the real number.

============================================================
HARD RULES
============================================================

1. DO NOT rebuild the category tree. DO NOT add new rows, remove rows, or
   rename/re-link existing rows, UNLESS you discover the link itself no
   longer resolves to the correct sub-category (see rule 6).
2. DO NOT touch any row that already has a real qty. Only rows explicitly
   listed as null-qty targets in your assignment below are in scope.
3. Use ONLY Claude-in-Chrome (mcp__claude-in-chrome__* tools) for this task
   — that is specifically the tier that was unavailable before and is the
   reason these rows are null. You do not need to re-attempt tiers (a)/(b);
   go straight to tier (c).
4. qty is the site's own exact number, read from the live rendered page
   (a "N results/products/items" header, or equivalent). Never estimate,
   round, infer, or copy a parent's/sibling's number. If the page still
   shows a rounded/capped count (e.g. "50,000+"), leave qty=null — do not
   record the rounded figure.
5. If a specific row's URL is STILL blocked (Akamai/CAPTCHA/etc.) even via
   Claude-in-Chrome, leave qty=null and update the row's `flag` field to
   note it was retried and is still blocked (e.g. "MANUAL REVIEW: retried
   via tier c YYYY-MM-DD, still Akamai-blocked"). Do not fabricate.
6. If a specific URL now 404s or redirects to a different page (site
   structure changed since the original research), note this in the row's
   `flag` field and leave qty=null rather than recording a number from the
   wrong page. Do not silently swap in a different category's number.
7. On the FIRST block for this company's host, stop — use whatever you
   already captured, do not chase the block further, do not retry the same
   blocked URL repeatedly.
8. Work entirely synchronously in the foreground. Do NOT launch a
   background job, use the Monitor tool, or end your turn waiting for a
   notification.
9. Never run system-wide process-kill commands. If you must kill a stray
   process, target only your own specific PID.
10. Multiple workers share this one Chrome browser/extension connection
    concurrently. If you find your tab was hijacked or navigated by another
    worker's task, that's expected in this shared environment — just create
    a fresh tab and continue; it is not a site block.

============================================================
OUTPUT
============================================================

Edit the existing pipeline/textile_storage_json_archive/ts<SR>.json file
directly (read it first, then write the updated version back). For each row
you successfully backfilled: set `qty` to the real number and set `evidence`
to a string describing exactly where it came from (e.g. "rendered header
text: '128 Results'"). For rows you could not backfill: leave qty=null and
update `flag` per rule 5/6 above. Do not touch the `status` field at the
top level unless you determine the company should now be "ok" instead of
"partial" (i.e. every previously-null row is now filled) — in that case
update status to "ok".

Before finishing, validate the file is well-formed JSON (e.g. `python -c
"import json; json.load(open('ts<SR>.json'))"`).

When finished, report: how many of the assigned null rows you successfully
backfilled with a real qty, how many remain null (and why), and whether you
updated the top-level status field.
