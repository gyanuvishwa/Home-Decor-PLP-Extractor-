"""Classify each source row into KD / LIGHT / WALL / None (unassigned).

Precedence, per instruction 13:  PRODUCT CATEGORY / SUBCATEGORY  ->  MAJOR CATEGORY
so a decisive sub-category name overrides the section's major Category.
"""
import re

KD, LIGHT, WALL, DECOR = 'KD', 'LIGHT', 'WALL', 'DECOR'
# Deferred to the NEXT task - identified, but deliberately left unassigned.
FUT_BATH, FUT_STORE, FUT_FURN = 'FUT_BATH', 'FUT_STORAGE', 'FUT_FURNITURE'

# ---------------------------------------------------------------- major Category
CAT_MAP = {
    # --- Lighting
    'lighting': LIGHT, 'outdoor lighting': LIGHT,
    # --- Kitchen & Dining
    'kitchen & dining': KD, 'kitchen and dining': KD, 'kitchen & tableware': KD,
    'kitchen & dinning': KD, 'dining & kitchen': KD, 'glassware': KD,
    'tableware': KD, 'silverware': KD, 'bar & drinkware': KD,
    'table linen & accessories': KD,
    # --- Wall Decor (mirrors + clocks live here per the brief)
    'wall decor & mirrors': WALL, 'wall decor': WALL, 'wall decor and mirrors': WALL,
    'wall decor & clocks': WALL, 'wall decorations': WALL, 'mirrors': WALL,
    'mirrors & art': WALL, 'clocks': WALL, 'wall art': WALL, 'wall arts': WALL,
    'art': WALL, 'fine art': WALL,
}

# ---------------------------------------------------------------- name rules
# Guard first: things that merely *sound* like another class.
NOT_LIGHT = re.compile(
    r'candle|tea\s?light|votive|wax\b|diffuser|fragrance|incense|scent'
    r'|\bsigns?\b|\bdiyas?\b', re.I)

# A mirror-shaped name whose head noun is really a light fixture
# ("Mirror Lights", "Bathroom Mirror Lighting", "Vanity/Bath Mirror Wall Lights").
# "Mirrors with Lights" / "Lighted Mirrors" are mirrors and must NOT match.
MIRROR_LIGHT = re.compile(
    r'\bmirrors?\s*[/&-]?\s*(bath\w*\s*|vanity\s*|wall\s*|picture\s*)*'
    r'light(s|ing)?\b', re.I)

WALL_RE = re.compile(
    r'\bmirrors?\b'
    r'|\bclocks?\b'
    r'|\bwall\s*(art|arts|decor|décor|decoration|decorations|hanging|hangings|'
    r'sculptures?|accents?|accessories|decals?|plaques?|panels?|murals?|prints?|'
    r'pictures?|frames?|tapestr\w*|shelves)\b'
    r'|\bwall[-\s]?mounted\s*decor'
    r'|\bwall\s*art\b|\bartwork\b|\bart\s*prints?\b|\bcanvas\s*art\b'
    r'|\bframed\s*art\b|\bpaintings?\b|\btapestr\w*|\bposters?\b'
    r'|\bwall\s*sculptures?\b|\bwall\s*hangings?\b'
    r'|\b(pictures?|canvas|art|framed)\s*(&|and|\+|/)?\s*prints?\b'
    r'|\bmirros\b'                       # source typo for "Mirrors"
    r'|\bplaques?\b|\bstained\s*glass\s*panels?\b|^pictures$'
    r'|\btextile\s*art\b|\bmixed\s*media\b|\bphotography\b', re.I)

# "Wall" plus a decor noun somewhere in the name ("Wall Decorative Art",
# "Wall Objects", "Wall Signs").  Deliberately does NOT fire on "Wall Lights",
# "Wall Sconces", "Wall Hooks", "Wall Vases".
WALL_LOOSE_A = re.compile(r'\bwall[-\s]?\w*\b|\bwall\b', re.I)
WALL_LOOSE_B = re.compile(
    r'\b(art|arts|decor|décor|decorative|decoration|decorations|hanging|hangings'
    r'|sculptures?|plaques?|panels?|murals?|decals?|signs?|objects?|tapestr\w*'
    r'|posters?|pictures?|frames?|clocks?|mirrors?)\b', re.I)

