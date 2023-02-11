import zipfile
import pickle
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
from selenium.webdriver.common.keys import Keys
import csv
import time
import glob


def parsing_product():
    datas = []
    targetPattern = r"C:\scrap_tutorial-master\webstaurantstore\data\*.html"
    files_html = glob.glob(targetPattern)
    datas = []
    for item in files_html:
        with open(item, encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        script = soup.find_all('script', type="application/json")[1].text.strip()[4:-3]
        data_json = json.loads(script)
        try:
            if data_json['productTemplates']:
                availability = data_json['productTemplates'][0]['isInStock']
                if availability:
                    av = 1
                else:
                    av = 0
                product_name = data_json['productTemplates'][0]['header']
                product_sky = data_json['productTemplates'][0]['upc']
                product_url = data_json['layoutConfiguration']['openGraphMeta']['url']
                product_price = data_json['layoutConfiguration']['openGraphMeta']['productPrice']['amount']
                product_price_tapa = data_json['productTemplates'][0]['unitOfMeasure']
                price_adn_tara = f"{product_price}/{product_price_tapa}"
                try:
                    product_price_min = data_json['productTemplates'][0]['price']['minimumAdvertisedPriceProperties'][
                        'price']
                    price_adn_tara_min = f"{product_price_min}/{product_price_tapa}"
                except:
                    product_price_min = 0
                    price_adn_tara_min = 0

                datas.append(
                    [product_url, product_name, product_sky, price_adn_tara, price_adn_tara_min, av]
                )
            else:
                continue
        except:
            continue
    write_csv(datas)


def write_csv(datas):
    # Создаем файл с заголовками
    with open(f"C:\\scrap_tutorial-master\\webstaurantstore\\test.csv", "w", errors='ignore') as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\r")
        writer.writerow(
            (
                'product_url',
                'product_name',
                'product_sky',
                'product_price',
                'price_adn_tara_min',
                'availability'
            )
        )
        # Дописываем данные из списка data в файл
        writer.writerows(
            datas
        )


if __name__ == '__main__':
    # # Собираем все ссылки на категории товаров
    # url = "https://dubai.dubizzle.com/motors/used-cars/toyota/?kilometers__lte=100000&ads_posted=1673567999"
    # save_link_all_product(url)
    # Парсим все товары из файлов с
    parsing_product()
