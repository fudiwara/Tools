// ダイアログボックスで画像が保存されたディレクトリを指定して開く

defRect rc;

float img_scale = 1.2; // 表示するスケール
String file_exts[] = {".jpg", ".png"}, buf_str;
File baseDir;
StringList img_list, img1st_list;
int img_idx = 0, numImg, label_number, img_id = 0, add_val = 0;
PImage srcImg, dispImg, cropImg;
boolean loadImagesFlag = false;

void setup(){
  surface.setResizable(true);
  
  String[] prms = loadStrings("cfg.txt");
  if(prms != null){
    int fx = int(prms[0]);
    int fy = int(prms[1]);
    surface.setLocation(fx, fy);
    img_scale = float(prms[2]);
    img_id = int(prms[3]);
  }else{
    surface.setLocation(50, 50);
  }
  
  selectFolder("select directory", "imagesPathDir"); // imagesPathDir()にて開く
   
  rc = new defRect();
  rectMode(CORNERS);
  textAlign(CENTER, CENTER);
  textSize(30);
  
}

void loadImageDisp(int i){
  String path = img_list.get(i);
  srcImg = loadImage(path);
  dispImg = srcImg.get();
  dispImg.resize(int(dispImg.width * img_scale), int(dispImg.height * img_scale));
  PImage buf = createImage(dispImg.width, dispImg.height, RGB);
  buf.loadPixels();
  for (int x = 0; x < buf.pixels.length; x++) buf.pixels[x] = color(add_val); 
  buf.updatePixels();
  dispImg.blend(buf, 0, 0, dispImg.width, dispImg.height, 0, 0, dispImg.width, dispImg.height, ADD);
  surface.setSize(dispImg.width, dispImg.height);
}

void imagesPathDir(File selDIr){
  int i;
  baseDir = selDIr; // ダイアログから得るパス
  File files[] = listFiles(baseDir); // listFiles関数でファイル一覧を得る
  img_list = new StringList();
  img1st_list = new StringList();
  String buf_name, buf_1st;
  
  for(i = 0; i < files.length; i++){ // ファイル一覧に対して順に処理する
    for(String ext : file_exts){ // 拡張子の配列に対してループ
      if(files[i].getPath().endsWith(ext)){ // ファイルパス末尾が一致するかチェック
        img_list.append(files[i].getAbsolutePath()); // フルパスのリスト
        buf_name = files[i].getName(); 
        buf_1st = buf_name.substring(0, buf_name.lastIndexOf('.')); // stem を得る
        img1st_list.append(buf_1st); // stemのみのリスト
      }
    }
  }
  img_list.sort();
  img1st_list.sort();
  numImg = img_list.size(); // 画像ファイル数
  
  loadImageDisp(0);
  loadImagesFlag = true;
  println("done init");
}


void draw(){
  if(loadImagesFlag){
    image(dispImg, 0, 0);
    buf_str = "[  " + nf(img_idx, 5) + "  /  " + nf(numImg - 1, 5) + "  ]   ";
    surface.setTitle(buf_str + img_list.get(img_idx));

    rc.mng();
  }
}

void keyPressed(){  
  if(keyCode == UP){
    img_idx--;
    if(img_idx < 0) img_idx = numImg - 1;
    println(img_list.get(img_idx));
    loadImageDisp(img_idx);
  }else if(keyCode == DOWN){
    img_idx++;
    if(img_idx == numImg) img_idx = 0;
    println(img_list.get(img_idx));
    loadImageDisp(img_idx);
  }else if(keyCode == RIGHT){
    img_scale += 0.1;
    changeScaleImage();
    loadImageDisp(img_idx);
    println(img_scale);
  }else if(keyCode == LEFT){
    if(0.4 <= img_scale){
      img_scale -= 0.1;
      changeScaleImage();
      loadImageDisp(img_idx);
      println(img_scale);
    }
  }
  
  if(key == 'c'){
    rc.stateDrawMode = 0;
  }
  
  if(key == 's'){
    cropImg = rc.getImgmg(dispImg);
    String outputFileName = baseDir + "/"  + img1st_list.get(img_idx) + "_c" + nf(img_id, 4) + ".png";
    println(outputFileName, cropImg.width);
    cropImg.save(outputFileName);
    img_id++;
  }
  
  if(key == 'p'){
    add_val += 10;
    println(add_val);
    loadImageDisp(img_idx);
  }
  if(key == 'o'){
    add_val -= 10;
    println(add_val);
    loadImageDisp(img_idx);
  }
}

void changeScaleImage(){
  dispImg = srcImg.get();
  dispImg.resize(int(dispImg.width * img_scale), int(dispImg.height * img_scale));
  surface.setSize(dispImg.width, dispImg.height);
  rc.stateDrawMode = 0;
}

import processing.awt.PSurfaceAWT;
void dispose(){
  PSurfaceAWT awtSurface = (PSurfaceAWT)surface;
  PSurfaceAWT.SmoothCanvas canvas = (PSurfaceAWT.SmoothCanvas)awtSurface.getNative();
  java.awt.Frame frame = canvas.getFrame();
  int fx, fy;
  
  fx = frame.getX();
  fy = frame.getY();
  
  String saveStr[] = new String[4];
  saveStr[0] = str(fx);
  saveStr[1] = str(fy);
  saveStr[2] = str(img_scale);
  saveStr[3] = str(img_id);
  saveStrings("cfg.txt", saveStr);
}
