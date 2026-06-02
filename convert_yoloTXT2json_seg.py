# LabelMeのJSONをYOLO形式の領域分割タスク用TXTファイルにコンバートするプログラム
# OBBも領域分割も図形は polygon なのでOBBタスク用のTXTもこのプログラムでOK
import sys
sys.dont_write_bytecode = True
import pathlib
import json
from PIL import Image

dataset_dir = pathlib.Path(sys.argv[1]) # 画像とTXTファイルがあるディレクトリ
output_dir = dataset_dir # 出力先のディレクトリ
class_list = sys.argv[2 : ] # LabelMe用のJsonに保存するクラス名

IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".gif", ".webp"] # 画像拡張子
image_files = sorted([p for p in dataset_dir.glob("**/*") if p.suffix.lower() in IMG_EXTS])
print(f"image files num: {len(image_files)}")

for img_path in image_files:
    json_file = img_path.with_suffix(".json") # 画像ファイル名と対のJSONファイル
    txt_file = img_path.with_suffix(".txt") # 画像ファイル名と対のTXTファイル

    # 画像サイズを取得
    with Image.open(img_path) as im:
        img_w, img_h = im.size

    shapes = []

    # TXTが存在しない場合は shapes 空でJSONを作成
    if txt_file.exists():
        with open(txt_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        for line_no, line in enumerate(lines, start=1):
            parts = line.split()
            if len(parts) < 3:
                print(f"skip invalid line ({txt_file.name}:{line_no}): {line}")
                continue

            # 先頭は class_id、残りは x y x y ...
            try:
                class_id = int(parts[0])
            except ValueError:
                print(f"skip invalid class_id ({txt_file.name}:{line_no}): {parts[0]}")
                continue

            if not (0 <= class_id < len(class_list)):
                print(f"skip unknown class_id ({txt_file.name}:{line_no}): {class_id}")
                continue

            coords = parts[1:]

            # x,y のペア数チェック（偶数個必要）
            if len(coords) % 2 != 0:
                print(f"skip odd number of coords ({txt_file.name}:{line_no})")
                continue

            points = []
            valid = True
            for i in range(0, len(coords), 2):
                try:
                    x_norm = float(coords[i])
                    y_norm = float(coords[i + 1])
                except ValueError:
                    print(f"skip non-float coords ({txt_file.name}:{line_no})")
                    valid = False
                    break

                # 念のため 0~1 に
                x_norm = max(0.0, min(1.0, x_norm))
                y_norm = max(0.0, min(1.0, y_norm))

                x = x_norm * img_w
                y = y_norm * img_h
                points.append([x, y])

            if not valid:
                continue

            # polygon は通常3点以上推奨
            if len(points) < 3:
                print(f"skip too few points ({txt_file.name}:{line_no})")
                continue

            shape = {
                "label": class_list[class_id],
                "points": points,
                "group_id": None,
                "description": "",
                "shape_type": "polygon",
                "flags": {},
                "mask": None
            }
            shapes.append(shape)

    # LabelMe形式JSON
    data = {
        "version": "5.11.3",
        "flags": {},
        "shapes": shapes,
        "imagePath": img_path.name,
        "imageData": None,
        "imageHeight": img_h,
        "imageWidth": img_w
    }

    with open(json_file, "w", encoding="utf-8") as out:
        json.dump(data, out, ensure_ascii=False, indent=2)

print("done.")