LIGHT_RE = re.compile(
    r'\blights?\b|\blighting\b|\blamps?\b|\blampshades?\b|\blamp\s*shades?\b'
    r'|\bsconces?\b|\bchandeliers?\b|\bpendants?\b|\blanterns?\b|\bluminaires?\b'
    r'|\bbulbs?\b|\bled\b|\bflush\s*mount\w*|\bsemi[-\s]?flush\w*|\brecessed\b'
    r'|\btrack\s*(lighting|light|rail|system)|\bdownlights?\b|\bspotlights?\b'
    r'|\bfloodlights?\b|\billuminat\w*|\blight\s*fixtures?\b|\bsuspension\b'
    r'|\buplights?\b|\bwall\s*wash\w*|\bpicture\s*lights?\b|\bnight\s*lights?\b',
    re.I)

KD_RE = re.compile(
    r'\bglassware\b|\bserveware\b|\bservingware\b|\bserving\s*ware\b|\bdrinkware\b'
    r'|\bdinnerware\b|\btableware\b|\bbarware\b|\bteaware\b|\bflatware\b'
    r'|\bcutlery\b|\bcrockery\b|\bdishware\b|\btabletop\b|\bopalware\b'
    r'|\bserving\s*(bowls?|trays?|platters?|dishes|plates?|sets?|pieces?|'
    r'accessories|utensils?|boards?|spoons?)\b'
    r'|\bplatters?\b|\bdinner\s*sets?\b|\bdinnerset\b'
    r'|\b(wine|beer|champagne|cocktail|shot|whisk\w*|martini|highball|water|'
    r'juice|drinking|bar)\s*glass(es)?\b'
    r'|\bglasses\b|\btumblers?\b|\bgoblets?\b|\bsteins?\b|\bstemware\b'
    r'|\bmugs?\b|\bteacups?\b|\btea\s*cups?\b|\bcups?\s*&\s*mugs?\b'
    r'|\bdecanters?\b|\bcarafes?\b|\bpitchers?\b|\bteapots?\b|\bjugs?\b'
    r'|\bfine\s*china\b|\bchinaware\b|\bcoasters?\b|\bplacemats?\b'
    r'|\btable\s*linens?\b|\bnapkins?\b|\btable\s*runners?\b'
    r'|\bcake\s*stands?\b|\bbutter\s*dish\w*|\bsalad\s*bowls?\b'
    r'|\bsugar\s*bowls?\b|\bcreamers?\b|\btrivets?\b|\bcondiment\b',
    re.I)

# "Decorative plates/bowls/trays" are decor objects, not serveware; and a bare
# "tabletop" must not drag frames / fountains / mirrors into Kitchen & Dining.
NOT_KD = re.compile(
    r'\bdecorative\b|\bdecor\b|\bframes?\b|\bmirrors?\b|\bpictures?\b'
    r'|\bphotos?\b|\bfountains?\b|\bclocks?\b|\bvases?\b|\blamps?\b'
    r'|\blights?\b|\blighting\b|\bvanity\b', re.I)


# ---------------------------------------------------------------- decorative
# STRICT: the product types the brief names explicitly as Decorative Home
# Accessories.  These override the section's major Category (but never Wall
# Decor or Lighting, which are tested first) - so "Decorative Bowls" filed by a
# site under Kitchen & Dining still lands in the decorative file.
DECOR_STRICT = re.compile(
    r'\bdecorative\s*(bowls?|trays?|plates?|platters?|dishes|vases?|objects?|'
    r'objets?|accessor\w*|accents?|boxes|box|jars?|baskets?|pots?|planters?|'
    r'figurines?|figures?|sculptures?|statues?|ornaments?|items?|globes?|'
    r'letters?|spheres?|centerpieces?|containers?|collectibles?|storage)\b'
    r'|\bdecor\s*(bowls?|trays?|objects?|accents?)\b'
    r'|\baccent\s*(bowls?|trays?)\b'
    r'|\bsculptures?\b|\bfigurines?\b|\bstatues?\b|\bbookends?\b|\bbook\s*ends?\b'
    r'|\bphoto\s*frames?\b|\bpicture\s*frames?\b|\bphotoframes?\b'
    r'|\bphoto\s*&\s*picture\s*frames?\b|\bphoto\s*and\s*picture\s*frames?\b'
    r'|\bornaments?\b|\bcandle\s*holders?\b|\bcandleholders?\b'
    r'|\btealight\s*holders?\b|\btea\s*light\s*holders?\b'
    r'|\bplanters?\b|\bplant\s*pots?\b'
    # A branch HEADED by "Vase(s)" is decorative wherever a site filed it.
    # "Table Vases" is not matched - see the Kitchen & Dining note below.
    r'|^vases?\b', re.I)
