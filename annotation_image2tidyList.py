# アノテーションのリストに対してフォルダ内の画像名だけを残す
# ファイル名以降はスペース区切りでもカンマ区切りでも対応させる (プログラム内で切り替え)

import sys, pathlib
sys.dont_write_bytecode = True

annotation_filepath = pathlib.Path(sys.argv[1])
dir_path = pathlib.Path(sys.argv[2])

separate_symbol = "," # ファイル名との区切りがカンマの場合
# separate_symbol = " " # ファイル名との区切りがスペースの場合
IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]
img_filenames = sorted([p.name for p in dir_path.glob("**/*") if p.suffix in IMG_EXTS])

lines, set_img_names = [], set()
with open(annotation_filepath, "r") as f:
    for line in f:
        data = line.split(separate_symbol)
        if 1 < len(data):
            lines.append(line)
            set_img_names.add(data[0])

output_list_path = dir_path / "_annotation_list_alt.txt"
fw = open(output_list_path, mode = "w")
for i in range(len(img_filenames)):
    if img_filenames[i] in set_img_names:
        print(lines[i].rstrip() , file = fw)
fw.close()
