# スペース区切りのデータセットのアノテーションファイルを読み込んで
# 各画像に矩形を描画して保存するプログラム

import sys
sys.dont_write_bytecode = True
import pathlib
import cv2

annot_file_name = sys.argv[1] # アノテーションファイル
img_dir_path = pathlib.Path(sys.argv[2]) # 画像フォルダ一式のあるパス
output_dir_path = pathlib.Path(sys.argv[3]) # 矩形描画結果を保存するフォルダ
if(not output_dir_path.exists()): output_dir_path.mkdir()

lines = []
with open(annot_file_name, "r") as f:
    for line in f:
        if 1 < len(line.split(" ")):
            lines.append(line)

colors = [(0, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
clr_num = len(colors)
for idx in range(len(lines)):
    l = lines[idx].split(" ") # スペース区切りのセットリスト
    img_name = l[0]
    img_path = img_dir_path / img_name
    # print(img_path, l)
    img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)

    if img is None:
        print("failed: ", img_path.name)
        continue

    for i in range(len(l) - 1):
        p = l[i + 1].split(",") # カンマ区切りの各セット
        x0 = int(p[0]) # 実数で読み込む
        y0 = int(p[1])
        x1 = int(p[2])
        y1 = int(p[3])
        cls_num = int(p[4])
        cv2.rectangle(img, (x0, y0), (x1, y1), colors[cls_num % clr_num], 3)
    
    output_filename = output_dir_path / img_name
    cv2.imwrite(str(output_filename), img)