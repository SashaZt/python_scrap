# import os
# import xml.etree.ElementTree as ET
# import csv
#
# # Множество для хранения уже встреченных городов
# seen_cities = set()
#
# # Просмотр всех файлов в директории
# for filename in os.listdir('C:/scrap_tutorial-master/Temp/poland/')[0:1]:
#     if filename.endswith('.osm'):
#         # Открытие CSV файла для записи
#         name_csv = filename.replace(".osm", '')
#         print(name_csv)
#
#         # Проверка, существует ли файл
#         if not os.path.exists(f'{name_csv}.csv'):
#             filepath = os.path.join('C:/scrap_tutorial-master/Temp/poland/', filename)
#
#             # Загрузка и парсинг XML файла
#             tree = ET.parse(filepath)
#             root = tree.getroot()
#
#             # Открываем CSV файл здесь, чтобы он оставался открытым во время работы с XML.
#             with open(f'{name_csv}.csv', 'w', newline='', encoding='utf-8') as csvfile:
#                 fieldnames = ['City']
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#                 # Запись заголовков
#                 writer.writeheader()
#
#                 # Обход всех узлов (node) в OSM XML
#                 for node in root.findall('node'):
#                     # Словарь для хранения интересующих нас тегов
#                     interesting_tags = {}
#
#                     # Обход дочерних элементов (например, тегов)
#                     for tag in node.findall('tag'):
#                         k = tag.get('k')
#                         v = tag.get('v')
#
#                         # Проверка, является ли тег интересующим нас
#                         if k == 'name':
#                             interesting_tags[k] = v
#
#                     # Если найден интересующий нас тег 'name' и его значение еще не встречалось.
#                     if 'name' in interesting_tags and interesting_tags['name'] not in seen_cities:
#                         seen_cities.add(interesting_tags['name'])
#                         writer.writerow({
#                             'City': interesting_tags['name']
#                         })

# import os
# import csv
#
# # Укажите путь к папке с CSV-файлами
# folder_path = "C:\\scrap_tutorial-master\\Temp\\poland\\"
#
# # Пройдитесь по всем файлам в указанной папке
# for filename in os.listdir(folder_path):
#     # Проверьте, является ли файл CSV-файлом
#     if filename.endswith('.csv'):
#         filepath = os.path.join(folder_path, filename)
#
#         # Откройте каждый CSV-файл и прочитайте его содержимое
#         with open(filepath, 'r', encoding='utf-8') as file:
#             csv_reader = csv.reader(file)
#             # ... остальной код
#
#             # Подсчитайте количество строк в файле
#             row_count = sum(1 for row in csv_reader)
#
#             # Выведите имя файла и количество строк
#             print(f"{filename}: {row_count} строк")

"""Рабочий код"""

import os
import xml.etree.ElementTree as ET
import json

# Список для хранения всех "воеводств" и их городов
all_voevodstvo = []

# Множество для хранения уже встреченных городов (для всех воеводств)
seen_cities = set()

# Просмотр всех файлов в директории
for filename in os.listdir('C:/scrap_tutorial-master/Temp/che/'):
    if filename.endswith('.osm'):
        # Открытие CSV файла для записи
        name_csv = filename.replace(".osm", '').replace('-latest', '')
        print(name_csv)

        filepath = os.path.join('C:/scrap_tutorial-master/Temp/che/', filename)

        # Загрузка и парсинг XML файла
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Множество для хранения городов текущего воеводства
        current_cities = set()

        for node in root.findall('node'):
            addr_tags = {}
            for tag in node.findall('tag'):
                k = tag.get('k')
                v = tag.get('v')


                if k in ['addr:city', 'addr:province', 'addr:place', 'addr:suburb']:
                    addr_tags[k] = v.replace('/', ' ').replace('\\', ' ')

            # Следуя вашим условиям, выбираем нужный тег
            if 'addr:city' in addr_tags:
                selected_value = addr_tags['addr:city']
            elif 'addr:province' in addr_tags:
                selected_value = addr_tags['addr:province']
            elif 'addr:place' in addr_tags:
                selected_value = addr_tags['addr:place']
            elif 'addr:suburb' in addr_tags:
                selected_value = addr_tags['addr:suburb']
            else:
                continue  # пропускаем этот узел, если не нашли нужных тегов

            if selected_value not in seen_cities:
                seen_cities.add(selected_value)
                current_cities.add(selected_value)


        # Добавляем текущее воеводство и его города в общий список
        all_voevodstvo.append({
            'voevodstvo': name_csv.replace('-latest', ''),
            'cities': list(current_cities)
        })








        # Сохраняем данные в JSON файл
        with open(f'{name_csv}.json', 'w', encoding='utf-8') as f:
            json.dump(all_voevodstvo, f, ensure_ascii=False, indent=4)
        """Рабочий код"""







# import os
# import xml.etree.ElementTree as ET
# import json
#
# # Множество для хранения уникальных тегов, начинающихся на 'addr:'
# unique_addr_tags = set()
#
# # Просмотр всех файлов в директории
# for filename in os.listdir('C:/scrap_tutorial-master/Temp/poland/')[:1]:
#     if filename.endswith('.osm'):
#         filepath = os.path.join('C:/scrap_tutorial-master/Temp/poland/', filename)
#         print(f"Processing {filepath}...")
#
#         # Загрузка и парсинг XML файла
#         tree = ET.parse(filepath)
#         root = tree.getroot()
#
#         # Проходимся по всем узлам и их тегам
#         for node in root.findall('node'):
#             for tag in node.findall('tag'):
#                 k = tag.get('k')
#
#                 # Проверяем, начинается ли тег на 'addr:' и не встречался ли он раньше
#                 if k.startswith('addr:') and k not in unique_addr_tags:
#                     unique_addr_tags.add(k)
#
# # Выводим уникальные теги
# print("Unique 'addr:' tags:")
# for tag in unique_addr_tags:
#     print(tag)
