# 縦長・横長の画像を端から最大サイズで正方形に切り抜くツール
# python imgCropSquareSubDir.py 読み込む画像があるディレクトリ 出力ディレクトリ

import sys
import pathlib
import cv2

dir_src = pathlib.Path(sys.argv[1]) # 読み込む画像があるディレクトリ
IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp"]
img_paths_src = sorted([p for p in dir_src.glob("**/*") if p.suffix.lower() in IMG_EXTS])

dir_dst = pathlib.Path(sys.argv[2]) # 出力ディレクトリ
if(not dir_dst.exists()): dir_dst.mkdir()

for i in range(len(img_paths_src)): # 読み込みディレクトリ内の全てのファイルについて処理する
    img = cv2.imread(str(img_paths_src[i]))
    h, w, _ = img.shape
    if w > h: # 横に長い場合
        im0 = img[0 : h, 0 : h] # 左
        im1 = img[0 : h, w - h : w] # 右
    else: # 縦に長い場合
        im0 = img[0 : w, 0 : w] # 上
        im1 = img[h - w  : h, 0 : w] # 下
    
    outputfilename0 = fileList[i].stem + "_0.png"
    outputfilePath = str(dir_dst / outputfilename0)
    print(outputfilePath)
    cv2.imwrite(outputfilePath, im0)

    outputfilename1 = fileList[i].stem + "_1.png"
    outputfilePath = str(dir_dst / outputfilename1)
    print(outputfilePath)
    cv2.imwrite(outputfilePath, im1)
