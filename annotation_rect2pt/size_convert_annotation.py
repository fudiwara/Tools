# CSV形式の各値を A -> B に変換する

import sys, pathlib, csv
sys.dont_write_bytecode = True

vals_num = 7
annotation_filepath = pathlib.Path(sys.argv[1])
output_annotation_filepath = pathlib.Path(sys.argv[2])
base_size = float(sys.argv[3])
target_size = float(sys.argv[4])

fw = open(output_annotation_filepath, mode = "w")
w_csv = csv.writer(fw)
with open(annotation_filepath, mode = "r") as fr:# アノテーションファイルオープン
    r_csv = csv.reader(fr)
    l = [ [] for i in range(vals_num)]
    for r in r_csv:
        l[0] = r[0] # 画像ファイル名が同一のインデクスを得る
        for i in range(1, vals_num):
            l[i] = target_size * float(r[i]) / base_size

        w_csv.writerow(l)
fw.close()
