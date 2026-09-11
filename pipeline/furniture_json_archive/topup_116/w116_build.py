import json, os, io

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'w116_raw.txt')
OUT = os.path.join(BASE, 'f116.json')
URL = 'https://www.maisonsdumonde.com/BE/nl/c/'

# index -> (english name, group key)
EN = {
    13: 'Garden Furniture Sets',
    14: 'Garden Sofas',
    15: 'Garden Tables',
    16: 'Garden Chairs',
    17: 'Garden Armchairs',
    18: 'Garden Sun Loungers',
    19: 'Garden Benches',
    20: 'Hanging Chairs and Hammocks',
    22: 'Outdoor Coffee Tables and Side Tables',
    23: 'Modular Garden Sofas',
    40: 'Sofas',
    41: 'Coffee Tables',
    42: 'Armchairs',
    43: 'TV and Media Units',
    44: 'Bookcases',
    45: 'Shelving Units',
    46: 'Storage Furniture',
    47: 'Console Tables',
    48: 'Side Tables',
    49: 'Stools',
    52: 'Dining Tables',
    53: 'Dining Chairs',
    54: 'Dining Armchairs',
    55: 'Sideboards',
    56: 'Sideboards and Dressers',
    57: 'Display Cabinets',
    58: 'Bar Units',
    59: 'Bar Chairs and Bar Stools',
    60: 'Benches',
    62: 'Beds',
    63: 'Headboards',
    64: 'Bedside Tables',
    67: 'Chests of Drawers',
    68: 'Cabinets',
    69: 'Dressing Tables',
    70: 'Wardrobes',
    71: 'Bed End Benches',
    72: 'Room Dividers',
    73: 'Clothes Rails and Stands',
    75: 'Shoe Cabinets',
    76: 'Hallway Benches',
    77: 'Coat Stands and Wall Hooks',
    79: 'Desks',
    80: 'Office Chairs',
    82: 'Kitchen Base Units',
    83: 'Kitchen Wall Units',
    84: 'Kitchen Islands and Trolleys',
    86: 'Single Basin Bathroom Vanity Units',
    163: 'Kids Wardrobes',
    164: 'Kids Chests of Drawers',
    165: 'Kids Desks',
    166: 'Kids Bookcases and Shelves',
    167: 'Kids Armchairs and Poufs',
    168: 'Kids Desk Chairs',
    169: 'Kids Garden Furniture',
    171: 'Kids Beds',
    172: 'Cribs',
    173: 'Kids Bedside Tables',
    174: 'Kids Headboards and Bed Accessories',
    204: 'Changing Tables',
}

GROUPS = [
    ('Garden Furniture', [13, 14, 23, 15, 22, 16, 17, 18, 19, 20]),
    ('Living Room Furniture', [40, 42, 41, 48, 43, 44, 45, 46, 47, 49]),
    ('Dining Room Furniture', [52, 53, 54, 55, 56, 57, 58, 59, 60]),
    ('Bedroom Furniture', [62, 63, 64, 67, 68, 69, 70, 71, 72, 73]),
    ('Hallway Furniture', [75, 76, 77]),
    ('Office Furniture', [79, 80]),
    ('Kitchen Furniture', [82, 83, 84]),
    ('Bathroom Furniture', [86]),
    ('Kids Furniture', [163, 164, 165, 166, 167, 168, 169]),
    ('Baby and Kids Bedroom Furniture', [171, 172, 173, 174]),
    ('Nursery Furniture', [204]),
]

FLAGS = {
    77: 'MANUAL REVIEW: node mixes coat stands (furniture) with wall hooks (not furniture); the site files it under its Hallway Furniture group',
    45: 'MANUAL REVIEW: ambiguous shelving - site files "Rekken" (shelving units) under Living Room Furniture, tiles are freestanding shelving units',
}


def load_raw():
    d = {}
    with io.open(RAW, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split('|')]
            i = int(parts[0])
            d[i] = {'nl': parts[1], 'cnt': parts[2], 'slug': parts[3]}
    return d


def main():
    raw = load_raw()
    rows = []
    missing = []
    for gname, idxs in GROUPS:
        kids = [i for i in idxs if i in raw and raw[i]['cnt'] not in ('DEAD',)]
        if not kids:
            continue
        rows.append({'category': 'Furniture', 'sub_category': gname, 'qty': None,
                     'link': None, 'is_group': True, 'evidence': None, 'flag': None})
        for i in idxs:
            if i not in raw:
                missing.append(i)
                continue
            r = raw[i]
            if r['cnt'] == 'DEAD':
                continue
            qty = None
            ev = None
            flag = FLAGS.get(i)
            if r['cnt'].isdigit():
                qty = int(r['cnt'])
                ev = "rendered listing header '%d artikelen' on the category page" % qty
            else:
                flag = (flag + ' | ' if flag else '') + 'MANUAL REVIEW: no product count found on the listing page'
            rows.append({'category': 'Furniture', 'sub_category': EN[i], 'qty': qty,
                         'link': URL + r['slug'], 'is_group': False,
                         'evidence': ev, 'flag': flag})
    doc = {
        'sr': 116,
        'company': 'Maisons du Monde BE',
        'brand_site': 'maisonsdumonde.com',
        'country': 'Belgium',
        'site_url': 'https://www.maisonsdumonde.com/BE/nl',
        'status': 'ok' if not missing else 'partial',
        'failure_reason': None if not missing else 'DataDome rate-limit blocked verification of %d leaf categories: %s' % (len(missing), missing),
        'notes': open(os.path.join(BASE, 'w116_notes.txt'), encoding='utf-8').read().strip() if os.path.exists(os.path.join(BASE, 'w116_notes.txt')) else '',
        'rows': rows,
    }
    with io.open(OUT, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print('rows', len(rows), 'leaves', sum(1 for r in rows if not r['is_group']),
          'groups', sum(1 for r in rows if r['is_group']), 'missing', missing)


if __name__ == '__main__':
    main()
