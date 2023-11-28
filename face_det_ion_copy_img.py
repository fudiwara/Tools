import sys
sys.dont_write_bytecode = True
import pathlib
import shutil
import cv2
import mediapipe as mp

targetDirPath = pathlib.Path(sys.argv[1]).resolve() # 入力画像のディレクトリ
if not targetDirPath.is_dir(): exit()

base_path = pathlib.Path(sys.argv[2]) # 出力先のディレクトリ (ココは存在していること)

dir_face_y = base_path / pathlib.Path("face_y")
if(not dir_face_y.exists()): dir_face_y.mkdir()
dir_face_n = base_path / pathlib.Path("face_n")
if(not dir_face_n.exists()): dir_face_n.mkdir()

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
        img = cv2.imread(str(fn)) # 画像ファイルの読み込み

        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # mediapipeに処理を渡す
        if results.detections:
            outputfilename = dir_face_y / fn.name # 顔検出できた場合
        else:
            outputfilename = dir_face_n / fn.name # 顔検出できなかった場合
        
        shutil.copy(fn, outputfilename) # 指定したパスにコピー
        