import glob
import shutil
import pandas as pd
import zipfile
import os
from lxml import html
from main_asio import main_asio as asio_main
import re
import simplejson as JS_S
import json
from bs4 import BeautifulSoup
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
from fake_useragent import UserAgent

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

useragent = UserAgent()
# Данные для прокси
PROXY_HOST = '141.145.205.4'
PROXY_PORT = 31281  # Без кавычек
PROXY_USER = 'proxy_alex'
PROXY_PASS = 'DbrnjhbZ88'

# Настройка для requests чтобы использовать прокси
# proxies = {'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}/'}

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"76.0.0"
}
"""

background_js = """
let config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

proxies = {'http': 'http://80.77.34.218:9999', 'https': 'http://80.77.34.218:9999'}
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.3"}

def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--proxy-server=37.233.3.100:9999')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    s = Service(
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    return driver


"""Сохраняем html страницы"""
def save_html_data ():
    """driver_mezczyzni"""
    driver_mezczyzni = get_chromedriver()
    url = 'https://www.adidas.pl/api/plp/content-engine?query=mezczyzni-buty'
    driver_mezczyzni.get(url)
    time.sleep(5)
    with open('c:\\adidas_pl\\html_data\\mezczyzni-buty_page.html', 'w', encoding='utf-8') as f:
        f.write(driver_mezczyzni.page_source)
    print("Получили спискок всех страниц кросовок mezczyzni-buty")
    with open('c:\\adidas_pl\\html_data\\mezczyzni-buty_page.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    json_data = re.search(r'{.*}', html_content, re.DOTALL).group()
    data = json.loads(json_data)
    totalResources_mezczyzni = data['raw']['itemList']['count'] // 48
    counter_mezczyzni = 0
    for page in range(1, totalResources_mezczyzni + 2):
        if page == 1:
            url_mezczyzni_api = 'https://www.adidas.pl/api/plp/content-engine?query=mezczyzni-buty'
            driver_mezczyzni.get(url_mezczyzni_api)
            time.sleep(5)
            with open(f'c:\\adidas_pl\\html_data\\mezczyzni-buty\\0{page}.html', 'w', encoding='utf-8') as f:
                f.write(driver_mezczyzni.page_source)
        if page > 1:
            counter_mezczyzni += 48
            url_mezczyzni_api = f'https://www.adidas.pl/api/plp/content-engine?query=mezczyzni-buty&start={counter_mezczyzni}'
            driver_mezczyzni.get(url_mezczyzni_api)
            time.sleep(5)
            with open(f'c:\\adidas_pl\\html_data\\mezczyzni-buty\\0{page}.html', 'w', encoding='utf-8') as f:
                f.write(driver_mezczyzni.page_source)
        print(f"mezczyzni {counter_mezczyzni} из {totalResources_mezczyzni * 48}")
    driver_mezczyzni.close()
    driver_mezczyzni.quit()
    """kobiety"""
    driver_kobiety = get_chromedriver()
    urls_kobiety = "https://www.adidas.pl/api/plp/content-engine?query=kobiety-buty"
    driver_kobiety.get(urls_kobiety)
    time.sleep(5)
    with open('c:\\adidas_pl\\html_data\\kobiety-buty_page.html', 'w', encoding='utf-8') as f:
        f.write(driver_kobiety.page_source)
    print("Получили спискок всех страниц кросовок kobiety-buty")
    with open('c:\\adidas_pl\\html_data\\kobiety-buty_page.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    json_data = re.search(r'{.*}', html_content, re.DOTALL).group()
    data = json.loads(json_data)
    totalResources_kobiety = data['raw']['itemList']['count'] // 48
    counter_kobiety = 0
    for page in range(1, totalResources_kobiety + 2):
        if page == 1:
            driver_kobiety.get(urls_kobiety)
            time.sleep(5)
            with open(f'c:\\adidas_pl\\html_data\\kobiety-buty\\0{page}.html', 'w', encoding='utf-8') as f:
                f.write(driver_kobiety.page_source)
        if page > 1:
            counter_kobiety += 48
            urls_kobiety = f'https://www.adidas.pl/api/plp/content-engine?query=kobiety-buty&start={counter_kobiety}'

            driver_kobiety.get(urls_kobiety)
            time.sleep(5)
            with open(f'c:\\adidas_pl\\html_data\\kobiety-buty\\0{page}.html', 'w', encoding='utf-8') as f:
                f.write(driver_kobiety.page_source)
        print(f"kobiety {counter_kobiety} из {totalResources_kobiety * 48}")
    driver_kobiety.close()
    driver_kobiety.quit()
    """chlopcy-buty"""
    driver_chlopcy = get_chromedriver()
    urls_chlopcy = "https://www.adidas.pl/api/plp/content-engine?query=chlopcy-buty"
    driver_chlopcy.get(urls_chlopcy)
    time.sleep(5)
    with open('c:\\adidas_pl\\html_data\\chlopcy-buty_page.html', 'w', encoding='utf-8') as f:
        f.write(driver_chlopcy.page_source)
    print("Получили спискок всех страниц кросовок chlopcy-buty")
    with open('c:\\adidas_pl\\html_data\\chlopcy-buty_page.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    json_data = re.search(r'{.*}', html_content, re.DOTALL).group()
    data = json.loads(json_data)
    totalResources_chlopcy_buty = data['raw']['itemList']['count'] // 48
    counter_chlopcy_buty = 0
    for page in range(1, totalResources_chlopcy_buty + 2):
        if page == 1:
            driver_chlopcy.get(urls_chlopcy)
            time.sleep(5)
            with open(f'c:\\adidas_pl\\html_data\\chlopcy-buty\\0{page}.html', 'w', encoding='utf-8') as f:
                f.write(driver_chlopcy.page_source)
        if page > 1:
            counter_chlopcy_buty += 48
            urls_chlopcy = f'https://www.adidas.pl/api/plp/content-engine?query=chlopcy-buty&start={counter_chlopcy_buty}'
            driver_chlopcy.get(urls_chlopcy)
            time.sleep(5)
            with open(f'c:\\adidas_pl\\html_data\\chlopcy-buty\\0{page}.html', 'w', encoding='utf-8') as f:
                f.write(driver_chlopcy.page_source)
        print(f"chlopcy {counter_chlopcy_buty} из {totalResources_chlopcy_buty * 48}")
    driver_chlopcy.close()
    driver_chlopcy.quit()
    """dziewczynki-buty"""
    driver_dziewczynki = get_chromedriver()
    urls_dziewczynki = "https://www.adidas.pl/api/plp/content-engine?query=dziewczynki-buty"
    driver_dziewczynki.get(urls_dziewczynki)
    time.sleep(5)
    with open('c:\\adidas_pl\\html_data\\dziewczynki-buty_page.html', 'w', encoding='utf-8') as f:
        f.write(driver_dziewczynki.page_source)
    print("Получили спискок всех страниц кросовок dziewczynki-buty")
    with open('c:\\adidas_pl\\html_data\\dziewczynki-buty_page.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    json_data = re.search(r'{.*}', html_content, re.DOTALL).group()
    data = json.loads(json_data)
    totalResources_dziewczynki_buty = data['raw']['itemList']['count'] // 48
    counter_dziewczynki_buty = 0
    for page in range(1, totalResources_dziewczynki_buty + 2):
        if page == 1:
            print(urls_dziewczynki)
            driver_dziewczynki.get(urls_dziewczynki)
            time.sleep(5)
            with open(f'c:\\adidas_pl\\html_data\\dziewczynki-buty\\0{page}.html', 'w', encoding='utf-8') as f:
                f.write(driver_dziewczynki.page_source)
        if page > 1:
            counter_dziewczynki_buty += 48
            urls_dziewczynki = f'https://www.adidas.pl/api/plp/content-engine?query=dziewczynki-buty&start={counter_dziewczynki_buty}'
            print(urls_dziewczynki)
            driver_dziewczynki.get(urls_dziewczynki)
            time.sleep(5)
            with open(f'c:\\adidas_pl\\html_data\\dziewczynki-buty\\0{page}.html', 'w', encoding='utf-8') as f:
                f.write(driver_dziewczynki.page_source)
        print(f"dziewczynki {counter_dziewczynki_buty} из {totalResources_dziewczynki_buty * 48}")
    driver_dziewczynki.close()
    driver_dziewczynki.quit()


def html_to_json ():
    folders = [
        r"c:\adidas_pl\html_data\mezczyzni-buty\*.html",
        r"c:\adidas_pl\html_data\dziewczynki-buty\*.html",
        r"c:\adidas_pl\html_data\kobiety-buty\*.html",
        r"c:\adidas_pl\html_data\chlopcy-buty\*.html"
               ]

    for folder in folders:
        urls = []
        files_json = glob.glob(folder)
        group = files_json[0].split("\\")[-2]
        coun = 0
        for item in files_json:

            with open(item, 'r', encoding='utf-8') as f:
                page_html = f.read()
                json_data = re.search(r'{.*}', page_html, re.DOTALL).group()
                data = json.loads(json_data)
                with open(f"c:\\adidas_pl\\json_data\\{group}\\0_{coun}.json", "w", encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                coun += 1





# def save_json_product():
    # proxies = {'http': 'http://80.77.34.218:9999', 'https': 'http://80.77.34.218:9999'}
    # header = {
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    #     "authority": "www.adidas.pl",
    #     "accept-language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6",
    #     'Accept-Encoding': "gzip, deflate, br"
    # }
    # auth = requests.auth.HTTPProxyAuth('proxy_alex', 'DbrnjhbZ88')
    #
    # url = 'https://www.adidas.pl/api/plp/content-engine?query=mezczyzni-buty'
    #
    # response = requests.get(url, headers=header, proxies=proxies) # , proxies=proxies, auth=auth
    #
    # print(response)
    # exit()
    # json_data = resp.json()
    # totalResources_mezczyzni = json_data['raw']['itemList']['count'] // 48
    # counter_mezczyzni = 0
    # for page in range(1, totalResources_mezczyzni + 2):
    #     if page == 1:
    #         url_mezczyzni_api = 'https://www.adidas.pl/api/plp/content-engine?query=mezczyzni-buty'
    #
    #         response = requests.get(url_mezczyzni_api, headers=header, proxies=proxies)
    #         if response.status_code == 200:
    #             data = response.json()
    #             with open(f"c:\\adidas_pl\\html_data\\mezczyzni-buty\\0_{page}.json", "w", encoding='utf-8') as f:
    #                 json.dump(data, f, indent=4, ensure_ascii=False)
    #         time.sleep(1)
    #     if page > 1:
    #         counter_mezczyzni += 48
    #         url_mezczyzni_api = f'https://www.adidas.pl/api/plp/content-engine?query=mezczyzni-buty&start={counter_mezczyzni}'
    #         response = requests.get(url_mezczyzni_api, headers=header, proxies=proxies)
    #         if response.status_code == 200:
    #             data_1 = response.json()
    #             with open(f"c:\\adidas_pl\\html_data\\mezczyzni-buty\\0_{page}.json", "w", encoding='utf-8') as f:
    #                 json.dump(data_1, f, indent=4, ensure_ascii=False)
    #
    #         time.sleep(1)
    #     print(f"mezczyzni {counter_mezczyzni} из {totalResources_mezczyzni * 48}")
    # print(f"Собрал mezczyzni")
    #
    # """kobiety"""
    # urls_kobiety = "https://www.adidas.pl/api/plp/content-engine?query=kobiety-buty"
    # resp = requests.get(urls_kobiety, headers=header, proxies=proxies)  # , proxies=proxies
    # json_data = resp.json()
    # totalResources_kobiety = json_data['raw']['itemList']['count'] // 48
    # counter_kobiety = 0
    # for page in range(1, totalResources_kobiety + 2):
    #     if page == 1:
    #         response = requests.get(urls_kobiety, headers=header, proxies=proxies)
    #         if response.status_code == 200:
    #             data = response.json()
    #             with open(f"c:\\adidas_pl\\html_data\\kobiety-buty\\0_{page}.json", "w", encoding='utf-8') as f:
    #                 json.dump(data, f, indent=4, ensure_ascii=False)
    #         time.sleep(1)
    #     if page > 1:
    #         counter_kobiety += 48
    #         url_kobiety_api = f'https://www.adidas.pl/api/plp/content-engine?query=kobiety-buty&start={counter_kobiety}'
    #         response = requests.get(url_kobiety_api, headers=header, proxies=proxies)
    #         if response.status_code == 200:
    #             data_1 = response.json()
    #             with open(f"c:\\adidas_pl\\html_data\\kobiety-buty\\0_{page}.json", "w", encoding='utf-8') as f:
    #                 json.dump(data_1, f, indent=4, ensure_ascii=False)
    #
    #         time.sleep(1)
    #     print(f"kobiety {counter_kobiety} из {totalResources_kobiety * 48}")
    # print(f"Собрал kobiety")
    #
    # """chlopcy-buty"""
    # urls_chlopcy_buty_api = "https://www.adidas.pl/api/plp/content-engine?query=chlopcy-buty"
    # resp = requests.get(urls_chlopcy_buty_api, headers=header, proxies=proxies)  # , proxies=proxies
    # json_data = resp.json()
    # totalResources_chlopcy_buty = json_data['raw']['itemList']['count'] // 48
    # counter_chlopcy_buty = 0
    # for page in range(1, totalResources_chlopcy_buty + 2):
    #     if page == 1:
    #         response = requests.get(urls_chlopcy_buty_api, headers=header, proxies=proxies)
    #         if response.status_code == 200:
    #             data = response.json()
    #             with open(f"c:\\adidas_pl\\html_data\\chlopcy-buty\\0_{page}.json", "w", encoding='utf-8') as f:
    #                 json.dump(data, f, indent=4, ensure_ascii=False)
    #         time.sleep(1)
    #     if page > 1:
    #         counter_chlopcy_buty += 48
    #         urls_chlopcy_buty = f'{urls_chlopcy_buty_api}&start={counter_chlopcy_buty}'
    #         response = requests.get(urls_chlopcy_buty, headers=header, proxies=proxies)
    #         if response.status_code == 200:
    #             data_1 = response.json()
    #             with open(f"c:\\adidas_pl\\html_data\\chlopcy-buty\\0_{page}.json", "w", encoding='utf-8') as f:
    #                 json.dump(data_1, f, indent=4, ensure_ascii=False)
    #
    #         time.sleep(1)
    #     print(f"chlopcy-buty {counter_chlopcy_buty} из {totalResources_chlopcy_buty * 48}")
    # print(f"Собрал chlopcy-buty")
    #
    # """dziewczynki-buty"""
    # urls_dziewczynki_buty_api = "https://www.adidas.pl/api/plp/content-engine?query=dziewczynki-buty"
    # resp = requests.get(urls_dziewczynki_buty_api, headers=header, proxies=proxies)  # , proxies=proxies
    # json_data = resp.json()
    # totalResources_dziewczynki_buty = json_data['raw']['itemList']['count'] // 48
    # counter_dziewczynki_buty = 0
    # for page in range(1, totalResources_dziewczynki_buty + 2):
    #     if page == 1:
    #         response = requests.get(urls_dziewczynki_buty_api, headers=header, proxies=proxies)
    #         if response.status_code == 200:
    #             data = response.json()
    #             with open(f"c:\\adidas_pl\\html_data\\dziewczynki-buty\\0_{page}.json", "w", encoding='utf-8') as f:
    #                 json.dump(data, f, indent=4, ensure_ascii=False)
    #         time.sleep(1)
    #     if page > 1:
    #         counter_dziewczynki_buty += 48
    #         urls_dziewczynki_buty = f'{urls_dziewczynki_buty_api}&start={counter_dziewczynki_buty}'
    #         response = requests.get(urls_dziewczynki_buty, headers=header, proxies=proxies)
    #         if response.status_code == 200:
    #             data_1 = response.json()
    #             with open(f"c:\\adidas_pl\\html_data\\dziewczynki-buty\\0_{page}.json", "w", encoding='utf-8') as f:
    #                 json.dump(data_1, f, indent=4, ensure_ascii=False)
    #
    #         time.sleep(1)
    #     print(f"dziewczynki_buty {counter_dziewczynki_buty} из {totalResources_dziewczynki_buty * 48}")
    # print(f"Собрал dziewczynki_buty")
    #

"""Собираем все ссылки на товары"""


def parsing_url_json():
    folders = [r"c:\adidas_pl\json_data\mezczyzni-buty\*.json",
               r"c:\adidas_pl\json_data\dziewczynki-buty\*.json",
               r"c:\adidas_pl\json_data\kobiety-buty\*.json",
               r"c:\adidas_pl\json_data\chlopcy-buty\*.json"
               ]

    for folder in folders:
        urls = []
        files_json = glob.glob(folder)
        group = files_json[0].split("\\")[-2]
        for item in files_json:

            with open(item, encoding='utf-8') as f:
                data = json.load(f)
                all_products = data['raw']['itemList']['items']
                coun = 0
                for url in all_products:
                    coun += 1
                    color_variations = url['colorVariations']
                    link = url['link']
                    if color_variations is None:
                        urls.append('https://www.adidas.pl' + link)
                    elif len(color_variations) > 2:
                        new_link = link.replace(color_variations[0], color_variations[1])
                        url['link'] = new_link
                        urls.append('https://www.adidas.pl' + new_link)
                    elif len(color_variations) == 2:
                        old_link = "/".join(link.split("/")[:2]) + "/"
                        link_01 = old_link + color_variations[0] + '.html'
                        link_02 = old_link + color_variations[1] + '.html'
                        urls.append('https://www.adidas.pl' + link_01)
                        urls.append('https://www.adidas.pl' + link_02)
                    else:
                        urls.append('https://www.reebok.pl' + link)
        with open(f'c:\\adidas_pl\\csv_url\\{group}\\url.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
            writer.writerow(urls)


def drop_duplicates():
    all_csv = ['c:\\adidas_pl\\csv_url\\chlopcy-buty\\url.csv',
               'c:\\adidas_pl\\csv_url\\dziewczynki-buty\\url.csv',
               'c:\\adidas_pl\\csv_url\\kobiety-buty\\url.csv', 'c:\\adidas_pl\\csv_url\\mezczyzni-buty\\url.csv']
    for f in all_csv:
        parts = f.split("\\")  # разбиваем строку на части, используя обратную косую черту как разделитель
        value = parts[-2]
        df = pd.read_csv(f)

        # удалить дубликаты строк и сохранить уникальные строки в новом DataFrame
        df_unique = df.drop_duplicates()

        # сохранить уникальные строки в CSV-файл
        df_unique.to_csv(f'c:\\adidas_pl\\csv_url\\{value}\\url.csv', index=False)
        print(f"У {value} осталось {len(df_unique)} уникальных строк.")
    # print("Дубликты удалили, переходим к обработке main_asio")


"""Собираем все ссылки на товары"""


def parsin_contact_html():
    today = datetime.today()
    date_str = today.strftime('%d/%m')
    folders_json = [r"c:\adidas_pl\html_product\chlopcy-buty",
                    r"c:\adidas_pl\html_product\dziewczynki-buty",
                    r"c:\adidas_pl\html_product\kobiety-buty",
                    r"c:\adidas_pl\html_product\mezczyzni-buty"
                    ]
    url_myfin_by = "https://myfin.by/currency/minsk"
    response = requests.get(url_myfin_by, headers=header, proxies=proxies)
    root = html.fromstring(response.text)
    value = root.xpath('//div[@class="c-best-rates"]//table//tbody//tr[4]//td[4]/text()')
    """Курс Беларуских"""
    bel = (float(value[0])) / 10
    for file in folders_json:  # Убарть срез!
        group = file.split('\\')[3]
        with open(f"c:\\adidas_pl\\csv_data\\{group}.csv", "w",
                  errors='ignore', encoding="utf-8") as file_csv:
            writer = csv.writer(file_csv, delimiter=",", lineterminator="\r")
            writer.writerow(
                (
                    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags', 'Published',
                    'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name',
                    'Option3 Value',
                    'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
                    'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                    'Variant Compare At Price',
                    'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src',
                    'Image Position',
                    'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
                    'Google Shopping / Google Product Category', 'Google Shopping / Gender',
                    'Google Shopping / Age Group',
                    'Google Shopping / MPN', 'Google Shopping / AdWords Grouping',
                    'Google Shopping / AdWords Labels',
                    'Google Shopping / Condition', 'Google Shopping / Custom Product',
                    'Google Shopping / Custom Label 0',
                    'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2',
                    'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4', 'Variant Image',
                    'Variant Weight Unit', 'Variant Tax Code', 'Cost per item', 'Included / Belarus',
                    'Included / International', 'Price / International', 'Compare At Price / International',
                    'Status'
                )
            )

        files_json = glob.glob(file)
        for item in files_json[:1]:  # Убарть срез!
            for dirpath, dirnames, filenames in os.walk(item):
                for dirname in dirnames:
                    json_pattern = re.compile(r'{.*}')
                    subdir_path = os.path.join(dirpath, dirname)
                    os.chdir(subdir_path)
                    # print(subdir_path)
                    if os.path.exists('data.json'):
                        with open('data.json', 'r', encoding='utf-8') as file_data:
                            data_json = json.load(file_data)
                        # print(json.dumps(data, indent=4, ensure_ascii=False))
                    json_match = json_pattern.search(data_json)
                    data_string = json_match.group()
                    data_json = json.loads(data_string)
                    # with open(f'c:\\adidas_pl\\Adidas.json', 'w') as f:
                    #     json.dump(data_json, f)
                    # exit()
                    if os.path.exists('size.json'):
                        with open('size.json', 'r', encoding='utf-8') as file_size:
                            size_json = json.load(file_size)
                        # print(json.dumps(size, indent=4, ensure_ascii=False))

                    json_match = json_pattern.search(size_json)

                    if json_match is not None:
                        size_string = json_match.group()
                    else:
                        continue
                    # size_string = json_match.group()
                    size_json = json.loads(size_string)
                    counter = 0
                    sizes = []
                    if 'variation_list' in size_json and size_json['variation_list'] is not None:
                        for obj in size_json['variation_list']:
                            if obj['availability_status'] == 'NOT_AVAILABLE' or obj['availability_status'] == 'PREVIEW':
                                continue
                            if 'size' in obj:
                                size_str = obj['size']
                                if ' ' in size_str:
                                    whole_number, fraction = size_str.split(' ')
                                    if fraction == '1/2':
                                        fraction = '.5'
                                    elif fraction == '2/3':
                                        fraction = '.6'
                                    elif fraction == '1/3':
                                        fraction = '.3'
                                    size_decimal = round(float(whole_number) + float(fraction), 1)
                                else:
                                    size_decimal = round(float(size_str), 1)
                                sizes.append(size_decimal)
                    Handle = f"{data_json['id']}_{data_json['model_number']}"
                    Title = "Adidas " + data_json['meta_data']['keywords']
                    id_product = data_json['id']


                    category_product_old = data_json['breadcrumb_list'][0]['text']
                    with open('c:\\adidas_pl\\dict.csv', newline='', encoding="utf-8") as csvfile:
                        reader = csv.reader(csvfile, delimiter=';')
                        for row in reader:
                            # print(row[0])
                            if row[0] == category_product_old:
                                category_product = row[1]
                                break
                            else:
                                category_product = category_product_old
                    Vendor = "Adidas"
                    picture_dicts = data_json['view_list']
                    alls_photo = []
                    for i, picture_dict in enumerate(picture_dicts):
                        index = i + 1
                        photo_link = picture_dict["image_url"].replace(
                            "https://assets.adidas.com/images/w_600,f_auto,q_auto",
                            "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto")
                        photo_link = photo_link.replace(f'/{index}.', f'/1.')
                        alls_photo.append(photo_link)
                    pfoto_site = []
                    coun = 0
                    color = ''
                    try:
                        color_old = data_json['attribute_list']['color'].split('/')[0].strip()
                        with open(r'c:\\adidas_pl\\colors.csv', newline='', encoding="utf-8") as csvfile:
                            reader = csv.reader(csvfile, delimiter=';')
                            for row in reader:
                                if row[0] == color_old:
                                    color = row[1]
                                    break
                                else:
                                    color = color_old
                    except:
                        color = None

                    img_groups = {
                        "chlopcy-buty": "img_chlopcy-buty",
                        "dziewczynki-buty": "img_dziewczynki-buty",
                        "kobiety-buty": "img_kobiety-buty",
                        "mezczyzni-buty": "img_mezczyzni-buty"
                    }

                    for coun, img in enumerate(alls_photo, 1):
                        img_group_folder = img_groups.get(group)
                        if img_group_folder:
                            pfoto_site.append(
                                f"https://loketsneakers.s3.eu-central-1.amazonaws.com/img_kobiety-buty/{img_group_folder}/{img_group_folder}/{id_product}_{coun}.webp")
                            file_path = f"c:\\adidas_pl\\data_img\\{img_group_folder}\\{id_product}_{coun}.webp"
                            new_file_path = f"c:\\adidas_pl\\csv_data\\{img_group_folder}\\{id_product}_{coun}.webp"
                            if not os.path.exists(file_path):
                                img_data = requests.get(img, headers=header, proxies=proxies)
                                with open(new_file_path, 'wb') as file_img:
                                    file_img.write(img_data.content)
                    #
                    # for img in alls_photo:
                    #     coun += 1
                    #     pfoto_site.append(
                    #         f"https://cdn.shopify.com/s/files/1/0667/5824/6699/files/{id_product}_{coun}.webp")
                    #
                    #     file_path = f"c:\\adidas_pl\\data_img\\img_{group}\\{id_product}_{coun}.webp"
                    #     new_file_path = f"c:\\adidas_pl\\csv_data\\img_{group}\\{id_product}_{coun}.webp"
                    #     if not os.path.exists(file_path):
                    #         img_data = requests.get(img, headers=header, proxies=proxies)
                    #         with open(new_file_path, 'wb') as file_img:
                    #             file_img.write(img_data.content)

                    try:
                        sell_price = data_json['pricing_information']['sale_price']
                    except:
                        sell_price = 0
                    base_price = data_json['pricing_information']['standard_price']
                    """Формирование цены с курсом"""
                    Variant_Price = 0
                    Variant_Compare_At_Price = 0
                    if sell_price > 0:
                        Variant_Price = round(((float(sell_price) + 60.0) * 1.1) * bel, 1)  # два знака после запятой
                        Variant_Price = str(Variant_Price).replace('.', ',')
                        Variant_Compare_At_Price = round(((float(base_price) + 60.0) * 1.1) * bel,
                                                         1)  # два знака после запятой
                        Variant_Compare_At_Price = str(Variant_Compare_At_Price).replace('.', ',')
                    elif sell_price == 0:
                        Variant_Price = round(((float(base_price) + 60.0) * 1.1) * bel, 1)  # два знака после запятой
                        Variant_Price = str(Variant_Price).replace('.', ',')
                        Variant_Compare_At_Price = ""
                    index_photo = 1  # Initialize photo index

                    for i, size in enumerate(sizes):
                        if i < len(pfoto_site):
                            photo = pfoto_site[i]
                            index_photo_str = str(index_photo)  # convert index to string
                            index_photo += 1  # Increment photo index for each iteration
                        else:
                            photo = ""
                            index_photo_str = ""  # leave index_photo_str empty
                        data = [Handle, Title, "", Vendor, 'Apparel & Accessories > Shoes', category_product,
                                f'{color}, {date_str}', 'TRUE',
                                'Размер', size, "", "", "", "", "", "", "", "999", "continue", "manual", Variant_Price,
                                Variant_Compare_At_Price, "TRUE", "TRUE", "", photo, index_photo_str, "", "", "", "",
                                "", "", "",
                                "",
                                "", "", "", "", "", "", "", "", "", "", "kg", "", "", "TRUE", "TRUE", "", "", "Active"]
                        with open(f"c:\\adidas_pl\\csv_data\\{group}.csv", "a",
                                  errors='ignore', encoding="utf-8") as file:
                            writer = csv.writer(file, delimiter=",", lineterminator="\r")
                            writer.writerow((data))

                    # If there are more photos than sizes, fill in the remaining rows with empty data except for photo and index
                    if len(pfoto_site) > len(sizes):
                        alls_photo = []
                        for picture_dict in picture_dicts:
                            photo_url = picture_dict["image_url"].replace(
                                "https://assets.adidas.com/images/w_600,f_auto,q_auto",
                                "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto")
                            alls_photo.append(photo_url)
                        for j in range(len(sizes), len(pfoto_site)):
                            photo = pfoto_site[j]
                            index_photo_str = str(index_photo)  # convert index to string
                            data = [Handle, Title, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                    '', '',
                                    '', '', '', '', '', photo, index_photo_str, '', '', '', '', '', '', '', '', '', '',
                                    '', '', '', '', '', '', '', '',
                                    '', '', '', '', '', '', '', ""]
                            with open(f"c:\\adidas_pl\\csv_data\\{group}.csv", "a",
                                      errors='ignore', encoding="utf-8") as file:
                                writer = csv.writer(file, delimiter=",", lineterminator="\r")
                                writer.writerow((data))
                            index_photo += 1
                    os.chdir('..')


def move_img():
    folders = {
        r'c:\adidas_pl\csv_data\img_chlopcy-buty': r'c:\adidas_pl\data_img\img_chlopcy-buty',
        r'c:\adidas_pl\csv_data\img_dziewczynki-buty': r'c:\adidas_pl\data_img\img_dziewczynki-buty',
        r'c:\adidas_pl\csv_data\img_kobiety-buty': r'c:\adidas_pl\data_img\img_kobiety-buty',
        r'c:\adidas_pl\csv_data\img_mezczyzni-buty': r'c:\adidas_pl\data_img\img_mezczyzni-buty'
    }

    for src, dest in folders.items():
        for root, dirs, files in os.walk(src):
            dest_root = root.replace(src, dest)
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_root, file)
                shutil.move(src_path, dest_path)


def del_files_html_product():
    folders_del = [r"c:\adidas_pl\html_product\chlopcy-buty",
                   r"c:\adidas_pl\html_product\dziewczynki-buty",
                   r"c:\adidas_pl\html_product\kobiety-buty",
                   r"c:\adidas_pl\html_product\mezczyzni-buty"
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
    """Перемещаем изображение в папку с БД"""
    move_img()
    print('Переместили фото')
    """Удаляем старые файлы HTML"""
    del_files_html_product()
    print('Удалили старые данные')
    save_html_data()
    # html_to_json ()
    # #### save_json_product()
    # parsing_url_json()
    # drop_duplicates()
    # asio_main()
    # parsin_contact_html()
