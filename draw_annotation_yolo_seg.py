import sys
sys.dont_write_bytecode = True
import pathlib
import cv2 as cv
import numpy as np

# カラー定義（class_idに応じてループ）
colors = [(255, 100, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
clr_num = len(colors)

def draw_polygons(img_w, img_h, lines):
    for line in lines:
        parts = line.split()
        if len(parts) < 7: # 少なくとも class_id と3つの座標(x, y)が必要
            continue
        
        cls_id = int(parts[0])
        coords = np.array([float(x) for x in parts[1 : ]]).reshape(-1, 2) # 座標リストを取得 (x1, y1, x2, y2, ...)
        
        # 正規化座標をピクセル座標に変換
        coords[:, 0] *= img_w
        coords[:, 1] *= img_h
        pts = coords.astype(np.int32).reshape((-1, 1, 2))
        
        cv.polylines(img, [pts], True, colors[cls_id % clr_num], 2, cv.LINE_AA) # ポリゴンの輪郭の描画

dataset_dir = pathlib.Path(sys.argv[1])
output_dir = pathlib.Path(sys.argv[2])
output_dir.mkdir(parents = True, exist_ok = True)

IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".gif", ".webp"] # 画像拡張子
image_files = sorted([p for p in dataset_dir.glob("**/*") if p.suffix.lower() in IMG_EXTS])

for img_path in image_files:
    yolo_txt_path = img_path.with_suffix(".txt") # 画像ファイル名と対のTXTファイル

    img = cv.imread(img_path, cv.IMREAD_COLOR)
    img_h, img_w = img.shape[ : 2]

    with open(yolo_txt_path, "r", encoding = "utf-8") as f: # ラベル読み込み
        lines = [line.strip() for line in f if line.strip()]

    draw_polygons(img_w, img_h, lines)

    out_path = output_dir / f"{img_path.stem}.jpg"
    cv.imwrite(out_path, img)
    # print(f"saved: {out_path}")