# NB: "Table Accents" / "Table Decor" / "Home Accents" are deliberately NOT in
# the override tier - a site that files Charger Plates or Table Vases under a
# Kitchen & Dining > Table Accents branch has stated an explicit hierarchy, and
# the brief says not to override that. They are picked up by DECOR_BROAD when
# nothing else claims them.

# BROAD: applied ONLY to records that would otherwise stay unassigned, so the
# three existing files are never quietly drained by it.
DECOR_BROAD = re.compile(
    r'\bvases?\b|\bvessels?\b|\burns?\b|\bcachepots?\b|\bflower\s*pots?\b'
    r'|\bflowerpots?\b|\bpots?\b|\bplant\s*pot\b|\bplanters?\b|\bterracotta\b'
    r'|\bcandles?\b|\bcandleholders?\b|\bcandlesticks?\b|\bcandelabras?\b'
    r'|\bcandleware\b|\bcandlelights?\b|\btealights?\b|\btea\s*lights?\b'
    r'|\bvotives?\b|\bhurricanes?\b|\bwindlights?\b|\bdiyas?\b|\bcandle\b'
    r'|\bfigurines?\b|\bsculptures?\b|\bstatues?\b|\bidols?\b|\bshowpieces?\b'
    r'|\bornaments?\b|\bcollectibles?\b|\bartefacts?\b|\bartifacts?\b'
    r'|\bbookends?\b|\bbook\s*ends?\b|\bpaperweights?\b|\bbooks?\b'
    r'|\bframes?\b|\bphoto\s*albums?\b|\bshadow\s*box\b|\bphoto\s*clips?\b'
    r'|\bdecorativ\w*|\bdecoratives?\b|\bdecorations?\b|\bdecorator\b'
    r'|\bdecor\b|\bdecor\s*accents?\b|\baccents?\b|\bdecoration\b'
    r'|\bbowls?\b|\btrays?\b|\bplatters?\b|\bplates?\b|\bdishes\b|\bjars?\b'
    r'|\bbottles?\b|\bcanisters?\b|\bcatchalls?\b|\bcloches?\b|\burli\b'
    r'|\btrinkets?\b|\bjewell?ery\s*box\w*|\bjewelry\s*box\w*|\bmoney\s*box\w*'
    r'|\bpiggy\s*banks?\b|\bcoin\s*banks?\b|\bsnow\s*globes?\b|\bglobes?\b'
    r'|\bboxes\b|\bbox\b|\bmirros\b|\bcenterpieces?\b|\bcentrepieces?\b'
    r'|\bwind\s*chimes?\b|\bwindchimes?\b|\bwind\s*spinners?\b|\bsuncatchers?\b'
    r'|\bfountains?\b|\bwater\s*features?\b|\bbird\s*baths?\b|\bbird\s*feeders?\b'
    r'|\bbirdhouses?\b|\bgarden\s*gnomes?\b|\bgnomes?\b|\bmailboxes\b'
    r'|\bdried\s*flowers?\b|\bfaux\s*flowers?\b|\bflowers?\b|\bplants?\b'
    r'|\bpebbles?\b|\bmoss\b|\bmobiles?\b|\bashtrays?\b|\btissue\s*box\w*'
    r'|\bumbrella\s*stands?\b|\bplinths?\b|\bpedestals?\b|\beasels?\b'
    r'|\bmagazine\s*holders?\b|\bkey\s*holders?\b|\bjharokhas?\b|\bmezuzahs?\b'
    r'|\bporcelain\b|\bbronzes?\b|\bpewter\b|\benamel\b|\bmarble\s*decor\b'
    r'|\bglass\s*decor\w*|\bbrass\s*decorativ\w*|\bpapier\s*mache\b'
    r'|\bmusical\s*boxes\b|\blimoges\b|\bherend\b|\bmeissen\b|\bdresden\b'
    r'|\bnymphenburg\b|\bhalcyon\b|\bhandblown\s*glass\b|\bart\s*glass\b'
    r'|\bart\s*objects?\b|\bart\s*toys?\b|\bart\s*pieces?\b|\bobjet\b'
    r'|\bobjects?\b|\bminiatures?\b|\bchess\s*sets?\b|\bnovetiles\b'
    r'|\bgarden\s*(decor\w*|accents?|statues?|sculptures?|showpieces?|'
    r'ornaments?|balls?|bells?)\b|\blawn\s*&\s*garden\b'
    r'|\bhome\s*decor\w*|\bhome\s*accessor\w*|\binterior\s*accessor\w*'
    r'|\bshowpiece\b|\breligious\b|\bspiritual\b|\bpooja\b|\bdevotion\b'
    r'|\bcelebration\s*ring\b|\bporcelain\s*houses?\b|\bcloche\b', re.I)

