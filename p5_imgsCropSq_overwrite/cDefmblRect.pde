class defRect{
  float x1, y1, x2, y2; // 作業補助用の矩形の角座標
  float rx1, ry1, rx2, ry2; // 矩形の角座標
  PVector rpv;
  float sx, sy, rw, rh; // d&d用のシフト座標、矩形の縦幅横幅
  float e_w, c_r, c_d, l_w; // 矩形、角、線のd&dの範囲を定める境界線の幅
  int stateDrawMode; // 矩形描画と移動、変形とかの状態
  int pnt_ovr; // ポインタの場所に関するフラグ
  
  defRect(){
    stateDrawMode = 0;
    e_w = 30;
    c_r = 7;
    c_d = c_r * 2;
    l_w = 9;
    pnt_ovr = -1;
    rpv = new PVector(0, 0);
  }
  
  void init(){
    stateDrawMode = 0;
  }
  
  PImage getSQimg(PImage img){
    PImage sq = img.get((int)rx1, (int)ry1, (int)(rx2 - rx1), (int)(ry2 - ry1));
    return sq;
  }
  
  void mng(){
    float x, y;
    if(stateDrawMode == 0){ // 矩形を描く前
      if(mousePressed && mouseButton == LEFT){
        x1 = mouseX;
        y1 = mouseY;
        stateDrawMode = 1; // 点1が決まったので対角線を得るモードへ
      }
    }else if(stateDrawMode == 1){
      x2 = mouseX;
      y2 = mouseY;
      rw = abs(x2 - x1);
      rh = abs(y2 - y1);
      float dif_r;
      if(rw < rh){
        dif_r = rh - rw;
        if(x1 < x2) x2 += dif_r;
        else x2 -= dif_r;
      }else{
        dif_r = rw - rh;
        if(y1 < y2) y2 += dif_r;
        else y2 -= dif_r;
      }
      chkCornerVal(); // x1, y1, x2, y2だと±の関係があれので調整
      if(mousePressed == false){ // マウスのボタンを放したら矩形確定
        rw = abs(x2 - x1);
        rh = abs(y2 - y1);
        
        stateDrawMode = 3; // 矩形確定後のモードへ
      }
      noFill();
      strokeWeight(3);
      stroke(255, 0, 0, 100);
      rect(rx1, ry1, rx2, ry2); // 入力中の矩形
    }else if(stateDrawMode == 3){ // 矩形移動もしくは変形の待ち状態
      x = mouseX;
      y = mouseY;
      pnt_ovr = -1;
      
      // ポインタの位置の判定
      if(c_r > dist(x, y, rpv.x, rpv.y)){ // 角点の中にあるとき
        pnt_ovr = 0;
        cursor(CROSS);
      }
      if(pnt_ovr == -1){
        if(rx1 + e_w < x && x < rx2 - e_w && ry1 + e_w < y && y < ry2 - e_w){
          cursor(HAND); // 矩形の中にあるとき
          pnt_ovr = 9;
        }else{
          cursor(ARROW); // どれにも該当しない場合
        }
      }
      
      if(mousePressed && mouseButton == LEFT){
        if(0 == pnt_ovr){
          stateDrawMode = 10; // 角点上なので変形モードへ
        }else if(pnt_ovr == 9){
          sx = x - rx1;
          sy = y - ry1;
          stateDrawMode = 20; // 矩形の中にあるときなので全体移動のモードへ
        }
      }
      fill(255, 120);
      strokeWeight(3);
      stroke(255, 160, 0);
      rect(rx1, ry1, rx2, ry2);
      stroke(0);
      strokeWeight(1);
      fill(50, 255, 150);
      ellipse(rpv.x, rpv.y, c_d, c_d);
    }else if(stateDrawMode == 10){
      if(mousePressed && mouseButton == LEFT){
        cursor(CROSS); // d&d状態の処理なのでこのカーソル
        if(0 == pnt_ovr) setVertex2Rect(mouseX, mouseY);
      }else if(mousePressed == false){
        cursor(ARROW); // d&dから離した状態なのでこのカーソル
        stateDrawMode = 3;
      }
      fill(255, 80);
      strokeWeight(3);
      stroke(255, 160, 0);
      rect(rx1, ry1, rx2, ry2);
      stroke(0);
      strokeWeight(1);
      fill(50, 255, 150);
      ellipse(rpv.x, rpv.y, c_d, c_d);
    }else if(stateDrawMode == 20){
      if(mousePressed && mouseButton == LEFT){
        cursor(HAND); // d&d状態の処理なのでこのカーソル
        rx1 = mouseX - sx; // マウスの位置から左上座標を求める
        ry1 = mouseY - sy;
        rx2 = rx1 + rw; // 縦幅横幅も固定なので右下も計算する
        ry2 = ry1 + rh;
        rpv.set(rx2, ry2);
      }else if(mousePressed == false){
        cursor(ARROW); // d&dから離した状態なのでこのカーソル
        stateDrawMode = 3;
      }
      fill(255, 80);
      strokeWeight(3);
      stroke(255, 160, 0);
      rect(rx1, ry1, rx2, ry2);
    }
    //println(stateDrawMode);
  }
  
  void chkCornerVal(){ // 角座表の位置関係の調整
    if(x1 < x2){
      rx1 = x1; rx2 = x2;
    }else{
      rx1 = x2; rx2 = x1;
    }
    if(y1 < y2){
      ry1 = y1; ry2 = y2;
    }else{
      ry1 = y2; ry2 = y1;
    }
    rpv.set(rx2, ry2);
  }
  
  void setVertex2Rect(float mx, float my){ // 右下座標を動かしたときの対応
    float tw, th, ts;
    tw = mx - rx1;
    th = my - ry1;
    
    if(tw < th){
      ts = th - tw;
      rx2 = mx;
      ry2 = my - ts;
    }else{
      ts = tw - th;
      rx2 = mx - ts;
      ry2 = my;
    }
    
    rw = rx2 - rx1;
    rh = ry2 - ry1;
    rpv.set(rx2, ry2);
  }
}
