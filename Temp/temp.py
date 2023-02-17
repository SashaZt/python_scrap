import csv
import random
import time
import re
import os

# Нажатие клавиш
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import glob
from datetime import datetime

# l = "https://www.11880.com/suche/Alfa-Romeo/deutschland"
# print(l.split("/")[-2])
with open('info.txt', 'r') as f:
    nums = f.read().splitlines()
for i in nums:

folder_url = "C://scrap_tutorial-master//archive//11800//url//"
os.mkdir(f'{folder_url}')
# str_ = 'Светильник потолочный MAYTONI 43265 (C032CL-L32MG3K) в стиле модерн ➤ Цвет: золото, белый ✈ БЕСПЛАТНАЯ ДОСТАВКА ✈ Киев и вся Украина: ✓ Одесса ✓ Харьков ✓ Днепр ✓ Львов'
url = 'https://www.bcautoencheres.fr/Lot?id=19346880&ItemId=58bffd67-1f4a-4570-b473-2cee37bb131a&q=&bq=saleid_exact%3A15b740e5-49bc-4e22-9c39-7470049e6f22&sort=LotNumber&missingMileage=True&awaitingAppraisal=True&page=1&extraFiltersActive=true&saleHeader=true&returnTo=2-XGJ-79&promoAppliedSets=&R=15&SR=10&SourceSystem=PEEP'
# # url = '=IMAGE("https://sortiment.lidl.ch/media/catalog/product/cache/38c728e59b3a47950872534eff8a1e63/2/3/2332_ApfelZimt_PSXX.jpg")'
# #
# print(re.search(r"[(\d{8})]"), url)

# # Регулярные выражения
# g2g = 'About 1,471 results'
#
# tttt = g2g.replace(',', '')
# # rr = re.search(r"(\d+)", tttt).group(0)
# rr = re.search(r"(\d+)", tttt).group(0)
# print(rr)

# import csv
#
# Читаем csv по строно
# proxy = [
#
# ]
# with open('proxies.csv', newline='', encoding='utf-8') as files:
#     csv_reader = list(csv.reader(files, delimiter=' ', quotechar='|'))
#     for row in csv_reader:
#         proxy.append(row[0])
# print(proxy)

# f = open(
#     'C:\\scrap_tutorial-master\\Temp\\view-source_https___www.webstaurantstore.com_bunn-27370-0000-solenoid_HP273700000.html',
#     'r')
# s = f.read()
# soup = BeautifulSoup(s, 'lxml')
# #
# js = re.findall(">\s*\{.*\}", html)
# # raw_json = soup.find_all(js)
# print(soup)

# import requests
#
# url = 'https://httpbin.org/anything'
# proxy = 'http://04c220013e9c68fe33f21bfa45fd5ba6ed3924d9:@proxy.zenrows.com:8001'
# proxies = {'http': proxy, 'https': proxy}
# response = requests.get(url, proxies=proxies, verify=False)
#
# print(response)
# new_url = url.split("https://www.bcautoencheres.fr/Lot?id=")
# ttt = re.search(r"(\w+)-(\w+)", str_).group(0)
# print(new_url)
#
# path = r'C:\\scrap_tutorial-master\\flagma.ua\\urls_card_01.json'
# files = path.replace(".json", "").strip('\\')[-12:]
# print(files)
#
# #
#
# targetPattern = f"C:\\scrap_tutorial-master\\vehiclebid_bot\\data\\*.html"
# files_html = glob.glob(targetPattern)
# for item in files_html:
#     if item.split("\\")[-1].replace(".html", "") in url:
#         print('YES')
#     else:
#         print('NOT')

# t = "Лампа в комплекте: Нет лампы"
# regex_ch_08 = 'Лампа'
# if regex_ch_08 in t:
#     print('+')
# else:
#     print("-")
