# Wall Decor — category boundary rules

Load with `_decor-extraction-core.md`. Workbook: `Wall_Decor.xlsx` (1,275 records
at the 2026-08-14 split).

**Mirrors and clocks live here.** Neither gets a file of its own, and neither goes
to Lighting.

**Executable source of truth:** `pipeline/category_split/classify.py` — `WALL_RE`,
`WALL_LOOSE_A` / `WALL_LOOSE_B`, `ART_HEAD`, `MIRROR_LIGHT`, and the `CAT_MAP`
entries mapping to `WALL`. This module documents that code; it does not replace it.

---

## PRECEDENCE — where Wall Decor sits

Tested second, immediately after the mirror-light guard
(`classify.py:name_class`):

1. `MIRROR_LIGHT` → LIGHT
2. `WALL_RE` **or** `ART_HEAD` → **WALL**
3. contains "wall" **and** a decor noun (`WALL_LOOSE_B`) **and not** a lighting
   word → **WALL**
4. Lighting → LIGHT
5. Decorative strict → DECOR
6. Kitchen & Dining → KD

---

## CLAIMS (in scope for Wall Decor)

`mirrors` · `clocks` · `wall art/arts/decor/décor/decoration(s)/hanging(s)/
sculptures/accents/accessories/decals/plaques/panels/murals/prints/pictures/frames/
tapestry*/shelves` · `wall-mounted decor` · `artwork` · `art prints` · `canvas art`
· `framed art` · `paintings` · `tapestry*` · `posters` · `wall sculptures` ·
`wall hangings` · `pictures/canvas/art/framed (&/and/+//) prints` · `plaques` ·
`stained glass panels` · `^pictures$` · `textile art` · `mixed media` ·
`photography`.

**`mirros` — the source's typo for "Mirrors" — has its own explicit rule.** Keep it.

Major Categories mapping straight to Wall Decor: `Wall Decor & Mirrors`,
`Wall Decor`, `Wall Decor and Mirrors`, `Wall Decor & Clocks`, `Wall Decorations`,
`Mirrors`, `Mirrors & Art`, `Clocks`, `Wall Art`, `Wall Arts`, `Art`, `Fine Art`.

### The loose "wall + decor noun" tier

Catches `Wall Decorative Art`, `Wall Objects`, `Wall Signs` — a "wall" token plus
any of `art`, `decor`, `decorative`, `decoration(s)`, `hanging(s)`, `sculptures`,
`plaques`, `panels`, `murals`, `decals`, `signs`, `objects`, `tapestry*`, `posters`,
`pictures`, `frames`, `clocks`, `mirrors`.

It deliberately does **not** fire on `Wall Lights`, `Wall Sconces`, `Wall Hooks` or
`Wall Vases` — the "and not a lighting word" clause plus the noun list handle this.

---

## `ART_HEAD` — "Art" as a branch head vs "Art" as a material

A name **headed** by `art` / `arts` / `artwork` / `fine art` is a wall-art branch
("Art & Picture Frames", "Art by Type") → **Wall Decor**.

But `Art Objects`, `Art Glass`, `Art Toys`, `Art Pieces` are decorative objects →
**Decorative Home Accessories**. The regex carries an explicit negative lookahead
for exactly those four. Do not collapse it.

---

## THE MIRROR/LIGHT BOUNDARY — the head noun decides

`Bathroom Mirrors`, `Vanity Mirrors`, `Lighted Mirrors` and `Mirrors with Lights`
are **Wall Decor**. `Mirror Lights`, `Bathroom Mirror Lighting` and
`Vanity/Bath Mirror Wall Lights` are **Lighting**.

"Mirrors **with** Lights" is still a mirror. See `lighting.md` for the full table —
the same rule is documented on both sides on purpose.

Room words never exclude (Rule 0), and **Rule 0.3: mirrors are always in scope**
regardless of how the site grouped them.

---

## THE INHERITANCE TRAP

A leaf inheriting its parent group's class can be dragged into the wrong workbook.
`Coat Racks and Wall Hooks` under an `Art` group became Wall Decor that way.

The rule: **check a next-task classification on the leaf's OWN name before
inheriting — but only inside umbrella Categories.** Inside a decisive section a
child is never deferred by its own name (a `Bath` group under Lighting is bath
*lighting*).

Related shelving guard: match `shelves` / `shelving`, **never a bare `shelf`** —
"Shelf and table accessories" is a decor-styling group, not furniture. `wall
shelves` is claimed by Wall Decor; `shelves`/`shelving`/`etageres`/`ledges` are
next-task furniture detectors.

---

## OPEN, UNRESOLVED: ambiguous wall shelving

The Furniture run has flagged "wall shelves" nodes across **ten companies**
(~1,300+ products) where the site files them under Furniture but the products are
wall-mounted. This crosses the Wall-Decor / Furniture line and is **one decision**,
recorded in `pipeline/furniture_json_archive/qa_notes.md`. Do not settle it
per-company or silently inside a re-split.
