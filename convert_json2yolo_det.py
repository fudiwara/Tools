# LabelMeのJSONをYOLO形式の検出タスク用TXTファイルにコンバートするプログラム
# 図形は rectangle もしくは polygon (polygonの場合は外接矩形を出す)
import sys
sys.dont_write_bytecode = True
import pathlib
import json

dataset_dir = pathlib.Path(sys.argv[1]) # jsonファイルがあるディレクトリ
output_dir = dataset_dir # 出力先のディレクトリ

class_list = sys.argv[2 : ] # LabelMeでつけたラベル名

def to_yolo_bbox_from_rect(points, img_w, img_h):
    xps = [x[0] for x in points]
    yps = [x[1] for x in points]
    x_min, y_min, x_max, y_max = min(xps), min(yps), max(xps), max(yps)

    w, h = x_max - x_min, y_max - y_min
    x_center, y_center = x_min + w / 2.0, y_min + h / 2.0

    # 正規化
    x_center /= img_w
    y_center /= img_h
    w /= img_w
    h /= img_h

    # 念のため0〜1にクリップ
    return max(0.0, min(1.0, x_center)), max(0.0, min(1.0, y_center)), max(0.0, min(1.0, w)), max(0.0, min(1.0, h))

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

    lines = []
    shapes = data.get("shapes", [])
    for shape in shapes:
        label = shape.get("label")
        points = shape.get("points")

        if label not in class_list:
            print(f"unknown label: {label} in {json_file.name}")
            continue # クラスリストにないラベルはスキップ

        class_id = class_list.index(label)
        xc, yc, w, h = to_yolo_bbox_from_rect(points, img_w, img_h)

        lines.append(f"{class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")

    with open(output_path, "w", encoding = "utf-8") as out: # アノテーション内容の書き込み
        out.write("\n".join(lines))
