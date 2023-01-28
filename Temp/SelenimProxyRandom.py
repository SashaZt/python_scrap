from selenium import webdriver

import datetime
import json
import csv
import os
import pickle
import lxml
import time
# Нажатие клавиш
from selenium.webdriver.common.keys import Keys
from random import randint
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import csv
from selenium import webdriver
import random
from fake_useragent import UserAgent
# Библиотеки для Асинхронного парсинга
import asyncio
import aiohttp
# Библиотеки для Асинхронного парсинга

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


proxylist = []
with open('proxylist_all.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # print(row[0])
        proxylist.append(row[0])
proxy = random.choice(proxylist)

# print(random.choice([line[0] for line in proxylist]))



options = webdriver.ChromeOptions()
# Отключение режима WebDriver
options.add_experimental_option('useAutomationExtension', False)
# # Работа в фоновом режиме
# options.headless = True
options.add_argument('--proxy-server=%s' % proxy)
driver_service = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
driver = webdriver.Chrome(
    service=driver_service,
    options=options
)

for i in range(5):
    print(proxy)
    driver.get('https://2ip.ua/ru/')
    time.sleep(1)
    driver.close()
    driver.quit()