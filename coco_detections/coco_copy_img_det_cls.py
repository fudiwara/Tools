import sys
sys.dont_write_bytecode = True
import pathlib
import shutil

from PIL import Image

import torch
import torchvision

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(DEVICE)
src_path = pathlib.Path(sys.argv[1]) # 入力画像のパス
save_path = pathlib.Path(sys.argv[2]) # 保存用のパス
save_path.mkdir(exist_ok = True)

detection_list = [1] # 検出対象とする
thDetection = 0.9

# モデルの定義と読み込みおよび評価用のモードにセットする
model = torchvision.models.detection.fcos_resnet50_fpn(weights="DEFAULT").to(DEVICE).eval()
data_transforms = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])

IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]
img_paths = sorted([p for p in src_path.iterdir() if p.suffix in IMG_EXTS])

for image_path in img_paths:
    # 画像の読み込み・変換
    img = Image.open(image_path).convert("RGB") # カラー指定で開く
    i_w, i_h = img.size
    data = data_transforms(img).unsqueeze(0) # テンソルに変換してから1次元追加

    data = data.to(DEVICE)
    outputs = model(data) # 推定処理
    
    bboxs = outputs[0]["boxes"].detach().cpu().numpy()
    scores = outputs[0]["scores"].detach().cpu().numpy()
    labels = outputs[0]["labels"].detach().cpu().numpy()

    flag_save = False
    img_area = i_w * i_h
    for i in range(len(scores)):
        b = bboxs[i]
        box_area = (b[2] - b[0]) * (b[3] - b[1])
        prd_val = scores[i]
        if prd_val < thDetection:
            continue # 推定確率が閾値以下はスキップ
        prd_cls = labels[i]
        if prd_cls not in detection_list:
            continue # 対象のクラス以外はスキップ
        
        if box_area / img_area < 0.2:
            continue # 画面内の面積比で0.2未満はスキップ

        flag_save = True # ここにたどり着くのは推定確率の高い対象のクラスがある場合
        break

    if flag_save:
        shutil.copy(image_path, save_path) # 指定したパスにコピー
