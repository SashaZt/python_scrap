from googletrans import Translator

import re
import boto3
import pandas as pd
import shutil
import os
import csv
import glob
from datetime import datetime, timedelta
import json
import time
import zipfile
from lxml import html
import requests
import asyncio
# from main_asio import main

from bs4 import BeautifulSoup

# Установка учетных данных AWS
ACCESS_KEY = 'AKIAQWBRT2HZZFWLS5EJ'
SECRET_KEY = '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'

# Создание клиента S3
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Настройка для requests чтобы использовать прокси
# proxies = {'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}/'}

header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

"""Сохраняем html страницы"""


def save_html_product():
    all_urls = ["https://nbsklep.pl/meskie/obuwie", "https://nbsklep.pl/damskie/obuwie",
                "https://nbsklep.pl/dzieciece/obuwie"]
    for u in all_urls:
        group = u.split("/")[-2]
        dir_path = f'c:\\nbsklep_pl\\html_data\\{group}'
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        coun = 0
        resp = requests.get(u, headers=header)
        soup = BeautifulSoup(resp.text, 'lxml')
        script_json_1 = soup.find('script', type="application/json")
        try:
            data_json_1 = json.loads(script_json_1.string)
        except:
            data_json_1 = ""
        try:
            lastPage = int(
                data_json_1['props']['pageProps']['dehydratedState']['queries'][7]['state']['data']['products'][
                    'pagination'][
                    'lastPage'])
        except:
            lastPage = int(
                data_json_1['props']['pageProps']['dehydratedState']['queries'][7]['state']['data']['products'][
                    'pagination'][
                    'lastPage'])

        urls = []
        for i in range(1, lastPage + 1):
            time.sleep(10)
            coun += 1
            if i == 1:
                resp = requests.get(u, headers=header)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'lxml')
                with open(f'c:\\nbsklep_pl\\html_data\\{group}\\data_{coun}.html', 'w', encoding='utf-8') as f:
                    f.write(soup.prettify())
            if i > 1:
                resp = requests.get(f'{u}?page={i}', headers=header)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'lxml')
                with open(f'c:\\nbsklep_pl\\html_data\\{group}\\data_{coun}.html', 'w',
                          encoding='utf-8') as f:
                    f.write(soup.prettify())
            print(f"{coun} из {lastPage + 1}, категория {group}")


"""Собираем все ссылки на товары"""


