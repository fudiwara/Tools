# 線分をアノテーションするツール
# CSV形式で出力されます：ファイル名,rx0,ry0,rx1,ry1,px,py
# 画像ファイル一式を予め一つのディレクトリにまとめておきます
# ファイルの送り 矢印の ↓：次へ ↑：前へ
# スケール 矢印の ←：小さく →：大きく
# s：保存 、c：アノテーションのクリア
# 手順1. ドラッグアンドドロップにて矩形アノテーション (点0 -> 点1)
# 手順2. その後にクリックで注視点のアノテーション

import sys, pathlib, csv
sys.dont_write_bytecode = True
import cv2
import numpy as np

dir_path = pathlib.Path(sys.argv[1]) # 画像のディレクトリ
IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]
img_paths = sorted([p for p in dir_path.iterdir() if p.suffix in IMG_EXTS])
num_files = len(img_paths)
img_idx = 0; scl_idx = 0; image_scale = 1; scl_param = 0.05
w_name = "image"
annotation_filename = "_annotation_rect2points.txt"
annotation_filepath = dir_path / annotation_filename
ann_list = [[img_paths[i].name, False, (0, 0), (0, 0), (0, 0)] for i in range(num_files)]
imgname_list = sorted([n.name for n in img_paths])

img = np.ones((100, 100, 3), np.uint8)
x0, y0, x1, y1, px, py, mx, my = 0, 0, 0, 0, 0, 0, 0, 0
flag_dd = False
flag_set = False
flag_line = False

if annotation_filepath.exists(): # 既にアノテーションファイルがある場合は
    f = open(annotation_filepath, mode = "r") # アノテーションファイルオープン
    r_csv = csv.reader(f)
    for r in r_csv:
        idx = imgname_list.index(r[0]) # 画像ファイル名が同一のインデクスを得る
        ann_list[idx][1] = True # アノテーション完了フラグを真に
        ann_list[idx][2] = (int(float(r[1])), int(float(r[2])))
        ann_list[idx][3] = (int(float(r[3])), int(float(r[4])))
        ann_list[idx][4] = (int(float(r[5])), int(float(r[6])))
        if idx == 0: # トップの画像の場合はGUI初期値にも代入する
            flag_set = True
            x0, y0 = int(float(r[1])), int(float(r[2]))
            x1, y1 = int(float(r[3])), int(float(r[4]))
            px, py = int(float(r[5])), int(float(r[6]))
    f.close()

def save_anno():
    f = open(annotation_filepath, mode = "w")
    w_csv = csv.writer(f)
    for i in range(num_files):
        if ann_list[i][1]: # その画像のアノテーション完了フラグが真なら書き込む
            a = ann_list[i]
            w_csv.writerow([a[0], a[2][0], a[2][1], a[3][0], a[3][1], a[4][0], a[4][1]])
    f.close()

def delete_anno():
    global ann_list, flag_dd, flag_set
    ann_list[img_idx][1] = False
    flag_dd = False
    flag_set = False
    flag_line = False

def chk_xyxy():
    global x0, y0, x1, y1
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0

def change_image(c_id, n_id):
    global ann_list, flag_dd, flag_set, x0, y0, x1, y1, py, px
    if flag_set:
        ann_list[c_id][1] = flag_set
        ann_list[c_id][2] = (x0 / image_scale, y0 / image_scale)
        ann_list[c_id][3] = (x1 / image_scale, y1 / image_scale)
        ann_list[c_id][4] = (px / image_scale, py / image_scale)
        print("->", ann_list[c_id])

    if ann_list[n_id][1]:
        print("<-", ann_list[n_id])
        flag_set = True
        x0, y0 = int(ann_list[n_id][2][0] * image_scale), int(ann_list[n_id][2][1] * image_scale)
        x1, y1 = int(ann_list[n_id][3][0] * image_scale), int(ann_list[n_id][3][1] * image_scale)
        px, py = int(ann_list[n_id][4][0] * image_scale), int(ann_list[n_id][4][1] * image_scale)
    else:
        flag_set = False
    
    flag_dd = False
    
