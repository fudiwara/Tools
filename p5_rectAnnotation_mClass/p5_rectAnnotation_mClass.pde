// セーブ後の画像追加処理
ArrayList<defRect> rc = new ArrayList<defRect>();
int NUM_rc = 1;
int wrok_id = 0;
int state = 0;
int label_number = 0;

String list_file_name = "_train_list.csv"; // 保存されるファイル名
float img_scale = 1.1;
String file_exts[] = {".jpg", ".JPG", ".png", ".PNG", ".jpeg", ".JPEG"}, buf_str;
File baseDir;
String img_list[], img_name_list[];
int img_idx = 0, numImg, add_val;
IntList imageWidth = new IntList(), imageHeight = new IntList();
PImage srcImg, dispImg;
boolean loadImgListFlag = false, frameInputFlag;
ArrayList<ArrayList<Integer>> ans = new ArrayList<ArrayList<Integer>>();

void loadImageDisp(int i){
  String path = img_list[i];
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
  StringList ipl, inl;
  baseDir = selDIr; // ベースのディレクトリ
  File files[] = listFiles(baseDir);
  ipl = new StringList();
  inl = new StringList();
  
  for(i = 0; i < files.length; i++){
    for(String ext : file_exts){
      if(files[i].getPath().endsWith(ext)){
        ipl.append(files[i].getAbsolutePath());
        inl.append(files[i].getName());
        ans.add(new ArrayList<Integer>());
      }
    }
  }
  
  numImg = ipl.size();
  img_list = new String[numImg];
  img_name_list = new String[numImg];
  for(i = 0; i < numImg; i++){
    img_list[i] = ipl.get(i);
    img_name_list[i] = inl.get(i);
    srcImg = loadImage(img_list[i]);
    imageWidth.append(srcImg.width);
    imageHeight.append(srcImg.height);
  }
  img_list = sort(img_list);
  img_name_list = sort(img_name_list);
  //println(img_list);
  
  anFile2Table();
  getTable2Rc();
  
  loadImageDisp(0);
  loadImgListFlag = true;
  println("done init");
}

void setup(){
  surface.setResizable(true);
  selectFolder("select directory", "imagesPathDir");
  
  rc.add(new defRect());
  rectMode(CORNERS);
  textAlign(CENTER, CENTER);
}

void draw(){
  if(loadImgListFlag){
    image(dispImg, 0, 0);
    buf_str = "[  " + nf(img_idx, 5) + "  /  " + nf(numImg - 1, 5) + "  ]   ";
    surface.setTitle(buf_str + img_list[img_idx]);
      
    int i;
    wrok_id = -1;
    
    for(i = 0; i < NUM_rc; i++){
      if(2 <= rc.get(i).stateRectmode){
        rc.get(i).disp();
      }
    }
    
    if(state == 0){
      for(i = 0; i < NUM_rc; i++){
        rc.get(i).mng();
        if(rc.get(i).in_prc){
          wrok_id = i;
          break;
        }
      }
    }
    if(wrok_id == -1){
      if(rc.get(NUM_rc - 1).stateRectmode < 2){ // 最大IDの矩形ができてないければ
        rc.get(NUM_rc - 1).gen(label_number); // 矩形生成の処理
        if(rc.get(NUM_rc - 1).stateRectmode == 1) state = 1;
      }else{
        rc.add(new defRect());
        NUM_rc++;
        state = 0;
        println(NUM_rc);
      }
    }
    int textPos = 50;
    textSize(30);
    noStroke();
    fill(255, 180);
    rect(0, 0, textPos, textPos);
    fill(255, 0, 0);
    if(label_number != -1) text(label_number, textPos / 2, textPos / 2);
  }
}

void keyPressed(){
  if(key >= '0' && key <= '9') label_number = Integer.parseInt("" + key);
  
  if(keyCode == UP){
    setRc2Table();
    img_idx--;
    if(img_idx < 0) img_idx = numImg - 1;
    println(img_list[img_idx], img_idx, NUM_rc);
    loadImageDisp(img_idx);
    getTable2Rc();
  }
  if(keyCode == DOWN){
    setRc2Table();
    img_idx++;
    if(img_idx == numImg) img_idx = 0;
    println(img_list[img_idx], img_idx, NUM_rc);
    loadImageDisp(img_idx);
    getTable2Rc();
  }
  if(keyCode == RIGHT){
    img_scale += 0.1;
    changeScaleImage();
    loadImageDisp(img_idx);
    getTable2Rc();
    println(img_scale);
  }
  if(keyCode == LEFT){
    if(0.4 <= img_scale){
      img_scale -= 0.1;
      changeScaleImage();
      loadImageDisp(img_idx);
      getTable2Rc();
      println(img_scale);
    }
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
  if(key == 'c'){
    rc.clear();
    rc.add(new defRect());
    NUM_rc = 1;
  }
  
  if(key == 's'){
    setRc2Table();
    table2anFile();
    println("done save");
  }
  
  if(key == 'y'){
    setRc2Table();
    outputYoloList();
    println("done space format list");
  }
  
  if(key == 'e'){
    setRc2Table();
    outputEffDetList();
    println("done ssd & effdet list");
  }
}

void changeScaleImage(){
  dispImg = srcImg.get();
  dispImg.resize(int(dispImg.width * img_scale), int(dispImg.height * img_scale));
  surface.setSize(dispImg.width, dispImg.height);
}
