import sys
sys.dont_write_bytecode = True
import cv2
import numpy as np

def gen_3ch_histogram(src, ch_id, col_histo):
    histo = cv2.calcHist([src], [ch_id], None, [256], [0, 256])
    histo = histo.reshape(-1)

    himg_w, himg_h = 512, 240
    histoImg = np.ones((himg_h, himg_w, 3), np.uint8) * 255
    rate_scale = himg_h / histo.max()

    px = 0
    py = int(himg_h - rate_scale * histo[0])
    for i in range (1, 256):
        x = i * 2
        y = int(himg_h - rate_scale * histo[i])
        cv2.line(histoImg, (x, y), (px, py), col_histo, 1, cv2.LINE_AA)
        px, py = x, y
    
    return histoImg

camId = int(sys.argv[1])
cap = cv2.VideoCapture(camId)
cw, ch = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cw)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, ch)
frame = np.ones((240 * 3, 512 + 640, 3), np.uint8) * 255
w_name = "cap histogram"

img_sp = np.zeros((240 * 3 - ch, cw, 3), np.uint8)

tm = cv2.TickMeter()
tm.start()
fps = 0

while(True):
    ret, img = cap.read()
    
    if ret:
        histo_b = gen_3ch_histogram(img, 0, (255, 0, 0))
        histo_g = gen_3ch_histogram(img, 1, (0, 255, 0))
        histo_r = gen_3ch_histogram(img, 2, (0, 0, 255))
        img_l = cv2.vconcat([img, img_sp])
        img_r = cv2.vconcat([histo_r, histo_g, histo_b])
        frame = cv2.hconcat([img_l, img_r])

    tm.stop()
    disp_fps = f"{tm.getTimeMilli():.2f}"
    tm.reset()
    tm.start()
    cv2.putText(frame, disp_fps, (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow(w_name, frame)
    
    key = cv2.waitKey(1) # キー入力を1ms待って、k が27（ESC）だったらBreakする
    if key == 27: break
