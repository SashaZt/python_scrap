# import csv
# import os
# import time
# import cloudscraper
# from typing import List, Dict
# import requests
#
#
# def get_page(url):
#     scraper = cloudscraper.create_scraper(browser={
#         'browser': 'firefox',
#         'platform': 'windows',
#         'mobile': False
#     })
#     proxy = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
#     header = {
#         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
#     }
#     """Get page by url"""
#     try:
#         scraper_get = scraper.get(url).content
#         # response = requests.get(url, headers=header)
#         if scraper_get.status_code == 200:
#             return response.text
#         else:
#             return None
#     except requests.exceptions.RequestException as e:
#         print(e)
#         return None
#
#
# def get_data_and_size(sku):
#     scraper = cloudscraper.create_scraper(browser={
#         'browser': 'firefox',
#         'platform': 'windows',
#         'mobile': False
#     })
#     proxy = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
#     header = {
#         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
#     }
#     """Get data and size json files by SKU"""
#     try:
#         data_url = f"https://www.reebok.pl/api/products/{sku}"
#         data_filename = f"data.json"
#         data_response = requests.get(data_url, headers=header, proxies=proxy)
#         if data_response.status_code == 200:
#             with open(data_filename, "w", encoding='utf-8') as f:
#                 f.write(data_response.text)
#
#         size_url = f"https://www.reebok.pl/api/products/{sku}/availability"
#         size_filename = f"size.json"
#         size_response = requests.get(size_url, headers=header, proxies=proxy)
#         if size_response.status_code == 200:
#             with open(size_filename, "w", encoding='utf-8') as f:
#                 f.write(size_response.text)
#
#         return True
#     except requests.exceptions.RequestException as e:
#         print(e)
#         return False
#
#
# def process_url(url, category):
#     """Process url to get SKU and call get_data_and_size"""
#     if "//www.reebok.pl//" in url:
#         sku = url.split("/")[-1].split(".")[0]
#         dir_path = f"c:\\reebok_pl\\html_product\\{category}\\{sku}"
#         if not os.path.exists(dir_path):
#             os.makedirs(dir_path)
#         os.chdir(dir_path)
#         get_data_and_size(sku)
#
#
# def main_asio():
#     categories = ['img_kids-baby-0-4-years-baby-shoes', 'img_kids-kids-5-8-years-kids-shoes', 'img_kids-youth-9-14', 'img_men-shoes', 'img_women-shoes']
#     for category in categories:
#         time.sleep(2)
#         count = 0
#         with open(f'c:\\reebok_pl\\csv_url\\{category}\\url.csv', newline='', encoding='utf-8') as files:
#             urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
#             for url in urls:
#                 count += 1
#                 process_url(url[0], category)
#                 print(f"{category} | ссылка {count} из {len(urls)}")
#                 time.sleep(2)
#
#
# if __name__ == '__main__':
#     main_asio()
import cloudscraper
import cloudscraper.exceptions
import random
import csv
import os
import re
import time
from typing import List, Dict
import requests


bad_url = []

wait_time = random.uniform(5, 10)
def get_page(url, category):
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })
    """Get page by url"""
    try:
        scraper_get = scraper.get(url).content
        return scraper_get
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def save_html(html, counter, category):
    """Save the html page with the given counter and category"""
    try:
        filename = f"c:\\salomon_pl\\html_product\\{category}\\0_{counter}.html"
        with open(filename, "w", encoding='utf-8') as f:
            f.write(html.decode('utf-8'))
    except cloudscraper.exceptions.CloudflareChallengeError:
        print("Ошибка Cloudflare Challenge. Пропуск URL.")


def process_url(url, counter, category):
    """Process url to get page and save as html"""
    if re.match(r'^https?://', url):
        try:
            html = get_page(url, category)  # передаем аргумент category в get_page()
            if html is not None:
                save_html(html, counter, category)
        except cloudscraper.exceptions.CloudflareChallengeError:
            print("Ошибка Cloudflare Challenge. Пропуск URL.")
            return

def main_asio():
    categories = ['kids', 'men', 'women']
    for category in categories:
        time.sleep(2)
        counter = 0
        with open(f'c:\\salomon_pl\\csv_url\\{category}\\url.csv', newline='', encoding='utf-8') as files:
            urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
            if os.path.isfile(f'c:\\salomon_pl\\csv_url\\{category}\\url.csv'):
                with open(f'c:\\salomon_pl\\csv_url\\{category}\\url.csv', newline='', encoding='utf-8') as files:
                    urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
            for url in urls:
                counter += 1
                filename = f"c:\\salomon_pl\\html_product\\{category}\\0_{counter}.html"
                if os.path.isfile(filename):
                    continue
                process_url(url[0], counter, category)
                print(f"{category} | ссылка {counter} из {len(urls)}")
                time.sleep(wait_time)


if __name__ == '__main__':
    main_asio()
