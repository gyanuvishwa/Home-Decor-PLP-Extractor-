import requests, re, json, time, sys

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}

urls = """https://royaldesign.com/us/storage
https://royaldesign.com/us/storage/clothing-storage
https://royaldesign.com/us/storage/clothing-storage/hooks-hangers
https://royaldesign.com/us/storage/clothing-storage/wardrobes-clothes-hangers
https://royaldesign.com/us/storage/furniture
https://royaldesign.com/us/storage/furniture/bookcases
https://royaldesign.com/us/storage/furniture/cabinets-display-cabinets
https://royaldesign.com/us/storage/furniture/cabinets-display-cabinets/ek
https://royaldesign.com/us/storage/furniture/cabinets-display-cabinets/svart
https://royaldesign.com/us/storage/furniture/cabinets-display-cabinets/tra
https://royaldesign.com/us/storage/furniture/cabinets-display-cabinets/vit
https://royaldesign.com/us/storage/furniture/chest-of-drawers
https://royaldesign.com/us/storage/furniture/drawer-unit
https://royaldesign.com/us/storage/furniture/modular-shelving-systems
https://royaldesign.com/us/storage/furniture/sideboards
https://royaldesign.com/us/storage/furniture/sideboards/ek
https://royaldesign.com/us/storage/furniture/sideboards/svart
https://royaldesign.com/us/storage/furniture/sideboards/vit
https://royaldesign.com/us/storage/furniture/step-stools
https://royaldesign.com/us/storage/furniture/tv-media-benches
https://royaldesign.com/us/storage/furniture/wall-cabinets
https://royaldesign.com/us/storage/furniture/wall-shelves
https://royaldesign.com/us/storage/hallway-storage
https://royaldesign.com/us/storage/hallway-storage/coat-stands
https://royaldesign.com/us/storage/hallway-storage/doorstops-shoe-horns
https://royaldesign.com/us/storage/hallway-storage/hat-racks
https://royaldesign.com/us/storage/hallway-storage/shoe-cabinets
https://royaldesign.com/us/storage/hallway-storage/shoe-racks
https://royaldesign.com/us/storage/hallway-storage/umbrella-stands
https://royaldesign.com/us/storage/kids-storage
https://royaldesign.com/us/storage/kids-storage/book-stands-boxes
https://royaldesign.com/us/storage/kids-storage/kids-clothing-storage
https://royaldesign.com/us/storage/kids-storage/toy-storage
https://royaldesign.com/us/storage/small-storage
https://royaldesign.com/us/storage/small-storage/baskets
https://royaldesign.com/us/storage/small-storage/boxes-crates
https://royaldesign.com/us/storage/small-storage/firewood-storage-fire-safety
https://royaldesign.com/us/storage/small-storage/flower-shelves
https://royaldesign.com/us/storage/small-storage/jewellery-boxes-bonbonnieres
https://royaldesign.com/us/storage/small-storage/magazine-storage
https://royaldesign.com/us/storage/small-storage/waste-bins-pedal-bins
https://royaldesign.com/us/textiles--rugs
https://royaldesign.com/us/textiles--rugs/bathroom-textiles
https://royaldesign.com/us/textiles--rugs/bathroom-textiles/bathrobes--slippers
https://royaldesign.com/us/textiles--rugs/bathroom-textiles/bathroom-rugs
https://royaldesign.com/us/textiles--rugs/bathroom-textiles/handtowels--bathtowels
https://royaldesign.com/us/textiles--rugs/bathroom-textiles/shower-curtains
https://royaldesign.com/us/textiles--rugs/bedroom-textiles
https://royaldesign.com/us/textiles--rugs/bedroom-textiles/bed-skirts
https://royaldesign.com/us/textiles--rugs/bedroom-textiles/bed-spreads
https://royaldesign.com/us/textiles--rugs/bedroom-textiles/bedding-sets
https://royaldesign.com/us/textiles--rugs/bedroom-textiles/bottom-sheets
https://royaldesign.com/us/textiles--rugs/bedroom-textiles/duvets
https://royaldesign.com/us/textiles--rugs/bedroom-textiles/pillowcases
https://royaldesign.com/us/textiles--rugs/bedroom-textiles/pillows--quilts
https://royaldesign.com/us/textiles--rugs/childrens-textiles/bed-canopies
https://royaldesign.com/us/textiles--rugs/curtains
https://royaldesign.com/us/textiles--rugs/curtains/curtains
https://royaldesign.com/us/textiles--rugs/curtains/roman-blinds
https://royaldesign.com/us/textiles--rugs/kitchen-textiles
https://royaldesign.com/us/textiles--rugs/kitchen-textiles/aprons
https://royaldesign.com/us/textiles--rugs/kitchen-textiles/kitchen-towels
https://royaldesign.com/us/textiles--rugs/kitchen-textiles/pot-holders--oven-gloves
https://royaldesign.com/us/textiles--rugs/plaids--decorative-cushions
https://royaldesign.com/us/textiles--rugs/plaids--decorative-cushions/decorative-cushions--covers
https://royaldesign.com/us/textiles--rugs/plaids--decorative-cushions/inner-cushions
https://royaldesign.com/us/textiles--rugs/plaids--decorative-cushions/plaids--blankets
https://royaldesign.com/us/textiles--rugs/rugs
https://royaldesign.com/us/textiles--rugs/rugs/cotton--rag-rugs
https://royaldesign.com/us/textiles--rugs/rugs/door-mats
https://royaldesign.com/us/textiles--rugs/rugs/jute-rugs
https://royaldesign.com/us/textiles--rugs/rugs/patterned-rugs
https://royaldesign.com/us/textiles--rugs/rugs/pile-rug
https://royaldesign.com/us/textiles--rugs/rugs/plain-weaved-rugs
https://royaldesign.com/us/textiles--rugs/rugs/plastic-rugs
https://royaldesign.com/us/textiles--rugs/rugs/sheepskin
https://royaldesign.com/us/textiles--rugs/rugs/tufted-rugs
https://royaldesign.com/us/textiles--rugs/rugs/wool-rugs
https://royaldesign.com/us/textiles-rugs/kids-textiles
https://royaldesign.com/us/textiles-rugs/kids-textiles/kids-bedding
https://royaldesign.com/us/textiles-rugs/kids-textiles/kids-blankets
https://royaldesign.com/us/textiles-rugs/kids-textiles/kids-cushions
https://royaldesign.com/us/textiles-rugs/kids-textiles/kids-rugs
https://royaldesign.com/us/textiles-rugs/kitchen-textiles/table-cloths-runners""".strip().split("\n")

results = {}
for u in urls:
    try:
        r = requests.get(u, headers=headers, timeout=25)
        html = r.text
        status = r.status_code
        final_url = r.url
        h1m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
        h1 = re.sub('<[^>]+>','', h1m.group(1)).strip() if h1m else None
        canon_m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        canon = canon_m.group(1) if canon_m else None
        tp_m = re.search(r'"totalProducts":(\d+)', html)
        tp = int(tp_m.group(1)) if tp_m else None
        results[u] = {'status': status, 'final_url': final_url, 'h1': h1, 'canonical': canon, 'totalProducts': tp, 'len': len(html)}
        print(u, '|', status, '|', h1, '|', tp, '|', canon)
    except Exception as e:
        results[u] = {'error': str(e)}
        print(u, 'ERROR', e)

with open('rd_fetch_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
