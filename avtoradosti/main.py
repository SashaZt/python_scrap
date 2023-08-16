from pathlib import Path
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
from proxi import proxies

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if '@' in line and ':' in line]


def get_random_proxy(proxies):
    return random.choice(proxies)


file_path = "proxies.txt"


def get_requests():
    cookies = {
        'LangId': '2',
        'MAXCOST': '0',
        'MINCOST': '0',
        'SIDS': '0',
        'avrsid': 'c2noes7uulnk00he5u1u96jcp5',
        'lst-cat': '',
        '_ga_HSTS5N7TNH': 'GS1.1.1692187785.1.0.1692187785.60.0.0',
        '_ga': 'GA1.1.1515260137.1692187785',
        '_gcl_au': '1.1.700059413.1692187785',
        '_fbp': 'fb.2.1692187785515.177623426',
    }

    headers = {
        'authority': 'www.avtoradosti.com.ua',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru',
        'cache-control': 'no-cache',
        # 'cookie': 'LangId=2; MAXCOST=0; MINCOST=0; SIDS=0; avrsid=c2noes7uulnk00he5u1u96jcp5; lst-cat=; _ga_HSTS5N7TNH=GS1.1.1692187785.1.0.1692187785.60.0.0; _ga=GA1.1.1515260137.1692187785; _gcl_au=1.1.700059413.1692187785; _fbp=fb.2.1692187785515.177623426',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.avtoradosti.com.ua/ua/katalog-tovara/avtolampy/p_1.html',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    for i in range(1, 197):
        proxies = load_proxies(file_path)
        proxy = get_random_proxy(proxies)
        login_password, ip_port = proxy.split('@')
        login, password = login_password.split(':')
        ip, port = ip_port.split(':')
        proxy_dict = {
            "http": f"http://{login}:{password}@{ip}:{port}",
            "https": f"http://{login}:{password}@{ip}:{port}"
        }
        response = requests.get(f'https://www.avtoradosti.com.ua/katalog-tovara/avtolampy/p_{i}.html', cookies=cookies,
                                headers=headers)
        print(response.status_code)
        src = response.text
        soup = BeautifulSoup(src, 'lxml')
        filename = f"c:\\DATA\\avtoradosti\\pages\\data_0{i}.html"
        with open(filename, "w", encoding='utf-8') as file:
            file.write(src)
        time.sleep(1)


def parsing_url():
    folder = r'c:\DATA\avtoradosti\pages\ru\*.html'
    files_html = glob.glob(folder)
    url_all = []
    with open('url_ru.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in files_html:
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            urls = soup.find_all('div', attrs={'class': 'p-imod'})
            for u in urls:
                url_product = u.find('a').get('href')
                url_all.append(url_product)
        for url in url_all:
            writer.writerow([url])


def parsin_product():
    folder = r'c:\DATA\avtoradosti\pages\ru\*.html'
    files_html = glob.glob(folder)
    with open('data_ru.csv', 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for item in files_html:
            proxy = random.choice(proxies)
            proxy_host = proxy[0]
            proxy_port = proxy[1]
            proxy_user = proxy[2]
            proxy_pass = proxy[3]
            proxi = f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            try:
                title = soup.find('h1').find('span', attrs={'itemprop': 'name'}).text
            except:
                title = None
            try:
                sku = soup.find('span', attrs={'itemprop': 'sku'}).text.replace('/', '_').strip()
            except:
                sku = None

            coun = 0

            table_char = soup.find('table', attrs={'class': 'cc-tech'})
            try:
                rows = table_char.select("table.cc-tech tr:not(:first-child)")  # исключаем первую строку с заголовком
            except:
                rows = None
                continue
            characteristics = []
            for row in rows:
                key_element = row.select_one("td.cc-pn")
                value_element = row.select_one("td:nth-child(2)")

                key = key_element.text if key_element else None
                value = value_element.text if value_element else None

                if key and value:  # Проверяем, что и ключ, и значение не None
                    characteristics.extend([key, value])

            brand_row = table_char.find('td', string='Бренд')
            brand_value = None
            if brand_row:
                brand_value = brand_row.find_next_sibling('td').text.replace('/', '_').strip()
            else:
                print("Бренд не найден")
            filenames = []
            img_dir = "c:\\DATA\\avtoradosti"
            try:
                all_img = soup.find('div', attrs={'class': 'slider-thumbs'}).find_all('a')
            except:
                all_img=None
                continue
            for i in all_img:
                coun +=1
                url_img = i.find('img').get('data-btnpic')
                filename = f"{brand_value}_{sku}_{coun}.jpg"
                file_path = os.path.join(img_dir, filename)

                filenames.append(filename)
                if os.path.exists(file_path):
                    continue  # Если файл уже существует, то завершаем выполнение функции
                img_data = requests.get(url_img)
                with open(file_path, 'wb') as file_img:
                    file_img.write(img_data.content)
                time.sleep(1)
            writer.writerow([title, sku,filenames] + characteristics)



if __name__ == '__main__':
    # get_requests()
    # parsing_url()
    parsin_product()
