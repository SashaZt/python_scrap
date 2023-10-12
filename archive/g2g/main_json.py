import csv
import json
import math
import os
import re
import pandas as pd


import time
from urllib.parse import urlparse, parse_qs
import glob
import requests
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

"""Для прокси нужно jre-8u371-windows-x64.exe т.е. java 8 версии"""
server_options = {
    'log_path': 'NUL'
}

server = Server(r"c:\Program Files (x86)\browsermob-proxy\bin\browsermob-proxy", options=server_options)
server.start()
proxy = server.create_proxy()


def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--auto-open-devtools-for-tabs=devtools://devtools/bundled/inspector.html')

    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)

    return driver


def selenium_get_curl(url):
    proxy.new_har("sls.g2g.com", options={'captureHeaders': True, 'captureContent': True})
    """Ссылка куда переходим"""
    driver = get_chromedriver()
    driver.get(url)
    time.sleep(10)

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

    counets_url = driver.find_element(By.XPATH, '//div[@class="text-secondary"]').text.replace(",", "")
    count_url = int(re.search(r"(\d+)", counets_url).group(0))
    url_in_page = 48
    list_url = math.ceil(count_url / url_in_page)

    curl_command = "curl "
    entries = proxy.har['log']['entries']
    for entry in entries:
        # print(entry)
        """Указываем тут url который нужно отслеживать"""
        if entry['request']['url'].startswith('https://sls.g2g.com/offer/search?service_id=lgc_service'):
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
    print(f'Всего {count_url}')
    return curl_command, list_url


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


def get_requests(url, params, cookies, headers, list_url):
    # Определите текущую директорию, где находится скрипт
    current_directory = os.getcwd()

    # Задайте имя папки data_json
    data_json_directory = 'data_json'

    # Создайте полный путь к папке data_json
    data_json_path = os.path.join(current_directory, data_json_directory)
    for i in range(1, list_url + 1):
        if i == 1:
            url = 'https://sls.g2g.com/offer/search'
            params['currency'] = ['USD']

            response = requests.get(url, params=params, headers=headers)
            json_data = response.json()
            filename = f'g2g_0{i}.json'
            file_path = os.path.join(data_json_path, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
            print(f'Паузка 1сек, скачал {file_path}')
            time.sleep(5)
        if i > 1:
            url = 'https://sls.g2g.com/offer/search'
            params['currency'] = ['USD']
            params['page'] = [i]
            response = requests.get(url, params=params, headers=headers)
            json_data = response.json()
            filename = f'g2g_0{i}.json'
            file_path = os.path.join(data_json_path, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
            print(f'Паузка 1сек, скачал {file_path}')
            time.sleep(5)


def parsing():
    # Определите текущую директорию, где находится скрипт
    current_directory = os.getcwd()

    # Задайте имя папки data_json
    data_json_directory = 'data_json'

    # Создайте полный путь к папке data_json
    data_json_path = os.path.join(current_directory, data_json_directory)

    folder = fr'{data_json_path}\*.json'
    files_html = glob.glob(folder)
    header_order = ['price', 'unit_price', 'name', 'region', 'checkout_devlivery', 'stock', 'Server', 'ServiceType']

    # Создайте множество для уникальных заголовков
    unique_headers = set(header_order)
    print("Название файла")
    file_name_csv = input()
    # Здесь мы создаем CSV файл и записываем заголовки
    with open(f'{file_name_csv}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(header_order)

    for item in files_html:
        with open(item, 'r', encoding="utf-8") as f:
            data_json = json.load(f)
        datas = data_json['payload']['results']

        for g in datas:
            title = g['title']
            unit_price = str(g['converted_unit_price']).replace('.', ',')
            available_qty = g['available_qty']
            min_qty = g['min_qty']
            display_price = str(unit_price * min_qty).replace('.', ',')
            offer_attributes = g['offer_attributes']
            region_id = g['region_id']

            if region_id == "dfced32f-2f0a-4df5-a218-1e068cfadffa":
                region_id = 'US'

            values = [display_price, unit_price, title, region_id, available_qty, min_qty]

            for o in offer_attributes:
                pattern = r'lgc_\d+_(\w+)'
                collection_id = re.findall(pattern, o['collection_id'])[0]
                value = o['value']

                unique_headers.add(collection_id)  # Добавляем новый заголовок в множество
                values.append(value)

            # Здесь мы добавляем значения в CSV файл построчно
            with open(f'{file_name_csv}.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow(values)

    # Теперь записываем уникальные заголовки в первую строку CSV файла в заданном порядке
    with open(f'{file_name_csv}.csv', 'r', newline='', encoding='utf-8') as f:
        lines = f.readlines()
    lines[0] = ",".join(header_order) + '\n'

    with open(f'{file_name_csv}.csv', 'w', newline='', encoding='utf-8') as f:
        f.writelines(lines)

    # Загрузка данных из файла CSV
    data = pd.read_csv(f'{file_name_csv}.csv', encoding='utf-8')

    # Сохранение данных в файл XLSX
    data.to_excel(f'{file_name_csv}.xlsx', index=False, engine='openpyxl')



    # Получаем список всех файлов в папке
    # files = glob.glob(os.path.join(data_json_path, '*'))
    # # Удаляем каждый файл
    # for f in files:
    #     if os.path.isfile(f):
    #         os.remove(f)
    #         print(f'Удаляю {f}')


if __name__ == '__main__':
    print("Вставьте ссылку")
    url = input()
    curl_result, list_url = selenium_get_curl(url)  # сохраняем результат функции в переменную
    get_cookie_header(curl_result)
    server.stop()  # остановка сервера должна быть здесь
    url, params, cookies, headers = get_cookie_header(curl_result)
    get_requests(url, params, cookies, headers, list_url)
    parsing()
