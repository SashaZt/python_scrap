from bs4 import BeautifulSoup
import random
import glob
import re
import requests
import json
import cloudscraper
import os
from playwright.sync_api import sync_playwright
from cf_clearance import sync_cf_retry, sync_stealth
import time
import shutil
import tempfile
# import undetected_chromedriver as webdriver


from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv

cookies = {
    'ab_group_version': 'A',
    'is_sync': '1',
    'PHPSESSID': '7q8g4muqonqqbjgl88gc2dvjj100lhnnqubo7d33bu7drn8s51e8q3ah9ih3ocp1k',
    'deviceId': 'p4em4tv9n56zyeyamrcbte61n9yq4l82',
    'sessionId': 'vla5nfaua2d1zhj7z1yp7z3qh3xbfxkz',
    'sourceTraffic': 'direct',
    'traffic_source_params': '%7B%7D',
    's': '0',
    'ins': '0',
    'i1': '1',
    'i2': '1',
    'c0': '{"Visit":true,"NoBounce":true,"Value":false,"Action":false,"Checkout":false,"NewOrder":false,"Accepted":false}',
    'ct0': '3',
    '_gid': 'GA1.2.972242398.1693219040',
    '_gcl_au': '1.1.340756755.1693219041',
    '_fbp': 'fb.1.1693219050031.796144061',
    'vh': '1',
    'lang': 'ru',
    '_gat': '1',
    '_ga': 'GA1.2.561442955.1693219040',
    'sendCnt1': '17',
    '_ga_YH59FJRK2C': 'GS1.1.1693219040.1.1.1693219164.60.0.0',
}

headers = {
    'authority': 'dok.ua',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru',
    'cache-control': 'no-cache',
    # 'cookie': 'ab_group_version=A; is_sync=1; PHPSESSID=7q8g4muqonqqbjgl88gc2dvjj100lhnnqubo7d33bu7drn8s51e8q3ah9ih3ocp1k; deviceId=p4em4tv9n56zyeyamrcbte61n9yq4l82; sessionId=vla5nfaua2d1zhj7z1yp7z3qh3xbfxkz; sourceTraffic=direct; traffic_source_params=%7B%7D; s=0; ins=0; i1=1; i2=1; c0={"Visit":true,"NoBounce":true,"Value":false,"Action":false,"Checkout":false,"NewOrder":false,"Accepted":false}; ct0=3; _gid=GA1.2.972242398.1693219040; _gcl_au=1.1.340756755.1693219041; _fbp=fb.1.1693219050031.796144061; vh=1; lang=ru; _gat=1; _ga=GA1.2.561442955.1693219040; sendCnt1=17; _ga_YH59FJRK2C=GS1.1.1693219040.1.1.1693219164.60.0.0',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://dok.ua/art-0092s50050-bosch-20271195',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}
def get_requests():
    response = requests.get('https://dok.ua/ua/art-0092s50050-bosch-20271195', cookies=cookies, headers=headers)
    src = response.text
    soup = BeautifulSoup(src, 'lxml')
    filename = f"ru.html"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(src)


def parsing():
    file = f"ua.html"
    with open(file, encoding="utf-8") as file:
         src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    characteristics = []

    # Находим все теги tr с нужным классом и извлекаем из них текст
    for tr in soup.find_all('tr', {'class': 'card-characts-list-item'}):
        span = tr.find('span', {'class': 'mistake-char-title'})
        if span:
            characteristics.append(span.text.strip())

    print(characteristics)






if __name__ == '__main__':
    # get_requests()
    parsing()
