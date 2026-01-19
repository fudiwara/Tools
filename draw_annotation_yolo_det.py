import sys
sys.dont_write_bytecode = True
import pathlib
import cv2 as cv

def yolo_to_xyxy(xc, yc, w, h, img_w, img_h):
    # xc, yc, w, h は正規化値(0..1)
    x_center, y_center = xc * img_w, yc * img_h
    box_w, box_h = w * img_w, h * img_h
    x0 = int(round(x_center - box_w / 2))
    y0 = int(round(y_center - box_h / 2))
    x1 = int(round(x_center + box_w / 2))
    y1 = int(round(y_center + box_h / 2))
    # 画像範囲にクリップ
    return max(0, min(img_w - 1, x0)), max(0, min(img_h - 1, y0)), max(0, min(img_w - 1, x1)), max(0, min(img_h - 1, y1))

dataset_dir = pathlib.Path(sys.argv[1])
output_dir = pathlib.Path(sys.argv[2])
output_dir.mkdir(parents = True, exist_ok = True)

# カラー定義（class_idに応じてループ）
colors = [(255, 100, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
clr_num = len(colors)
font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 0.6
thickness = 2

IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".gif", ".webp"] # 画像拡張子
image_files = sorted([p for p in dataset_dir.glob("**/*") if p.suffix.lower() in IMG_EXTS])

for img_path in image_files:
    yolo_txt_path = img_path.with_suffix(".txt") # 画像ファイル名と対のTXTファイル

    img = cv.imread(img_path, cv.IMREAD_COLOR)
    img_h, img_w = img.shape[ : 2]

    with open(yolo_txt_path, "r", encoding = "utf-8") as f: # ラベルと座標の読み込み
        lines = [line.strip() for line in f if line.strip()]

    for line in lines: # 行ごとに矩形を描画
        parts = line.split()
        if len(parts) != 5:
            continue # 不正行はスキップ
        cls_id = int(parts[0])
        xc = float(parts[1])
        yc = float(parts[2])
        w  = float(parts[3])
        h  = float(parts[4])

        # 範囲外の正規化値はクリップ
        xc = max(0.0, min(1.0, xc))
        yc = max(0.0, min(1.0, yc))
        w  = max(0.0, min(1.0, w))
        h  = max(0.0, min(1.0, h))

        x0, y0, x1, y1 = yolo_to_xyxy(xc, yc, w, h, img_w, img_h)
        color = colors[cls_id % clr_num]
        cv.rectangle(img, (x0, y0), (x1, y1), color, 2)

        disp_text = str(cls_id) # クラスIDテキストを左上に表示
        (t_w, t_h), baseline = cv.getTextSize(disp_text, font, font_scale, thickness)
        bg_x0, bg_y0 = x0, max(0, y0 - t_h - baseline)
        bg_x1, bg_y1 = x0 + t_w + 4, y0
        cv.rectangle(img, (bg_x0, bg_y0), (bg_x1, bg_y1), color, -1) # テキスト背景
        cv.putText(img, disp_text, (x0 + 2, y0 - baseline), font, font_scale, (0, 0, 0), thickness, cv.LINE_AA)

    out_path = output_dir / f"{img_path.stem}.jpg"
    cv.imwrite(out_path, img)
    # print(f"saved: {out_path}")
