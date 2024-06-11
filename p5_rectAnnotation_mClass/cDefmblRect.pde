class defRect{
  float x1, y1, x2, y2; // 作業補助用の矩形の角座標
  float rx1, ry1, rx2, ry2; // 矩形の角座標
  PVector rpv[];
  float sx, sy, rw, rh; // d&d用のシフト座標、矩形の縦幅横幅
  float e_w, c_r, c_d, l_w; // 矩形、角、線のd&dの範囲を定める境界線の幅
  int stateDrawMode; // 矩形描画と移動、変形とかの状態
  int pnt_ovr; // ポインタの場所に関するフラグ
  int stateRectmode; // 矩形未定義：0、矩形処理中：1、矩形定義後：2、次のを作った後：3
  boolean in_prc;
  int lb_num;
  
  defRect(){
    stateDrawMode = 3;
    e_w = 5;
    c_r = 7;
    c_d = c_r * 2;
    l_w = 9;
    pnt_ovr = -1;
    rpv = new PVector[4];
    for(int i = 0; i < 4; i++) rpv[i] = new PVector(0, 0);
    stateRectmode = 0;
    in_prc = false;
  }
  
  void gen(int ln){
    if(stateRectmode == 0){ // 矩形を描く前
      if(mousePressed && mouseButton == LEFT){
        x1 = mouseX;
        y1 = mouseY;
        stateRectmode = 1; // 点1が決まったので対角線を得るモードへ
      }
    }else if(stateRectmode == 1){
      x2 = mouseX;
      y2 = mouseY;
      
      if(x1 < 0) x1 = 0;
      if(y1 < 0) y1 = 0;
      if(dispImg.width <= x2) x2 = dispImg.width - 1;
      if(dispImg.height <= y2) y2 = dispImg.height - 1;
      if(x2 < 0) x2 = 0;
      if(y2 < 0) y2 = 0;
      if(dispImg.width <= x1) x1 = dispImg.width - 1;
      if(dispImg.height <= y1) y1 = dispImg.height - 1;
      
      chkCornerVal(); // x1, y1, x2, y2だと±の関係があれなので調整
      if(mousePressed == false){ // マウスのボタンを放したら矩形確定
        rw = rx2 - rx1;
        rh = ry2 - ry1;
        if(20 < rw * rh){
          stateRectmode = 2; // 矩形確定後のモードへ
          lb_num = ln;
        }else{
          stateRectmode = 0;
        }
      }
      if(0 < stateRectmode){
        noFill();
        strokeWeight(3);
        stroke(255, 0, 0, 180);
        rect(rx1, ry1, rx2, ry2); // 入力中の矩形
      }
    }
  }
  
  void disp(){
    if(in_prc == false){
      fill(255, 100);
      strokeWeight(3);
      stroke(255, 160, 0);
      rect(rx1, ry1, rx2, ry2);
      stroke(0);
      strokeWeight(1);
      fill(50, 255, 150);
      for(int i = 0; i < 4; i++) ellipse(rpv[i].x, rpv[i].y, c_d, c_d);
      fill(255, 0, 0);
      text(lb_num, (rx1 + rx2) / 2, (ry1 + ry2) / 2);
    }
  }
  
  void mng(){
    if(stateRectmode < 2) return;
    float x, y;
    int i;
    if(stateDrawMode == 3){ // 矩形移動もしくは変形の待ち状態
      x = mouseX;
      y = mouseY;
      pnt_ovr = -1;
      
      // ポインタの位置の判定
      for(i = 0; i < 4; i++){ // 角点の中にあるとき
        if(c_r > dist(x, y, rpv[i].x, rpv[i].y)){
          pnt_ovr = i; // 0〜3
          cursor(CROSS);
          break;
        }
      }
      if(pnt_ovr == -1){
        if(rx1 + e_w < x && x < rx2 - e_w && ry1 + e_w < y && y < ry2 - e_w){
          cursor(HAND); // 矩形の中にあるとき
          pnt_ovr = 9;
        }else if(rx1 + l_w < x && x < rx2 - l_w && ry1 - l_w < y && y < ry1 + l_w){
          pnt_ovr = 4; // 上側
          cursor(CROSS);
        }else if(rx2 - l_w < x && x < rx2 + l_w && ry1 + l_w < y && y < ry2 - l_w){
          pnt_ovr = 5; // 右側
          cursor(CROSS);
        }else if(rx1 + l_w < x && x < rx2 - l_w && ry2 - l_w < y && y < ry2 + l_w){
          pnt_ovr = 6; // 下側
          cursor(CROSS);
        }else if(rx1 - l_w < x && x < rx1 + l_w && ry1 + l_w < y && y < ry2 - l_w){
          pnt_ovr = 7; // 左側
          cursor(CROSS);
        }else{
          cursor(ARROW); // どれにも該当しない場合
        }
      }
      
      if(mousePressed && mouseButton == LEFT){
        if(0 <= pnt_ovr && pnt_ovr <= 7){
          stateDrawMode = 10; // 矩形の中にあるときなので角点変形モードへ
          in_prc = true;
        }else if(pnt_ovr == 9){
          sx = x - rx1;
          sy = y - ry1;
          rw = rx2 - rx1;
          rh = ry2 - ry1;
          stateDrawMode = 20; // 矩形の中にあるときなので全体移動のモードへ
          in_prc = true;
        }
      }
      fill(255, 150);
      strokeWeight(3);
      stroke(255, 160, 0);
      rect(rx1, ry1, rx2, ry2);
      stroke(0);
      strokeWeight(1);
      fill(50, 255, 150);
      for(i = 0; i < 4; i++) ellipse(rpv[i].x, rpv[i].y, c_d, c_d);
    }else if(stateDrawMode == 10){
      if(mousePressed && mouseButton == LEFT){
        cursor(CROSS); // d&d状態の処理なのでこのカーソル
        if(0 <= pnt_ovr && pnt_ovr <= 3) setVertex2Rect(pnt_ovr, mouseX, mouseY);
        else if(4 <= pnt_ovr && pnt_ovr <= 7) setLine2Rect(pnt_ovr, mouseX, mouseY);
        in_prc = true;
      }else if(mousePressed == false){
        cursor(ARROW); // d&dから離した状態なのでこのカーソル
        stateDrawMode = 3;
        in_prc = false;
      }
      fill(255, 150);
      strokeWeight(3);
      stroke(255, 160, 0);
      rect(rx1, ry1, rx2, ry2);
      stroke(0);
      strokeWeight(1);
      fill(50, 255, 150);
      for(i = 0; i < 4; i++) ellipse(rpv[i].x, rpv[i].y, c_d, c_d);
      fill(255, 0, 0);
      text(lb_num, (rx1 + rx2) / 2, (ry1 + ry2) / 2);
    }else if(stateDrawMode == 20){
      if(mousePressed && mouseButton == LEFT){
        cursor(HAND); // d&d状態の処理なのでこのカーソル
        rx1 = mouseX - sx; // マウスの位置から左上座標を求める
        ry1 = mouseY - sy;
        rx2 = rx1 + rw; // 縦幅横幅も固定なので右下も計算する
        ry2 = ry1 + rh;
        setRectVertex();
        in_prc = true;
      }else if(mousePressed == false){
        cursor(ARROW); // d&dから離した状態なのでこのカーソル
        stateDrawMode = 3;
        in_prc = false;
      }
      fill(255, 150);
      strokeWeight(3);
      stroke(255, 0, 0);
      rect(rx1, ry1, rx2, ry2);
    }
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
    setRectVertex();
  }
  
  void setRectVertex(){
    rpv[0].set(rx1, ry1);
    rpv[1].set(rx2, ry1);
    rpv[2].set(rx2, ry2);
    rpv[3].set(rx1, ry2);
  }
  
  void setVertex2Rect(int pos, float mx, float my){
    if(pos == 0){
      rx1 = mx;
      ry1 = my;
    }else if(pos == 1){
      rx2 = mx;
      ry1 = my;
    }else if(pos == 2){
      rx2 = mx;
      ry2 = my;
    }else if(pos == 3){
      rx1 = mx;
      ry2 = my;
    }
    setRectVertex();
  }
  
  void setLine2Rect(int lineNum, float mx, float my){
    if(lineNum == 4) ry1 = my;
    else if(lineNum == 5) rx2 = mx;
    else if(lineNum == 6) ry2 = my;
    else if(lineNum == 7) rx1 = mx;
    setRectVertex();
  }
  
  boolean isVal0(){
    if(rx1 == 0 && ry1 == 0 && rx2 == 0 && ry2 == 0) return true;
    return false;
  }
  void printVals(){
    println(rx1, ry1, rx2, ry2);
  }
}
