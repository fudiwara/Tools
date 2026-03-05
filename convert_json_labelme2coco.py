import json
import os
import glob

def labelme2coco(labelme_json_dir, output_json_path):
    # COCOフォーマットの基本構造
    coco_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    
    category_map = {}  # クラス名とIDを紐付ける辞書
    category_id_counter = 1
    image_id_counter = 1
    annotation_id_counter = 1
    
    # フォルダ内のすべてのJSONファイルを取得
    json_files = glob.glob(os.path.join(labelme_json_dir, "*.json"))
    
    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # 1. images への登録
        # LabelmeのJSONに保存されている画像パスとサイズを取得
        file_name = data.get("imagePath", os.path.basename(json_file).replace(".json", ".jpg"))
        height = data.get("imageHeight")
        width = data.get("imageWidth")
        
        coco_data["images"].append({
            "id": image_id_counter,
            "file_name": file_name,
            "width": width,
            "height": height
        })
        
        # 2. annotations への登録
        # shapesが空（背景画像）の場合はこのループがスキップされます
        for shape in data.get("shapes", []):
            label = shape["label"]
            
            # 新しいクラス名が出てきたらcategoriesに登録
            if label not in category_map:
                category_map[label] = category_id_counter
                category_id_counter += 1
                
            cat_id = category_map[label]
            
            # 今回は矩形（rectangle）のみを対象として変換
            if shape["shape_type"] == "rectangle":
                points = shape["points"]
                x1, y1 = points[0]
                x2, y2 = points[1]
                
                # ユーザーが右下から左上に向かって枠を描画した場合を考慮し、最小値・最大値を判定
                x_min = min(x1, x2)
                y_min = min(y1, y2)
                x_max = max(x1, x2)
                y_max = max(y1, y2)
                
                bbox_width = x_max - x_min
                bbox_height = y_max - y_min
                area = bbox_width * bbox_height
                
                coco_data["annotations"].append({
                    "id": annotation_id_counter,
                    "image_id": image_id_counter,
                    "category_id": cat_id,
                    "bbox": [x_min, y_min, bbox_width, bbox_height],
                    "area": area,
                    "iscrowd": 0,
                    "segmentation": [] # 物体検出では空でOK
                })
                annotation_id_counter += 1
                
        image_id_counter += 1
        
    # 3. categories の構築
    for label, cat_id in category_map.items():
        coco_data["categories"].append({
            "id": cat_id,
            "name": label,
            "supercategory": "none"
        })
        
    # JSONファイルとして出力
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(coco_data, f, indent=4)
        
    print(f"変換完了: {len(json_files)}個のファイルを {output_json_path} に統合しました。")
    print(f"検出されたクラス: {list(category_map.keys())}")

# --- 実行部分 ---
if __name__ == "__main__":
    # LabelmeのJSONが入っているフォルダのパス
    INPUT_DIR = "./labelme_data" 
    
    # 出力するCOCO形式JSONのパス
    OUTPUT_FILE = "./_annotations.coco.json" 
    
    labelme2coco(INPUT_DIR, OUTPUT_FILE)