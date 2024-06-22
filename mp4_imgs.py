import sys
sys.dont_write_bytecode = True
import pathlib

import cv2
import numpy as np

mp4_path = sys.argv[1]
output_path = pathlib.Path(sys.argv[2])
if(not output_path.exists()): output_path.mkdir()

vc = cv2.VideoCapture(mp4_path)
frame_count = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
print(frame_count)

for i in range(frame_count):
    ret, frame = vc.read()

    if ret:
        output_img_path = output_path / f"i{i:05}.png"
        cv2.imwrite(str(output_img_path), frame)
        print(f"{output_img_path}")
vc.release()