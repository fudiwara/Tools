void setRc2Table(){
  if(0 < ans.get(img_idx).size()) ans.get(img_idx).clear();
  for(int i = 0; i < NUM_rc - 1; i++){
    if(rc.get(i).isVal0()) continue;
    ans.get(img_idx).add( int(rc.get(i).rx1 / img_scale + 0.5) );
    ans.get(img_idx).add( int(rc.get(i).ry1 / img_scale + 0.5) );
    ans.get(img_idx).add( int(rc.get(i).rx2 / img_scale + 0.5) );
    ans.get(img_idx).add( int(rc.get(i).ry2 / img_scale + 0.5) );
    ans.get(img_idx).add( rc.get(i).lb_num );
  }
  print("set: ", img_idx, " ");
  for(int j = 0; j < ans.get(img_idx).size(); j++){
    print(ans.get(img_idx).get(j), " ");
  }
  println();
}

void getTable2Rc(){
  NUM_rc = ans.get(img_idx).size() / 5;
  print("get: ", img_idx, NUM_rc, " ");
  for(int j = 0; j < ans.get(img_idx).size(); j++){
    print(ans.get(img_idx).get(j), " ");
  }
  println();
  //println(NUM_rc, ans.get(img_idx));
  //if(0 < NUM_rc) NUM_rc--;
  
  rc.clear();
  for(int i = 0; i < NUM_rc; i++){
    rc.add(new defRect());
    rc.get(i).rx1 = ans.get(img_idx).get(i * 5 + 0) * img_scale;
    rc.get(i).ry1 = ans.get(img_idx).get(i * 5 + 1) * img_scale;
    rc.get(i).rx2 = ans.get(img_idx).get(i * 5 + 2) * img_scale;
    rc.get(i).ry2 = ans.get(img_idx).get(i * 5 + 3) * img_scale;
    rc.get(i).lb_num = ans.get(img_idx).get(i * 5 + 4);
    rc.get(i).setRectVertex();
    rc.get(i).stateRectmode = 2;
  }
  rc.add(new defRect());
  NUM_rc++;
  state = 0;
}
