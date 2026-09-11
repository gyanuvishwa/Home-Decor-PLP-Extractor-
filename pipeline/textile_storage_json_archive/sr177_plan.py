# -*- coding: utf-8 -*-
# Plan: list of (group_jp, group_en, cat, subcat_jp, subcat_en, href, confidence)
# cat: "textile" or "storage"

PLAN = []

def g(group_jp, group_en, cat, items):
    for jp, en, href, conf in items:
        PLAN.append({
            "group_jp": group_jp, "group_en": group_en, "cat": cat,
            "sub_jp": jp, "sub_en": en, "href": href, "confidence": conf
        })

# ---------------- TEXTILE ----------------

g("布団・寝具", "Futon & Bedding", "textile", [
 ("ひんやり接触冷感寝具(Nクール)", "Cool-Touch Bedding (N-Cool)", "https://www.nitori-net.jp/ec/cat/Shingu/Ncool/1/", "HIGH"),
 ("敷きパッド・ベッドパッド", "Mattress Pads & Bed Pads", "https://www.nitori-net.jp/ec/cat/Shingu/PadSikiBed/1/", "HIGH"),
 ("ボックスシーツ・ベッドシーツ・敷き布団カバー・シーツ", "Fitted Sheets, Bed Sheets & Futon Mattress Covers", "https://www.nitori-net.jp/ec/cat/Shingu/Boxsheet_FutonSikiSheet/1/", "HIGH"),
 ("敷布団・折りたたみマットレス", "Futon Mattress & Folding Mattress", "https://www.nitori-net.jp/ec/cat/Shingu/futonsiki-mattressfolding/1/", "MEDIUM"),
 ("掛け布団カバー", "Duvet Covers", "https://www.nitori-net.jp/ec/cat/Shingu/FutonKakeCover/1/", "HIGH"),
 ("掛け布団・羽毛布団・毛布・タオルケット・肌布団", "Duvets, Down Duvets, Blankets & Throws", "https://www.nitori-net.jp/ec/cat/Shingu/FutonKakeseries/1/", "HIGH"),
 ("枕・抱き枕", "Pillows & Body Pillows", "https://www.nitori-net.jp/ec/cat/Shingu/Pillow/1/", "MEDIUM"),
 ("枕カバー・ピローケース", "Pillowcases", "https://www.nitori-net.jp/ec/cat/Shingu/PillowCover/1/", "HIGH"),
 ("布団セット", "Bedding Sets", "https://www.nitori-net.jp/ec/cat/Shingu/FutonSet/1/", "HIGH"),
 ("布団カバー・ベッドカバーセット", "Duvet Cover & Bed Cover Sets", "https://www.nitori-net.jp/ec/cat/Shingu/CoveringSet/1/", "HIGH"),
 ("ジャンボクッション・カバー", "Jumbo Cushions & Covers", "https://www.nitori-net.jp/ec/cat/Shingu/m1JumboCushion/1/", "HIGH"),
 ("マルチカバー", "Multi-Purpose Furniture Covers", "https://www.nitori-net.jp/ec/cat/Shingu/m1SofaMultiCoverMulti/1/", "HIGH"),
 ("子供用ベッド・布団", "Kids Beds & Futons", "https://www.nitori-net.jp/ec/cat/Shingu/m1KidsShingu/1/", "MEDIUM"),
 ("着る毛布", "Wearable Blankets", "https://www.nitori-net.jp/ec/cat/Shingu/m1BlanketWears/1/", "MEDIUM"),
 ("Nウォーム", "Warm Bedding (N-Warm)", "https://www.nitori-net.jp/ec/cat/Shingu/Nwarm/1/", "HIGH"),
])

