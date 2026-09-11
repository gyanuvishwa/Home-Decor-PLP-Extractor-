from curl_cffi import requests
import re

names = [
"bed_sheets","dhurries","door_mats","kids_furnishings","curtain_accessories",
"bath_mats","yoga_mats","runners","bath_linen","bed_linen","curtains",
"sofaa_covers_and_throws","cushions_and_covers","essentials","laundry_baskets",
"blankets_and_quilts","home_linen","carpets","pet_furnishings","furnishing_gift_sets",
"mosquito_nets","picnic_mats","chair_covers_and_pads","sofa_covers_and_throws",
"furnishing_finds","bedroom_furnishings","living_room_furnishings","rugs_and_carpets"
]

for n in names:
    url = f"https://www.pepperfry.com/sitemap/{n}.xml"
    try:
        r = requests.get(url, impersonate="chrome", timeout=20)
        locs = re.findall(r"<loc>(.*?)</loc>", r.text)
        print(f"=== {n} ({r.status_code}) — {len(locs)} locs ===")
        for l in locs:
            print("  ", l)
    except Exception as e:
        print(n, "ERROR", e)
