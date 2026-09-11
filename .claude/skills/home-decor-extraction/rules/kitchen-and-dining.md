# Kitchen & Dining — category boundary rules

Load with `_decor-extraction-core.md`. Workbook: `Kitchen_and_Dining.xlsx`
(2,352 records at the 2026-08-14 split).

**Executable source of truth:** `pipeline/category_split/classify.py` — `KD_RE`,
`NOT_KD`, `KD_HARD`, and the `CAT_MAP` entries mapping to `KD`. This module
documents that code; it does not replace it. To re-split, run the scripts.

---

## PRECEDENCE — where K&D sits

Kitchen & Dining is tested **last** of the four (`classify.py:name_class`):
Mirror-light → Wall → Wall-loose → Lighting → Decorative-strict → **K&D**.

Being last is why K&D needs two guards: `NOT_KD`, which stops decor objects being
pulled in, and `KD_HARD`, which stops genuine serveware being pulled *out* by the
decorative tier.

---

## CLAIMS (in scope for Kitchen & Dining)

Scope words: `glassware`, `serveware` / `servingware` / `serving ware`, `drinkware`,
`dinnerware`, `tableware`, `barware`, `teaware`, `flatware`, `cutlery`, `crockery`,
`dishware`, `tabletop`, `opalware`.

Serving forms: `serving bowls/trays/platters/dishes/plates/sets/pieces/accessories/
utensils/boards/spoons`, `platters`, `dinner sets`.

Drinking vessels: `wine/beer/champagne/cocktail/shot/whisky/martini/highball/water/
juice/drinking/bar glass(es)`, `glasses`, `tumblers`, `goblets`, `steins`,
`stemware`, `mugs`, `teacups` / `tea cups`, `cups & mugs`, `decanters`, `carafes`,
`pitchers`, `teapots`, `jugs`.

China and table dressing: `fine china`, `chinaware`, `coasters`, `placemats`,
`table linens`, `napkins`, `table runners`, `cake stands`, `butter dishes`,
`salad bowls`, `sugar bowls`, `creamers`, `trivets`, `condiment`.

Major Categories mapping straight to K&D: `Kitchen & Dining`, `Kitchen and Dining`,
`Kitchen & Tableware`, `Kitchen & Dinning` *(source typo, keep it)*,
`Dining & Kitchen`, `Glassware`, `Tableware`, `Silverware`, `Bar & Drinkware`,
`Table Linen & Accessories`.

---

## DOES NOT CLAIM — `NOT_KD`

A name containing any of these is **not** Kitchen & Dining even if a K&D word also
appears: `decorative`, `decor`, `frames`, `mirrors`, `pictures`, `photos`,
`fountains`, `clocks`, `vases`, `lamps`, `lights`, `lighting`, `vanity`.

Two reasons this guard exists:
- **"Decorative plates / bowls / trays" are decor objects, not serveware.**
- **A bare `tabletop` must not drag picture frames, mirrors or fountains into K&D.**
  `tabletop` is a K&D scope word, so without this guard "Tabletop Frames" and
  "Tabletop Fountains" land in the wrong workbook.

Cookware, pans, kitchen appliances, hardware and utensils are out of scope for the
whole project — see `_decor-extraction-core.md` EXCLUDE.

---

## `KD_HARD` — the counter-override that protects K&D

The decorative tier is tested *before* K&D, so an explicit serveware scope note
could otherwise be stolen by a "Decorative …" phrase buried inside the name.
`KD_HARD` beats the decorative-strict tier:

`serveware`, `servingware`, `tableware`, `drinkware`, `glassware`, `dinnerware`,
`barware`, `teaware`, `flatware`, `crockery`, `serving`.

Worked example that drove this rule:
`Serveware (Decorative Objects & Vases, filtered to Serveware)` → **Kitchen &
Dining**, not Decorative.

---

## THE DRAINING TRAP — read this before touching the decorative rules

A single broad "looks decorative" rule **silently drained Kitchen & Dining** in the
first split pass. A `Table Accents` group sitting under a `Kitchen & Dining`
Category swept `Charger Plates`, `Table Vases` and `Flower Centerpieces` out of the
K&D workbook.

The fix is the two-tier decorative design, and it must stay two-tier:
- the *override* tier only contains product types the brief names outright;
- `Table Accents`, `Table Decor` and `Home Accents` are **fallback tier only**,
  applied solely to records nothing else claimed.

A site that files Charger Plates or Table Vases under `Kitchen & Dining > Table
Accents` has stated an explicit hierarchy, and the brief says not to override it.

Note the asymmetry that follows: `^vases?` heads a decorative branch and goes to
Decorative wherever it is filed, but **`Table Vases` is deliberately not matched**
by the override tier and stays in K&D.

Glassware and serveware stay inside Kitchen & Dining — they never move to
Decorative.
