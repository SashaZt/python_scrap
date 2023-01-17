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

useragent = UserAgent()

def get_content(url):
    start_time = datetime.datetime.now()
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": f"{useragent.random}"

    }
    categ_url = []
    start_time = datetime.datetime.now()
    resp = requests.get(url, headers=header)
    soup = BeautifulSoup(resp.text, 'lxml')
    table_category = soup.find('div', attrs={'class': 'menu__box-wrap'}).find('ul', attrs={'class': 'menu-list'}).find_all('li')
    for i in table_category:
        categ_url.append('https://dok.ua/ua' + i.find('a').get("href"))
    for j in categ_url[1:2]:
        resp = requests.get(j, headers=header)
        soup = BeautifulSoup(resp.text, 'lxml')
        rubric = soup.find('div', attrs={'class': 'rubric'})
        rubric_li = rubric.find_all('a')
        for k in rubric_li:
            print(k)
            print(k.get("href"))










    diff_time = datetime.datetime.now() - start_time
    print(f'Время на выполнение {diff_time}')







def parse_content():
    url = "https://dok.ua/ua"
    get_content(url)


if __name__ == '__main__':
    parse_content()
