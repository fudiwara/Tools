
import sys, time, copy
sys.dont_write_bytecode = True
import cv2
import numpy as np
from PIL import Image
import pathlib

import torch
import torchvision

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(DEVICE)
input_file_name = pathlib.Path(sys.argv[1]) # 入力のmp4ファイル
vc = cv2.VideoCapture(sys.argv[1])
output_path = pathlib.Path(sys.argv[2]) # 出力先ディレクトリ
if(not output_path.exists()): output_path.mkdir()

detection_list = [1] # 検出対象とする
scale_rate = 1.5
thDetection = 0.6

# モデルの定義と読み込みおよび評価用のモードにセットする
model = torchvision.models.detection.fcos_resnet50_fpn(weights="DEFAULT") # fcos
model.to(DEVICE)
model.eval()

data_transforms = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])

sw = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
sh = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
ssize = (sw, sh)
frame_count = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
frame_rate = int(vc.get(cv2.CAP_PROP_FPS))
img_prv = np.ones((sh, sw, 3), np.uint8) 
print(ssize, frame_count, frame_rate)

for f in range(frame_count):
# for f in range(220, 250):
    ret, frame = vc.read()
    if (img_prv - frame).sum() == 0:
        print("same")
        continue
    img_prv = copy.deepcopy(frame)
    
    src_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(src_img) # OpenCV形式からPIL形式へ変換
    data = data_transforms(img).unsqueeze(0) # テンソルに変換してから1次元追加
    data = data.to(DEVICE)
    outputs = model(data) # 推定処理
    # print(outputs)
    bboxs = outputs[0]["boxes"].detach().cpu().numpy()
    scores = outputs[0]["scores"].detach().cpu().numpy()
    labels = outputs[0]["labels"].detach().cpu().numpy()
    # print(bboxs, scores, labels)

    for i in range(len(scores)):
        b = bboxs[i]
        # print(b)
        prd_val = scores[i]
        if prd_val < thDetection: continue # 閾値以下が出現した段階で終了
        prd_cls = labels[i]
        if prd_cls not in detection_list: continue # 対象のクラス以外はスキップ

        x0, y0 = int(b[0]), int(b[1]) # 矩形の左上座標
        x1, y1 = int(b[2]), int(b[3]) # 矩形の右上座標
        xc, yc = (x1 + x0) / 2, (y1 + y0) / 2 # 矩形の中心座標
        w_d, h_d = x1 - x0, y1 - y0 # 矩形の横幅、縦幅
        w_dst, h_dst = w_d * scale_rate, h_d * scale_rate # クロップのサイズ
        cropx0, cropy0 = int(xc - w_dst / 2), int(yc - h_dst / 2)
        cropx1, cropy1 = int(xc + w_dst / 2), int(yc + h_dst / 2)
        img_crop = img.crop((cropx0, cropy0, cropx1, cropy1))
        print(x0, y0, x1, y1, xc, yc, cropx0, cropy0, cropx1, cropy1)
        output_file_name = output_path / f"c{f:05}_{i:03}.png"
        img_crop.save(output_file_name)
        print(f"{f:6} {i:3}")

vc.release()