g("カーテン", "Curtains", "textile", [
 ("ドレープカーテン", "Drape Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtain/1/", "HIGH"),
 ("遮光カーテン", "Blackout Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainLightshiel/1/", "HIGH"),
 ("レースカーテン", "Lace Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/LaceCurtain/1/", "HIGH"),
 ("カーテン・レースセット", "Curtain & Lace Sets", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/CurtainLaceSet/1/", "HIGH"),
 ("ロールスクリーン・ロールカーテン", "Roll Screens & Roll Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/RollScreen/1/", "MEDIUM"),
 ("ジャカードカーテン", "Jacquard Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainjacquard/1/", "HIGH"),
 ("オーダーカーテン", "Made-to-Order Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/OrdCurtain/1/", "HIGH"),
 ("オーダーレースカーテン", "Made-to-Order Lace Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/OrdLacecurtain/1/", "HIGH"),
 ("オーダーロールスクリーン", "Made-to-Order Roll Screens", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/OrderRollScreen/1/", "MEDIUM"),
 ("カフェカーテン・出窓カーテン", "Cafe Curtains & Bay Window Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/CafeCurtainCafe/1/", "HIGH"),
 ("のれん・すだれ・間仕切り", "Noren Door Curtains, Sudare & Room Dividers", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/Noren/1/", "MEDIUM"),
 ("シェード・シェードカーテン", "Shade Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/Screen/1/", "MEDIUM"),
 ("シャワーカーテン", "Shower Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/m1BathArticleShowercurt/1/", "HIGH"),
 ("遮熱カーテン", "Heat-Shielding Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainHeatshield/1/", "HIGH"),
 ("遮音（防音）カーテン", "Soundproof Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainSoundproofing/1/", "HIGH"),
 ("消臭カーテン", "Deodorizing Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainDeodorize/1/", "HIGH"),
 ("防炎カーテン", "Fireproof Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainFireretard/1/", "HIGH"),
 ("花粉対策カーテン", "Pollen-Blocking Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/DrapeCurtainPollencatch/1/", "HIGH"),
 ("イージーオーダーカーテン", "Easy-Order Curtains", "https://www.nitori-net.jp/ec/cat/CurtainRailBlind/EOCurtain/1/", "HIGH"),
])

g("カーペット・ラグ・マット", "Carpets, Rugs & Mats", "textile", [
 ("ひんやり接触冷感ラグ(Nクール)", "Cool-Touch Rugs (N-Cool)", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/Cooling_contact_rug/1/", "HIGH"),
 ("ラグ", "Rugs", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/Rug/1/", "HIGH"),
 ("厚地ラグ", "Thick Rugs", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/ThickRug/1/", "HIGH"),
 ("カーペット", "Carpets", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/Carpet/1/", "HIGH"),
 ("タイルカーペット・吸着タイルマット", "Carpet Tiles & Adhesive Tile Mats", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/JointMatTileCarpetTile-adhesive-tilemat/1/", "MEDIUM"),
 ("天然素材ラグ・自然素材ラグ・ユニット畳", "Natural Fiber Rugs & Tatami Units", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/Tatami/1/", "MEDIUM"),
 ("フロアマット", "Floor Mats", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/FloorMatEntranceLong/1/", "HIGH"),
 ("キッチンマット", "Kitchen Mats", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/FloorMat/1/", "HIGH"),
 ("玄関マット", "Entrance Mats", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/FloorMatEntranceEntrance/1/", "HIGH"),
 ("階段マット・防音マット", "Stair Mats & Soundproof Mats", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/SoundproofSlipSheetSound/1/", "MEDIUM"),
 ("ドアマット", "Door Mats", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/FloorMatEntranceDoor/1/", "HIGH"),
 ("あったか吸湿発熱ラグ(Nウォーム）", "Warm Heat-Generating Rugs (N-Warm)", "https://www.nitori-net.jp/ec/cat/CarpetRugMat/NwarmRug/1/", "HIGH"),
])

g("クッション・カバー", "Cushions & Covers", "textile", [
 ("ひんやり接触冷感クッション・ソファーカバー", "Cool-Touch Cushions & Sofa Covers", "https://www.nitori-net.jp/ec/cat/Cushion/cool-cushion-sofa-cover/1/", "HIGH"),
 ("クッションカバー", "Cushion Covers", "https://www.nitori-net.jp/ec/cat/Cushion/CushionCover/1/", "HIGH"),
 ("ビーズクッション・カバー", "Bead Cushions & Covers", "https://www.nitori-net.jp/ec/cat/Cushion/BeadsCushion/1/", "HIGH"),
 ("ソファカバー", "Sofa Covers", "https://www.nitori-net.jp/ec/cat/Cushion/SofaMultiCoverSofa/1/", "HIGH"),
 ("モチモチクッション", "Squishy Cushions", "https://www.nitori-net.jp/ec/cat/Cushion/SheetCushionMochimochi/1/", "HIGH"),
 ("シートクッション・円座クッション", "Seat Cushions & Donut Cushions", "https://www.nitori-net.jp/ec/cat/Cushion/SheetCushionSheetcushi/1/", "HIGH"),
 ("長座布団・カバー", "Long Floor Cushions & Covers", "https://www.nitori-net.jp/ec/cat/Cushion/ZabutonLong/1/", "HIGH"),
 ("フロアクッション", "Floor Cushions", "https://www.nitori-net.jp/ec/cat/Cushion/SheetCushionFloorcushi/1/", "HIGH"),
 ("ジャンボクッション・カバー", "Jumbo Cushions & Covers", "https://www.nitori-net.jp/ec/cat/Cushion/JumboCushion/1/", "HIGH"),
 ("マルチカバー", "Multi-Purpose Furniture Covers", "https://www.nitori-net.jp/ec/cat/Cushion/SofaMultiCoverMulti/1/", "HIGH"),
 ("低反発クッション", "Low-Rebound Cushions", "https://www.nitori-net.jp/ec/cat/Cushion/SheetCushionLowrepulsi/1/", "HIGH"),
 ("座布団・カバー", "Floor Cushions & Covers", "https://www.nitori-net.jp/ec/cat/Cushion/ZabutonCoverZabuton/1/", "HIGH"),
 ("ミニクッション", "Mini Cushions", "https://www.nitori-net.jp/ec/cat/Cushion/CushionMinicushio/1/", "HIGH"),
 ("クッション", "Cushions", "https://www.nitori-net.jp/ec/cat/Cushion/CushionCushion/1/", "HIGH"),
 ("動物クッション・キャラクタークッション", "Animal & Character Cushions", "https://www.nitori-net.jp/ec/cat/Cushion/character-animal-cushion/1/", "HIGH"),
 ("オーダークッションカバー", "Made-to-Order Cushion Covers", "https://www.nitori-net.jp/ec/cat/Cushion/CushionOrder/1/", "HIGH"),
 ("あったかクッション・ソファーカバー", "Warm Cushions & Sofa Covers", "https://www.nitori-net.jp/ec/cat/Cushion/warm-cushion-sofa-cover/1/", "HIGH"),
])

g("バス・洗面用品", "Bath & Washroom Goods", "textile", [
 ("タオル", "Towels", "https://www.nitori-net.jp/ec/cat/BathToiletLaundry/m1Towel/1/", "HIGH"),
 ("バスマット", "Bath Mats", "https://www.nitori-net.jp/ec/cat/BathToiletLaundry/BathMat/1/", "HIGH"),
 ("ボディタオル・ボディブラシ", "Body Towels & Body Brushes", "https://www.nitori-net.jp/ec/cat/BathToiletLaundry/BathArticleBodycare/1/", "MEDIUM"),
])

g("生活雑貨・日用品", "Daily Necessities", "textile", [
 ("タオル", "Towels", "https://www.nitori-net.jp/ec/cat/LifeSuppliesDailyNecessities/Towel/1/", "HIGH"),
])

g("ベビー用品・ベビーベッド・キッズアイテム", "Baby & Kids Items", "textile", [
 ("ベビーベッド・布団・寝具", "Baby Beds, Futons & Bedding", "https://www.nitori-net.jp/ec/cat/Baby/BabyBed/1/", "MEDIUM"),
 ("子供用ラグ・プレイマット", "Kids Rugs & Play Mats", "https://www.nitori-net.jp/ec/cat/Baby/m1KidsRug/1/", "MEDIUM"),
 ("子供用ベッド・布団", "Kids Beds & Futons", "https://www.nitori-net.jp/ec/cat/Baby/m2KidsShingu/1/", "MEDIUM"),
])

# ---------------- STORAGE ----------------

g("バス・洗面用品", "Bath & Washroom Goods", "storage", [
 ("洗面ラック・洗面収納", "Washstand Racks & Washroom Storage", "https://www.nitori-net.jp/ec/cat/BathToiletLaundry/LaundryToiletArticleStorage/1/", "HIGH"),
 ("マグネット浴室収納・マグネット洗面収納", "Magnetic Bathroom & Washroom Storage", "https://www.nitori-net.jp/ec/cat/BathToiletLaundry/MagnetBathLaundry/1/", "HIGH"),
 ("浴室ラック・浴室収納", "Bathroom Racks & Bathroom Storage", "https://www.nitori-net.jp/ec/cat/BathToiletLaundry/BathArticleStorage/1/", "HIGH"),
 ("突っ張り棒・棚", "Tension Rods & Shelves", "https://www.nitori-net.jp/ec/cat/BathToiletLaundry/m1ShelfStrutRack_Strut/1/", "HIGH"),
])

g("洗濯用品", "Laundry Goods", "storage", [
 ("ランドリーラック・洗濯機ラック", "Laundry Racks & Washing Machine Racks", "https://www.nitori-net.jp/ec/cat/Laundry/ShelfStrutRackRack/1/", "HIGH"),
 ("ランドリー収納", "Laundry Storage", "https://www.nitori-net.jp/ec/cat/Laundry/CreviceStorage/1/", "HIGH"),
 ("ランドリーバスケット", "Laundry Baskets", "https://www.nitori-net.jp/ec/cat/Laundry/LaundryBasket/1/", "HIGH"),
])

g("収納家具", "Storage Furniture", "storage", [
 ("チェスト・タンス", "Chests & Drawers", "https://www.nitori-net.jp/ec/cat/Storage-Furniture/Chest/1/", "MEDIUM"),
 ("クローゼット・ワードローブ", "Closets & Wardrobes", "https://www.nitori-net.jp/ec/cat/Storage-Furniture/WardrobeLocker/1/", "HIGH"),
 ("ハンガーラック・ポールハンガー", "Hanger Racks & Pole Hangers", "https://www.nitori-net.jp/ec/cat/Storage-Furniture/HangarRack/1/", "HIGH"),
 ("ドレッサー・鏡台", "Dressers & Vanities", "https://www.nitori-net.jp/ec/cat/Storage-Furniture/Dresser/1/", "MEDIUM"),
 ("玄関収納", "Entryway Storage", "https://www.nitori-net.jp/ec/cat/Storage-Furniture/EntranceStorage/1/", "HIGH"),
 ("オーダー収納", "Made-to-Order Storage", "https://www.nitori-net.jp/ec/cat/Storage-Furniture/f2Orderstorage/1/", "HIGH"),
 ("組み合わせ壁面収納", "Modular Wall Storage", "https://www.nitori-net.jp/ec/cat/Storage-Furniture/f2wallstorage/1/", "HIGH"),
 ("リビングチェスト", "Living Room Chests", "https://www.nitori-net.jp/ec/cat/Storage-Furniture/m1LivingStorageCabinet/1/", "MEDIUM"),
 ("キッズ収納・家具", "Kids Storage Furniture", "https://www.nitori-net.jp/ec/cat/Storage-Furniture/m1KidsStorageFurniture/1/", "MEDIUM"),
])

g("収納ケース・衣類整理用品", "Storage Cases & Clothing Organizers", "storage", [
 ("衣装ケース・衣類収納ケース", "Clothing Storage Cases", "https://www.nitori-net.jp/ec/cat/StorageRackDresser/ClothingCase/1/", "HIGH"),
 ("プラスチックチェスト", "Plastic Chests", "https://www.nitori-net.jp/ec/cat/StorageRackDresser/ClothingCaseLiving/1/", "HIGH"),
 ("収納ボックス・かご・バスケット", "Storage Boxes, Baskets & Bins", "https://www.nitori-net.jp/ec/cat/StorageRackDresser/StorageBasket/1/", "HIGH"),
 ("収納袋・圧縮袋", "Storage Bags & Compression Bags", "https://www.nitori-net.jp/ec/cat/StorageRackDresser/StorageBag/1/", "HIGH"),
 ("すのこ・押入れ棚", "Slatted Boards & Closet Shelves", "https://www.nitori-net.jp/ec/cat/StorageRackDresser/Futondaiosiiresunoko/1/", "MEDIUM"),
 ("収納仕切り・小物収納", "Storage Dividers & Small Item Storage", "https://www.nitori-net.jp/ec/cat/StorageRackDresser/StorageStorage/1/", "HIGH"),
 ("コレクションケース・メイクボックス・ジュエリーボックス", "Collection Cases, Makeup & Jewelry Boxes", "https://www.nitori-net.jp/ec/cat/StorageRackDresser/Accessorybox/1/", "HIGH"),
 ("突っ張り棒・棚", "Tension Rods & Shelves", "https://www.nitori-net.jp/ec/cat/StorageRackDresser/ShelfStrutRackStrut/1/", "HIGH"),
])

g("本棚・ラック・シェルフ", "Bookshelves, Racks & Shelves", "storage", [
 ("Nポルダ", "N-Polder Storage Shelving", "https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/Npolder/1/", "HIGH"),
 ("カラーボックス", "Cube Storage Boxes", "https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/ColorBox/1/", "HIGH"),
 ("スチールラック・スチールシェルフ", "Steel Racks & Steel Shelves", "https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/RackShelfMetal/1/", "HIGH"),
 ("木製シェルフ・ウッドラック", "Wood Shelves & Wood Racks", "https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/RackShelfWood/1/", "MEDIUM"),
 ("収納ボックス", "Storage Boxes", "https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/m1Storagebasket/1/", "HIGH"),
 ("突っ張り収納", "Tension Pole Storage", "https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/tensionWallStorage/1/", "HIGH"),
 ("コレクションケース", "Collection Cases", "https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/InteriorArticleDisplaybox/1/", "MEDIUM"),
 ("オーダー収納", "Made-to-Order Storage", "https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/f1Orderstorage/1/", "HIGH"),
 ("セミオーダーラック", "Semi-Custom Racks", "https://www.nitori-net.jp/ec/cat/OfficeBookshelfStationery/SemiOrderrack/1/", "HIGH"),
])

g("キッチン整理・キッチン収納", "Kitchen Organization & Storage", "storage", [
 ("キッチンワゴン・隙間収納", "Kitchen Wagons & Gap Storage", "https://www.nitori-net.jp/ec/cat/KitchenStorage/KDKitchenStorageWagon/1/", "HIGH"),
 ("シンク下・コンロ下収納", "Under-Sink & Under-Stove Storage", "https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenSink/1/", "HIGH"),
 ("引出し整理・カトラリー収納", "Drawer Organizers & Cutlery Storage", "https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenAccessorie/1/", "HIGH"),
 ("冷蔵庫収納", "Refrigerator Storage", "https://www.nitori-net.jp/ec/cat/KitchenStorage/RefrigeratorStorage/1/", "HIGH"),
 ("水切りかご・ラック・マット", "Dish Drainer Baskets & Racks", "https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenBucket/1/", "MEDIUM"),
 ("マグネット収納・壁面整理", "Magnetic Storage & Wall Organization", "https://www.nitori-net.jp/ec/cat/KitchenStorage/MagnetKitchenStorage/1/", "HIGH"),
 ("キッチンラック・キッチン収納棚", "Kitchen Racks & Storage Shelves", "https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenRack/1/", "HIGH"),
 ("吊戸棚収納・その他", "Hanging Cabinet Storage & Other", "https://www.nitori-net.jp/ec/cat/KitchenStorage/KitchenStorageOther/1/", "HIGH"),
])

g("テレビ台・リビング収納・仏壇", "TV Stands & Living Room Storage", "storage", [
 ("組み合わせ壁面収納", "Modular Wall Storage", "https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/f1wallstorage/1/", "HIGH"),
 ("組み合わせキャビネット", "Modular Cabinets", "https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/f1middleboardporte/1/", "MEDIUM"),
 ("リビングボード・キャビネット", "Living Room Sideboards & Cabinets", "https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/LivingStorageSideboard/1/", "MEDIUM"),
 ("リビングチェスト", "Living Room Chests", "https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/LivingStorageCabinet/1/", "MEDIUM"),
 ("ディスプレイラック", "Display Racks", "https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/LivingStorageDisplayrac/1/", "MEDIUM"),
 ("CD・DVDラック", "CD & DVD Racks", "https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/LivingStorageCddvd/1/", "HIGH"),
 ("マガジンラック", "Magazine Racks", "https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/StorageMagazinera/1/", "HIGH"),
 ("リモコンケース", "Remote Control Cases", "https://www.nitori-net.jp/ec/cat/TvStandLivingStorage/StorageRemote/1/", "MEDIUM"),
])

g("デスク・オフィスチェア", "Desks & Office Chairs", "storage", [
 ("デスクワゴン", "Desk-Side Storage Wagons", "https://www.nitori-net.jp/ec/cat/Desk-Officechair/WagonRack/1/", "MEDIUM"),
])

if __name__ == "__main__":
    print(len(PLAN))
