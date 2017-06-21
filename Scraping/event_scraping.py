import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime

now = datetime.datetime.today()


#url = "https://www.tokyo-dome.co.jp/dome/schedule/"
year =str(now.year)
month = str(now.month)
url = "https://www.tokyo-dome.co.jp/dome/schedule/?y="+year+"&m="+month
response = urllib.request.urlopen(url)
dome= response.read().decode("utf-8")

soup2 = BeautifulSoup(dome, 'html.parser')
time_table = soup2.find("table", attrs = {"class": "info_table"})
date = time_table.find_all("th",scope="row",rowspan="1")
event = time_table.find_all("p",class_=lambda x: x!= "img_left" and x != "bn")
date_time = []
for i in date:
    date_time.append(year+"-"+month+"-"+i.text.replace("\n","").replace("\t","")[0:-4])
event_name=[]
event
for i in event:
    event_name.append(i.text.replace("\n","").replace("\t",""))

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

open_date_time = []
for i in range(0,len(date_time)):
    open_date_time.append(pd.Timestamp(date_time[i] + " " +open_time[i]))
open_date_time

close_date_time = []
for i in range(0,len(date_time)):
    close_date_time.append(pd.Timestamp(date_time[i] + " " +close_time[i]))
close_date_time

e = pd.DataFrame(event_name)
o = pd.DataFrame(open_date_time)
c = pd.DataFrame(close_date_time)
schedule = pd.concat([e,o,c],axis = 1)
schedule.columns = ["イベント名","開始時間","終了時間"]
schedule.to_csv("schedule.csv")
