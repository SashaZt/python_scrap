import time
import glob
import requests
import os
import json
import csv
from config import cookies, headers
from bs4 import BeautifulSoup

current_directory = os.getcwd()
temp_directory = 'temp'
# Создайте полный путь к папке temp
temp_path = os.path.join(current_directory, temp_directory)
json_path = os.path.join(temp_path, 'json')
json_product = os.path.join(temp_path, 'json_product')
json_tags = os.path.join(temp_path, 'json_tags')
json_statistic = os.path.join(temp_path, 'json_statistic')
html_path = os.path.join(temp_path, 'html')

"""Создание временых папок"""


def creative_temp_folders():
    # Убедитесь, что папки существуют или создайте их
    for folder in [temp_path, json_path, html_path, json_product, json_tags, json_statistic]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def get_product():
    all_products_keys = parsing_statistic()
    for a in all_products_keys:
        params = {
            'date_range': 'all_time',
            'channel': 'etsy-retail',
        }
        product = a
        response = requests.get(
            f'https://www.etsy.com/api/v3/ajax/bespoke/shop/48000300/stats/dashboard-listing/{product}',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        json_data = response.json()
        filename_tender = os.path.join(json_product, f'product_{product}.json')
        with open(filename_tender, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
        time.sleep(10)


def pars_product():
    filename_tender = os.path.join(json_product, 'product*.json')
    filenames = glob.glob(filename_tender)
    all_objects = []
    for filename in filenames:
        with open(filename, 'r', encoding="utf-8") as f:
            data_json = json.load(f)
        json_data = data_json['pages']
        listing_id = \
            json_data[0]['list'][0]['stacked_graphs_view'][0]['inventory_detail']['datasets'][0]['entries'][0][
                'listing'][
                'listing_id']
        listing_title = \
            json_data[0]['list'][0]['stacked_graphs_view'][0]['inventory_detail']['datasets'][0]['entries'][0][
                'listing'][
                'title']
        """Данные по таблицам"""
        all_data_table_01_data = json_data[0]['list'][2]['filters'][0]['options']
        all_data_table_02_data = json_data[0]['list'][3]['stacked_graphs_view'][0]['donut_chart']['datasets'][0][
            'entries']
        all_data_table_03_data = json_data[0]['list'][4]['paginated_view'][0]
        # Итерация по списку entries для получения количества элементов и их обработки

        """Словари по таблицам"""
        dict_table_01 = {entry['label']: entry['total'] for entry in all_data_table_01_data}
        dict_table_02 = {entry['label']: entry['value'] for entry in all_data_table_02_data}
        dict_table_03 = {}

        for item in json_data[0]['list'][4]['paginated_view']:
            # Проверяем, есть ли нужные ключи и данные
            if 'horizontal_line_chart' in item and \
                    'datasets' in item['horizontal_line_chart'] and \
                    len(item['horizontal_line_chart']['datasets']) > 0:

                # Получаем список 'entries'
                entries = item['horizontal_line_chart']['datasets'][0]['entries']

                # Итерация по каждому 'entry' для заполнения словаря
                for entry in entries:
                    # Проверяем, есть ли 'label' и 'value' в 'entry'
                    if 'label' in entry and 'value' in entry:
                        # Добавляем пару в словарь
                        dict_table_03[entry['label']] = entry['value']

        current_object = {
            "object": {
                "listing_id": listing_id,
                "title": listing_title
            },
            "dict_table_01": dict_table_01,
            "dict_table_02": dict_table_02,
            "dict_table_03": dict_table_03
        }
        all_objects.append(current_object)
    with open('all_product.json', 'w', encoding='utf-8') as f:
        json.dump(all_objects, f, ensure_ascii=False, indent=4)  # Записываем в файл

    # # Объединение ключей всех словарей
    # headers = list(set(dict_table_01) | set(dict_table_02) | set(dict_table_03))
    #
    # # Создание и запись в CSV файл
    # with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=headers)
    #
    #     # Запись заголовков
    #     writer.writeheader()
    #
    #     # Объединение данных из всех трех словарей в один словарь для записи
    #     combined_data = {}
    #     for header in headers:
    #         combined_value = str(dict_table_01.get(header, '')) + str(dict_table_02.get(header, '')) + str(
    #             dict_table_03.get(header, ''))
    #         combined_data[header] = combined_value
    #
    #     # Запись объединенных данных
    #     writer.writerow(combined_data)


def get_json_tags():
    search_pattern = os.path.join(json_tags, f'product_*.json')
    matching_files = glob.glob(search_pattern)

    # Подсчёт количества найденных файлов
    number_of_files = (len(matching_files) // 40) + 1
    offset = 0
    for p in range(0, number_of_files):
        params = {
            'limit': '40',
            'offset': offset,
            'sort_field': 'ending_date',
            'sort_order': 'descending',
            'state': 'inactive',
            'language_id': '0',
            'query': '',
            'shop_section_id': '',
            'listing_tag': '',
            'is_featured': '',
            'shipping_profile_id': '',
            'return_policy_id': '',
            'production_partner_id': '',
            'is_retail': 'true',
            'is_retail_only': '',
            'is_pattern': '',
            'is_pattern_only': '',
            'is_digital': '',
            'channels': '',
            'is_waitlisted': '',
            'has_video': '',
        }

        response = requests.get(
            'https://www.etsy.com/api/v3/ajax/shop/48000300//listings/search',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        json_data = response.json()
        filename_tender = os.path.join(json_tags, f'tags_{offset}.json')
        with open(filename_tender, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
        offset += 40
        time.sleep(10)


def par_tags():
    filename_tags = os.path.join(json_tags, 'tags*.json')
    filenames = glob.glob(filename_tags)
    all_objects = []  # список для хранения всех словарей
    for filename in filenames:
        with open(filename, 'r', encoding="utf-8") as f:
            data_json = json.load(f)
        json_data = data_json
        all_tags = []
        for i, entry in enumerate(json_data):
            listing_id = entry['listing_id']
            title = entry['title']
            tags = entry['tags']
            current_object = {
                "listing_id": entry['listing_id'],
                "object": {
                    "title": entry['title'],
                    "tags": entry['tags']
                    # Обратите внимание, что здесь должно быть "tags": entry['tags'], а не просто tags: entry['tags']
                }
            }
            all_objects.append(current_object)
    with open('all_tags.json', 'w', encoding='utf-8') as f:
        json.dump(all_objects, f, ensure_ascii=False, indent=4)  # Записываем в файл
    # print(all_objects)
            # Добавляем словарь в список
        #     all_objects.append(current_object)
        #     values = [listing_id, title, tags]
        #     all_tags.extend(values)
        #     # all_products.update(dict_table_04)
        # print(all_tags)


"""Скачать все индетификаторы продуктов"""


def get_page_statistic():
    params = {
        'date_range': 'all_time',
        'channel': 'etsy-retail',
        'limit': '5',
        'offset': '0',
        'sort_direction': 'DESC',
        'sort_by': 'visits',
        'selected_listings_filter': 'all',
    }

    response = requests.get(
        'https://www.etsy.com/api/v3/ajax/bespoke/shop/48000300/shop-analytics-stats/listings',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    json_data = response.json()
    filename_tender_statistic = os.path.join(json_statistic, 'statistic.json')
    with open(filename_tender_statistic, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл

    with open(filename_tender_statistic, 'r', encoding="utf-8") as f:
        data_json = json.load(f)
    json_data = data_json
    pages = int(json_data['pagination']['total_pages'])
    print(f'Всего страниц {pages}')
    pages = pages + 1
    offset = 5
    for p in range(2, pages):
        params = {
            'date_range': 'all_time',
            'channel': 'etsy-retail',
            'limit': '5',
            'offset': offset,
            'sort_direction': 'DESC',
            'sort_by': 'visits',
            'selected_listings_filter': 'all',
        }
        response = requests.get(
            'https://www.etsy.com/api/v3/ajax/bespoke/shop/48000300/shop-analytics-stats/listings',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        json_data = response.json()
        filename_tender_statistic = os.path.join(json_path, f'statistic_{offset}.json')
        with open(filename_tender_statistic, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл

        offset += 5
        print(f'Страница {p}')
        time.sleep(10)


def parsing_statistic():
    filename_tender = os.path.join(json_statistic, 'statistic*.json')
    filenames = glob.glob(filename_tender)
    all_products = {}
    for filename in filenames:
        with open(filename, 'r', encoding="utf-8") as f:
            data_json = json.load(f)
        json_data = data_json
        dict_table_04 = {entry['id']: entry['title'] for entry in json_data['listings']}
        all_products.update(dict_table_04)
    all_products_keys = list(all_products.keys())
    return all_products_keys


if __name__ == '__main__':
    # creative_temp_folders()
    # get_product()
    pars_product()
    # get_json_tags()
    # par_tags()
    # get_page_statistic()
