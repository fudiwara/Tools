import sys
sys.dont_write_bytecode = True
import cv2 as cv

cap = cv.VideoCapture(0)

save_count = 0 # 画像保存時のカウンタ
while(True):
    ret, frame = cap.read()
    
    if not ret: # フレームの読み込みに失敗したら
        break # ループ終了

    cv.imshow("cap", frame)
    
    key = cv.waitKey(1)
    if key == 27:
        break
    elif key == ord("s"): # sキーが押されたら
        save_filename = f"{save_count:03}.png" # ファイル名指定
        cv.imwrite(save_filename, frame)
        save_count += 1 # 画像保存後にカウンタ+1
