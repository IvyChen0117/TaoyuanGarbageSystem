import json
import sys

try:
    import urllib2 as httplib   # 2.x
except Exception:
    import urllib.request as httplib  # 3.x

import ssl
context = ssl._create_unverified_context()

#v333333333333333333333333333333


try:
 import MySQLdb                         # pip install MySQL-python
except:
 import pymysql as MySQLdb             #  pip install MySQLdb



url="https://data.tycg.gov.tw/api/v1/rest/datastore/0c7bcfbf-b151-4411-b888-9ff685ff7a75?format=json"  #仔細看下面限制100筆
url="https://data.tycg.gov.tw/api/v1/rest/datastore/0c7bcfbf-b151-4411-b888-9ff685ff7a75?format=json&offset=100" # 由第幾筆開始
url="https://data.tycg.gov.tw/api/v1/rest/datastore/0c7bcfbf-b151-4411-b888-9ff685ff7a75?format=json&limit=800" # 最大資料量800筆
url="https://data.tycg.gov.tw/api/v1/rest/datastore/0c7bcfbf-b151-4411-b888-9ff685ff7a75?format=json&limit=6000" # 最大資料量6000筆

req=httplib.Request(url)
try:
    reponse = httplib.urlopen(req, context=context)
    if reponse.code==200:
        if (sys.version_info > (3, 0)):
            contents = reponse.read();
        else:
            contents = reponse.read()
        data = json.loads(contents)


        #確認是否有資料
        if(len(data)>=1):
            with open('垃圾車資料.json','w') as f: #存取
                json.dump(data,f)
        #print(data)#印出確認

except:                #  處理網路連線異常
    print("error")

#即時的資料先寫成檔案再載入處理
with open('垃圾車資料.json', 'r',encoding="utf-8") as f:
    data = json.load(f) # 讀取檔案 要用 load


import matplotlib.pyplot as plt
#三行可呈現中文
from matplotlib.font_manager import FontProperties # 步驟一

plt.rcParams['font.sans-serif'] = ['SimSun'] # 步驟一（替換sans-serif字型）
plt.rcParams['axes.unicode_minus'] = False  # 步驟二（解決座標軸負數的負號顯示問題）


"""
{"_id":2,
"項次":"2",
"清運序":"2",
"行政區":"蘆竹區",
"清運路線名稱":"山腳區1線",
"清運點名稱":"山林路一段與武聖街口",
"一般垃圾清運時間":"星期一二四五六:17:00",
"廚餘回收清運時間":"星期一二四五六:17:00",
"資源回收清運時間":"星期一二四五六:17:00"}


"""
"""
RubbishCarTable

id  A_I   (int)
項次 Item
清運序 Preface
行政區 District
清運路線名稱 ClearRoute
清運點名稱 SpotName
一般垃圾清運時間 GeneralGarbageTime
廚餘回收清運時間 FoodWasteTime
資源回收清運時間 GarbageRecycleTime

"""

db = MySQLdb.connect(host="127.0.0.1", user="admin", passwd="admin", db="mydatabase")
cursor = db.cursor()
print(len(data["result"]["records"])) #有幾筆資料
for x in range(int(len(data["result"]["records"]))):
    print("id:", data["result"]["records"][x]["_id"])
    print("清運序:", data["result"]["records"][x]["清運序"])
    print("行政區:", data["result"]["records"][x]["行政區"])
    print("清運路線名稱:", data["result"]["records"][x]["清運路線名稱"])
    print("清運點名稱:", data["result"]["records"][x]["清運點名稱"])
    print("一般垃圾清運時間:", data["result"]["records"][x]["一般垃圾清運時間"])
    print("廚餘回收清運時間", data["result"]["records"][x]["廚餘回收清運時間"])
    print("資源回收清運時間", data["result"]["records"][x]["資源回收清運時間"])

    a = data["result"]["records"][x]["項次"]
    b = data["result"]["records"][x]["清運序"]
    c = data["result"]["records"][x]["行政區"]
    d = data["result"]["records"][x]["清運路線名稱"]
    e = data["result"]["records"][x]["清運點名稱"]
    f = data["result"]["records"][x]["一般垃圾清運時間"]
    g = data["result"]["records"][x]["廚餘回收清運時間"]
    h = data["result"]["records"][x]["資源回收清運時間"]

    sql = "INSERT INTO RubbishCarTable (Item, Preface, District,ClearRoute,SpotName,GeneralGarbageTime,FoodWasteTime,GarbageRecycleTime) " \
          "VALUES ('%s', '%s', '%s','%s', '%s','%s', '%s', '%s') ;" % (a, b, c,d,e,f,g ,h )
    cursor.execute(sql)
    db.commit()


"""
參考資料:
https://data.tycg.gov.tw/opendata/datalist/datasetMeta/outboundDesc?id=88bdf93f-1b8d-4e8d-ade5-16670d909f38&rid=0c7bcfbf-b151-4411-b888-9ff685ff7a75


"""