def disp_img_rectangle_line():
    global img
    disp_img_reset()
    r_s = 10
    if flag_set: th_width = 2
    else: th_width = 1
    cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 255), thickness = th_width)
    cv2.circle(img, (x0, y0), 9, (0, 255, 0), thickness = th_width)
    cv2.circle(img, (x1, y1), 9, (255, 0, 0), thickness = th_width)
    if flag_line or flag_set:
        cv2.line(img, ((x0 + x1) // 2, (y0 + y1) // 2), (px, py), (0, 0, 0), th_width, cv2.LINE_AA)
        cv2.circle(img, (px, py), 15, (255, 0, 255), thickness = th_width)
        
    cv2.imshow(w_name, img)

def disp_img_reset():
    global img
    img = img_disp.copy()

def onMouse(event, x, y, flag, params):
    global x0, y0, x1, y1, px, py, mx, my, flag_dd, flag_line, flag_set

    if not flag_set and event == cv2.EVENT_LBUTTONDOWN:
        if flag_line:
            pass
        elif not flag_dd:
            # x0 = x; y0 = y
            x0 = mx; y0 = my
            if not flag_set:
                flag_dd = True

    if not flag_set and event == cv2.EVENT_MOUSEMOVE:
        if flag_dd:
            x1 = x; y1 = y
            disp_img_rectangle_line()
            # dist = np.linalg.norm(np.array([x0 - x1, y0 - y1])) # 2点間の距離
            # print(dist)
        elif flag_line:
            px = x; py = y
            disp_img_rectangle_line()

    elif not flag_set and event == cv2.EVENT_LBUTTONUP:
        if flag_dd:
            # x1 = x; y1 = y
            x1 = mx; y1 = my
            chk_xyxy()
            flag_dd = False
            flag_line = True
        elif flag_line:
            # px = x; py = y
            px = mx; py = my
            flag_set = True
            flag_line = False
            disp_img_rectangle_line()
            ann_list[img_idx][1] = True
            ann_list[img_idx][2] = (x0 / image_scale, y0 / image_scale)
            ann_list[img_idx][3] = (x1 / image_scale, y1 / image_scale)
            ann_list[img_idx][4] = (px / image_scale, py / image_scale)
    mx, my = x, y
    

def change_scale_annotation():
    global x0, y0, x1, y1, px, py
    if flag_set: # このフレームのアノテーションが終わっていれば書き込む
        x0 = int(ann_list[img_idx][2][0] * image_scale)
        y0 = int(ann_list[img_idx][2][1] * image_scale)
        x1 = int(ann_list[img_idx][3][0] * image_scale)
        y1 = int(ann_list[img_idx][3][1] * image_scale)
        px = int(ann_list[img_idx][4][0] * image_scale)
        py = int(ann_list[img_idx][4][1] * image_scale)

cv2.namedWindow(w_name)
cv2.setMouseCallback(w_name, onMouse)

# print(ann_list)
while True:
    img = cv2.imread(str(img_paths[img_idx]))
    img_disp = cv2.resize(img, None, fx = image_scale, fy = image_scale)
    cv2.imshow(w_name, img_disp)
    if flag_set:
        disp_img_rectangle_line()

    key = cv2.waitKey(0)
    if key == 27: # ESC 終了
        break
    elif key == 0: # 上 画面送りを前へ
        next_idx = img_idx - 1
        if next_idx < 0: next_idx = num_files - 1 # 画像枚数-1 の要素数の最大値
        change_image(img_idx, next_idx)
        img_idx = next_idx
    elif key == 1: # 下 画面送りを次へ
        next_idx = img_idx + 1
        if next_idx == num_files: next_idx = 0
        change_image(img_idx, next_idx)
        img_idx = next_idx
    elif key == 2: # 左 縮小
        current_image_scale = image_scale
        scl_idx -= 1
        image_scale = 1 + scl_idx * scl_param
        if image_scale <= 0:
            scl_idx += 1
            image_scale = 1 + scl_idx * scl_param
        change_scale_annotation()
    elif key == 3: # 右 拡大
        scl_idx += 1
        image_scale = 1 + scl_idx * scl_param
        change_scale_annotation()
    elif key == 99: # c 当該フレームのアノテーション削除
        delete_anno()
    elif key == 115: # s 保存
        save_anno()
