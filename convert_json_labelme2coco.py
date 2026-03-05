import sys
sys.dont_write_bytecode = True
import json, pathlib
from PIL import Image

image_dir = pathlib.Path(sys.argv[1])  # 画像ファイルとLabelmeのJSONファイルが保存されているディレクトリ
output_json_path = pathlib.Path(sys.argv[2])  # 出力するCOCO形式のJSONファイルのパス
coco_data = {"images": [],"annotations": [],"categories": []} # COCOフォーマットの基本構造

category_list = sys.argv[3 : ] # LabelMeでつけたラベル名をコマンドライン引数で受け取る
category_map = {label: idx + 1 for idx, label in enumerate(category_list)} # クラス名とIDを紐付ける辞書
category_id_counter, image_id_counter, annotation_id_counter = 1, 1, 1

# 指定パス内の画像ファイルを取得
IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
image_paths = sorted([p for p in image_dir.iterdir() if p.suffix.lower() in IMG_EXTS])

for img_p in image_paths:
    json_file = img_p.with_suffix(".json") # 画像ファイルと同名のJSONファイルを想定
    if not json_file.exists():
        img = Image.open(img_p)
        width, height = img.size
        coco_data["images"].append({"id": image_id_counter,"file_name": img_p.name,"width": width,"height": height})
        image_id_counter += 1
        continue
    
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    coco_data["images"].append({
        "id": image_id_counter,
        "file_name": data.get("imagePath"),
        "width": data.get("imageWidth"),
        "height":  data.get("imageHeight")
    })

    # annotations への登録
    for shape in data.get("shapes", []):
        label = shape["label"]

        cat_id = category_map.get(label)
        if cat_id is None:
            print(f"unknown label: {label}") # ラベルが一覧になかったら警告を出す
            continue
        
        if shape["shape_type"] == "rectangle": # 矩形だけを対象にする
            points = shape["points"]
            x1, y1 = points[0]
            x2, y2 = points[1]
            
            # ユーザーが右下から左上に向かって枠を描画した場合を考慮し、最小値・最大値を判定
            x_min, y_min, x_max, y_max = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
            
            bbox_width, bbox_height = x_max - x_min, y_max - y_min
            area = bbox_width * bbox_height
            
            coco_data["annotations"].append({
                "id": annotation_id_counter,
                "image_id": image_id_counter,
                "category_id": cat_id,
                "bbox": [x_min, y_min, bbox_width, bbox_height],
                "area": area,
                "iscrowd": 0,
                "segmentation": [] # 物体検出なので空で
            })
            annotation_id_counter += 1
            
    image_id_counter += 1
    
for label, cat_id in category_map.items(): # categories の構築
    coco_data["categories"].append({"id": cat_id,"name": label,"supercategory": "none"})
    
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(coco_data, f, indent=4) # JSONファイルとして出力
