import csv
import json
import math
from datetime import datetime
import os
import re
import pandas as pd
import mysql.connector
from concurrent.futures import ProcessPoolExecutor
import time
# from headers_cookies import cookies, headers
from urllib.parse import urlparse, parse_qs
import glob
import requests
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import random
from selenium.webdriver.common.by import By


"""Настройка browsermob-proxy"""
server_options = {
    'log_path': 'NUL'
}

server = Server(r"c:\Program Files (x86)\browsermob-proxy\bin\browsermob-proxy", options=server_options)
server.start()
proxy = server.create_proxy()


"""Настройка для Selenium"""
def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--auto-open-devtools-for-tabs=devtools://devtools/bundled/inspector.html')

    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)

    return driver


"""Получаем curl с помощью Selenium и browsermob-proxy"""
def selenium_get_curl(url):
    proxy.new_har("exist.ua", options={'captureHeaders': True, 'captureContent': True})
    """Ссылка куда переходим"""
    driver = get_chromedriver()
    driver.get(url)
    time.sleep(5)

    driver.execute_script('''
        var elements = document.querySelectorAll('[aria-label="Network panel"]');
        for (var i = 0; i < elements.length; i++) {
            var element = elements[i];
            if (element.offsetWidth > 0 && element.offsetHeight > 0) {
                element.click();
                break;
            }
        }
    ''')
    time.sleep(5)
    # получить все запросы из Network panel
    requests = driver.execute_script('''
        var performanceEntries = performance.getEntriesByType("resource");
        var fetchRequests = [];
        for (var i = 0; i < performanceEntries.length; i++) {
            var entry = performanceEntries[i];
            fetchRequests.push(entry);
        }
        return fetchRequests;
    ''')

    curl_command = "curl "
    entries = proxy.har['log']['entries']
    for entry in entries:
        # print(entry)
        """Указываем тут url который нужно отслеживать"""
        if entry['request']['url'].startswith('https://exist.ua/api/v1/catalogue/product-index'):
            # Method (GET, POST, etc.)
            curl_command += "-X {} ".format(entry['request']['method'])

            # URL
            curl_command += "'{}' \\\n".format(entry['request']['url'])

            # Headers
            for header in entry['request']['headers']:
                header_name = header['name']
                header_value = header['value']
                curl_command += "  -H '{}: {}' \\\n".format(header_name, header_value)

            if entry['request']['method'] == 'POST' and 'postData' in entry['request']:
                if 'text' in entry['request']['postData']:
                    curl_command += "  --data '{}'".format(entry['request']['postData']['text'])

            break

    # Extracting cookies
    cookies_match = re.search(r"Cookie:\s(.*?)'", curl_command)
    if cookies_match:
        cookies_str = cookies_match.group(1)
        cookies_list = cookies_str.split('; ')
        cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies_list}

    # Extracting headers
    headers_match = re.findall(r"-H '(.*?)'", curl_command)
    headers = {header.split(': ')[0]: header.split(': ')[1] for header in headers_match}
    print(curl_command)

    return curl_command

"""curl разбираем на cookies и headers"""
def get_cookie_header(curl_command):
    cookies = {}
    headers = {}
    params = {}
    method = "GET"  # по умолчанию

    url_match = re.search(r"'(.*?)'", curl_command)
    if url_match:
        url = url_match.group(1)
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)

    method_match = re.search(r"-X (\w+)", curl_command)
    if method_match:
        method = method_match.group(1)

    cookies_match = re.search(r"Cookie:\s(.*?)'", curl_command)
    if cookies_match:
        cookies_str = cookies_match.group(1)
        cookies_list = cookies_str.split("; ")
        cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies_list}

    headers_match = re.findall(r"-H '(.*?)'", curl_command)
    headers = {header.split(": ")[0]: header.split(": ")[1] for header in headers_match}
    url_match = re.search(r"'(.*?)'", curl_command)
    url = None
    if url_match:
        url = url_match.group(1)

    return url, params, cookies, headers
# def save_to_file(url, params, cookies, headers):
#     with open("headers_cookies.py", "w") as f:
#         f.write("url = '{}'\n\n".format(url))
#
#         f.write("params = {\n")
#         for key, value in params.items():
#             f.write("    '{}': {},\n".format(key, value))
#         f.write("}\n\n")
#
#         f.write("cookies = {\n")
#         for key, value in cookies.items():
#             f.write("    '{}': '{}',\n".format(key, value))
#         f.write("}\n\n")
#
#         f.write("headers = {\n")
#         for key, value in headers.items():
#             f.write("    '{}': '{}',\n".format(key, value))
#         f.write("}\n")

"""Получаем общее количество объявлений"""
def get_totalElements():
    json_data = {
        'query': [
            '*',
        ],
        'filter': {
            'NLTS': [
                'expected_sale_assigned_ts_utc:[NOW/DAY-1DAY TO NOW/DAY]',
            ],
        },
        'sort': None,
        'page': 0,
        'size': 100,
        'start': 0,
        'watchListOnly': False,
        'freeFormSearch': False,
        'hideImages': False,
        'defaultSort': False,
        'specificRowProvided': False,
        'displayName': '',
        'searchName': '',
        'backUrl': '',
        'includeTagByField': {},
        'rawParams': {},
    }
    response = requests.post('https://www.copart.com/public/lots/search-results', cookies=cookies,
                             headers=headers, json=json_data)

    data_json = response.json()
    totalElements = data_json['data']['results']['totalElements']
    print(f'Всего {totalElements}')
    return totalElements


