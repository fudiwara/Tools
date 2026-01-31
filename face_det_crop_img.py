import sys
sys.dont_write_bytecode = True
import pathlib
import cv2 as cv
import mediapipe as mp

# パスをコマンドライン引数で受け取る
targetDirPath = pathlib.Path(sys.argv[1]).resolve()
if not targetDirPath.is_dir(): exit() # ディレクトリのみ処理する

output_dir = pathlib.Path(sys.argv[2]) # 出力先のディレクトリ

# 指定されたディレクトリの"画像ファイル"一覧を取得
fileList = list(pathlib.Path(targetDirPath).iterdir())
fileList.sort()

# mediapipe関連
mp_face_detection = mp.solutions.face_detection # mediapipeの初期化
face_detection = mp_face_detection.FaceDetection(min_detection_confidence = 0.5)

# ターゲットのディレクトリ内を順にチェックしていく
exts = [".jpg", ".png", ".jpeg", ".JPG", ".PNG", ".JPEG"]
for fn in fileList:
    if fn.is_file() and (fn.suffix in exts): # ファイルのみ処理する
        # print(fn)
        img = cv.imread(str(fn)) # 画像ファイルの読み込み
        ch, cw, _ = img.shape

        results = face_detection.process(cv.cvtColor(img, cv.COLOR_BGR2RGB)) # mediapipeに処理を渡す
        if results.detections:
            for i in range(len(results.detections)):
                # 顔領域の検出結果描画
                b = results.detections[i].location_data.relative_bounding_box
                x0 = int(b.xmin * cw)
                y0 = int(b.ymin * ch)
                x1 = int((b.xmin + b.width) * cw)
                y1 = int((b.ymin + b.height) * ch)
                # cv.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0))

                dst_face_img = img[y0 : y1, x0 : x1]
                outputfilename = output_dir / f"_f{i:02}_{fn.stem}.png"
                cv.imwrite(str(outputfilename), dst_face_img)