# A name headed by "Art" is a wall-art branch ("Art & Picture Frames",
# "Art by Type"), but "Art Objects/Glass/Toys/Pieces" are decorative objects.
ART_HEAD = re.compile(
    r'^(arts?|artwork|fine\s+art)\b(?!\s*(objects?|glass|toys?|pieces?))', re.I)

# Unambiguous Kitchen & Dining scope words - these beat DECOR_STRICT.
KD_HARD = re.compile(
    r'\bserveware\b|\bservingware\b|\btableware\b|\bdrinkware\b|\bglassware\b'
    r'|\bdinnerware\b|\bbarware\b|\bteaware\b|\bflatware\b|\bcrockery\b'
    r'|\bserving\b', re.I)

# ---------------------------------------------------------------- future tasks
FUTURE_BATH = re.compile(
    r'\bbathrooms?\b|\bbath\b|\bsoap\b|\btoothbrush\b|\btoilet\b'
    r'|\bshower\b|\bvanity\s*(sets?|accessor\w*)\b', re.I)
FUTURE_BATH_CATS = {
    'bathroom', 'bathroom accessories', 'bath', 'bath accessories',
    'bed & bath', 'bath & more', 'bathroom decor',
}
FUTURE_STORAGE = re.compile(
    r'\bstorage\b|^baskets?$|\bstorage\s*baskets?\b|\bbins?\b', re.I)
FUTURE_FURNITURE = re.compile(
    # "shelves"/"shelving" only - a bare "shelf" appears inside decor-styling
    # group names such as "Shelf and table accessories".
    r'\bshelves\b|\bshelving\b|\betageres?\b|\bledges\b'
    r'|\bcoat\s*stands?\b|\bcoat\s*racks?\b|\bhat\s*stands?\b', re.I)


def future_class(name, cat=None):
    """A record that clearly belongs to a NEXT-task category, or None."""
    if cat and str(cat).strip().lower() in FUTURE_BATH_CATS:
        return FUT_BATH
    if not name:
        return None
    s = str(name).strip()
    if FUTURE_BATH.search(s):
        return FUT_BATH
    if FUTURE_STORAGE.search(s):
        return FUT_STORE
    if FUTURE_FURNITURE.search(s):
        return FUT_FURN
    return None


def decor_fallback(name):
    """Broad decorative sweep - only for otherwise-unassigned records."""
    if not name:
        return None
    return DECOR if DECOR_BROAD.search(str(name).strip()) else None


def name_class(name):
    """Decisive class implied by a Sub-Category name, or None."""
    if not name:
        return None
    s = str(name).strip()
    if MIRROR_LIGHT.search(s):
        return LIGHT
    if WALL_RE.search(s) or ART_HEAD.search(s):
        return WALL
    if re.search(r'\bwall\b|\bwall[-\s]', s, re.I) and WALL_LOOSE_B.search(s) \
            and not LIGHT_RE.search(s):
        return WALL
    if LIGHT_RE.search(s) and not NOT_LIGHT.search(s):
        return LIGHT
    # An explicit serveware/tableware scope note wins over a "Decorative ..."
    # phrase buried inside it, e.g. "Serveware (Decorative Objects & Vases,
    # filtered to Serveware)".
    if DECOR_STRICT.search(s) and not KD_HARD.search(s):
        return DECOR
    if KD_RE.search(s) and not NOT_KD.search(s):
        return KD
    return None


def cat_class(cat):
    if not cat:
        return None
    return CAT_MAP.get(str(cat).strip().lower())