"""Получаем все объявления"""
def get_request(totalElements):

    ad = totalElements
    page_ad = ad // 100
    start = 0
    page = 0
    # for i in range(0, 1):
    for i in range(page_ad + 1):
        filename = f"c:\\DATA\\copart\\list\\data_{page}.json"
        if not os.path.exists(filename):
            # Создаем сессию
            json_data = {
                'query': [
                    '*',
                ],
                'filter': {
                    'NLTS': [
                        'expected_sale_assigned_ts_utc:[NOW/DAY-1DAY TO NOW/DAY]',
                    ],
                },
                'sort': None,
                'page': page,
                'size': 100,
                'start': start,
                'watchListOnly': False,
                'freeFormSearch': False,
                'hideImages': False,
                'defaultSort': False,
                'specificRowProvided': False,
                'displayName': '',
                'searchName': '',
                'backUrl': '',
                'includeTagByField': {},
                'rawParams': {},
            }

            try:
                response = requests.post('https://www.copart.com/public/lots/search-results', cookies=cookies,
                                         headers=headers, json=json_data)
            except:
                continue
            data = response.json()
            print(f'Пауза 1 сек')
            time.sleep(1)

            with open(filename, 'w') as f:
                json.dump(data, f)
        page += 1
        start += 100
    now = datetime.now()
    print(f'Все {page_ad} страницы скачаны в {now}')

"""Собираем все ссылки"""
def get_id_ad_and_url():
    folders_html = r"c:\DATA\copart\list\*.json"
    files_html = glob.glob(folders_html)
    file_csv = f"url.csv"
    with open(file_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for i in files_html:
            with open(i, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            content = json_data['data']['results']['content']
            for c in content:
                url_ad = f'https://www.copart.com/public/data/lotdetails/solr/lotImages/{c["ln"]}/USA'
                writer.writerow([url_ad])
    now = datetime.now()
    print(f'Получили список всех url в {now}')


def get_product(cookies, headers):

    with open("url.csv", newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        counter = 0
        for url in urls:
            filename = f"c:\\DATA\\copart\\product\\data_{counter}.json"
            if not os.path.exists(filename):
                try:
                    response = requests.get(url[0], cookies=cookies, headers=headers)  # , proxies=proxi

                except Exception as e:
                    print(e)

                try:
                    data_json = response.json()
                except Exception as e:
                    data_json = None
                    print(e)
                    continue

                with open(filename, 'w') as f:
                    json.dump(data_json, f)
                    print(filename)
                time.sleep(5)
            print(f'Сохранил объявлений {counter}')
            counter += 1

"""Следующие 3 функции для работы с Selenium"""
def split_urls(urls, n):
    """Делит список URL-адресов на n равных частей."""
    avg = len(urls) // n
    urls_split = [urls[i:i + avg] for i in range(0, len(urls), avg)]
    return urls_split



def worker(sub_urls, start_counter):
    driver = get_chromedriver()
    for counter, url in enumerate(sub_urls, start=start_counter):
        try:
            filename = f"c:\\DATA\\copart\\product\\data_{counter}.json"
            if not os.path.exists(filename):
                driver.get(url[0])
                time.sleep(1)
                json_content = driver.page_source
                json_content = json_content.replace(
                    '<html><head><meta name="color-scheme" content="light dark"><meta charset="utf-8"></head><body style="margin: 0"><div></div><pre>',
                    '')
                json_content = json_content.replace('</pre></body></html>', '')
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(json_content)

        except Exception as e:
            print(f"Error processing URL {url[0]}: {e}")
    driver.quit()


def get_product_s():
    with open("url.csv", newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        max_workers = 10
        splitted_urls = split_urls(urls, max_workers)
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for idx, sub_urls in enumerate(splitted_urls):
                executor.submit(worker, sub_urls, idx * len(sub_urls))
"""Следующие 3 функции для работы с Selenium"""

def parsin():
    heandler_set = set()
    with open('amortyzatory.json', 'r', encoding="utf-8") as f:
        data_json = json.load(f)
    dict_results = data_json['data']['results']
    for i in dict_results:
        upc = i['upc'] # Номер товару
        trademark = i['trademark']['description'] # Бренд
        name = i['description']
        price = i['price']['price']
        quantity = i['price']['quantity']
        attributes = i['attributes']
        for item in attributes:
            heandler_set.add(item['name'])
        result_dict = {item['name']: item['value'] for item in attributes}


if __name__ == '__main__':
    # print("Вставьте ссылку")
    # url = 'https://exist.ua/api/v1/catalogue/product-index/?page=1&slug=amortyzatory-stijky-pidvisky'
    # curl_result = selenium_get_curl(url)  # сохраняем результат функции в переменную
    # get_cookie_header(curl_result)
    # server.stop()  # остановка сервера должна быть здесь
    # url, params, cookies, headers = get_cookie_header(curl_result)
    # # # save_to_file(url, params, cookies, headers)
    # totalElements = get_totalElements()
    # get_request(totalElements)
    # get_id_ad_and_url()
    # get_product_s()
    parsin()
