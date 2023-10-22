import csv
import datetime
import glob
import os
import re
import time
from datetime import datetime
from io import StringIO

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

current_directory = os.getcwd()
temp_directory = 'temp'
# Создайте полный путь к папке temp
temp_path = os.path.join(current_directory, temp_directory)
list_path = os.path.join(temp_path, 'list')
product_path = os.path.join(temp_path, 'product')
img_path = os.path.join(temp_path, 'img')
cookies = {
    'PHPSESSID': 'y46XRseJa01FdwxsfBTBxIs6IFpyXhFc',
    '_ym_uid': '16977015098771791',
    '_ym_d': '1697701509',
    '__utma': '197302824.1165919871.1697701509.1697701509.1697701509.1',
    '__utmc': '197302824',
    '__utmz': '197302824.1697701509.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmt': '1',
    '__utmb': '197302824.1.10.1697701509',
    '_ym_isad': '2',
    'BX_USER_ID': '3304339f1fce1f8b8863297ab0e125ea',
    '_ym_visorc': 'w',
}

headers = {
    'authority': 'voltag.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru',
    'cache-control': 'max-age=0',
    # 'cookie': 'PHPSESSID=y46XRseJa01FdwxsfBTBxIs6IFpyXhFc; _ym_uid=16977015098771791; _ym_d=1697701509; __utma=197302824.1165919871.1697701509.1697701509.1697701509.1; __utmc=197302824; __utmz=197302824.1697701509.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=197302824.1.10.1697701509; _ym_isad=2; BX_USER_ID=3304339f1fce1f8b8863297ab0e125ea; _ym_visorc=w',
    'dnt': '1',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}


def delete_old_data():
    # Убедитесь, что папки существуют или создайте их
    for folder in [temp_path, list_path, product_path]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Удалите файлы из папок list и product
    for folder in [list_path, product_path]:
        files = glob.glob(os.path.join(folder, '*'))
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
        # print(f'Очистил папку {os.path.basename(folder)}')


names = 'f2-166'


def get_request():
    urls = [
        # 'https://voltag.ru/catalog/list/f2-39/',
        #     'https://voltag.ru/catalog/list/f2-547/',
        #     'https://voltag.ru/catalog/list/f2-153/',
        #     'https://voltag.ru/catalog/list/f2-159/',
        #     'https://voltag.ru/catalog/list/f2-158/',
        #     'https://voltag.ru/catalog/list/f2-179/',
        #     'https://voltag.ru/catalog/list/f2-506/',
        # 'https://voltag.ru/catalog/list/f2-167/',
        # 'https://voltag.ru/catalog/list/f2-165/',
        # 'https://voltag.ru/catalog/list/f2-166/',
        # 'https://voltag.ru/catalog/list/f2-41/',
        # 'https://voltag.ru/catalog/list/f2-280/',
        # 'https://voltag.ru/catalog/list/f2-292/p-7/',
        # 'https://voltag.ru/catalog/list/f2-428/p-7/',
        # 'https://voltag.ru/catalog/list/f2-267/',
        # 'https://voltag.ru/catalog/list/f2-359/',
        # 'https://voltag.ru/catalog/list/f2-396/',
        # 'https://voltag.ru/catalog/list/f2-339/p-7/',
        # 'https://voltag.ru/catalog/list/f2-350/',
        # 'https://voltag.ru/catalog/list/f2-225/',
        # 'https://voltag.ru/catalog/list/f2-318/',
        # 'https://voltag.ru/catalog/list/f2-119/'
        ]

    pages = 29
    coun = 1

    for i in range(1, pages):
        filename = os.path.join(product_path, f'0{coun}.html')
        coun += 1
        print(coun)
        if not os.path.exists(filename):
            if i == 1:
                response = requests.get(f'https://voltag.ru/catalog/list/{names}/', cookies=cookies, headers=headers)
                src = response.text
                with open(filename, "w", encoding='utf-8') as file:
                    file.write(src)
                time.sleep(5)
            if i > 1:
                response = requests.get(f'https://voltag.ru/catalog/list/{names}/p-{coun}/', cookies=cookies,
                                        headers=headers)
                src = response.text
                with open(filename, "w", encoding='utf-8') as file:
                    file.write(src)
                time.sleep(5)


