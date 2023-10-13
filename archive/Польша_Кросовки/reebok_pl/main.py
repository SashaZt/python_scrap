import shutil
import glob
import boto3
import cloudscraper
import urllib.parse
import pandas as pd
from playwright.sync_api import sync_playwright
from cf_clearance import sync_cf_retry, sync_stealth
import zipfile
import os
import shutil
import random
import tempfile
import shutil
from lxml import html
from main_asio import *
import re
import json
from bs4 import BeautifulSoup
import undetected_chromedriver
import csv
import shutil
import time
import requests
from datetime import datetime, timedelta
# Нажатие клавиш
import glob
import shutil
import zipfile
import os
from lxml import html
import re
import json
import csv
import time
import requests
# Нажатие клавиш
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from selenium import webdriver
import random

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Установка учетных данных AWS
ACCESS_KEY = 'AKIAQWBRT2HZZFWLS5EJ'
SECRET_KEY = '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'
file_path = "all_proxy.txt" #Тут все прокси которые есть

# Создание клиента S3
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if '@' in line and ':' in line]


def get_random_proxy(proxies):
    return random.choice(proxies)

def get_cookies_sf(url):
    url_pl = url
    # res = requests.get(url_pl)
    # if '<title>Just a moment...</title>' in res.text:
    #     print("cf challenge fail")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        sync_stealth(page, pure=True)
        page.goto(url_pl)
        res = sync_cf_retry(page)
        if res:
            cookies = page.context.cookies()
            for cookie in cookies:
                if cookie.get('name') == 'cf_clearance':
                    cf_clearance_value = cookie.get('value')
                    # print(cf_clearance_value)
            ua = page.evaluate('() => {return navigator.userAgent}')
            # print(ua)
            # get_cloudscraper(ua, cf_clearance_value)

        else:
            print("cf challenge fail")

        browser.close()
        # print(url)
    headers = {"user-agent": ua}
    cookies = {"cf_clearance": cf_clearance_value}
    return headers, cookies




