# Decorative Home Accessories — category boundary rules

Load with `_decor-extraction-core.md`. Workbook:
`Decorative_Home_Accessories.xlsx` (1,706 records at the 2026-08-14 split).

This is the **fourth** file, added in a refinement pass because the first split's
narrow rules left 1,704 valid decor records unassigned. Do not repeat that
under-inclusive first cut.

**Executable source of truth:** `pipeline/category_split/classify.py` —
`DECOR_STRICT`, `DECOR_BROAD`, `KD_HARD`, `decor_fallback()`. This module documents
that code; it does not replace it.

---

## THE TWO TIERS — this is the load-bearing design

**A single broad "looks decorative" rule corrupts the other three files.** It
silently drained Kitchen & Dining: a `Table Accents` group under a `Kitchen &
Dining` Category swept `Charger Plates`, `Table Vases` and `Flower Centerpieces`
out with it. Hence two tiers, and they must stay two tiers.

### Tier 1 — OVERRIDE (`DECOR_STRICT`)
May beat a decisive source Category. Runs *after* Wall Decor and Lighting (so it
never steals from those two) and *before* Kitchen & Dining.

Only the product types the brief names outright:
`decorative <bowls/trays/plates/platters/dishes/vases/objects/objets/accessories/
accents/boxes/box/jars/baskets/pots/planters/figurines/figures/sculptures/statues/
ornaments/items/globes/letters/spheres/centerpieces/containers/collectibles/
storage>` · `decor <bowls/trays/objects/accents>` · `accent <bowls/trays>` ·
`sculptures` · `figurines` · `statues` · `bookends` · `photo/picture frames` ·
`ornaments` · `candle holders` · `tealight holders` · `planters` · `plant pots` ·
and a branch **headed** by `^vase(s)`.

So "Decorative Bowls" filed by a site under Kitchen & Dining still lands here.

**Counter-override:** `KD_HARD` beats this tier — an explicit serveware/tableware
scope word (`serveware`, `servingware`, `tableware`, `drinkware`, `glassware`,
`dinnerware`, `barware`, `teaware`, `flatware`, `crockery`, `serving`) keeps the row
in Kitchen & Dining even when a "Decorative …" phrase is buried inside the name.

**Deliberately NOT in tier 1:** `Table Accents`, `Table Decor`, `Home Accents`, and
`Table Vases`. A site that files Charger Plates or Table Vases under a `Kitchen &
Dining > Table Accents` branch has stated an explicit hierarchy, and the brief says
not to override it. These reach this file only through tier 2, if nothing else
claimed them.

### Tier 2 — FALLBACK (`DECOR_BROAD`)
Applied **only** to records that would otherwise stay unassigned, so the other three
files can never be quietly drained by it.

Broad decorative vocabulary: vases/vessels/urns/cachepots/flower pots/planters/
terracotta · candles, candleholders, candlesticks, candelabras, tealights, votives,
hurricanes, windlights, **diyas** · figurines/sculptures/statues/idols/showpieces/
ornaments/collectibles/artefacts · bookends/paperweights/books · frames/photo albums/
shadow box · decorative*/decorations/decor/accents · bowls/trays/platters/plates/
dishes/jars/bottles/canisters/catchalls/cloches/urli · trinkets/jewellery boxes/
money boxes/piggy banks/snow globes/globes/boxes · centerpieces · wind chimes/
spinners/suncatchers · fountains/water features/bird baths/feeders/birdhouses/
garden gnomes/mailboxes · dried & faux flowers/plants/pebbles/moss/mobiles ·
ashtrays/tissue boxes/umbrella stands/plinths/pedestals/easels/magazine holders/
key holders/jharokhas/mezuzahs · porcelain/bronzes/pewter/enamel/marble decor/
glass decor/brass decorative/papier mache · musical boxes and the porcelain maker
names (Limoges, Herend, Meissen, Dresden, Nymphenburg, Halcyon) · handblown glass/
art glass/art objects/art toys/art pieces/objet/objects/miniatures/chess sets ·
garden decor/accents/statues/sculptures/showpieces/ornaments/balls/bells ·
home decor*/home accessories/interior accessories · religious/spiritual/pooja/
devotion · `mirros` *(source typo, also caught here)*.

Tier 2 is applied to the row's own name first, then to its parent group's name.

---

## BOUNDARY NOTES

- **Candles and tealights are decor, not lighting.** The Lighting guard
  (`NOT_LIGHT`) pushes `candle`, `tea light`, `votive`, `wax`, `diffuser`,
  `fragrance`, `incense`, `scent` and `diyas` out of Lighting; they land here.
- **`Diyas (Decorative Oil Lamps)`** matched the lighting rule on "lamps" and had to
  be guarded out explicitly — they are decorative/religious items.
- **`Art Objects` / `Art Glass` / `Art Toys` / `Art Pieces` are decorative objects**,
  not wall art. A name *headed* by `art`/`arts`/`artwork`/`fine art` is a wall-art
  branch and goes to Wall Decor instead.
- Mirrors and clocks are **never** here — Wall Decor owns both.
- Home fragrance and diffusers are in project scope and land here.

---

## WHAT STAYS UNASSIGNED — do not sweep it in

Tier 2 is broad, so the deferral tests run around it deliberately. Leave these out:

- **Next-task records:** Bathroom (27), Furniture (14), Storage (7) — 48 records
  held in the review pool **on purpose** for a future task, not a gap to fill.
  Detectors are `FUTURE_BATH` / `FUTURE_STORAGE` / `FUTURE_FURNITURE`.
- **Genuinely out of scope (43):** curtain rods/poles/tiebacks (~35), hooks and
  racks, desk accessories, fire screens.

Final reconciliation at the 2026-08-14 split:
**2,352 K&D / 2,499 Lighting / 1,275 Wall Decor / 1,706 Decorative = 7,832 of 7,923
quantity records, 0 duplicates, 0 lost.** Any re-split must reconcile to zero lost
rows — that is what `pipeline/category_split/reconcile.py` is for.
