# Lighting — category boundary rules

Load with `_decor-extraction-core.md`. Workbook: `Lighting.xlsx` (2,499 records at
the 2026-08-14 split).

**Executable source of truth:** `pipeline/category_split/classify.py` — `LIGHT_RE`,
`NOT_LIGHT`, `MIRROR_LIGHT`, and the `CAT_MAP` entries mapping to `LIGHT`. This
module documents that code; it does not replace it. To re-split, run the scripts.

---

## PRECEDENCE — where Lighting sits

A decisive Sub-Category name overrides the section's major Category. Tests run in
this fixed order (`classify.py:name_class`), and **Lighting is tested both before
and after Wall Decor** — that is deliberate, not a bug:

1. `MIRROR_LIGHT` → **LIGHT** *(runs first, ahead of Wall Decor)*
2. Wall Decor rules → WALL
3. "wall" + a decor noun, and **not** a lighting word → WALL
4. `LIGHT_RE` and **not** `NOT_LIGHT` → **LIGHT**
5. Decorative strict → DECOR
6. Kitchen & Dining → KD

Then: the section's major Category, then the parent group's class, then next-task
deferral, then the broad decorative fallback.

---

## CLAIMS (in scope for Lighting)

Head-noun lighting words: `lights`, `lighting`, `lamps`, `lampshades`,
`lamp shades`, `sconces`, `chandeliers`, `pendants`, `lanterns`, `luminaires`,
`bulbs`, `LED`, `flush mount` / `semi-flush`, `recessed`, `track lighting/light/
rail/system`, `downlights`, `spotlights`, `floodlights`, `illuminated*`,
`light fixtures`, `suspension`, `uplights`, `wall wash*`, `picture lights`,
`night lights`.

Major Categories that map straight to Lighting: `Lighting`, `Outdoor Lighting`.

Room words never exclude (Rule 0): **Bathroom Lighting and the whole Outdoor
Lighting branch are in scope** — a room-word exclusion would have wrongly dropped
them, and did not.

---

## DOES NOT CLAIM — the guards that keep Lighting clean

`NOT_LIGHT` blocks a name that merely *sounds* like lighting:
`candle`, `tea light` / `tealight`, `votive`, `wax`, `diffuser`, `fragrance`,
`incense`, `scent`, `signs`, **`diyas`**.

- **Tealights and LED candles are candles, not lighting.** They go to Decorative
  Home Accessories.
- **`Diyas (Decorative Oil Lamps)` matched on "lamps" and must not.** They are
  decorative/religious items — the `diya` guard exists specifically for this.
- **Lampshades are lighting** and stay here.

---

## THE MIRROR/LIGHT BOUNDARY — the head noun decides

This is the single most error-prone line in the split. `MIRROR_LIGHT` runs *first*,
before the Wall Decor test, precisely to catch fixtures whose name starts with
"mirror".

| Name | Goes to | Why |
|---|---|---|
| `Mirror Lights` | **Lighting** | head noun is a light fixture |
| `Bathroom Mirror Lighting` | **Lighting** | head noun is lighting |
| `Vanity / Bath Mirror Wall Lights` | **Lighting** | head noun is a light |
| `Mirrors with Lights` | Wall Decor | still a mirror |
| `Lighted Mirrors` | Wall Decor | still a mirror |
| `Bathroom Mirrors`, `Vanity Mirrors` | Wall Decor | mirrors, room word irrelevant |

The regex is written so `Mirrors with Lights` and `Lighted Mirrors` do **not**
match. Do not "simplify" it.

---

## UMBRELLA-CATEGORY TRAP

Inside a decisive section (Lighting / Kitchen & Dining / Wall Decor) a child never
gets deferred to a next-task category by its own name: **a `Bath` group under
Lighting means bath *lighting*, not bathroom.** Next-task deferral only applies
inside an umbrella Category (`Home Accessories`, `Home Decor`, `Decorative
Accessories`, `Decor` …) where the section provides no decisive scope.

Umbrella sections must be classified per group-subtree, not per section — roughly
2,700 rows sit under them with clocks, mirrors and lamps side by side.
