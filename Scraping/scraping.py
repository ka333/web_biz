import urllib.request
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd

#url = "https://www.tokyo-dome.co.jp/dome/schedule/"
year = "2017"
month = "6"
url = "https://www.tokyo-dome.co.jp/dome/schedule/?y="+year+"&m="+month
response = urllib.request.urlopen(url)
dome= response.read().decode("utf-8")

soup2 = BeautifulSoup(dome, 'html.parser')
time_table = soup2.find("table", attrs = {"class": "info_table"})
date = time_table.find_all("th",scope="row",rowspan="1")
event = time_table.find_all("p",class_=lambda x: x!= "img_left" and x != "bn")
info = []
for i in date:
    info.append(i.text.replace("\n","").replace("\t",""))
info
info2=[]
event
for i in event:
    info2.append(i.text.replace("\n","").replace("\t",""))

time = time_table.find_all("td",class_=lambda x: x!= "txt_left")
info3 = []
info4 = []
a = 0
for i in time:
    if a % 2 == 0:
        info3.append(i.text.replace("\xa0"," "))
    if a %2 == 1:
        info4.append(i.text.replace("\xa0"," "))
    a += 1
while " " in info3:
    info3.remove(" ")
open_time = info3
while " " in info4:
    info4.remove(" ")
close_time = info4
open_time,close_time


d = pd.DataFrame(info)
e = pd.DataFrame(info2)
o = pd.DataFrame(open_time)
c = pd.DataFrame(close_time)
schedule = pd.concat([d,e,o,c],axis = 1)
schedule.columns = ["日付","イベント名","開始時間","終了時間"]
print(schedule)
