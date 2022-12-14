// 各画像のアノテーション情報を配列化
void anFile2Table(){
  int i, j, u;
  Table src = null;
  src = loadTable(baseDir + "/" + list_file_name);
  if(src == null) return;
  println(numImg, src.getColumnCount() / 5);
  String img_file_name;
  for(i = 0; i < numImg; i++){
    img_file_name = src.getString(i, 0);
    //print(img_file_name, img_name_list.get(i));
    if(img_name_list[i].equals(img_file_name)){
      print(img_file_name, " ");
      for(j = 0; j < src.getColumnCount() / 5; j++){
        boolean isUse = false;
        for(u = 0; u < 5; u++){
          int val = src.getInt(i, 1 + j * 5 + u);
          if(val != 0) isUse = true;
          //print(val, " ");
        }
        if(isUse){
          for(u = 0; u < 5; u++){
            ans.get(i).add(src.getInt(i, 1 + j * 5 + u));
          }
        }
      }
      println();
    }
  }
}

// 配列化されたアノテーション情報を保存
void table2anFile(){
  int i, j, maxCols = 0;
  
  for(i = 0; i < numImg; i++) if(maxCols < ans.get(i).size()) maxCols = ans.get(i).size();
  Table dst = new Table();
  for(i = 0; i < maxCols + 1; i++) dst.addColumn();
  for(i = 0; i < numImg; i++) dst.addRow();
  
  for(i = 0; i < numImg; i++){
    println(img_name_list[i]);
    dst.setString(i, 0, img_name_list[i]);
    for(j = 0; j < ans.get(i).size(); j++){
      dst.setInt(i, j + 1, ans.get(i).get(j));
    }
  }
  saveTable(dst, baseDir + "/" + list_file_name);
}

// yolo形式で保存
void outputYoloList(){
  int i, j, n, outputNum = 0, c = 0;
  
  for(i = 0; i < numImg; i++) if(0 < ans.get(i).size()) outputNum++;
  String listsStr[] = new String[outputNum];
  //println(numImg, outputNum);
  
  for(i = 0; i < numImg; i++){
    if(0 < ans.get(i).size()){
      //print(i, " ", img_name_list.get(i), " ");
      String boxs_annots = "";
      for(n = 0; n < ans.get(i).size() / 5; n++){
        if(0 < n) boxs_annots += " ";
        String box_vals = "";
        for(j = 0; j < 5; j++){
          box_vals += ans.get(i).get(n * 5 + j) + ",";
        }
        boxs_annots += box_vals.substring(0, box_vals.length() - 1); // 最後のカンマ一つを削除
      }
      listsStr[c] = img_name_list[i] + " " + boxs_annots;
      c++;
    }
  }
  saveStrings(baseDir + "/_train_list_space.txt", listsStr);
}

// pytorch系ssdとかeffdet用のリストに保存
void outputEffDetList(){
  int i, j, n, c = 0;
  
  String listsStr[] = {};
  
  for(i = 0; i < numImg; i++){
    if(0 < ans.get(i).size()){
      //print(i, " ", img_name_list.get(i), " ");
      for(n = 0; n < ans.get(i).size() / 5; n++){
        String box_vals = "";
        for(j = 0; j < 5; j++){
          if(j == 4) box_vals += ans.get(i).get(n * 5 + j) + 1;
          else box_vals += ans.get(i).get(n * 5 + j) + ",";
        }
        c++;
        listsStr = expand(listsStr, c);
        listsStr[c - 1] = img_name_list[i] + "," + box_vals;
        
      }
    }
  }
  saveStrings(baseDir + "/_train_list_part.txt", listsStr);
}
