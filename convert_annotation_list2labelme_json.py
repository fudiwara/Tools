# スペース区切りのデータセットのアノテーションファイルを読み込んで
# JSON形式のファイルを出力するプログラム

import sys
sys.dont_write_bytecode = True
import pathlib
import json
import cv2 as cv

annot_file_name = pathlib.Path(sys.argv[1]) # アノテーションファイル
base_dir = pathlib.Path(sys.argv[2]) # 画像のあるディレクトリ & 保存先
class_name = sys.argv[3 : ] # 保存するクラス名

def create_labelme_json(img_path, bounding_boxes):
    img = cv.imread(img_path, cv.IMREAD_COLOR)
    imageHeight, imageWidth = img.shape[ : 2]

    shapes = []
    for bbox in bounding_boxes:
        x0, y0, x1, y1, label_name = bbox
        
        shapes.append({
            "label": label_name,
            "points": [
                [x0, y0],
                [x1, y1]
            ],
            "group_id": None,
            "description": "",
            "shape_type": "rectangle",
            "flags": {},
            "mask": None
        })

    labelme_data = { # JSONデータ構造の構築
        "version": "5.8.2",
        "flags": {},
        "shapes": shapes,
        "imagePath": img_name,
        "imageData": None,
        "imageHeight": imageHeight,
        "imageWidth": imageWidth
    }
    
    return labelme_data


lines = []
with open(annot_file_name, "r") as f:
    for line in f:
        if 1 < len(line.split(" ")):
            lines.append(line)

for idx in range(len(lines)):
    l = lines[idx].split(" ") # スペース区切りのセットリスト
    img_name = l[0]
    img_path = base_dir / img_name

    bounding_boxes = []
    for i in range(len(l) - 1):
        p = l[i + 1].split(",") # カンマ区切りの各セット
        x0 = float(p[0]) # 実数で読み込む
        y0 = float(p[1])
        x1 = float(p[2])
        y1 = float(p[3])
        cls_idx = int(p[4]) - 1 # pytorchシリーズではクラスIDが1スタートなので
        bounding_boxes.append([x0, y0, x1, y1, class_name[cls_idx]])
        print(idx, i, x0, y0, x1, y1, p[4])
    
    json_data = create_labelme_json(img_path, bounding_boxes)
    json_file_name = img_path.with_suffix(".json")
    with open(json_file_name, "w") as f:
        json.dump(json_data, f, indent = 2)