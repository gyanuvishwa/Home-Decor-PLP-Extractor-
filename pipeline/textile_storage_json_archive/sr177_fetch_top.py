import json
from sr177_lib import get_category_info

slugs = [
    "CurtainRailBlind", "CarpetRugMat", "Cushion",
    "BathToiletLaundry", "Laundry", "CleaningLaundry",
    "InteriorLifeGoods", "LifeSuppliesDailyNecessities", "Baby",
    "Storage-Furniture", "StorageRackDresser", "OfficeBookshelfStationery",
    "KitchenStorage", "TvStandLivingStorage",
    "GardeningLeisureOutdoor", "OutdoorTravel", "Desk-Officechair",
]

out = {}
for slug in slugs:
    url = f"https://www.nitori-net.jp/ec/cat/{slug}/1/"
    info = get_category_info(url)
    out[slug] = info
    print(slug, "->", info.get("h1"), "subcats:", len(info.get("subcats", [])), "total:", info.get("total_results"))

with open("sr177_top_levels.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
