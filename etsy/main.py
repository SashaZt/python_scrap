import time
import glob
import requests
import os
import json
import re
from config import cookies, headers, shop, time_a, time_b
from bs4 import BeautifulSoup
import gspread
import numpy as np
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import random

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

spreadsheet_id = '1DVFlQ_UI2JdJb-smkjKXnMa20YwhKbOzJ1UAU9MGi-E'


def get_google():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    creds_file = os.path.join(current_directory, 'access.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    client = gspread.authorize(creds)
    return client, spreadsheet_id


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
        filename_tender = os.path.join(json_product, f'product_{product}.json')
        if not os.path.exists(filename_tender):
            response = requests.get(
                f'https://www.etsy.com/api/v3/ajax/bespoke/shop/{shop}/stats/dashboard-listing/{product}',
                params=params,
                cookies=cookies,
                headers=headers,
            )
            json_data = response.json()

            with open(filename_tender, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
            sleep_time = random.randint(time_a, time_b)
            time.sleep(sleep_time)


def split_into_words(text):
    # Убираем знаки пунктуации и разбиваем по пробелам, приводя всё к нижнему регистру
    return re.findall(r'\b\w+\b', text.lower())


def pars_product():
    client, spreadsheet_id = get_google()
    sheet = client.open_by_key(spreadsheet_id).worksheet('Парсинг тест')

    filename_tender = os.path.join(json_product, 'product*.json')
    filenames = glob.glob(filename_tender)
    all_objects = []
    all_tags = par_tags()

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
        dict_table_01['Revenue'] = dict_table_01['Revenue'].replace('USD ', '').replace('.', ',')

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

        img_url = \
            json_data[0]['list'][0]['stacked_graphs_view'][0]['inventory_detail']['datasets'][0]['entries'][0][
                'listing'][
                'image']['url']
        url_product = \
        json_data[0]['list'][0]['stacked_graphs_view'][0]['inventory_detail']['datasets'][0]['entries'][0][
            'listing']['url']
        img_url_for_google = f'=IMAGE("{img_url}")'
        current_object = {
            "object": {
                "listing_id": listing_id,
                "title": listing_title,
                "img_url_for_google": img_url_for_google,
                "url_product": url_product
            },
            "dict_table_01": dict_table_01,
            "dict_table_02": dict_table_02,
            "dict_table_03": dict_table_03
        }

        all_objects.append(current_object)

    values = []

    for index, item in enumerate(all_objects, start=2):
        # Найдите теги, соответствующие текущему listing_id
        tags = next((tag_item['object']['tags'] for tag_item in all_tags if
                     tag_item['listing_id'] == item['object']['listing_id']), None)

        # Преобразуйте список тегов в строку, если теги найдены
        tags_str = ', '.join(tags) if tags else ''
        dict_to_string = ', '.join([f"{k}: {v}" for k, v in item['dict_table_03'].items()]) if item[
            'dict_table_03'] else ''
        row_data = [
            item['object']['img_url_for_google'],
            item['object']['title'],
            item['object']['url_product'],
            str(item['dict_table_01'].get('Visits', '')),
            str(item['dict_table_01'].get('Total Views', '')),
            str(item['dict_table_01'].get('Orders', '')),
            str(item['dict_table_01'].get('Revenue', '')),
            item['dict_table_02']['Direct & other traffic'],
            item['dict_table_02']['Etsy app & other Etsy pages'],
            item['dict_table_02']['Etsy Ads'],
            item['dict_table_02']['Etsy marketing & SEO'],
            item['dict_table_02']['Social media'],
            item['dict_table_02']['Etsy search'],
            dict_to_string,  # Используйте преобразованный словарь
            tags_str
        ]
        values.append(row_data)
    new_values = []
    for v in values:
        matched_in_tags_set = set()
        unmatched_in_tags_set = set()
        matched_in_title_set = set()
        unmatched_in_title_set = set()
        title = v[1]
        products = v[13]
        tags_listing = v[14]
        title_words = set(split_into_words(title))
        tags_words = set(split_into_words(tags_listing))
        products_list = re.split(r' : \d+, ?', products)
        for product_info in products_list:
            product_name = product_info.split(" : ")[0]
            # print(f"\nАнализируем продукт: {product_name}")
            # Определяем product_words заранее
            product_words = split_into_words(product_name)

            # Шаг 1
            if product_name.lower() in title.lower():
                print("\nНайдено целиком в заголовке.")
            else:
                print("\nНе найдено целиком в заголовке.")
            # Шаг 2
            product_words = split_into_words(product_name)
            product_words = [re.sub(r'\d+', '', word) for word in product_words if re.sub(r'\d+', '', word)]

            matched_in_title = [word for word in product_words if word in title_words]
            unmatched_in_title = [word for word in product_words if word not in title_words]

            matched_in_title_set.update(matched_in_title)
            unmatched_in_title_set.update(unmatched_in_title)

            # Шаг 3
            matched_in_tags = [word for word in product_words if word in tags_words]
            unmatched_in_tags = [word for word in product_words if word not in tags_words and word]
            matched_in_tags_set.update(matched_in_tags)
            unmatched_in_tags_set.update(unmatched_in_tags)

            #     # Обновляем множества на основе сравнения слов продукта с заголовками и тегами
            #     matched_in_title_set.update(word for word in product_words if word in title_words)
            #     unmatched_in_title_set.update(word for word in product_words if word not in title_words)
            #     matched_in_tags_set.update(word for word in product_words if word in tags_words)
            #     unmatched_in_tags_set.update(word for word in product_words if word not in tags_words)
            #
            # Преобразуем множества в списки и формируем строку для Google Sheets
            # Преобразовываем множества в списки и объединяем их в одну строку для добавления
        matched_in_tags_str = ", ".join(list(matched_in_tags_set))
        unmatched_in_tags_str = ", ".join(list(unmatched_in_tags_set))
        matched_in_title_str = ", ".join(list(matched_in_title_set))
        unmatched_in_title_str = ", ".join(list(unmatched_in_title_set))
        # print(matched_in_tags_str)
        # print(unmatched_in_tags_str)
        # print(matched_in_title_str)
        # print(unmatched_in_title_str)
        # exit()
        # Создаем новую строку, добавляя результаты анализа к исходным данным
        new_row = v + [matched_in_tags_str, unmatched_in_tags_str, matched_in_title_str, unmatched_in_title_str]
        new_values.append(new_row)
        # print(matched_in_tags_list)
        # print(unmatched_in_tags_list)
        # print(matched_in_title_list)
        # print(unmatched_in_title_list)
        #
        # # Формируем одну строку данных для добавления в new_values
        # new_values_row = matched_in_tags_list + unmatched_in_tags_list + matched_in_title_list + unmatched_in_title_list
        # new_values.append([new_values_row])  # Добавляем как один элемент (строку данных)
    # print(new_values)
    # new_values.append(matched_in_tags_list)
    # new_values.append(unmatched_in_tags_list)
    # new_values.append(matched_in_title_list)
    # new_values.append(unmatched_in_title_list)
    # # Выводим итоговые множества
    # print("\nИтоговые множества:")
    # print("Слова, найденные в заголовке:", matched_in_title_set)
    # print("Слова, не найденные в заголовке:", unmatched_in_title_set)
    # print("Слова, найденные в тегах:", matched_in_tags_set)
    # print("Слова, не найденные в тегах:", unmatched_in_tags_set)
    # print("Слова, найденные в тегах:", ", ".join(matched_in_tags) if matched_in_tags else "нет совпадений")
    # print("Слова, не найденные в тегах:",
    #       ", ".join(unmatched_in_tags) if unmatched_in_tags else "все слова найдены")

    # """"Рабочий код"""
    # for v in values[5:6]:
    #     # print(v[1]) #title
    #     # print(v[12]) #dict_table_03
    #     # print(v[13]) #tags_listing
    #     # Разбиваем строку с описанием на отдельные продукты
    #     products = v[12].split(", ")
    #
    #     # Извлекаем названия продуктов
    #     product_names = [product.split(" : ")[0] for product in products]
    #     for product_name in product_names:
    #         # Проверка полного совпадения названия продукта с заголовком
    #         found_match = False
    #         if product_name in v[1]:
    #             print(f"Полное совпадение найдено: {product_name}")
    #         else:
    #             # Проверяем совпадение по словам, если полного совпадения нет
    #             matched_words = []
    #             for word in product_name.split(" "):
    #                 if word.lower() in v[1].lower():  # Добавлено .lower() для регистронезависимой проверки
    #                     matched_words.append(word)
    #
    #             # Выводим найденные слова, если они есть
    #             if matched_words:
    #                 print(f"Слова, найденные в заголовке для '{product_name}': {', '.join(matched_words)}")
    #                 # Для добавления тегов в список, если они соответствуют условиям
    #                 matching_tags = [tag for tag in v[13].split(", ") if
    #                                  any(word.lower() in tag.lower() for word in matched_words)]
    #                 print(f"Соответствующие теги для '{product_name}': {', '.join(matching_tags)}")
    #             else:
    #                 print(f"Нет совпадений по словам для: {product_name}")
    #                 # Если совпадений не найдено, выводим сообщение об этом
    #         if not found_match:
    #             print(f"Совпадения для не найдены '{product_name}.")
    # # Проверяем полное совпадение первого продукта
    # if product_names[0] in v[1]:
    #     print(f"Полное совпадение найдено: {product_names[0]}")
    # else:
    #     # Проверяем совпадение по словам, если полного совпадения нет
    #     matched_words = []
    #     for word in product_names[0].split(" "):
    #         if word in v[1].lower():
    #             matched_words.append(word)
    #
    #     print(f"Слова, найденные во второй колонке: {', '.join(matched_words)}")

    # Для добавления тегов в список, если они соответствуют условиям
    # matching_tags = [tag for tag in v[13].split(", ") if any(word in tag for word in matched_words)]
    # print(f"Соответствующие теги: {', '.join(matching_tags)}")
    # print(new_values)
    try:
        # Отправляем данные в Google Sheets, начиная с ячейки A2
        # ВАЖНО: Убедитесь, что формат 'new_values' подходит для вашей задачи
        # Возможно, потребуется дополнительная обработка для корректной записи в таблицу
        sheet.update(new_values, 'A2', value_input_option='USER_ENTERED')
    except Exception as e:
        print(f"Произошла ошибка при обновлении Google Sheets: {e}")

    # with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file, delimiter=";")
    #     for w in values:
    #         writer.writerow(w)
    # """Запись в Google Таблицу"""
    # # Читаем CSV файл
    # df = pd.read_csv('output.csv', sep=";")
    #
    # # Конвертируем DataFrame в список списков
    # values = df.values.tolist()
    #
    # # Добавляем заголовки столбцов в начало списка
    # values.insert(0, df.columns.tolist())
    #
    # # Очистка всего листа
    # # sheet.clear()
    # # Обновляем данные в Google Sheets
    # sheet.update(values, 'A1')
    # Запись данных одним запросом
    # range = f'A2:C{1 + len(all_objects)}'  # Например, 'A2:C12'
    # sheet.batch_update([{
    #     'range': range,
    #     'values': values
    # }])
    # with open('all_product.json', 'w', encoding='utf-8') as f:
    #     json.dump(all_objects, f, ensure_ascii=False, indent=4)  # Записываем в файл

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
        filename_tender = os.path.join(json_tags, f'tags_{offset}.json')
        if not os.path.exists(filename_tender):
            response = requests.get(
                f'https://www.etsy.com/api/v3/ajax/shop/{shop}/listings/search',
                params=params,
                cookies=cookies,
                headers=headers,
            )
            json_data = response.json()

            with open(filename_tender, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
            offset += 40
            sleep_time = random.randint(time_a, time_b)
            time.sleep(sleep_time)


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
    return all_objects
    # with open('all_tags.json', 'w', encoding='utf-8') as f:
    #     json.dump(all_objects, f, ensure_ascii=False, indent=4)  # Записываем в файл
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
    filename_tender_statistic = os.path.join(json_statistic, 'statistic.json')
    if not os.path.exists(filename_tender_statistic):
        response = requests.get(
            f'https://www.etsy.com/api/v3/ajax/bespoke/shop/{shop}/shop-analytics-stats/listings',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        json_data = response.json()

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
        filename_tender_statistic = os.path.join(json_statistic, f'statistic_{offset}.json')
        if not os.path.exists(filename_tender_statistic):
            response = requests.get(
                f'https://www.etsy.com/api/v3/ajax/bespoke/shop/{shop}/shop-analytics-stats/listings',
                params=params,
                cookies=cookies,
                headers=headers,
            )
            json_data = response.json()
            filename_tender_statistic = os.path.join(json_statistic, f'statistic_{offset}.json')
            with open(filename_tender_statistic, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл

            offset += 5
            sleep_time = random.randint(time_a, time_b)
            print(f'Страница {p}')

            time.sleep(sleep_time)


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
    # get_page_statistic()
    # get_product()

    # get_json_tags()

    pars_product()

    # par_tags()
