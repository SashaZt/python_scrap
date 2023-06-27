from bs4 import BeautifulSoup
import csv
import os
import glob
import random
from proxi import proxies
from headers_cookies import cookies, headers
import requests
import re
from pathlib import Path
import time


def get_categories_to_html_file():
    url_all = []
    name_files = Path('c:/data_wmmotor/') / 'all_categories_url.html'
    response = requests.get('http://www.wmmotor.pl/hurtownia/drzewo.php',
                            headers=headers, cookies=cookies)  # , cookies=cookies
    if response.status_code == 200:
        src = response.text
        soup = BeautifulSoup(src, 'lxml')

        with open(name_files, "w", encoding='utf-8') as file:
            file.write(response.text)
        with open('categories.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            with open(name_files, encoding="utf-8") as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')
            table_treee = soup.find('td', attrs={'class': 'boxContentsMainNoBorder'})
            treelevel1 = table_treee.find_all('a', attrs={'class': 'treelevel1'})

            for item in treelevel1:
                urls = 'http://www.wmmotor.pl/hurtownia/' + item.get('href')
                url_all.append(urls)

            for url in url_all:
                writer.writerow([url])
    else:
        print(response.status_code)


def get_urls_product():
    name_files = 'categories.csv'

    with open(name_files, newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        count = 0
        for url in urls:
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
            count += 1
            response = requests.get(url[0],
                                    headers=headers, cookies=cookies, proxies=proxi)  # , cookies=cookies
            src = response.text
            soup = BeautifulSoup(src, 'lxml')
            group = soup.find_all('a', attrs={'class': 'nodecoration'})[1].text.replace(" - ", "_").replace(",",
                                                                                                            "").replace(
                ".", "").replace("  ", " ").replace(" ", "_").replace("/", "_")
            table_pagin = int(
                soup.find('td', attrs={'class': 'boxContentsMainNoBorder'}).find('td', attrs={
                    'valign': 'middle'}).text.replace("razem towarów: ", ""))
            amount_page = table_pagin // 50
            all_urls = []
            count = 0
            for i in range(1, amount_page + 2):
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
                count += 1
                print(f"{count} из {amount_page + 2}")
                pause_time = random.randint(1, 10)
                name_files = Path(f'c:/data_wmmotor/list/') / 'data.csv'
                if i == 1:
                    response = requests.get(url[0],
                                            headers=headers, cookies=cookies, proxies=proxi)  # , cookies=cookies

                    src = response.text
                    soup = BeautifulSoup(src, 'lxml')
                    product_listing_even = soup.find('table', attrs={'class': 'productListing'}).find_all('td', attrs={
                        'class': 'productListingEven'})
                    product_listing_odd = soup.find('table', attrs={'class': 'productListing'}).find_all('td', attrs={
                        'class': 'productListingOdd'})
                    all_products = product_listing_even + product_listing_odd
                    for u in all_products:
                        url_ = u.find_all('a')
                        for a_tag in url_:
                            href = a_tag['href']
                            if 'towar.php' in href:
                                url_to_write = 'http://www.wmmotor.pl/hurtownia/' + href
                                with open(name_files, 'a', newline='') as csvfile:
                                    writer = csv.writer(csvfile)
                                    writer.writerow([url_to_write])  # добавление URL в csv
                print(f'Пауза {pause_time}')
                time.sleep(pause_time)

                if i > 1:
                    response = requests.get(f'{url[0]}&page={i}',
                                            headers=headers, cookies=cookies, proxies=proxi)  # , cookies=cookies
                    src = response.text
                    soup = BeautifulSoup(src, 'lxml')
                    product_listing_even = soup.find('table', attrs={'class': 'productListing'}).find_all('td', attrs={
                        'class': 'productListingEven'})
                    product_listing_odd = soup.find('table', attrs={'class': 'productListing'}).find_all('td', attrs={
                        'class': 'productListingOdd'})
                    all_products = product_listing_even + product_listing_odd
                    for u in all_products:
                        url__ = u.find_all('a')
                        for a_tag in url__:
                            href = a_tag['href']
                            if 'towar.php' in href:
                                url_to_write = 'http://www.wmmotor.pl/hurtownia/' + href
                                # all_urls.append('http://www.wmmotor.pl/hurtownia/' + href)
                                with open(name_files, 'a', newline='') as csvfile:
                                    writer = csv.writer(csvfile)
                                    writer.writerow([url_to_write])  # добавление URL в csv
                print(f'Пауза {pause_time}')
                time.sleep(pause_time)


def folders():
    name_files = Path(f'c:/data_wmmotor/list/') / 'data.csv'
    coun = 0
    with open(name_files, newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        for row in urls:
            pause_time = random.randint(1, 3)
            coun += 1
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
            # Предполагается, что URL это первый элемент строки
            url = row[0]

            # Отправляем запрос
            name_files = Path('c:/data_wmmotor/products/') / f'data_{coun}.html'
            if not os.path.exists(name_files):
                response = requests.get(url, headers=headers, cookies=cookies, proxies=proxi)
                with open(name_files, "w", encoding='utf-8') as file:
                    file.write(response.text)
                print(f'Осталось {len(urls) - coun}')


def parsing_products():
    folder = r'c:\data_wmmotor\products\*.html'
    files_html = glob.glob(folder)
    heandler = ['nazva', 'symbol', 'price_netto', 'price_brutto', 'opis_tovaru', 'in_stock', 'category']
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(heandler)  # Записываем заголовки только один раз
        for item in files_html:
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            try:
                table_product = soup.find_all('td', attrs={'colspan': '2'})[0].find_all('td', attrs={'valign': 'top'})[
                    0]
            except:
                continue
            tovar_in_magazine = table_product.find('img', attrs={'title': 'Towar dostępny w naszym magazynie'})
            tovar_in_magazine_big_1 = table_product.find('span', attrs={'title': 'Towar dostępny w naszym magazynie'})
            in_stock = ''
            if tovar_in_magazine or tovar_in_magazine_big_1:
                # product_yes = tovar_in_magazine.get('src')
                # if product_yes:
                in_stock = 9
                try:
                    product_name = table_product.find(class_='productPageName').get_text()
                except:
                    product_name = ""

                try:
                    symbol = table_product.text.split("Symbol: ")[1].split("\n")[0]
                except:
                    symbol = ''
                    print(f'Нет symbol')

                try:
                    price_netto = table_product.find_all(class_='productPageName')[1].get_text().replace(',',
                                                                                                         ".").replace(
                        ' zł', "")
                except:
                    price_netto = ''
                    print(f'Нет price_netto')

                try:
                    price_brutto = table_product.find_all(class_='productPageName')[2].get_text().replace(',',
                                                                                                          ".").replace(
                        ' zł', "")
                except:
                    price_brutto = ''
                    print(f'Нет price_brutto')

                urls_photo = []
                photos = soup.find_all('a', attrs={'rel': 'lightbox[galeria]'})
                for p in photos:
                    url_photo = p.get("href").replace('../', 'http://www.wmmotor.pl/')
                    urls_photo.append(url_photo)
                '//span[@style="font-weight: bold; color: #CE0000;"]'
                category = soup.find('span', attrs={'style': 'font-weight: bold; color: #CE0000;'}).text.replace(
                    '  ', "_").replace(' - ', "_").replace('.', "").replace(',', "").replace(' ', "_")
                # print(category)
                try:
                    opis_tovaru = table_product.find_all('td', attrs={'valign': 'top'})[1].get_text(strip=True)
                except:
                    opis_tovaru = None

                coun = 0
                for u in urls_photo:
                    pause_time = random.randint(1, 3)
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

                    if len(urls_photo) > 1 and coun > 0:
                        file_path = f'c:\\data_wmmotor\\img\\{symbol}_{coun}.jpg'
                    else:
                        file_path = f'c:\\data_wmmotor\\img\\{symbol}.jpg'

                    if not os.path.exists(file_path):
                        try:
                            img_data = requests.get(u, headers=headers, cookies=cookies, proxies=proxi)
                            with open(file_path, 'wb') as file_img:
                                file_img.write(img_data.content)
                        except:
                            print(f"Ошибка при выполнении запроса для URL: {u}")
                    coun += 1

                values = [product_name, symbol, price_netto, price_brutto, opis_tovaru, in_stock, category]
                # print(values)
                writer.writerow(values)  # Дописываем значения из values
            # else:
            #     continue
            # if tovar_in_magazine_big_1:
            #     in_stock = 9
            #     try:
            #         product_name = table_product.find(class_='productPageName').get_text()
            #     except:
            #         product_name = ""
            #
            #     try:
            #         symbol = table_product.text.split("Symbol: ")[1].split("\n")[0]
            #     except:
            #         symbol = ''
            #         print(f'Нет symbol')
            #
            #     try:
            #         price_netto = table_product.find_all(class_='productPageName')[1].get_text().replace(',',
            #                                                                                              ".").replace(
            #             ' zł', "")
            #     except:
            #         price_netto = ''
            #         print(f'Нет price_netto')
            #
            #     try:
            #         price_brutto = table_product.find_all(class_='productPageName')[2].get_text().replace(',',
            #                                                                                               ".").replace(
            #             ' zł', "")
            #     except:
            #         price_brutto = ''
            #         print(f'Нет price_brutto')
            #
            #     urls_photo = []
            #     photos = soup.find_all('a', attrs={'rel': 'lightbox[galeria]'})
            #     for p in photos:
            #         url_photo = p.get("href").replace('../', 'http://www.wmmotor.pl/')
            #         urls_photo.append(url_photo)
            #     '//span[@style="font-weight: bold; color: #CE0000;"]'
            #     category = soup.find('span', attrs={'style': 'font-weight: bold; color: #CE0000;'}).text.replace(
            #         '  ', "_").replace(' - ', "_").replace('.', "").replace(',', "").replace(' ', "_")
            #     # print(category)
            #     try:
            #         opis_tovaru = table_product.find_all('td', attrs={'valign': 'top'})[1].get_text(strip=True)
            #     except:
            #         opis_tovaru = None
            #
            #     coun = 0
            #     for u in urls_photo:
            #         pause_time = random.randint(1, 3)
            #         """Настройка прокси серверов случайных"""
            #         proxy = random.choice(proxies)
            #         proxy_host = proxy[0]
            #         proxy_port = proxy[1]
            #         proxy_user = proxy[2]
            #         proxy_pass = proxy[3]
            #
            #         proxi = {
            #             'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
            #             'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
            #         }
            #
            #         if len(urls_photo) > 1 and coun > 0:
            #             file_path = f'c:\\data_wmmotor\\img\\{symbol}_{coun}.jpg'
            #         else:
            #             file_path = f'c:\\data_wmmotor\\img\\{symbol}.jpg'
            #
            #         if not os.path.exists(file_path):
            #             try:
            #                 img_data = requests.get(u, headers=headers, cookies=cookies, proxies=proxi)
            #                 with open(file_path, 'wb') as file_img:
            #                     file_img.write(img_data.content)
            #             except:
            #                 print(f"Ошибка при выполнении запроса для URL: {u}")
            #         coun += 1
            #
            #     values = [product_name, symbol, price_netto, price_brutto, opis_tovaru, in_stock, category]
            #     # print(values)
            #     writer.writerow(values)  # Дописываем значения из values



if __name__ == '__main__':
    # get_categories_to_html_file()
    # get_urls_product()
    # folders()
    parsing_products()
