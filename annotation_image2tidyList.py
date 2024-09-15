# アノテーションのリストとディレクトリの画像一覧をすりあわせる
# アノテーションのファイル名重複もチェックする
# アノテーションのリストに対してフォルダ内の画像名だけの登録を残す
# ファイル名以降はスペース区切りでもカンマ区切りでも対応させる (プログラム内で切り替え)

import sys, pathlib
sys.dont_write_bytecode = True
import collections

annotation_filepath = pathlib.Path(sys.argv[1]) # アノテーションファイルのパス
dir_path = pathlib.Path(sys.argv[2]) # 画像一式のあるディレクトリ

# separate_symbol = "," # ファイル名との区切りがカンマの場合
separate_symbol = " " # ファイル名との区切りがスペースの場合
IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]
dir_img_names = sorted([p.name for p in dir_path.glob("**/*") if p.suffix in IMG_EXTS])

lines, list_img_names = [], []
with open(annotation_filepath, "r") as f: # アノテーションファイルのオープン
    for line in f:
        data = line.split(separate_symbol) # 区切り文字で分割
        if 1 < len(data): # 2つ以上に分割されていなければ処理しない
            lines.append(line) # 各行をリストに追加
            list_img_names.append(data[0]) # ファイル名だけのリストに追加

f_names = [k for k, v in collections.Counter(list_img_names).items() if v > 1] # リストで重複するファイル名を得る
if 0 < len(f_names): # 重複ファイル名がある場合
    print("Duplication of list:")
    for n in f_names:
        print(n)
    print("done: Exit Program") # 一覧を表示してプログラムを終わっておく
    exit() # 手作業で重複を取り除いてから以降の作業で!

output_list_path = dir_path / "_annotation_list_alt.txt" # 出力用のアノテーションファイル
set_list_img_names = set(list_img_names) # リストからファイル名だけの集合
fw = open(output_list_path, mode = "w")
for i in range(len(dir_img_names)): # ディレクトリ内の画像についてチェック
    if dir_img_names[i] in set_list_img_names: # 画像ファイル名で一致するものがあるかチェック
        idx = list_img_names.index(dir_img_names[i]) # リストの何番目かを得る
        print(lines[idx].rstrip() , file = fw) # ファイル名に該当する行を書き込み
    else:
        print(dir_img_names[i], ": list x - dir o") # ファイルはあるけどリストにない画像
fw.close()

set_dir_img_names = set(dir_img_names) # ディレクトリからファイル名だけの集合
for i in range(len(list_img_names)): # アノテーションファイルのリストに対してチェック
    if list_img_names[i] not in set_dir_img_names:
        print(list_img_names[i], ": list o - dir x") # リストにはあるけどディレクトリにない画像ファイル
