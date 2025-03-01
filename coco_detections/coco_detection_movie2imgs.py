# 動画から1フレームあたり1枚の検出結果画像を出力していく
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
output_path.mkdir(exist_ok = True)

thDetection = 0.6

# モデルの定義と読み込みおよび評価用のモードにセットする
model = torchvision.models.detection.fcos_resnet50_fpn(weights="DEFAULT") # fcos
model.to(DEVICE)
model.eval()

data_transforms = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])

# フォント、枠の設定
font_scale = cv2.getFontScaleFromHeight(cv2.FONT_HERSHEY_DUPLEX, 11, 1)
colors = [(255, 100, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
clr_num = len(colors)
class_names = ["", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "street sign", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "hat", "backpack", "umbrella", "shoe", "eye glasses", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "plate", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "mirror", "dining table", "window", "desk", "toilet", "door", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "blender", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush", "hair brush"]

sw = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
sh = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
ssize = (sw, sh)
frame_count = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
frame_rate = int(vc.get(cv2.CAP_PROP_FPS))
img_prv = np.ones((sh, sw, 3), np.uint8) 
print(ssize, frame_count, frame_rate)

# for f in range(frame_count):
for f in range(100):
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

        x0, y0 = int(b[0]), int(b[1])
        p0, p1 = (x0, y0), (int(b[2]), int(b[3]))
        print(prd_cls, prd_val, p0, p1)
        
        box_col = colors[prd_cls % clr_num]

        # text = f" {prd_cls}  {prd_val:.3f} " # クラスIDと確率を表示させる場合
        text = f" {class_names[prd_cls]} " # クラス名のみを表示させる場合
        (t_w, t_h), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, font_scale, 1) # テキスト部の矩形サイズ取得
        cv2.rectangle(frame, p0, p1, box_col, thickness = 2) # テキストの背景の矩形
        cv2.rectangle(frame, (x0, y0 - t_h), (x0 + t_w, y0), box_col, thickness = -1) # 検出領域の矩形
        cv2.putText(frame, text, p0, cv2.FONT_HERSHEY_DUPLEX, font_scale, (255, 255, 255), 1, cv2.LINE_AA)
    
    cv2.imwrite(str(output_path / f"c{f:06}.jpg"), frame)

vc.release()