# アノテーションされた情報を可視化するツール
# CSV形式で出力された：ファイル名,rx0,ry0,rx1,ry1,px,py
# を読み込んで矩形と線分を描画した画像を指定したフォルダに保存します

import sys, pathlib, csv
sys.dont_write_bytecode = True
import cv2
import numpy as np

annotation_filepath = pathlib.Path(sys.argv[1])
dir_path = pathlib.Path(sys.argv[2])
output_dir = pathlib.Path(sys.argv[3])
if(not output_dir.exists()): output_dir.mkdir()

f = open(annotation_filepath, mode = "r")
r_csv = csv.reader(f)
for r in r_csv:
    input_filename = dir_path / r[0]
    img = cv2.imread(str(input_filename))

    if img is None:
        print("failed: ", input_filename)
        continue

    x0, y0 = int(float(r[1])), int(float(r[2]))
    x1, y1 = int(float(r[3])), int(float(r[4]))
    px, py = int(float(r[5])), int(float(r[6]))
    cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 255), thickness = 3)
    cv2.circle(img, (x0, y0), 9, (0, 255, 0), thickness = 1)
    cv2.circle(img, (x1, y1), 9, (255, 0, 0), thickness = 1)
    cv2.line(img, ((x0 + x1) // 2, (y0 + y1) // 2), (px, py), (0, 0, 0), 2, cv2.LINE_AA)
    cv2.circle(img, (px, py), 15, (255, 0, 255), thickness = 3)

    img_filename = output_dir / r[0]
    cv2.imwrite(str(img_filename), img)
f.close() # csv.readerは後からのアクセスもあるので処理後にファイルクローズ
