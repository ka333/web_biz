import urllib.request
from bs4 import BeautifulSoup
import time
import os


url = "https://www.tokyo-dome.co.jp/dome/schedule/"
response = urllib.request.urlopen(url)
dome = response.read().decode("utf-8")

soup2 = BeautifulSoup(dome, 'html.parser')
time_table = soup2.find("table", attrs={"class": "info_table"})
date = time_table.find_all("th", scope="row")
event = time_table.find_all("td")
info = []