def parsing_url_html():
    folders = [r"c:\nbsklep_pl\html_data\meskie\*.html",
               r"c:\nbsklep_pl\html_data\damskie\*.html",
               r"c:\nbsklep_pl\html_data\dzieciece\*.html"]

    urls = []
    for folder in folders:
        files_html = glob.glob(folder)
        group = files_html[0].split("\\")[-2]
        dir_path = f'c:\\nbsklep_pl\\csv_url\\{group}'
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        for item in files_html:
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            script_json = soup.find('script', type="application/ld+json")
            try:
                data_json = json.loads(script_json.string)
            except:
                data_json = ""
            """Тестовое сохранение json"""
            # with open(f'./dict.json', 'a', encoding='utf-8') as f:
            #     json.dump(data_json, f, indent=4, ensure_ascii=False)
            script_json_1 = soup.find('script', type="application/json")
            try:
                data_json_1 = json.loads(script_json_1.string)
            except:
                data_json_1 = ""
            # print(data_json_1['props']['pageProps']['dehydratedState']['queries'][7]['state']['data']['products']['pagination']['lastPage'])
            # with open('obuwie.json', 'w') as f:
            #     json.dump(data_json_1['props']['pageProps']['dehydratedState']['queries'][7], f)

            for element in data_json['@graph'][0]['itemListElement']:
                url = element['item']['offers']['url']
                urls.append(url)
        with open(f'c:\\nbsklep_pl\\csv_url\\{group}\\url.csv', 'a', newline='',
                  encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
            writer.writerow(urls)
        if os.path.exists(f'c:\\nbsklep_pl\\csv_url\\{group}\\url.csv'):
            folder_path = f"c:\\nbsklep_pl\\html_data\\{group}"
            files = os.listdir(folder_path)
            for file in files:
                file_path = os.path.join(folder_path, file)
                os.remove(file_path)
    print("Все ссылки собраны")


"""Собираем все ссылки на товары"""


def drop_duplicates():
    all_csv = ['c:\\nbsklep_pl\\csv_url\\damskie\\url.csv',
               'c:\\nbsklep_pl\\csv_url\\dzieciece\\url.csv',
               'c:\\nbsklep_pl\\csv_url\\meskie\\url.csv']
    for f in all_csv:
        parts = f.split("\\")  # разбиваем строку на части, используя обратную косую черту как разделитель
        value = parts[-2]
        df = pd.read_csv(f)

        # удалить дубликаты строк и сохранить уникальные строки в новом DataFrame
        df_unique = df.drop_duplicates()

        # сохранить уникальные строки в CSV-файл
        df_unique.to_csv(f'c:\\nbsklep_pl\\csv_url\\{value}\\url.csv', index=False)
    print("Дубликты удалили, переходим к обработке main_asio")


"""Сбор информации с html страниц товаров"""


def parsin_contact_html():
    today = datetime.today()
    date_str = today.strftime('%d/%m')
    folders = [r"c:\nbsklep_pl\html_product\damskie\*.html",
               r"c:\nbsklep_pl\html_product\meskie\*.html",
               r"c:\nbsklep_pl\html_product\dzieciece\*.html"]
    # """Курс Беларуских"""
    url_myfin_by = "https://myfin.by/bank/kursy_valjut_nbrb/pln"
    response = requests.get(url_myfin_by, headers=header)
    if response.status_code == 200:
        root = html.fromstring(response.text)
        value = root.xpath('//div[@class="h1"][1]/text()')[0]
        bel = float(value) / 10
    else:
        bel = 0.6
    urls = []
    ajax = []
    for folder in folders[:1]:
        files_html = glob.glob(folder)
        group = files_html[0].split("\\")[-2]

        with open(f"c:\\nbsklep_pl\\csv_data\\{group}.csv", "w",
                  errors='ignore', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\r")
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
        data_dict = {"date": datetime.now().strftime("%d.%m.%Y"), "products": []}
        for item in files_html[:1]:
            with open(item, encoding="utf-8") as file:
                src = file.read()
            counter += 1
            # print(f"{counter} из {len(files_html)}| {item}")
            soup = BeautifulSoup(src, 'lxml')
            script_json = soup.find('script', type="application/json")
            try:
                data_json = json.loads(script_json.string)
            except:
                data_json = ""
            script_gtin = soup.find('script', type="application/ld+json")
            try:
                data_json_gtin = json.loads(script_gtin.string)
            except:
                data_json_gtin = ""
            gtin8 = data_json_gtin['@graph'][0]['gtin8']
            # with open(f'New_Balance.json', 'w') as f:
            #     json.dump(data_json, f)
            # exit()
            try:
                # Handle = (data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product']['name']).replace('–', '-').split('-')[0].strip()
                Handle = (
                data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product']['name'])
                last_word_Handle = Handle.split()[-1]  # выбрать последнее слово
                Handle_new = ' '.join(["New Balance", last_word_Handle])
            except:
                print("Ошибка в Handle")
                continue
            Title = (data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product'][
                'name']).replace('–', '-').split('-')[0].strip()


            descriptions = data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product'][
                'description']
            soup_d = BeautifulSoup(descriptions, 'lxml')
            description_p = soup_d.text
            translator = Translator()
            translation_ru = translator.translate(text=description_p, src='pl', dest='ru').text.replace('\r\n', ' ')


            color = ''
            try:
                color_old = \
                data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product'][
                    'properties'][8]['value']['dataList'][0]
                with open('colors.csv', newline='', encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    for row in reader:
                        # print(row[0])
                        if row[0] == color_old:
                            color = row[1]
                            break
                        else:
                            color = color_old
            except:
                color = None
            last_word_Title = Title.split()[-1]  # выбрать последнее слово
            Title_new = ' '.join(["New Balance", last_word_Title])
            Vendor = (
                data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product'][
                    'producer'][
                    'name'])
            Tags = (
                data_json['props']['pageProps']['dehydratedState']['queries'][3]['state']['data']['menu']['children'][
                    1][
                    'children'][1]['children'][8]['title'])

            sell_price = \
                data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product']['prices'][
                    'sellPrice']['gross']
            base_price = \
                data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product']['prices'][
                    'basePrice']['gross']
            """Формирование цены с курсом"""
            Variant_Price = 0
            Variant_Compare_At_Price = 0
            if sell_price < base_price:
                Variant_Price = round(((float(sell_price) + 60.0) * 1.25) * bel, 1)  # два знака после запятой
                Variant_Price = str(Variant_Price).replace('.', ',')
                Variant_Compare_At_Price = round(((float(base_price) + 60.0) * 1.25) * bel,
                                                 1)  # два знака после запятой
                Variant_Compare_At_Price = str(Variant_Compare_At_Price).replace('.', ',')
            elif sell_price == base_price:
                Variant_Price = round(((float(sell_price) + 60.0) * 1.15) * bel, 1)  # два знака после запятой
                Variant_Price = str(Variant_Price).replace('.', ',')
                Variant_Compare_At_Price = ""

            breds_value = data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product'][
                'properties']
            data_bred = [item['value']['dataList'] for item in breds_value]
            bred_value = data_bred[0]
            id_product = data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product'][
                'id']

            """Размеры"""
            sizes = []
            data_size = \
                data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product'][
                    'variants']

            for item in data_size:
                if item["availability"]["message"]["content"] == "Dostępny":
                    size = item["option"].split()[0]  # получаем первое слово из опции
                    size = ''.join(
                        filter(lambda x: x.isdigit() or x == '.', size))  # удаляем все символы, кроме цифр и точки
                    sizes.append(size)
                    # sizes.append(item["option"].replace(" D", ""))
            """Размеры"""
            category_product_old = \
                data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product'][
                    'categories'][0][
                    'name']
            # category_product= ""

            with open('dict.csv', newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for row in reader:
                    # print(row[0])
                    if row[0] == category_product_old:
                        category_product = row[1]
                        break
                    else:
                        category_product = category_product_old

            picture_dicts = \
            data_json['props']['pageProps']['dehydratedState']['queries'][5]['state']['data']['product'][
                'picturesCategories'][1]['pictures']

            """Тестовый вариант"""
            alls_photo = []
            for i, picture_dict in enumerate(picture_dicts):
                index = i + 1
                photo_link = picture_dict['filename'].replace('https://nbsklep.pl/{imageSafeUri}',
                                                              'https://nbsklep.pl/picture')
                photo_link = photo_link.replace(f'/{index}.', f'/1.')
                alls_photo.append(photo_link)
            photo_link_str = " ; ".join(alls_photo)

            """Тестовый скрипт на проверку, если файл есть, тогда его не выкачивать"""
            coun = 0
            pfoto_site = []
            # for img in alls_photo:
            #     coun += 1
            img_groups = {
                "meskie": "img_meskie",
                "damskie": "img_damskie",
                "dzieciece": "img_dzieciece"
            }

            bucket_name = 'loketsneakers'

            for coun, img in enumerate(alls_photo, 1):
                img_group_folder = img_groups.get(group)
                if img_group_folder:
                    pfoto_site.append(
                        f"https://loketsneakers.s3.eu-central-1.amazonaws.com/newbalance/{img_group_folder}/{id_product}_{coun}.webp")
                    file_path = f"newbalance/{img_group_folder}/{id_product}_{coun}.webp"

                    # Проверка наличия файла в S3 бакете
                    try:
                        s3.head_object(Bucket=bucket_name, Key=file_path)
                        print(f"Файл {file_path} уже существует в S3 бакете. Пропуск загрузки.")
                    except:
                        # Загрузка файла из удаленного источника
                        print(f"Файл {file_path} отсутствует в S3 бакете. Загрузка из удаленного источника.")
                        img_data = requests.get(img, headers=header)  # , proxies=proxies

                        # Загрузка данных изображения в S3 бакет
                        s3.put_object(Body=img_data.content, Bucket=bucket_name, Key=file_path)
                        print(f"Файл {file_path} успешно загружен в S3 бакет.")

            index_photo = 1  # Initialize photo index

            for i, size in enumerate(sizes):
                if i < len(pfoto_site):
                    photo = pfoto_site[i]
                    index_photo_str = str(index_photo)  # convert index to string
                    index_photo += 1  # Increment photo index for each iteration
                else:
                    photo = ""
                    index_photo_str = ""  # leave index_photo_str empty
                data = [Handle, Title_new, translation_ru, Vendor, 'Apparel & Accessories > Shoes', category_product,
                        f'{color}, {date_str}', 'TRUE',
                        'Размер', size, "", "", "", "", gtin8, "", "", "999", "continue", "manual", Variant_Price,
                        Variant_Compare_At_Price, "TRUE", "TRUE", "", photo, index_photo_str, "", "", "", "", "", "",
                        "",
                        "",
                        "", "", "", "", "", "", "", "", "", "", "kg", "", "", "TRUE", "TRUE", "", "", "Active"]
                with open(f"c:\\nbsklep_pl\\csv_data\\{group}.csv", "a",
                          errors='ignore', encoding="utf-8") as file:
                    writer = csv.writer(file, delimiter=",", lineterminator="\r")
                    writer.writerow((data))

            # If there are more photos than sizes, fill in the remaining rows with empty data except for photo and index
            if len(pfoto_site) > len(sizes):
                alls_photo = []
                for picture_dict in picture_dicts:
                    alls_photo.append(
                        picture_dict['filename'].replace('https://nbsklep.pl/{imageSafeUri}',
                                                         'https://nbsklep.pl/picture'))
                for j in range(len(sizes), len(pfoto_site)):
                    photo = pfoto_site[j]
                    index_photo_str = str(index_photo)  # convert index to string
                    data = [Handle, Title_new, '', '', '', category_product, color, '', '', '', '', '', '', '', '', '',
                            '', '', '', '',
                            '', '', '', '', '', photo, index_photo_str, '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '',
                            '', '', '', '', '', '', '', ""]
                    with open(f"c:\\nbsklep_pl\\csv_data\\{group}.csv", "a",
                              errors='ignore', encoding="utf-8") as file:
                        writer = csv.writer(file, delimiter=",", lineterminator="\r")
                        writer.writerow((data))
                    index_photo += 1


"""Создание архива новых данных"""


def move_img():
    folders = {
        r'c:\nbsklep_pl\csv_data\img_damskie': r'c:\nbsklep_pl\data_img\img_damskie',
        r'c:\nbsklep_pl\csv_data\img_dzieciece': r'c:\nbsklep_pl\data_img\img_dzieciece',
        r'c:\nbsklep_pl\csv_data\img_meskie': r'c:\nbsklep_pl\data_img\img_meskie'
    }

    for src, dest in folders.items():
        for root, dirs, files in os.walk(src):
            dest_root = root.replace(src, dest)
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_root, file)
                shutil.move(src_path, dest_path)