"""Сохраняем все json"""
def save_json_product():

    url_men = "https://www.reebok.eu/en-pl/shopping/men-shoes"
    headers, cookies = get_cookies_sf(url_men)
    response = requests.get(url_men, cookies=cookies, headers=headers)
    # proxy = get_random_proxy(proxies)
    # login_password, ip_port = proxy.split('@')
    # login, password = login_password.split(':')
    # ip, port = ip_port.split(':')
    # proxy_dict = {
    #     "http": f"http://{login}:{password}@{ip}:{port}",
    #     "https": f"http://{login}:{password}@{ip}:{port}"
    # }
    # s.proxies = proxy_dict
    # html = response.content
    # filename = f"amazon.html"
    # with open(filename, "w", encoding='utf-8') as f:
    #     f.write(html.decode('utf-8'))
    # scraper_get_men = scraper.get(url_men).content
    # # time.sleep(10)
    soup = BeautifulSoup(response.text, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_mezczyzni = data['numberOfItems'] // 48
    counter_mezczyzni = 0
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\json_data\\men-shoes'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    for page in range(1, totalResources_mezczyzni + 2):
        if page == 1:
            counter_mezczyzni += 1
            response = requests.get(url_men, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\men-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(10)
        if page > 1:
            counter_mezczyzni += 1
            url_mezczyzni_api = f'https://www.reebok.eu/en-pl/shopping/men-shoes?pageindex={counter_mezczyzni}'
            response = requests.get(url_mezczyzni_api, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\men-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(f"men-shoes {counter_mezczyzni} из {totalResources_mezczyzni + 1 }")
    print(f"Собрал men-shoes")

    """women"""
    url_women = "https://www.reebok.eu/en-pl/shopping/women-shoes"
    headers, cookies = get_cookies_sf(url_women)
    response = requests.get(url_women, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_women = data['numberOfItems'] // 48
    counter_women = 1
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\json_data\\women-shoes'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for page in range(1, totalResources_women + 2):
        if page == 1:
            url_women = "https://www.reebok.eu/en-pl/shopping/women-shoes"
            response = requests.get(url_women, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\women-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(1)
        if page > 1:
            counter_women += 1
            url_women_api = f'https://www.reebok.eu/en-pl/shopping/women-shoes?pageindex={counter_women}'
            response = requests.get(url_women_api, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\women-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(f"women-shoes {counter_women} из {totalResources_women + 1}")
    print(f"Собрал women-shoes")

    """kids_youth_9_14"""
    url_kids_youth_9_14 = "https://www.reebok.eu/en-pl/shopping/kids-youth-9-14"
    headers, cookies = get_cookies_sf(url_kids_youth_9_14)
    response = requests.get(url_kids_youth_9_14, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_kids_youth_9_14 = data['numberOfItems'] // 48
    counter_kids_youth_9_14 = 1
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\json_data\\kids-youth-9-14'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for page in range(0, totalResources_kids_youth_9_14 + 2):
        if page == 1:
            url_kids_youth_9_14 = "https://www.reebok.eu/en-pl/shopping/kids-youth-9-14"
            response = requests.get(url_kids_youth_9_14, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\kids-youth-9-14\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(1)
        if page > 1:
            counter_kids_youth_9_14 += 1
            url_kids_youth_9_14_api = f'https://www.reebok.eu/en-pl/shopping/kids-youth-9-14?pageindex={counter_kids_youth_9_14}'
            response = requests.get(url_kids_youth_9_14_api, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\kids-youth-9-14\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(f"kids_youth_9_14 {counter_kids_youth_9_14} из {totalResources_kids_youth_9_14 + 1 }")
    print(f"Собрал kids_youth_9_14")

    """kids_kids_5_8"""
    url_kids_kids_5_8_years_kids_shoes = "https://www.reebok.eu/en-pl/shopping/kids-kids-5-8-years-kids-shoes"
    headers, cookies = get_cookies_sf(url_kids_kids_5_8_years_kids_shoes)
    response = requests.get(url_kids_kids_5_8_years_kids_shoes, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_kids_kids_5_8_years_kids_shoes = data['numberOfItems'] // 48
    counter_kids_kids_5_8_years_kids_shoes = 1
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\json_data\\kids-kids-5-8-years-kids-shoes'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for page in range(0, totalResources_kids_kids_5_8_years_kids_shoes + 2):
        if page == 1:
            url_kids_kids_5_8_years_kids_shoes = "https://www.reebok.eu/en-pl/shopping/kids-kids-5-8-years-kids-shoes"
            response = requests.get(url_kids_kids_5_8_years_kids_shoes, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\kids-kids-5-8-years-kids-shoes\\0_{page}.json", "w",
                      encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(1)
        if page > 1:
            counter_kids_kids_5_8_years_kids_shoes += 1
            url_kids_kids_5_8_years_kids_shoes_api = f'https://www.reebok.eu/en-pl/shopping/kids-kids-5-8-years-kids-shoes?pageindex={counter_kids_kids_5_8_years_kids_shoes}'
            response = requests.get(url_kids_kids_5_8_years_kids_shoes_api, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\kids-kids-5-8-years-kids-shoes\\0_{page}.json", "w",
                      encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(
            f"kids-kids-5-8-years-kids-shoes {counter_kids_kids_5_8_years_kids_shoes} из {totalResources_kids_kids_5_8_years_kids_shoes + 1}")
    print(f"Собрал kids-kids-5-8-years-kids-shoes")

    """_kids_baby_0_4"""
    url_kids_baby_0_4_years_baby_shoes = "https://www.reebok.eu/en-pl/shopping/kids-baby-0-4-years-baby-shoes"
    headers, cookies = get_cookies_sf(url_kids_baby_0_4_years_baby_shoes)
    response = requests.get(url_kids_baby_0_4_years_baby_shoes, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_kids_baby_0_4_years_baby_shoes = data['numberOfItems'] // 48
    counter_kids_baby_0_4_years_baby_shoes = 1
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\json_data\\kids-baby-0-4-years-baby-shoes'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for page in range(0, totalResources_kids_baby_0_4_years_baby_shoes + 2):
        if page == 1:
            url_kids_baby_0_4_years_baby_shoes = "https://www.reebok.eu/en-pl/shopping/kids-baby-0-4-years-baby-shoes"
            response = requests.get(url_kids_baby_0_4_years_baby_shoes, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\kids-baby-0-4-years-baby-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(1)
        if page > 1:
            counter_kids_baby_0_4_years_baby_shoes += 1
            url_kids_baby_0_4_years_baby_shoes_api = f'https://www.reebok.eu/en-pl/shopping/kids-baby-0-4-years-baby-shoes?pageindex={counter_kids_baby_0_4_years_baby_shoes}'
            response = requests.get(url_kids_baby_0_4_years_baby_shoes_api, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\json_data\\kids-baby-0-4-years-baby-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(f"kids-baby-0-4-years-baby-shoes {counter_kids_baby_0_4_years_baby_shoes} из {totalResources_kids_baby_0_4_years_baby_shoes + 1}")
    print(f"Собрал kids-baby-0-4-years-baby-shoes")


"""Собираем все ссылки на товары"""
def parsing_url_json():
    folders = [r"c:\reebok_pl\json_data\men-shoes\*.json",
               r"c:\reebok_pl\json_data\kids-kids-5-8-years-kids-shoes\*.json",
               r"c:\reebok_pl\json_data\kids-youth-9-14\*.json",
               r"c:\reebok_pl\json_data\women-shoes\*.json",
               r"c:\reebok_pl\json_data\kids-baby-0-4-years-baby-shoes\*.json"
               ]
    for folder in folders:
        urls = []
        files_json = glob.glob(folder)
        group = files_json[0].split("\\")[-2]
        for item in files_json:
            with open(item, encoding='utf-8') as f:
                data = json.load(f)
                all_products = data['itemListElement']
                coun = 0
                for url in all_products:
                    coun +=1
                    urls.append(url['url'])
        with open(f'c:\\reebok_pl\\csv_url\\{group}\\url.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
            writer.writerow(urls)
    print("Собрали все url")



def del_files_html_product():
    folders_del = [r"c:\reebok_pl\json_data\kids-baby-0-4-years-baby-shoes",
               r"c:\reebok_pl\json_data\kids-kids-5-8-years-kids-shoes",
               r"c:\reebok_pl\json_data\kids-youth-9-14",
               r"c:\reebok_pl\json_data\men-shoes",
               r"c:\reebok_pl\json_data\women-shoes"
               ]
    for folder in folders_del:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")





if __name__ == '__main__':
    del_files_html_product()
    print("Удалили старые файлы HTML")
    save_json_product()
    print("Сохранили все JSON")
    parsing_url_json()
    print('Собрали все ссылки')
    print('Переходим к скрипту main_asio.py')
