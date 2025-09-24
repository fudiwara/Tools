import sys
import json
import pathlib

def transform_json(filename): # "imagePath"のスペースを詰めて"imageData"をnullに
    with open(filename, "r", encoding="utf-8") as f: # JSONファイルの読み込み
        data = json.load(f)

    if "imagePath" in data and isinstance(data["imagePath"], str):
        data["imagePath"] = data["imagePath"].replace(" ", "") #"imagePath"のスペースを詰める

    if "imageData" in data:
        data["imageData"] = None # "imageData"の内容をnullにする

    with open(filename, "w", encoding="utf-8") as f: # 同じファイルに上書き保存
        json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"convert: {filename}")

dir_src = pathlib.Path(sys.argv[1])
json_paths = sorted([p for p in dir_src.iterdir() if p.suffix in [".json", ".JSON"]])

for p_j in json_paths:
    transform_json(p_j)
