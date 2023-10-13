import csv
import glob
from datetime import datetime
import shutil
from main_asio import main_asio
import json
import os
import time
import zipfile
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import html
from selenium import webdriver
# Нажатие клавиш
from selenium.webdriver.chrome.service import Service

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки

useragent = UserAgent()
# Данные для прокси
PROXY_HOST = '141.145.205.4'
PROXY_PORT = 31281  # Без кавычек
PROXY_USER = 'proxy_alex'
PROXY_PASS = 'DbrnjhbZ88'
proxies = {'http': 'http://80.77.34.218:9999', 'https': 'http://80.77.34.218:9999'}
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

def save_url_csv():
    """mezczyzni"""
    urls_mezczyzni = "https://www.asics.com/pl/pl-pl/mens-gear/c/as10000000/?sz=96"
    response = requests.get(urls_mezczyzni, headers=header)  # , proxies=proxies
    soup = BeautifulSoup(response.text, 'lxml')
    totalResources_mezczyzni = 0
    if response.status_code == 200:
        results_hits = soup.select_one('.results-hits')
        totalResources_mezczyzni = int(results_hits.text.replace("(", "").replace(")", "").split()[0]) // 96
    counter_mezczyzni = 0
    links_mezczyzni = []

    for page in range(1, totalResources_mezczyzni + 2):
        if page == 1:
            url_mezczyzni_api = 'https://www.asics.com/pl/pl-pl/mens-gear/c/as10000000/?sz=96'
        else:
            counter_mezczyzni += 96
            url_mezczyzni_api = f'https://www.asics.com/pl/pl-pl/mens-gear/c/as10000000/?start={counter_mezczyzni}&sz=96'

        response = requests.get(url_mezczyzni_api, headers=header)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for li in soup.find_all("li", class_="grid-tile"):
                a = li.find("a", href=True)
                if a:
                    links_mezczyzni.append(a["href"])
            time.sleep(1)
        print(f"mens {counter_mezczyzni} из {totalResources_mezczyzni * 96}")

    with open(f'c:\\asics_pl\\csv_url\\mens-gear\\url.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
        writer.writerow(links_mezczyzni)

    print('Пауза 10 сек')
    time.sleep(10)

    """womens"""
    urls_womens = "https://www.asics.com/pl/pl-pl/womens-gear/c/as20000000/?sz=96"
    response = requests.get(urls_womens, headers=header)  # , proxies=proxies
    soup = BeautifulSoup(response.text, 'lxml')
    totalResources_womens = 0
    if response.status_code == 200:
        results_hits = soup.select_one('.results-hits')
        totalResources_womens = int(results_hits.text.replace("(", "").replace(")", "").split()[0]) // 96
    counter_womens = 0
    links_womens = []

    for page in range(1, totalResources_womens + 2):
        if page == 1:
            url_womens_api = 'https://www.asics.com/pl/pl-pl/womens-gear/c/as20000000/?sz=96'
        else:
            counter_womens += 96
            url_womens_api = f'https://www.asics.com/pl/pl-pl/womens-gear/c/as20000000/?start={counter_womens}&sz=96'

        response = requests.get(url_womens_api, headers=header)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for li in soup.find_all("li", class_="grid-tile"):
                a = li.find("a", href=True)
                if a:
                    links_womens.append(a["href"])
            time.sleep(1)
        print(f"womens {counter_womens} из {totalResources_womens * 96}")

    with open(f'c:\\asics_pl\\csv_url\\womens-gear\\url.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
        writer.writerow(links_womens)

    print('Пауза 10 сек')
    time.sleep(10)

    """kids"""
    urls_kids = "https://www.asics.com/pl/pl-pl/kids-gear/c/as30000000/?sz=96"
    response = requests.get(urls_kids, headers=header) #, proxies=proxies
    soup = BeautifulSoup(response.text, 'lxml')
    totalResources_kids = 0
    if response.status_code == 200:
        results_hits = soup.select_one('.results-hits')
        totalResources_kids = int(results_hits.text.replace("(", "").replace(")", "").split()[0]) // 96
    counter_kids = 0
    links_kids = []

    for page in range(1, totalResources_kids + 2):
        if page == 1:
            url_kids_api = 'https://www.asics.com/pl/pl-pl/kids-gear/c/as30000000/?sz=96'
        else:
            counter_kids += 96
            url_kids_api = f'https://www.asics.com/pl/pl-pl/kids-gear/c/as30000000/?start={counter_kids}&sz=96'

        response = requests.get(url_kids_api, headers=header)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for li in soup.find_all("li", class_="grid-tile"):
                a = li.find("a", href=True)
                if a:
                    links_kids.append(a["href"])
            time.sleep(1)
        print(f"kids {counter_kids} из {totalResources_kids * 96}")

    with open(f'c:\\asics_pl\\csv_url\\kids-gear\\url.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
        writer.writerow(links_kids)



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
        print( f"У {value} осталось {len(df_unique)} уникальных строк.")
    print("Дубликты удалили, переходим к обработке main_asio")
"""Собираем все ссылки на товары"""


def parsin_contact_html():
    today = datetime.today()
    date_str = today.strftime('%d/%m')
    folders_html = [r"c:\asics_pl\html_product\kids-gear\*.html",
               r"c:\asics_pl\html_product\mens-gear\*.html",
               r"c:\asics_pl\html_product\womens-gear\*.html"
               ]
    """Курс Беларуских"""
    url_myfin_by = "https://myfin.by/currency/minsk"
    response = requests.get(url_myfin_by, headers=header)
    root = html.fromstring(response.text)
    value = root.xpath('//div[@class="c-best-rates"]//table//tbody//tr[4]//td[4]/text()')
    bel = (float(value[0])) / 10

    for file in folders_html: # Убарть срез для категории!
        group = file.split('\\')[3]
        with open(f"c:\\asics_pl\\csv_data\\{group}.csv", "w",
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
        coun = 0
        files_json = glob.glob(file)
        for item in files_json: # Убарть срез для файла!
            counter = 0
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            sizes = []
            for tag in soup.find_all('li', {'data-instock': 'true'}):
                size = tag.find('a').get_text(strip=True)
                if size:
                    sizes.append(size)

            scripts = soup.find_all('script', {'type': 'text/javascript'})
            data = ''
            product_id = None
            for script in scripts[2:3]: # оставить т.к. на странице несколько скриптов
                script_ = script.text.strip()
                utag_data = json.loads(script_.split('var utag_data = ')[1].strip()[:-1])
                # with open(f'asics.json', 'w') as f:
                #     json.dump(utag_data, f)
                # exit()

                # Извлечение необходимых значений
                id_product = utag_data.get('product_id')[0]
                Title = "ASICS " + utag_data.get('product_name')[0]
                base_price_float = float(utag_data.get('product_unit_original_price')[0]) # Базовая цена без скидки
                base_price_round = round(base_price_float)
                base_price = int(base_price_round)
                sell_price_float = float(utag_data.get('product_unit_price')[0]) # Цена со скидкой
                sell_price_round = round(sell_price_float)
                sell_price = int(sell_price_round)
                category_product_old = utag_data.get('product_category')[0].split('/')[-1]
                with open('dict.csv', newline='', encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    for row in reader:
                        # print(row[0])
                        if row[0] == category_product_old:
                            category_product = row[1]
                            break
                        else:
                            category_product = category_product_old

                # color_old = utag_data.get('product_variant')[0]
                color = ''
                try:
                    color_old = utag_data.get('product_variant')[0]
                    with open('colors.csv', newline='', encoding="utf-8") as csvfile:
                        reader = csv.reader(csvfile, delimiter=';')
                        for row in reader:
                            if row[0] == color_old:
                                color = row[1]
                                break
                            else:
                                color = color_old
                except:
                    color = None

            alls_photo = []
            product_image_divs = soup.find_all('ul', class_='product-primary-image')
            for product_image_div in product_image_divs:
                for img in product_image_div.find_all('img', class_='primary-image js-primary-image'):
                    alls_photo.append(img['src'].replace('$sfcc-product$', '$zoom$'))
                for img in product_image_div.find_all('img', class_='primary-image js-primary-image b-lazy'):
                    alls_photo.append(img['data-src'].replace('$sfcc-product$', '$zoom$'))
            Handle = id_product.replace(".", "-")
            Vendor = "ASICS"


            # picture_dicts = data_json['view_list']
            # alls_photo = []
            # for i, picture_dict in enumerate(picture_dicts):
            #     index = i + 1
            #     photo_link = picture_dict["image_url"].replace("https://assets.adidas.com/images/w_600,f_auto,q_auto", "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto")
            #     photo_link = photo_link.replace(f'/{index}.', f'/1.')
            #     alls_photo.append(photo_link)

            coun = 0
            pfoto_site = []
            # for img in alls_photo:
            #     coun += 1
            img_groups = {
                "kids-gear": "img_kids-gear",
                "mens-gear": "img_mens-gear",
                "womens-gear": "img_womens-gear"
            }

            for coun, img in enumerate(alls_photo, 1):
                img_group_folder = img_groups.get(group)
                if img_group_folder:
                    pfoto_site.append(
                        f"https://loketsneakers.s3.eu-central-1.amazonaws.com/{img_group_folder}/{id_product}_{coun}.webp")
                    file_path = f"c:\\asics_pl\\data_img\\{img_group_folder}\\{id_product}_{coun}.webp"
                    new_file_path = f"c:\\asics_pl\\csv_data\\{img_group_folder}\\{id_product}_{coun}.webp"
                    if not os.path.exists(file_path):
                        img_data = requests.get(img, headers=header, proxies=proxies)
                        with open(new_file_path, 'wb') as file_img:
                            file_img.write(img_data.content)


















            # pfoto_site = []
            # for img in alls_photo:
            #     coun += 1
            #     pfoto_site.append(
            #         f"https://cdn.shopify.com/s/files/1/0667/5824/6699/files/{id_product}_{coun}.webp")
            #
            #     file_path = f"c:\\asics_pl\\data_img\\img_{group}\\{id_product}_{coun}.webp"
            #     new_file_path = f"c:\\asics_pl\\csv_data\\img_{group}\\{id_product}_{coun}.webp"
            #     if not os.path.exists(file_path):
            #         img_data = requests.get(img, headers=header, proxies=proxies)
            #         with open(new_file_path, 'wb') as file_img:
            #             file_img.write(img_data.content)
            # try:
            #     sell_price = data_json['pricing_information']['sale_price']
            # except:
            #     sell_price = 0
            # base_price = data_json['pricing_information']['standard_price']
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
                        "", "TRUE", "TRUE", "", photo, index_photo_str, "", "", "", "",
                        "", "", "",
                        "",
                        "", "", "", "", "", "", "", "", "", "", "kg", "", "", "TRUE", "TRUE", "", "", "Active"]
                with open(f"c:\\asics_pl\\csv_data\\{group}.csv", "a",
                          errors='ignore', encoding="utf-8") as file:
                    writer = csv.writer(file, delimiter=",", lineterminator="\r")
                    writer.writerow((data))

            # If there are more photos than sizes, fill in the remaining rows with empty data except for photo and index
            if len(pfoto_site) > len(sizes):
                # alls_photo = []
                # for picture_dict in picture_dicts:
                #     photo_url =picture_dict["image_url"].replace("https://assets.adidas.com/images/w_600,f_auto,q_auto", "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto")
                #     alls_photo.append(photo_url)
                for j in range(len(sizes), len(pfoto_site)):
                    photo = pfoto_site[j]
                    index_photo_str = str(index_photo)  # convert index to string
                    data = [Handle, Title, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '',
                            '', '', '', '', '', photo, index_photo_str, '', '', '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '', '', ""]
                    with open(f"c:\\asics_pl\\csv_data\\{group}.csv", "a",
                              errors='ignore', encoding="utf-8") as file:
                        writer = csv.writer(file, delimiter=",", lineterminator="\r")
                        writer.writerow((data))
                    index_photo += 1

def move_img():
    folders = {
        r'c:\asics_pl\csv_data\img_kids-gear': r'c:\asics_pl\data_img\img_kids-gear',
        r'c:\asics_pl\csv_data\img_mens-gear': r'c:\asics_pl\data_img\img_mens-gear',
        r'c:\asics_pl\csv_data\img_womens-gear': r'c:\asics_pl\data_img\img_womens-gear'
    }

    for src, dest in folders.items():
        for root, dirs, files in os.walk(src):
            dest_root = root.replace(src, dest)
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_root, file)
                shutil.move(src_path, dest_path)

def del_files_html_product():
    folders_del = [r"c:\asics_pl\html_product\kids-gear",
               r"c:\asics_pl\html_product\mens-gear",
               r"c:\asics_pl\html_product\womens-gear"
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
    # save_url_csv()
    # drop_duplicates()
    # main_asio()
    parsin_contact_html()
