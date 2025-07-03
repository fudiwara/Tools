# LabelMeのJSONを検出用のリスト形式のアノテーションに変換するプログラム
# LabelMeのJSONはRECTだけでなくPOLYGON入力されたものでもOK
import sys
sys.dont_write_bytecode = True
import json
import pathlib

annos_dir = pathlib.Path(sys.argv[1]) # JSONのアノテーションファイルが置いてあるパス
category_name_file = sys.argv[2] # クラス名の一式
output_anno_name = sys.argv[3] # 出力するファイル名 hogehoge.txt

# クラス名一式を読み込み先頭(ID 0)にbackgroundを挿入する
category_name = ["background"] + [line.strip() for line in open(category_name_file, "r", encoding="utf-8") if line.strip()]
anno_paths = sorted([p for p in annos_dir.glob("**/*") if p.suffix in [".json", ".JSON"]])
relative_directory_paths = [p.relative_to(annos_dir).parent for p in anno_paths] # ディレクトリのパスも得る

f_a = open(output_anno_name, mode = "w")
for i in range(len(anno_paths)): # 全てのJSONファイルに対して処理する
    json_name = anno_paths[i]
    with open(json_name, "r") as f: # JSONファイルオープン
        temp = json.loads(f.read())

        save_line = str(relative_directory_paths[i] / temp["imagePath"]) # 各行に書き込むテキスト (先頭は相対パス付き画像ファイル名)

        lmsps = temp["shapes"] # LabelMeの各パーツ情報
        for j in range(len(lmsps)):
            cat_idx = category_name.index(lmsps[j]["label"]) # クラス名で一致する番号を得る
            pts = lmsps[j]["points"] # 座標のリスト
            xps = [x[0] for x in pts]
            yps = [x[1] for x in pts]
            x0, y0, x1, y1 = min(xps), min(yps), max(xps), max(yps)
            w, h = x1 - x0, y1 - y0

            if w == 0 or h == 0 or w * h < 30: # 小さすぎる領域は無視する
                print(f"{num}: {box}")
                continue # 不適格なbboxの場合は処理対象としない
            
            save_line += f" {x0},{y0},{x1},{y1},{cat_idx}"

        print(save_line, file = f_a)
f_a.close()
