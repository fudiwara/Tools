import sys
sys.dont_write_bytecode = True
import cv2
import numpy as np
from scipy.spatial import distance

cw, ch = 640, 480
pnum = 4 # マウスイベントで使う点数
r_c = 60 # マウスの吸着するサイズ
base_pts = [(0, 0), (0, ch), (cw, ch), (cw, 0)]
pts = [(100, 100), (100, ch - 100), (cw - 100, ch - 100), (cw - 100, 100)]
p_c_id = -1
w_name = "image"
flag_trans = False

cap = cv2.VideoCapture(0) # VideoCaptureのインスタンス
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cw)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, ch)
ret, frame = cap.read()
img = np.ones((ch, cw, 3), np.uint8) * 255
disp_img = img.copy()
warpM = img.copy()


def onMouse(event, x, y, flag, params):
    global p_c_id, flag_trans
    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(pnum):
            if distance.euclidean((x, y), pts[i]) < r_c:
                pts[i] = (x, y) # ボタンを押したときに範囲内の座標を記録
                p_c_id = i
    
    if event == cv2.EVENT_LBUTTONUP:
        p_c_id = -1 # ボタンを離すときに各種処理をする
        flag_trans = True

    if 0 <= p_c_id: # move含めた座標の更新
        if distance.euclidean((x, y), pts[p_c_id]) < r_c: pts[p_c_id] = (x, y)
        else: p_c_id = -1

cv2.namedWindow(w_name)
cv2.setMouseCallback(w_name, onMouse)

while True:
    # VideoCaptureから1フレーム読み込む
    ret, frame = cap.read()
    # print(ret)
    img = frame.copy()
    disp_img = img.copy()

    cv2.polylines(disp_img, [np.array(pts).astype(int)], True, (0, 0, 255), 2, cv2.LINE_AA) # 線
    for i in range(pnum): cv2.circle(disp_img, pts[i], r_c // 2, (0, 255, 0), 3) # 点

    cv2.imshow(w_name, disp_img)

    if flag_trans:
        H = cv2.getPerspectiveTransform(np.float32(pts), np.float32(base_pts))
        warpM = cv2.warpPerspective(img, H, (cw, ch), borderValue=(255, 255, 255))
        cv2.imshow("warp", warpM)
    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord("s"):
        with open("warp_pts.txt", mode="w") as f:
            for i in range(len(pts)):
                f.write(f"{pts[i][0]} {pts[i][1]}\n")
