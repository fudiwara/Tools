import sys
sys.dont_write_bytecode = True
import cv2 as cv
import numpy as np
from scipy.spatial import distance

src = cv.imread(sys.argv[1])
ch, cw = src.shape[ : 2]
img = np.ones((ch, cw, 3), np.uint8) * 255
disp_img = img.copy()
warpM = img.copy()

pnum = 4 # マウスイベントで使う点数
r_c = 60 # マウスの吸着するサイズ
base_pts = [(0, 0), (0, ch), (cw, ch), (cw, 0)]
with open("warp_pts.txt") as f:
    pts = []
    for line in f:
        line = line.rstrip("\n")
        l = line.split(" ")
        pts.append((int(l[0]), int(l[1])))
w_name = "image"

while True:
    img = src.copy()
    disp_img = img.copy()

    cv.polylines(disp_img, [np.array(pts).astype(int)], True, (0, 0, 255), 2, cv.LINE_AA) # 線
    for i in range(pnum): cv.circle(disp_img, pts[i], r_c // 2, (0, 255, 0), 3) # 点

    cv.imshow(w_name, disp_img)

    H = cv.getPerspectiveTransform(np.float32(pts), np.float32(base_pts))
    warpM = cv.warpPerspective(img, H, (cw, ch), borderValue=(255, 255, 255))
    cv.imshow("warp", warpM)
    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv.waitKey(1)
    if k == 27:
        break
    elif k == ord("s"):
        with open("warp_pts.txt", mode="w") as f:
            for i in range(len(pts)):
                f.write(f"{pts[i][0]} {pts[i][1]}\n")