def parsing():
    folder = os.path.join(product_path, '*.html')

    files_html = glob.glob(folder)
    heandler = ['catalog_item_title', 'catalog_item_subtitle', 'nz','tc',
                'hi' 'catalog_item_crosses',
                'catalog_item_application']

    with open(f'{names}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(heandler)
        for item in files_html:  # срез на файлы
            print(item)
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            table = soup.find('div', attrs={'class': 'catalog_list'})
            products = table.find_all('div', attrs={'class': 'catalog_item one_photo'})
            for p in products:  # срез на позиции в таблице
                imgs = []
                catalog_item_title = p.find('div', attrs={'class': 'catalog_item_title_wrap'}).find('h2').text
                catalog_item_subtitle = p.find('div', attrs={'class': 'catalog_item_subtitle'}).text
                """Извлечь весь текст"""
                catalog_item_params = p.find('div', attrs={'class': 'catalog_item_params'})
                data_dict = {}

                # Извлекаем все строки таблицы
                rows = soup.select("table tr")
                for row in rows:
                    key_col = row.select_one("td b")
                    value_col = row.select_one("td.info-width div, td.info-width span")

                    # Если оба значения существуют и имеют текст, сохраняем их в словаре
                    if key_col and value_col and key_col.text.strip() and value_col.text.strip():
                        key = key_col.text.strip()[:-1]  # убираем ':' из ключа
                        value = value_col.text.strip()
                        data_dict[key] = value

                # Присваиваем значения переменным
                nz = data_dict.get("nz", None)
                tc = data_dict.get("tc", None)
                print(nz, tc)


                catalog_item_crosses_text = p.find('div', attrs={'class': 'catalog_item_crosses'}).get_text(
                    separator=", ",
                    strip=True).replace(
                    '\t', '').replace(" ", "")
                catalog_item_crosses = re.sub(r'\s+', ' ', catalog_item_crosses_text).strip()
                catalog_item_application_text = p.find('div', attrs={'class': 'catalog_item_application'}).get_text()
                catalog_item_application = re.sub(r'\s+', ' ', catalog_item_application_text).strip()
                catalog_item_photo_div = p.find('div', attrs={'class': 'catalog_item_photo'})

                if catalog_item_photo_div:
                    a_tag = catalog_item_photo_div.find('a')
                    if a_tag:
                        catalog_item_photo = a_tag.get('href')
                        if catalog_item_photo:  # Проверка на случай, если атрибут href отсутствует
                            imgs.append(catalog_item_photo)

                catalog_item_photo_hidden_photos = p.find_all('div', attrs={'class': 'catalog_item_photo hidden_photo'})
                for j in catalog_item_photo_hidden_photos:
                    a_tag = j.find('a')
                    if a_tag:
                        img = a_tag.get('href')
                        if img:  # Проверка на случай, если атрибут href отсутствует
                            imgs.append(img)

                cointer = 0
                for url in imgs:
                    files_img = os.path.join(img_path, f'{catalog_item_title}_{cointer}.jpg')
                    if not os.path.exists(files_img):
                        img_data = requests.get(url, headers=headers, cookies=cookies)
                        with open(files_img, 'wb') as file_img:
                            file_img.write(img_data.content)

                        cointer += 1
                values = [catalog_item_title, catalog_item_subtitle, nz,tc, catalog_item_crosses,
                          catalog_item_application]
                writer.writerow(values)


if __name__ == '__main__':
    # delete_old_data()
    # extract_data_from_csv()
    # get_request()
    parsing()
