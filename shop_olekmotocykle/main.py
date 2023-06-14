import random
from typing import Optional
import csv
import time
import os
from proxi import proxies
import asyncio
import aiofiles
import aiohttp
# import main_asio_photo


import pandas as pd
import glob
import json
import html
import re

import requests
from bs4 import BeautifulSoup
import csv
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}


def parsing_url_category_in_html():
    url = "https://shop.olekmotocykle.com/"
    response = requests.get(url, headers=header)  # , proxies=proxies
    url_ = 'https://shop.olekmotocykle.com/'
    category_product = []
    if response.content:
        soup = BeautifulSoup(response.content, 'lxml')

        for link in soup.select('.category-links-ui a'):
            href = link.get('href')
            if 'produkty/' in href:
                category_product.append(url_ + href)

        with open('category_product.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=";", lineterminator="\r")
            for item in category_product:
                writer.writerow([item])
    else:
        print("No content received")


def parsing_product():

    targetPattern = f"c:\\Data_olekmotocykle\\*.html"
    files_html = glob.glob(targetPattern)
    data = []
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id_product', 'name', 'brandName', 'gtin', 'brutto_price', 'netto_price'])
        for item in files_html:
            print(item)
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'html.parser')
            script_tag = soup.find('script', {'id': 'datablock1'})
            json_content = script_tag.contents[0].strip().replace('},\n}\n}', '}\n}\n}')
            try:
                data = json.loads(json_content)
                id_product = soup.find('div', {'class': 'product-code-ui product-code-lq'}).text
                name = data['itemOffered']['productName'][0]['@value']
                brandName = data['itemOffered']['brand']['brandName'][0]['@value']
                gtin = data['itemOffered']['gtin']
                brutto_price = soup.find('div', {'class': 'brutto-price-ui'}).text.strip().replace(" PLN", "").replace("\nbrutto", "")
                netto_price = soup.find('div', {'class': 'netto-price-ui'}).text.strip().replace(" PLN", "").replace("\nnetto", "")
                writer.writerow([id_product, name, brandName, gtin, brutto_price, netto_price])
            except:
                continue
            div = soup.find_all("div", {"class": "lazyslider-container-lq"})[0]
            imgs = div.find_all("img", {"class": "open-gallery-lq"})

            urls_photo = []
            for img in imgs:
                urls_photo.append('https://' + img["data-src"].replace("//", ""))

            coun = 0
            file_path_1 = f'c:\\Data_olekmotocykle\\img\\{id_product.replace("/", "_")}.jpg'
            file_path_2 = f'c:\\Data_olekmotocykle\\img\\{id_product.replace("/", "_")}_{coun}.jpg'
            for u in urls_photo:
                """Настройка прокси серверов случайных"""
                proxy = random.choice(proxies)
                proxy_host = proxy[0]
                proxy_port = proxy[1]
                proxy_user = proxy[2]
                proxy_pass = proxy[3]

                proxi = {
                    'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
                    'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
                }
                coun += 1
                if len(urls_photo) == 1:
                    if not os.path.exists(file_path_1):
                        try:
                            img_data = requests.get(u, headers=header, proxies=proxi)
                            with open(file_path_1, 'wb') as file_img:
                                file_img.write(img_data.content)
                        except:
                            print(f"Ошибка при выполнении запроса для URL: {u}")
                            continue
                elif len(urls_photo) > 1:
                    if not os.path.exists(file_path_2):
                        img_data = requests.get(u, headers=header, proxies=proxi)
                        with open(file_path_2, 'wb') as file_img:
                            file_img.write(img_data.content)

def urls_photo():
    targetPattern = f"c:\\Data_olekmotocykle\\*.html"
    files_html = glob.glob(targetPattern)

    result_dict = {}
    for item in files_html:
        with open(item, encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, 'html.parser')
        div = soup.find_all("div", {"class": "lazyslider-container-lq"})[0]
        id_product = soup.find('div', {'class': 'product-code-ui product-code-lq'}).text.strip()
        imgs = div.find_all("img", {"class": "open-gallery-lq"})

        item_dict = {}
        for i, img in enumerate(imgs):
            url_photo = 'https://' + img["data-src"].replace("//", "")
            item_dict[f"url_{i + 1}"] = url_photo
            item_dict[f"id_{i + 1}"] = id_product

        result_dict[item.replace("c:\\Data_olekmotocykle\\", "")] = item_dict

    # записываем результат в файл JSON
    with open("result.json", "w") as json_file:
        json.dump(result_dict, json_file)

def run_main_asio_photo():
    import main_asio_photo
    asyncio.run(main_asio_photo.main())
def main_download_url():
    import main_url_asio
    asyncio.run(main_url_asio.main())

def main_asio_html():
    import main_asio
    asyncio.run(main_asio.main_asio())


if __name__ == '__main__':
    print("Собираем категории товаров")
    parsing_url_category_in_html()
    print("Скачиваем все ссылки")
    main_download_url()
    print("Скачиваем все HTML страницы")
    main_asio_html()
    print("Получаем все url на фото")
    urls_photo()
    print("Скачиваем все фото")
    run_main_asio_photo()
    print("Получаем все данные")
    parsing_product()
    print("Все получилось")