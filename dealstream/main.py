import csv
import glob
import requests
import os
from pathlib import Path
from multiprocessing import Pool


current_directory = os.getcwd()
temp_directory = 'temp'
# Создайте полный путь к папке temp
temp_path = os.path.join(current_directory, temp_directory)
list_path = os.path.join(temp_path, 'list')
product_path = os.path.join(temp_path, 'product')

api_key = 'a818a4bc04f177c7ae82bb950ccf95ac'


def delete_old_data():
    # Убедитесь, что папки существуют или создайте их
    for folder in [temp_path, list_path, product_path]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Удалите файлы из папок list и product
    for folder in [list_path, product_path]:
        files = glob.glob(os.path.join(folder, '*'))
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
        # print(f'Очистил папку {os.path.basename(folder)}')
# Функция для скачивания и сохранения данных по URL
def download_url(url, index):
    headers = {
        # Вставьте ваш заголовок сюда
    }
    filename = os.path.join(product_path, f'data_{index}.html')
    if not os.path.exists(filename):
        try:
            # response = requests.get(url, headers=headers)
            response = requests.get(f'http://api.scraperapi.com?api_key={api_key}&url={url}')
            src = response.text
            with open(filename, "w", encoding='utf-8') as file:
                file.write(src)
        except Exception as e:
            print(f"Ошибка при скачивании URL {url}: {str(e)}")

# Функция для обработки одного процесса
def process_chunk(chunk, start_index):
    for index, url in enumerate(chunk, start=start_index):
        download_url(url, index)

def get_requests():
    if __name__ == "__main__":
        # Загрузите список URL из файла csv
        csv_file = Path('c:/scrap_tutorial-master/exist/') / 'url_amortyzatory.csv'
        with open(csv_file, 'r') as file:
            url_list = [line.strip() for line in file]

        # Разделите список URL на части для каждого процесса
        num_processes = 5  # Укажите количество желаемых процессов
        chunk_size = len(url_list) // num_processes
        chunks = [url_list[i:i + chunk_size] for i in range(0, len(url_list), chunk_size)]

        # Создайте пул процессов и выполните обработку URL
        with Pool(processes=num_processes) as pool:
            pool.starmap(process_chunk, [(chunk, i * chunk_size) for i, chunk in enumerate(chunks)])

if __name__ == "__main__":
    delete_old_data()
    # get_requests()



# """Рабочий код"""
# from bs4 import BeautifulSoup
# import csv
# import glob
# import re
# import requests
# import json
# import cloudscraper
# import os
# import time
# import undetected_chromedriver as webdriver
# from selenium.common.exceptions import TimeoutException
# # from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from concurrent.futures import ThreadPoolExecutor
# import csv
#
# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from concurrent.futures import ThreadPoolExecutor
# import requests
#
# api_key = 'a818a4bc04f177c7ae82bb950ccf95ac'
# url = 'https://exist.ru/Price/?pid=6D6023C3'
#
#
# def get_requests():
#     response = requests.get(f'http://api.scraperapi.com?api_key={api_key}&url={url}')
#     src = response.text
#     filename = f"amazon.html"
#     with open(filename, "w", encoding='utf-8') as file:
#         file.write(src)
#
#
# def parsing():
#     heandler = ['name', 'description', 'url', 'productid', 'image', 'logo', 'price', 'priceCurrency', 'addressCountry',
#                 'addressLocality', 'addressRegion','industry']
#     with open('output.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file, delimiter=";")
#         writer.writerow(heandler)
#
#         file = f"amazon.html"
#         with open(file, encoding="utf-8") as file:
#             src = file.read()
#         soup = BeautifulSoup(src, 'lxml')
#         script = soup.find_all('script', type="application/ld+json")[0]
#         data_json = json.loads(script.string)
#         rows = soup.find_all('div', attrs={"class": "list-group-item post"})
#
#         for j, r in zip(data_json['about'], rows):
#             name = j.get('item', {}).get('name', None)
#             description = j.get('item', {}).get('description', None)
#             url = j.get('item', {}).get('url', None)
#             productid = j.get('item', {}).get('productid', None)
#             image = j.get('item', {}).get('image', None)
#             logo = j.get('item', {}).get('logo', None)
#             price = j.get('item', {}).get('offers', {}).get('price', None)
#             priceCurrency = j.get('item', {}).get('offers', {}).get('priceCurrency', None)
#             addressCountry = j.get('item', {}).get('offers', {}).get('availableAtOrFrom', {}).get('address', {}).get(
#                 'addressCountry', None)
#             addressLocality = j.get('item', {}).get('offers', {}).get('availableAtOrFrom', {}).get('address', {}).get(
#                 'addressLocality', None)
#             addressRegion = j.get('item', {}).get('offers', {}).get('availableAtOrFrom', {}).get('address', {}).get(
#                 'addressRegion', None)
#             industry = r.find('span', attrs={"title": "Industry"}).text
#
#             values = [name, description, url, productid, image, logo, price, priceCurrency, addressCountry,
#                       addressLocality, addressRegion, industry]
#
#             writer.writerow(values)
#
#
# if __name__ == '__main__':
#     # get_requests()
#     # get_cloudscraper()
#     # get_selenium()
#     parsing()
