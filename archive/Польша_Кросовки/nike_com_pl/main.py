from googletrans import Translator
import glob
import asyncio
from main_asio import main
import pandas as pd
import zipfile
import os
import re
import json
from bs4 import BeautifulSoup
import csv
import shutil
import time
from lxml import html
import requests
import random
from datetime import datetime, timedelta

# Данные для прокси
PROXY_HOST = '141.145.205.4'
PROXY_PORT = 31281  # Без кавычек
PROXY_USER = 'proxy_alex'
PROXY_PASS = 'DbrnjhbZ88'

# Настройка для requests чтобы использовать прокси
# proxies = {'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}/'}
proxies = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

"""Сохраняем json всех страниц"""


def save_json_product():
    # proxies = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
    # header = {
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

    """mezczyzni"""
    urls_mezczyzni = "https://www.nike.com/pl/w/mezczyzni-buty-nik1zy7ok"
    resp = requests.get(urls_mezczyzni, headers=header, proxies=proxies)
    soup = BeautifulSoup(resp.text, 'lxml')
    script_json = soup.find('script', type="application/json")
    data_json = json.loads(script_json.string)
    totalResources_mezczyzni = data_json['props']['pageProps']['initialState']['Wall']['pageData'][
                                   'totalResources'] // 24
    counter_mezczyzni = 24
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\nike_com_pl\\html_data\\mezczyzni'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for page in range(1, totalResources_mezczyzni + 1):
        url_mezczyzni_api = f'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=D7E5438731B3C14E83AA7C911A8964F7&country=pl&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(PL)%26filter%3Dlanguage(pl)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c)%26anchor%3D{counter_mezczyzni}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=pl&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%93%20%7BhighestPrice%7D'
        counter_mezczyzni += 24
        response = requests.get(url_mezczyzni_api)
        if response.status_code == 200:
            data = response.json()
            with open(f"c:\\nike_com_pl\\html_data\\mezczyzni\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        time.sleep(1)
    print(f"Собрал mezczyzni")

    """kobiety"""
    urls_kobiety = "https://www.nike.com/pl/w/kobiety-buty-5e1x6zy7ok"
    resp = requests.get(urls_kobiety, headers=header, proxies=proxies)
    soup = BeautifulSoup(resp.text, 'lxml')
    script_json = soup.find('script', type="application/json")
    data_json = json.loads(script_json.string)
    totalResources_kobiety = data_json['props']['pageProps']['initialState']['Wall']['pageData'][
                                 'totalResources'] // 24
    counter_kobiety = 24

    """Очистка папки с старыми данными"""
    dir_path = f'c:\\nike_com_pl\\html_data\\kobiety'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    for page in range(1, totalResources_kobiety + 1):
        url_kobiety_api = f'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=D7E5438731B3C14E83AA7C911A8964F7&country=pl&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(PL)%26filter%3Dlanguage(pl)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C7baf216c-acc6-4452-9e07-39c2ca77ba32)%26anchor%3D{counter_kobiety}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=pl&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%93%20%7BhighestPrice%7D'
        counter_kobiety += 24
        response = requests.get(url_kobiety_api)
        if response.status_code == 200:
            data = response.json()
            with open(f"c:\\nike_com_pl\\html_data\\kobiety\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        time.sleep(1)
    print(f"Собрал kobiety")

    """kids"""
    urls_kids = "https://www.nike.com/pl/w/kids-buty-v4dhzy7ok"
    resp = requests.get(urls_kids, headers=header, proxies=proxies)
    soup = BeautifulSoup(resp.text, 'lxml')
    script_json = soup.find('script', type="application/json")
    data_json = json.loads(script_json.string)
    totalResources_kids = data_json['props']['pageProps']['initialState']['Wall']['pageData'][
                              'totalResources'] // 24
    counter_kids = 24
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\nike_com_pl\\html_data\\kids'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    for page in range(1, totalResources_kids + 1):
        url_kids_api = f'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=D7E5438731B3C14E83AA7C911A8964F7&country=pl&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(PL)%26filter%3Dlanguage(pl)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C145ce13c-5740-49bd-b2fd-0f67214765b3)%26anchor%3D{counter_kids}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=pl&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%93%20%7BhighestPrice%7D'
        counter_kids += 24
        response = requests.get(url_kids_api)
        if response.status_code == 200:
            data = response.json()
            with open(f"c:\\nike_com_pl\\html_data\\kids\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        time.sleep(1)
    print(f"Собрал kids")


"""Собираем все ссылки на товары"""


def parsing_url_json():
    # proxies = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
    # header = {
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    folders = [r"c:\nike_com_pl\html_data\kids\*.json",
               r"c:\nike_com_pl\html_data\kobiety\*.json",
               r"c:\nike_com_pl\html_data\mezczyzni\*.json"]
    # targetPattern = r"C:\scrap_tutorial-master\Польша_Кросовки\nike_com_pl\html_url\*.html"
    # files_html = glob.glob(targetPattern)

    for folder in folders:
        urls = []
        files_json = glob.glob(folder)
        group = files_json[0].split("\\")[-2]
        for item in files_json:
            print(item)
            with open(item, encoding='utf-8') as f:
                data = json.load(f)
                all_products = data['data']['products']['products']
                if all_products:
                    coun = 0
                    for url in all_products:
                        coun += 1
                        urls.append(url['url'].replace("{countryLang}/", "https://www.nike.com/pl/"))
                else:
                    continue
        with open(f'c:\\nike_com_pl\\csv_url\\{group}\\url.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
            writer.writerow(urls)


#
"""Сбор информации с html в json файл"""


def parsin_html_to_json():
    folders = [r"c:\nike_com_pl\html_product\kids\*.html",
               r"c:\nike_com_pl\html_product\kobiety\*.html",
               r"c:\nike_com_pl\html_product\mezczyzni\*.html"]
    for file in folders:
        group = file.split('\\')[3]
        coun = 0
        files_html = glob.glob(file)
        for item in files_html:
            coun += 1
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            script_json = soup.find('script', type="application/json")
            if script_json is not None:
                json_content = json.loads(script_json.string)
                with open(f'c:\\nike_com_pl\\json\\{group}\\data_{coun}.json', 'w', encoding='utf-8') as f:
                    json.dump(json_content, f, indent=4, ensure_ascii=False)


"""Собираем информацию с json  в  csv"""


def parsin_contact_json():
    today = datetime.today()
    date_str = today.strftime('%d/%m')
    # header = {
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    folders = [r"c:\nike_com_pl\json\kids\*.json",
               r"c:\nike_com_pl\json\kobiety\*.json",
               r"c:\nike_com_pl\json\mezczyzni\*.json"]
    url_myfin_by = "https://myfin.by/currency/minsk"
    response = requests.get(url_myfin_by, headers=header, proxies=proxies)
    root = html.fromstring(response.text)
    value = root.xpath('//div[@class="c-best-rates"]//table//tbody//tr[4]//td[4]/text()')
    """Курс Беларуских"""
    bel = 0.6
    for file in folders[2:]:
        files_html = glob.glob(file)
        group = file.split('\\')[3]
        with open(f"c:\\nike_com_pl\\csv_data\\{group}.csv", "w",
                  errors='ignore', encoding="utf-8") as file_csv:
            writer = csv.writer(file_csv, delimiter=",", lineterminator="\r")
            writer.writerow(
                (
                    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags', 'Published',
                    'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value',
                    'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
                    'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                    'Variant Compare At Price',
                    'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position',
                    'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
                    'Google Shopping / Google Product Category', 'Google Shopping / Gender',
                    'Google Shopping / Age Group',
                    'Google Shopping / MPN', 'Google Shopping / AdWords Grouping', 'Google Shopping / AdWords Labels',
                    'Google Shopping / Condition', 'Google Shopping / Custom Product',
                    'Google Shopping / Custom Label 0',
                    'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2',
                    'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4', 'Variant Image',
                    'Variant Weight Unit', 'Variant Tax Code', 'Cost per item', 'Included / Belarus',
                    'Included / International', 'Price / International', 'Compare At Price / International', 'Status'
                )
            )
        counter = 0
        for item in files_html:
            print(item)
            with open(item, 'r', encoding="utf-8") as f:
                data_json = json.load(f)
            counter += 1
            # with open(f'Nike.json', 'w') as f:
            #     json.dump(data_json, f)
            # exit()
            # print(f"{counter} из {len(files_html)} ") #| {item}
            products_list = []
            for _ in data_json['props']['pageProps']['initialState']['Threads']['products']:
                products_list.append(_)
            all_sku_size = {}
            available_skus = []

            for j in products_list:
                sizes = []
                gtins = []
                sku = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}']['skus']
                for item in sku:
                    all_sku_size[item['skuId']] = 'id'
                    all_sku_size[item['localizedSize']] = 'localizedSize'

                availableSkus = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}'][
                    'availableSkus']
                for i in availableSkus:
                    available_skus.append(i['id'])
                for item in sku:
                    if item['skuId'] in available_skus:
                        sizes.append(item['localizedSize'])
                        gtins.append(item['gtin'])

                Handle = f"{data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}']['styleColor']}_{data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}']['pid']}"
                # color_product = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}']['colorDescription']

                color = ''
                try:
                    color_old = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}'][
                        'colorDescription']
                    with open('colors.csv', newline='', encoding="utf-8") as csvfile:
                        reader = csv.reader(csvfile, delimiter=';')
                        for row in reader:
                            if row[0] == color_old.split('/')[0]:
                                color = row[1]

                                break
                            else:
                                color = color_old
                except:
                    color = None
                Title = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}']['title']
                id_product = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}']['pid']

                category_product_old = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}'][
                    'subTitle']
                with open('dict.csv', newline='', encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    for row in reader:
                        # print(row[0])
                        if row[0] == category_product_old:
                            category_product = row[1]
                            break
                        else:
                            category_product = category_product_old
                descriptionPreview = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}']['descriptionPreview']
                translator = Translator()
                translation_ru = translator.translate(text=descriptionPreview, src='pl', dest='ru').text.replace('\r\n', ' ')
                Vendor = "Nike"
                picture_dicts = \
                    data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}']['nodes'][0]['nodes']
                alls_photo = []

                # Проходимся по каждому элементу в JSON и извлекаем значение squarishURL, если оно есть
                for i, picture_dict in enumerate(picture_dicts):
                    if "squarishURL" in picture_dict["properties"]:
                        index = i + 1
                        photo_link = picture_dict["properties"]["squarishURL"].replace(
                            'https://static.nike.com/a/images/t_default/',
                            'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/')
                        photo_link = photo_link.replace(f'/{index}.', f'/1.')
                        alls_photo.append(photo_link)
                coun = 0
                pfoto_site = []
                for img in alls_photo:
                    coun += 1
                    pfoto_site.append(
                        f"https://loketsneakers.s3.eu-central-1.amazonaws.com/Nike/{group}/{id_product}_{coun}.webp")

                    file_path = f"c:\\nike_com_pl\\data_img\\img_{group}\\{id_product}_{coun}.webp"
                    new_file_path = f"c:\\nike_com_pl\\csv_data\\img_{group}\\{id_product}_{coun}.webp"
                    if not os.path.exists(file_path):
                        img_data = requests.get(img, headers=header, proxies=proxies)
                        with open(new_file_path, 'wb') as file_img:
                            file_img.write(img_data.content)
                sell_price = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}'][
                    'currentPrice']
                base_price = data_json['props']['pageProps']['initialState']['Threads']['products'][f'{j}']['fullPrice']

                """Формирование цены с курсом"""
                Variant_Price = 0
                Variant_Compare_At_Price = 0
                if sell_price < base_price:
                    Variant_Price = round(((float(sell_price) + 60.0) * 1.1) * bel, 1)  # два знака после запятой
                    Variant_Price = str(Variant_Price).replace('.', ',')
                    Variant_Compare_At_Price = round(((float(base_price) + 60.0) * 1.1) * bel,
                                                     1)  # два знака после запятой
                    Variant_Compare_At_Price = str(Variant_Compare_At_Price).replace('.', ',')
                elif sell_price == base_price:
                    Variant_Price = round(((float(sell_price) + 60.0) * 1.1) * bel, 1)  # два знака после запятой
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
                    gtin = gtins[i]
                    data = [Handle, Title, "", Vendor, 'Apparel & Accessories > Shoes',
                            category_product.replace("\n", ""), f'{color}, {date_str}', 'TRUE', 'Размер', size, "", "",
                            "", "", gtin, "", "", "999", "continue", "manual", Variant_Price, Variant_Compare_At_Price,
                            "TRUE", "TRUE", "", photo, index_photo_str, "", "", "", "", "", "", "", "", "", "", "", "",
                            "", "", "", "", "", "", "kg", "", "", "TRUE", "TRUE", "", "", "Active"]
                    with open(f"c:\\nike_com_pl\\csv_data\\{group}.csv", "a",
                              errors='ignore', encoding="utf-8") as file:
                        writer = csv.writer(file, delimiter=",", lineterminator="\r")
                        writer.writerow((data))

                # If there are more photos than sizes, fill in the remaining rows with empty data except for photo and index
                if len(pfoto_site) > len(sizes):
                    alls_photo = []
                    for picture_dict in picture_dicts:
                        if "squarishURL" in picture_dict["properties"]:
                            photo_url = picture_dict["properties"]["squarishURL"].replace(
                                'https://static.nike.com/a/images/t_default/',
                                'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/')
                            alls_photo.append(photo_url)
                    for j in range(len(sizes), len(pfoto_site)):
                        photo = pfoto_site[j]
                        index_photo_str = str(index_photo)  # convert index to string
                        data = [Handle, Title, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                '', '',
                                '', '', '', '', '', photo, index_photo_str, '', '', '', '', '', '', '', '', '', '',
                                '', '', '', '', '', '', '', '',
                                '', '', '', '', '', '', '', ""]
                        with open(f"c:\\nike_com_pl\\csv_data\\{group}.csv", "a",
                                  errors='ignore', encoding="utf-8") as file:
                            writer = csv.writer(file, delimiter=",", lineterminator="\r")
                            writer.writerow((data))
                        index_photo += 1


"""Перемещаем фото в папку с БД"""


def move_img():
    folders = {
        r'c:\nike_com_pl\csv_data\img_kids': r'c:\nike_com_pl\data_img\img_kids',
        r'c:\nike_com_pl\csv_data\img_kobiety': r'c:\nike_com_pl\data_img\img_kobiety',
        r'c:\nike_com_pl\csv_data\img_mezczyzni': r'c:\nike_com_pl\data_img\img_mezczyzni'
    }

    for src, dest in folders.items():
        for root, dirs, files in os.walk(src):
            dest_root = root.replace(src, dest)
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_root, file)
                shutil.move(src_path, dest_path)


def del_files_html_product():
    folders_del = [r"c:\nike_com_pl\html_product\kids",
                   r"c:\nike_com_pl\html_product\kobiety",
                   r"c:\nike_com_pl\html_product\mezczyzni"
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
    # """Перемещаем изображение в папку с БД"""
    # move_img()
    # """Удаляем старые файлы HTML"""
    # del_files_html_product()
    #
    # save_json_product()
    # parsing_url_json()
    # categories = ['kids', 'kobiety', 'mezczyzni']
    # for category in categories:
    #     asyncio.run(main(category))
    # parsin_html_to_json()
    parsin_contact_json()
