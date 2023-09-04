from datetime import datetime
import json
import html
import csv
import requests
from bs4 import BeautifulSoup
from headers_cookies import cookies, headers
import os
import glob
from collections import defaultdict
import shutil
# from proxi import proxies



def get_requests(url):
    # Получаем значение переменной окружения USERPROFILE
    user_profile = os.environ.get('USERPROFILE')

    # Создаем путь к новой папке
    new_folder_path = os.path.join(user_profile, 'prom')

    # Создаем папку
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    url = f'{url}testimonials'
    response = requests.get(url, cookies=cookies, headers=headers)
    src = response.text
    # filename = f"amazon.html"
    # with open(filename, "w", encoding='utf-8') as file:
    #     file.write(src)
    soup = BeautifulSoup(src, 'lxml')
    pagin_old = int(soup.find('div', attrs={'class': 'b-pager'}).find('div', {'data-pagination-pages-count': True})[
                        'data-pagination-pages-count'])
    with open(f'{new_folder_path}\\urls.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(1, pagin_old + 1):
            page = f'{url}/page_{i}'
            writer.writerow([page])

def pars():
    # Получаем значение переменной окружения USERPROFILE
    user_profile = os.environ.get('USERPROFILE')

    # Создаем путь к новой папке
    new_folder_path = os.path.join(user_profile, 'prom')
    files_html = glob.glob(os.path.join(new_folder_path, '*.html'))
    with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for item_html in files_html:
            with open(item_html, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            url_site = soup.find('a', attrs={'class': 'b-header-company-name__logo'}).get('href')
            url_site = url_site.replace("teplowest.com.ua/ua/", "teplowest.com.ua")

            table_comments = soup.find('ul', attrs={'class': 'b-comments__list'})
            comments = table_comments.find_all('li', attrs={'class': 'b-comments__item'})
            for c in comments:
                data_comments = c.find('div', attrs={'class': 'b-comments__item-table'}).find('div', attrs={'class': 'b-comments__item-table-cell b-comments__item-table-cell_type_date'}).find('time', attrs={'class': 'b-date'}).get('datetime')
                dt_object = datetime.strptime(data_comments, "%Y-%m-%dT%H:%M:%S")
                formatted_date = dt_object.strftime("%d.%m.%Y")
                try:
                    product_comments = c.find('div', attrs={'class': 'b-comments__answer'}).get('data-reviews-products')
                except:
                    product = []
                    product.append(formatted_date)  # Сначала дата
                    # product.append(item_html)
                    url_no_category = 'Нет url'
                    name_no_category = 'Без названия товара'
                    product.append(url_no_category)
                    product.append(name_no_category)
                    writer.writerow(product)
                if product_comments is not None:
                    decoded_str = html.unescape(product_comments)
                    # Декодирование JSON
                    data = json.loads(decoded_str)
                    for item in data:
                        product = []
                        if item['url']:
                            url = f"{url_site}{item['url']}"
                        else:
                            url ='Нет url'
                        product.append(formatted_date)
                        product.append(url)
                        product.append(item['name'])
                        writer.writerow(product)
                else:
                    product = []
                    product.append(formatted_date)  # Сначала дата
                    # product.append(item_html)
                    url_no_category = 'Нет url'
                    name_no_category = 'Без названия товара'
                    product.append(url_no_category)
                    product.append(name_no_category)
                    writer.writerow(product)

def analis_product():
    import csv
    from collections import defaultdict

    # Читаем данные из исходного CSV файла
    data = []
    with open('products.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            data.append(row)

    # Собираем статистику по годам и товарам
    stats_by_year_and_product = defaultdict(lambda: defaultdict(int))
    product_urls = {}  # для хранения URL каждого продукта

    # Получаем уникальные года и сортируем их
    unique_years = sorted({date.split('.')[-1] for date, _, _ in data}, reverse=True)

    total_count = 0  # Итого по всем позициям и всем годам

    # Пишем в новый CSV файл
    with open('products_.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')

        # Заголовок
        writer.writerow(['Название продукта', 'url'] + unique_years + ['Итого'])

        for row in data:
            date, url, product_name = row
            year = date.split('.')[-1]
            stats_by_year_and_product[product_name][year] += 1
            product_urls[product_name] = url  # сохраняем URL продукта

        for product_name, stats in stats_by_year_and_product.items():
            row = [product_name, product_urls.get(product_name, 'No URL')]  # извлекаем URL из словаря product_urls
            total_for_product = 0  # сумма отзывов для данного продукта по всем годам
            for year in unique_years:
                count_for_year = stats.get(year, 0)
                row.append(count_for_year)
                total_for_product += count_for_year
            row.append(total_for_product)  # добавляем колонку "Итого" в каждую строку
            total_count += total_for_product  # обновляем итоговую сумму по всем позициям и всем годам
            writer.writerow(row)

        # Добавляем строку с итоговой суммой
        writer.writerow(['', '', ] + ['' for _ in unique_years] + [total_count])


if __name__ == '__main__':
    # site = input()
    # get_requests(site)
    # pars()
    analis_product()
