# import csv
# import os
# import time
# from typing import List, Dict
# import requests
#
#
# def get_page(url):
#     proxy = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
#     header = {
#         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
#     }
#     """Get page by url"""
#     try:
#         response = requests.get(url, headers=header, proxies=proxy)
#         if response.status_code == 200:
#             return response.text
#         else:
#             return None
#     except requests.exceptions.RequestException as e:
#         print(e)
#         return None
#
#
# def get_data_and_size(sku):
#     proxy = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
#     header = {
#         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
#     }
#     """Get data and size json files by SKU"""
#     try:
#         data_url = f"https://www.adidas.pl/api/products/{sku}"
#         data_filename = f"data.json"
#         data_response = requests.get(data_url, headers=header, proxies=proxy)
#         if data_response.status_code == 200:
#             with open(data_filename, "w", encoding='utf-8') as f:
#                 f.write(data_response.text)
#
#         size_url = f"https://www.adidas.pl/api/products/{sku}/availability"
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
#     if "https://www.adidas.pl" in url:
#         sku = url.split("/")[-1].split(".")[0]
#         dir_path = f"c:\\adidas_pl\\html_product\\{category}\\{sku}"
#         if not os.path.exists(dir_path):
#             os.makedirs(dir_path)
#         os.chdir(dir_path)
#         get_data_and_size(sku)
#
#
# def main_asio():
#     categories = ['chlopcy-buty', 'dziewczynki-buty', 'kobiety-buty', 'mezczyzni-buty']
#     for category in categories:
#         time.sleep(2)
#         count = 0
#         with open(f'c:\\adidas_pl\\csv_url\\{category}\\url.csv', newline='', encoding='utf-8') as files:
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
import os
import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--proxy-server=37.233.3.100:9999')
    chrome_options.add_argument('--disable-gpu')
    s = Service(
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    return driver

def get_data_and_size(sku, driver):
    """Get data and size json files by SKU"""
    try:
        data_url = f"https://www.adidas.pl/api/products/{sku}"
        data_filename = f"data.json"
        driver.get(data_url)
        data_response = driver.page_source
        if data_response:
            with open(data_filename, "w", encoding='utf-8') as f:
                json.dump(data_response, f)

        size_url = f"https://www.adidas.pl/api/products/{sku}/availability"
        size_filename = f"size.json"
        driver.get(size_url)
        size_response = driver.page_source
        if size_response:
            with open(size_filename, "w", encoding='utf-8') as f:
                json.dump(size_response, f)

        return True
    except:
        return False

def process_url(url, category, driver):
    """Process url to get SKU and call get_data_and_size"""
    if "https://www.adidas.pl" in url:
        sku = url.split("/")[-1].split(".")[0]
        dir_path = f"c:\\adidas_pl\\html_product\\{category}\\{sku}"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        os.chdir(dir_path)
        get_data_and_size(sku, driver)


def main_asio():
    categories = ['chlopcy-buty', 'dziewczynki-buty', 'kobiety-buty', 'mezczyzni-buty']
    for category in categories:
        time.sleep(2)
        count = 0
        with open(f'c:\\adidas_pl\\csv_url\\{category}\\url.csv', newline='', encoding='utf-8') as files:
            urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
            driver = get_chromedriver()
            for url in urls:
                count += 1
                process_url(url[0], category, driver)
                print(f"{category} | ссылка {count} из {len(urls)}")
                time.sleep(5)
            driver.quit()

if __name__ == '__main__':
    main_asio()
