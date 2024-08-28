# com d0 l0 d1 l1 ...

import sys
sys.dont_write_bytecode = True
import pathlib
import shutil

ext = [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]
output_dir = pathlib.Path(sys.argv[1]) # コピー先のディレクトリ
list_combine = sys.argv[2] # 結合後のリストファイル名
if(not output_dir.exists()): output_dir.mkdir() # ディレクトリ生成
fw = open(list_combine, mode = "w")
print("argvs:", len(sys.argv))
filne_name_list = []
for n in range(2, int(1 + len(sys.argv) / 2)):
    img_dir_path = pathlib.Path(sys.argv[n * 2 - 1])
    annot_file_name = pathlib.Path(sys.argv[n * 2])
    print("dataset:", n-1)
    print(img_dir_path)
    print(annot_file_name)
    if img_dir_path.is_dir() == False:
        print(f"[{n-1}] ファイルが指定されています: {str(img_dir_path)}")
        exit()
    lines = []
    with open(annot_file_name, "r") as f: # 各リストを開く
        for line in f:
            l = line.split(" ")
            if 1 < len(l): # フォーマットチェック
                if l[0] not in filne_name_list: # ファイル名重複チェック
                    filne_name_list.append(l[0])
                    fw.write(line) # フォーマットが正しい行を残す
                    shutil.copy(img_dir_path / l[0], output_dir)

fw.close()