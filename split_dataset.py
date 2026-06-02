# 画像ファイル、joson、txtファイルを指定した2つのフォルダに分割
import sys
sys.dont_write_bytecode = True
import pathlib, random, shutil

src_dir = pathlib.Path(sys.argv[1]) # 分割元のディレクトリ
dst_dir1 = pathlib.Path(sys.argv[2]) # 分割先のディレクトリ1
dst_dir2 = pathlib.Path(sys.argv[3]) # 分割先のディレクトリ2
rate_1 = float(sys.argv[4]) # 分割先1の割合
r_seed = int(sys.argv[5]) # シャッフルの乱数シード
random.seed(r_seed)

if dst_dir1.is_dir():
    shutil.rmtree(dst_dir1)
if dst_dir2.is_dir():
    shutil.rmtree(dst_dir2)

dst_dir1.mkdir(parents=True)
dst_dir2.mkdir(parents=True)

IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".gif", ".webp"] # 画像拡張子
image_files = sorted([p for p in src_dir.glob("**/*") if p.suffix.lower() in IMG_EXTS])

random.shuffle(image_files) # 並びをランダムにシャッフル
dst_1_count = int(len(image_files) * rate_1)
print(f"total: {len(image_files)}, dst_dir1: {dst_1_count}, dst_dir2: {len(image_files) - dst_1_count}")

for i, img_path in enumerate(image_files):
    json_file = img_path.with_suffix(".json") # 画像ファイル名と対のJSONファイル
    txt_file = img_path.with_suffix(".txt") # 画像ファイル名と対のTXTファイル

    if i < dst_1_count:
        dst_img_path = dst_dir1 / img_path.name
        dst_json_path = dst_dir1 / json_file.name
        dst_txt_path = dst_dir1 / txt_file.name
    else:
        dst_img_path = dst_dir2 / img_path.name
        dst_json_path = dst_dir2 / json_file.name
        dst_txt_path = dst_dir2 / txt_file.name
    
    shutil.copy(img_path, dst_img_path)
    shutil.copy(json_file, dst_json_path)
    shutil.copy(txt_file, dst_txt_path)
    