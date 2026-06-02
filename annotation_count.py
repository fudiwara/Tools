# フォルダ指定でYOLO形式のアノテーションファイルを読み込み各種情報をカウントする
# ラベル指定された画像枚数、クラス毎のアノテーション数、背景画像の枚数
# 検出とセグメンテーションは行頭がクラスIDなので同じコードで対応可

import sys
sys.dont_write_bytecode = True
import pathlib

dataset_root_dir = pathlib.Path(sys.argv[1])
annotation_files = list(dataset_root_dir.glob("**/*.txt"))
class_counts = {}
labelled_img_count = 0
background_img_count = 0

for annotation_file in annotation_files:
    with open(annotation_file, "r") as f: # アノテーションファイルを読み込む
        lines = f.readlines() # アノテーションファイルの内容を行ごとにリストとして取得
        if len(lines) > 0:
            labelled_img_count += 1
            for line in lines:
                class_id = line.split()[0]
                if class_id not in class_counts:
                    class_counts[class_id] = 0
                class_counts[class_id] += 1
        else:
            background_img_count += 1 # アノテーションファイルが空の場合は背景画像

print(f"Labelled images: {labelled_img_count}")
print(f"Background images: {background_img_count}")
for class_id, count in class_counts.items():
    print(f"Class {class_id}: {count}")