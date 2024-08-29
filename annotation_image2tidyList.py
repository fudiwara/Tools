# アノテーションのリストに対してフォルダ内の画像名だけを残す
# ファイル名以降はスペース区切りでもカンマ区切りでも対応させる (プログラム内で切り替え)

import sys, pathlib
sys.dont_write_bytecode = True

annotation_filepath = pathlib.Path(sys.argv[1]) # アノテーションファイルのパス
dir_path = pathlib.Path(sys.argv[2]) # 画像一式のあるディレクトリ

separate_symbol = "," # ファイル名との区切りがカンマの場合
# separate_symbol = " " # ファイル名との区切りがスペースの場合
IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]
img_filenames = sorted([p.name for p in dir_path.glob("**/*") if p.suffix in IMG_EXTS])

lines, list_img_names = [], []
with open(annotation_filepath, "r") as f: # アノテーションファイルのオープン
    for line in f:
        data = line.split(separate_symbol) # 区切り文字で分割
        if 1 < len(data): # 2つ以上に分割されていなければ処理しない
            lines.append(line) # 各行をリストに追加
            list_img_names.append(data[0]) # ファイル名だけのリストに追加

set_img_names = set(list_img_names) # ファイル名だけの集合
output_list_path = dir_path / "_annotation_list_alt.txt" # 出力用のアノテーションファイル
fw = open(output_list_path, mode = "w")
for i in range(len(img_filenames)):
    if img_filenames[i] in set_img_names: # 画像ファイル名で一致するものがあるかチェック
        idx = list_img_names.index(img_filenames[i]) # リストの何番目かを得る
        print(lines[idx].rstrip() , file = fw) # ファイル名に該当する行を書き込み
fw.close()
