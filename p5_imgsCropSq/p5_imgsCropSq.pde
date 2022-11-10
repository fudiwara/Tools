// ダイアログボックスで画像が保存されたディレクトリを指定して開く

defRect rc;

float img_scale = 1.2; // 表示用のスケール (適当に手持ちの画像に合わせて変える)

String file_exts[] = {".jpg", ".png"}, buf_str;
File baseDir;
StringList img_list, img1st_list;
int img_idx = 0, numImg, label_number, img_id = 0;
PImage srcImg, dispImg, sqImg, resImg;
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
  
  selectFolder("select directory", "imagesPathDir");
   
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
  surface.setSize(dispImg.width, dispImg.height);
}

void imagesPathDir(File selDIr){
  int i;
  baseDir = selDIr;
  File files[] = listFiles(baseDir);
  img_list = new StringList();
  img1st_list = new StringList();
  String buf_name, buf_1st;
  
  for(i = 0; i < files.length; i++){
    for(String ext : file_exts){
      if(files[i].getPath().endsWith(ext)){
        img_list.append(files[i].getAbsolutePath());
        buf_name = files[i].getName();
        buf_1st = buf_name.substring(0, buf_name.lastIndexOf('.'));
        img1st_list.append(buf_1st);
      }
    }
  }
  img_list.sort();
  img1st_list.sort();
  numImg = img_list.size();
  
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
    img_scale += 0.2;
    changeScaleImage();
  }else if(keyCode == LEFT){
    if(0.4 <= img_scale){
      img_scale -= 0.2;
      changeScaleImage();
    }
  }
  
  if(key == 'c'){
    rc.stateDrawMode = 0;
  }
  
  if(key == 's'){
    sqImg = rc.getSQimg(dispImg);
    String outputFileName = baseDir + "/"  + img1st_list.get(img_idx) + "_c" + nf(img_id, 4) + ".png";
    sqImg.save(outputFileName);
    img_id++;
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
