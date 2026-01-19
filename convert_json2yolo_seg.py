# LabelMeのJSONをYOLO形式の領域分割タスク用TXTファイルにコンバートするプログラム
# OBBも領域分割も図形は polygon なのでOBBタスク用のTXTもこのプログラムでOK
import sys
sys.dont_write_bytecode = True
import pathlib
import json

dataset_dir = pathlib.Path(sys.argv[1]) # jsonファイルがあるディレクトリ
output_dir = dataset_dir # 出力先のディレクトリ
class_list = sys.argv[2 : ] # LabelMeでつけたラベル名

IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".gif", ".webp"] # 画像拡張子
image_files = sorted([p for p in dataset_dir.glob("**/*") if p.suffix.lower() in IMG_EXTS])
print(f"image files num: {len(image_files)}")

for img_path in image_files:
    json_file = img_path.with_suffix(".json") # 画像ファイル名と対のJSONファイル
    output_path = img_path.with_suffix(".txt") # 画像ファイル名と対のTXTファイル

    if not json_file.exists(): # JSONファイルが存在しない場合
        with open(output_path, "w", encoding = "utf-8") as out:
            out.write("") # 空のアノテーションファイルを作成 (当該の画像は背景となる)
        continue

    with open(json_file, "r", encoding = "utf-8") as f:
        data = json.load(f)

    img_w, img_h = data["imageWidth"], data["imageHeight"] # 画像サイズの取得
    
    with open(output_path, "w", encoding = "utf-8") as out:
        for shape in data["shapes"]:
            label = shape["label"]
            
            if shape["shape_type"] != "polygon":
                continue # shape_typeはpolygonのみ
            
            if label not in class_list:
                print(f"unknown label: {label}")
                continue # クラスリストにないラベルはスキップ

            class_id = class_list.index(label)
            points = shape["points"]

            normalized_points = []
            for point in points: # 座標の正規化 (x / width, y / height)
                x_norm = point[0] / img_w
                y_norm = point[1] / img_h
                
                # 0~1の範囲へ正規化
                x_norm = max(0, min(1, x_norm))
                y_norm = max(0, min(1, y_norm))
                
                normalized_points.extend([f"{x_norm:.6f}", f"{y_norm:.6f}"])

            # 書き込み: <class_id> <x1> <y1> <x2> <y2> ...
            print(f"{class_id} " + " ".join(normalized_points), file = out)