def del_files_html_product():
    folders_del = [r"c:\nbsklep_pl\html_product\damskie",
                   r"c:\nbsklep_pl\html_product\dzieciece",
                   r"c:\nbsklep_pl\html_product\meskie"
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


"""Очистка папки после создания архива"""
# def delete_files_and_folders():
#     DATE_FORMAT = "%d_%m_%y"
#     zipfile_name = datetime.now().strftime(DATE_FORMAT) + ".7z"
#     directory_to_delete = "c:\\nbsklep_pl\\csv_data"
#     archive_name = f"c:\\nbsklep_pl\\{zipfile_name}"
#     archive_path = os.path.join(directory_to_delete, archive_name)
#
#     if os.path.exists(archive_path):
#         # Archive file exists, so delete all files in each subdirectory of directory_to_delete
#         for dirpath, dirnames, filenames in os.walk(directory_to_delete):
#             for filename in filenames:
#                 file_path = os.path.join(dirpath, filename)
#                 os.remove(file_path)
# #
# # def main():
# #     print("1 - Сохранение всех страниц \n 2 - Собираем ссылки на товар \n 3 - удаляем дубликаты ссылок \n 4 - собираем csv \n 5 - создаем архив \n 6 - перемещение фото в БД \n 7 - очистка всех папок \n  0 - завершить скрипт")
# #     while True:
# #         user_input = int(input("Введите номер функции, которую хотите запустить: "))
# #         if user_input == 0:
# #             break
# #         if user_input == 1:
# #             save_html_product()
# #         elif user_input == 2:
# #             parsing_url_html()
# #         elif user_input == 3:
# #             drop_duplicates()
# #         elif user_input == 4:
# #             parsin_contact_html()
# #         elif user_input == 5:
# #             creating_an_archive()
# #         elif user_input == 6:
# #             move_img()
# #         elif user_input == 7:
# #             delete_files_and_folders()
# #         else:
# #             print("Ошибка: Неверный номер функции.")


if __name__ == '__main__':
    ## main()
    # """Перемещаем изображение в папку с БД"""
    # move_img()
    # # """Удаляем старые файлы HTML"""
    # del_files_html_product()
    # save_html_product()
    # parsing_url_html()
    # drop_duplicates()
    # categories = ['damskie', 'dzieciece', 'meskie']
    # for category in categories:
    #     asyncio.run(main(category))

    parsin_contact_html()
    # creating_an_archive()
    # move_img()
    # delete_files_and_folders()
