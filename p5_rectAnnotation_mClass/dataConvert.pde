// 各画像のアノテーション情報を配列化
void anFile2Table(){
  int i, j, u;
  Table src = null;
  src = loadTable(baseDir + "/" + list_file_name);
  if(src == null) return;
  println(numImg, src.getColumnCount() / 5);
  String img_file_name;
  int src_i = 0; // 追加ファイルがある場合は元のリストとidxが変わるので
  for(i = 0; i < numImg; i++){
    img_file_name = src.getString(src_i, 0);
    //print(img_file_name, img_name_list.get(i));
    if(img_name_list[i].equals(img_file_name)){
      print(img_file_name, " ");
      for(j = 0; j < src.getColumnCount() / 5; j++){
        boolean isUse = false;
        for(u = 0; u < 5; u++){
          int val = src.getInt(src_i, 1 + j * 5 + u);
          if(val != 0) isUse = true;
          //print(val, " ");
        }
        if(isUse){
          for(u = 0; u < 5; u++){
            ans.get(i).add(src.getInt(src_i, 1 + j * 5 + u));
          }
        }
      }
      println();
      src_i++;
    }else{
      println(img_file_name, ": new file");
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

// 1行毎にファイル名と矩形情報がスペース区切りになる形式で保存
void outputTrainList(){
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


void imgAn2Xml(){
  String folder_name = "data_yolo";
  String annotation_labels[] = {"worker", "obj1", "obj2", "obj3", "obj4"};
  String pose_state = "Unspecified";
  String dirPath = baseDir + "/xmls";
  //println(dirPath);
  File xmlDir = new File(dirPath);
  xmlDir.mkdir();
  int i, j;
  
  for(i = 0; i < numImg; i++){
    String fileName = img_name_list[i];
    //println(ans.get(i).size());
    if(ans.get(i).size() < 5) continue;
    String xmlName = dirPath + "/" + fileName.substring(0, fileName.lastIndexOf('.')) + ".xml";
    XML xml = new XML("annotation");
    XML nc, ncs, nco, ncob;
    nc = xml.addChild("folder");
    nc.setContent(folder_name);
    nc = xml.addChild("filename");
    nc.setContent(img_name_list[i]);
    
    nc = xml.addChild("size");
    ncs = nc.addChild("width");
    ncs.setContent(str(imageWidth.get(i)));
    ncs = nc.addChild("height");
    ncs.setContent(str(imageHeight.get(i)));
    ncs = nc.addChild("depth");
    ncs.setContent("3");
    
    for(j = 0; j < ans.get(i).size() / 5; j++){
      nc = xml.addChild("object");
      nco = nc.addChild("name");
      nco.setContent( annotation_labels[ans.get(i).get(j * 5 + 4)] );
      nco = nc.addChild("pose");
      nco.setContent(pose_state);
      nco = nc.addChild("truncated");
      nco.setContent("0");
      nco = nc.addChild("difficult");
      nco.setContent("0");
      
      nco = nc.addChild("bndbox");
      ncob = nco.addChild("xmin");
      ncob.setContent(str(ans.get(i).get(j * 5 + 0)));
      ncob = nco.addChild("ymin");
      ncob.setContent(str(ans.get(i).get(j * 5 + 1)));
      ncob = nco.addChild("xmax");
      ncob.setContent(str(ans.get(i).get(j * 5 + 2)));
      ncob = nco.addChild("ymax");
      ncob.setContent(str(ans.get(i).get(j * 5 + 3)));
    }
    saveXML(xml, xmlName);
  }
  
}
