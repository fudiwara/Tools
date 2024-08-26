# スペース区切りのデータセットのアノテーションファイルを読み込んで
# 閾値以下の面積となる矩形があったら表示するプログラム

import sys, os, random
sys.dont_write_bytecode = True
import pathlib
import cv2

annot_file_name = sys.argv[1] # アノテーションファイル
err_area = 20 # エラーとして報告する面積

lines = []
with open(annot_file_name, "r") as f:
    for line in f:
        if 1 < len(line.split(" ")):
            lines.append(line)

for idx in range(len(lines)):
    l = lines[idx].split(" ") # スペース区切りのセットリスト
    img_name = l[0]

    for i in range(len(l) - 1):
        p = l[i + 1].split(",") # カンマ区切りのセットリスト
        x0 = int(p[0]) # 整数で読み込む
        y0 = int(p[1])
        x1 = int(p[2])
        y1 = int(p[3])
        cls_num = int(p[4])

        w = x1 - x0
        h = y1 - y0

        if w * h < err_area or w < 0 or h < 0:
            print(f"{img_name} {i}: {x0} {y0} {x1} {y1} {cls_num}")
