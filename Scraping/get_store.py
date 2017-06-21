import sys
import urllib
import urllib.parse
import urllib.request
import json
import pandas as pd
store = pd.DataFrame()

####
# 変数の型が文字列かどうかチェック
####
def is_str( data = None ) :
  if isinstance( data, str ) or isinstance( data, bytes ) :
    return True
  else :
    return False

####
# 初期値設定
####

# APIアクセスキー
#自分のキーを登録
keyid     = "82ba8d6049f8d175615b16572aeaca50"
# エンドポイントURL
url       = "https://api.gnavi.co.jp/RestSearchAPI/20170530/"
# 緯度・経度、範囲を変数に入れる
# 緯度経度は日本測地系で日比谷シャンテのもの。範囲はrange=1で300m以内を指定している。
# 緯度
latitude  = "35.670083"
# 経度
longitude = "139.763267"
# 範囲
range     = "1"

page= 100

####
# APIアクセス
####
# URLに続けて入れるパラメータを組立
query = [
  ( "format",    "json"    ),
  ( "keyid",     keyid     ),
  ( "latitude",  latitude  ),
  ( "longitude", longitude ),
  ( "range",     range     ),
    ("hit_per_page",100)
]

# URL生成
url += "?{0}".format( urllib.parse.urlencode( query ) )
# API実行
try :
  result = urllib.request.urlopen( url ).read()
except ValueError :
  print ("APIアクセスに失敗しました。")
  sys.exit()


####
# 取得した結果を解析
####
data = json.loads( result.decode('utf-8') )

# エラーの場合
if "error" in data :
  if "message" in data :
    print ("{0}".format( data["message"] ))
  else :
    print ("データ取得に失敗しました。")
  sys.exit()

# ヒット件数取得
total_hit_count = None
if "total_hit_count" in data :
  total_hit_count = data["total_hit_count"]

# ヒット件数が0以下、または、ヒット件数がなかったら終了
if total_hit_count is None or int(total_hit_count) <= 0 :
  print ("指定した内容ではヒットしませんでした。")
  sys.exit()

# レストランデータがなかったら終了
if not "rest" in data :
  print ("レストランデータが見つからなかったため終了します。")
  sys.exit()

# ヒット件数表示
print ("{0}件ヒットしました。".format( total_hit_count ))
print ("----")

# 出力件数
disp_count = 0
store = pd.DataFrame()
# レストランデータ取得
for rest in data["rest"] :
  line                 = []
  id                   = ""
  name                 = ""
  access_line          = ""
  access_station       = ""
  access_walk          = ""
  code_category_name_s = []
  tel                  = ""
  address              = ""
  shop_image1          = ""
  url                  = ""
  # 店舗番号
  if "id" in rest and is_str( rest["id"] ) :
    id = rest["id"]
  line.append( id )
  # 店舗名
  if "name" in rest and is_str( rest["name"] ) :
    name = u"{0}".format( rest["name"] )
  line.append( name )
  if "tel" in rest and is_str(rest["tel"]):
    tel =rest["tel"]
    line.append(tel)
  if "address" in rest and is_str(rest["address"]):
    address =rest["address"]
    line.append(address)
  if "shop_image1" in rest["image_url"] and is_str(rest["image_url"]["shop_image1"]):
    shop_image1 =rest["image_url"]["shop_image1"]
    line.append(shop_image1)
  elif "shop_image2" in rest["image_url"] and is_str(rest["image_url"]["shop_image2"]):
    shop_image1 =rest["image_url"]["shop_image2"]
    line.append(shop_image1)
  else:
    line.append("No image")
  if "url" in rest and is_str(rest["url"]):
    url =rest["url"]
    line.append(url)
  # タブ区切りで出力
  print ("\t".join( line ))
  store[str(disp_count)] = line
  disp_count += 1

# 出力件数を表示して終了
print ("----")
print (u"{0}件出力しました。".format( disp_count ))
store_T = store.T
store_T.columns = ["ID","name","phone_number","address","shopimage_url","url"]
store_T["location_id"] = "東京ドーム"
store_T.to_csv("store_infomation.csv")
