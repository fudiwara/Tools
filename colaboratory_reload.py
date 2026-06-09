import sys, time
sys.dont_write_bytecode = True
import datetime
import webbrowser

target_url = "https://colab... URLをダブルクォーテーション内に貼り付ける"
sleep_time_minutes = 1 # 再度開く時間を 分単位 で指定する

# 指定した時間毎に任意のノートブックを開く
for i in range(12):
    webbrowser.open(target_url) # デフォルトブラウザで指定URLを開く
    print(i, datetime.datetime.today()) # 開いた回数と現在の日時を表示
    time.sleep(sleep_time_minutes * 60)