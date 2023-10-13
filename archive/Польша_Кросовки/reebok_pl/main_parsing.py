import shutil
import glob
import cloudscraper
import urllib.parse
import pandas as pd
import zipfile
import os
import shutil
from proxi import proxies
import tempfile
import shutil
from lxml import html
from main_asio import *
import re
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from cf_clearance import sync_cf_retry, sync_stealth
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
import boto3
# Установка учетных данных AWS
ACCESS_KEY = 'AKIAQWBRT2HZZFWLS5EJ'
SECRET_KEY = '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'

# Создание клиента S3
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
def get_cookies_sf():
    url_pl = 'https://www.reebok.eu/en-pl'
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
def parsin_contact_html():

    today = datetime.today()
    date_str = today.strftime('%d/%m')
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    folders_html = [r"c:\reebok_pl\html_product\men-shoes\*.html",
               r"c:\reebok_pl\html_product\women-shoes\*.html",
               r"c:\reebok_pl\html_product\kids-youth-9-14\*.html",
               r"c:\reebok_pl\html_product\kids-kids-5-8-years-kids-shoes\*.html",
               r"c:\reebok_pl\html_product\kids-baby-0-4-years-baby-shoes\*.html"
               ]

    # """Курс Беларуских"""
    proxy = random.choice(proxies)
    proxy_host = proxy[0]
    proxy_port = proxy[1]
    proxy_user = proxy[2]
    proxy_pass = proxy[3]

    proxi = {
        'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
        'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
    }
    url_myfin_by = "https://myfin.by/bank/kursy_valjut_nbrb/pln"
    response = requests.get(url_myfin_by, headers=header, proxies=proxi)
    if response.status_code == 200:
        root = html.fromstring(response.text)
        value = root.xpath('//div[@class="h1"][1]/text()')[0]
        bel = float(value) / 10
    else:
        bel = 0.6
    # print(bel)
    for file in folders_html: # Убарть срез выбор папки!
        headers, cookies = get_cookies_sf()
        group = file.split('\\')[3]
        # print(group)
        with open(f"c:\\reebok_pl\\csv_data\\{group}.csv", "w",
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

        for item in files_json: # Убарть срез выбор файла!
            with open(item, 'r', encoding='utf-8') as file:
                html_content = file.read()
            counter = 0
            sizes = []
            soup = BeautifulSoup(html_content, 'lxml')

            # try:
            #     table_size = soup.find('div', class_='css-4sx26k')
            # except:
            #     print('-------------------')
            #     pass

            try:
                div_elements = soup.find_all('div', class_='css-19xoysq')
            except:
                continue
            for div in div_elements:
                disabled_attr = div.find('input', disabled=True)
                if disabled_attr is not None:
                    continue  # Пропускаем элемент, если атрибут "disabled" присутствует
                label = div.find('label', class_='css-zcfdzo')

                if label is not None:
                    extracted_value = label.text.strip()
                    sizes.append(extracted_value)
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text_1 = script[1].text.replace("\\'n\\'", ' ')
            data_1 = json.loads(json_text_1)
            Handle = data_1['productID']
            Title = "Reebok " + soup.find('h2', class_="css-1wx06p0").text
            #
            id_product = data_1['productID']
            category_product_old = soup.find('p', class_="css-18y5zfz").text
            if category_product_old == 'Classics':
                category_product = 'Lifestyle/Повседневные'
            else:
                category_product = 'Спорт/Зал'
            Vendor = "Reebok"
            picture_dicts = data_1['image']
            alls_photo = []
            for i, photo_url in enumerate(picture_dicts):
                index = i + 1
                photo_link = photo_url.replace("_200.jpg", "_1000.jpg")
                alls_photo.append(photo_link)
            color_old = data_1['color']
            color = ''
            try:
                color_old = data_1['color'].split('/')[0].strip()
                with open(r'c:\\reebok_pl\\colors.csv', newline='', encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    for row in reader:
                        if row[0] == color_old:
                            color = row[1]
                            break
                        else:
                            color = color_old
            except:
                color = None

            coun = 0
            pfoto_site = []
            # for img in alls_photo:
            #     coun += 1
            img_groups = {
                "kids-baby-0-4-years-baby-shoes": "img_kids-baby-0-4-years-baby-shoes",
                "kids-kids-5-8-years-kids-shoes": "img_kids-kids-5-8-years-kids-shoes",
                "kids-youth-9-14t": "img_kids-youth-9-14",
                "men-shoes": "img_men-shoes",
                "women-shoes": "img_women-shoes"
            }

            bucket_name = 'loketsneakers'

            for coun, img in enumerate(alls_photo, 1):
                # proxy = random.choice(proxies)
                # proxy_host = proxy[0]
                # proxy_port = proxy[1]
                # proxy_user = proxy[2]
                # proxy_pass = proxy[3]
                #
                # proxi = {
                #     'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
                #     'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
                # }
                img_group_folder = img_groups.get(group)
                if img_group_folder:
                    pfoto_site.append(
                        f"https://loketsneakers.s3.eu-central-1.amazonaws.com/reebok/{img_group_folder}/{id_product}_{coun}.webp")
                    file_path = f"reebok/{img_group_folder}/{id_product}_{coun}.webp"

                    # Проверка наличия файла в S3 бакете
                    try:
                        s3.head_object(Bucket=bucket_name, Key=file_path)
                        # print(f"Файл {file_path} уже существует в S3 бакете. Пропуск загрузки.")
                    except:
                        # Загрузка файла из удаленного источника
                        print(f"Файл {file_path} отсутствует в S3 бакете. Загрузка из удаленного источника.")
                        img_data = requests.get(img, cookies=cookies, headers=headers) #, proxies=proxies

                        # Загрузка данных изображения в S3 бакет
                        s3.put_object(Body=img_data.content, Bucket=bucket_name, Key=file_path)
                        print(f"Файл {file_path} успешно загружен в S3 бакет.")

            table_price = soup.find('section', class_="css-a5s3hw")
            try:
                sell_price = int(table_price.find('span', attrs={'data-test': 'product-salePrice'}).text.replace(" z\\xc5\\x82", ""))
            except:
                sell_price = 0
            try:
                base_price = int(table_price.find('span', attrs={'data-test': 'product-price'}).text.replace(" z\\xc5\\x82", ""))
            except:
                base_price = 0
            if not base_price:
                base_price = 0
            """Формирование цены с курсом"""
            Variant_Price = 0
            Variant_Compare_At_Price = 0
            if sell_price > 0:
                Variant_Price = round(((float(sell_price) + 60.0) * 1.15) * bel, 1)  # два знака после запятой
                Variant_Price = str(Variant_Price).replace('.', ',')
                Variant_Compare_At_Price = round(((float(base_price) + 60.0) * 1.25) * bel,
                                                 1)  # два знака после запятой
                Variant_Compare_At_Price = str(Variant_Compare_At_Price).replace('.', ',')
            elif sell_price == 0:
                Variant_Price = round(((float(base_price) + 60.0) * 1.15) * bel, 1)  # два знака после запятой
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
                data_dict = [Handle, Title, "", Vendor, 'Apparel & Accessories > Shoes', category_product,
                        f'{color}, {date_str}', 'TRUE',
                        'Размер', size, "", "", "", "", "", "", "", "999", "continue", "manual", Variant_Price,
                        Variant_Compare_At_Price, "TRUE", "TRUE", "", photo, index_photo_str, "", "", "", "",
                        "", "", "",
                        "",
                        "", "", "", "", "", "", "", "", "", "", "kg", "", "", "TRUE", "TRUE", "", "", "Active"]
                with open(f"c:\\reebok_pl\\csv_data\\{group}.csv", "a",
                          errors='ignore', encoding="utf-8") as file:
                    writer = csv.writer(file, delimiter=",", lineterminator="\r")
                    writer.writerow((data_dict))

            # If there are more photos than sizes, fill in the remaining rows with empty data except for photo and index
            if len(pfoto_site) > len(sizes):
                alls_photo = []
                for picture_dict in picture_dicts:
                    # print(picture_dict)
                    photo_url =picture_dict.replace("_200.jpg", "_1000.jpg")
                    alls_photo.append(photo_url)
                for j in range(len(sizes), len(pfoto_site)):
                    photo = pfoto_site[j]
                    index_photo_str = str(index_photo)  # convert index to string
                    data_d = [Handle, Title, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '',
                            '', '', '', '', '', photo, index_photo_str, '', '', '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '', '', ""]
                    with open(f"c:\\reebok_pl\\csv_data\\{group}.csv", "a",
                              errors='ignore', encoding="utf-8") as file:
                        writer = csv.writer(file, delimiter=",", lineterminator="\r")
                        writer.writerow((data_d))
                    index_photo += 1




if __name__ == '__main__':
    parsin_contact_html()
    print("Все получили")

