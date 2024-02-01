import glob
import glob
import json
import os
import random

import requests

from config import headers
from proxi import proxies

current_directory = os.getcwd()
temp_directory = 'temp'
# Создайте полный путь к папке temp
temp_path = os.path.join(current_directory, temp_directory)
cookies_path = os.path.join(temp_path, 'cookies')
login_pass_path = os.path.join(temp_path, 'login_pass')
daily_sales_path = os.path.join(temp_path, 'daily_sales')
monthly_sales_path = os.path.join(temp_path, 'monthly_sales')
payout_history_path = os.path.join(temp_path, 'payout_history')


def proxy_random():
    proxy = random.choice(proxies)
    proxy_host = proxy[0]
    proxy_port = proxy[1]
    proxy_user = proxy[2]
    proxy_pass = proxy[3]
    formatted_proxy = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    # Возвращаем словарь с прокси
    return {
        "http": formatted_proxy,
        "https": formatted_proxy
    }


def get_requests_daily_sales():
    proxi = proxy_random()
    filename_cookies = os.path.join(cookies_path, '*.json')
    files_json = glob.glob(filename_cookies)
    for item in files_json:
        with open(item, 'r') as f:
            cookies = json.load(f)
        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[1].replace('.json', '')
        # Создание сессии
        session = requests.Session()

        # Добавление кук в сессию
        for name, value in cookies.items():
            session.cookies.set(name, value)

        data = {
            'mvtoken': mvtoken,
            'day': '',
            'month': '1',
            'filterYear': '2024',
        }
        mvtoken_value = data['mvtoken']
        month_value = data['month']
        filterYear_value = data['filterYear']
        filename = os.path.join(daily_sales_path, f'{mvtoken_value}_{month_value}_{filterYear_value}.json')
        if not os.path.exists(filename):
            response = session.post('https://www.manyvids.com/includes/get_earnings.php', headers=headers,
                                    proxies=proxi, data=data)

            json_data = response.json()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


def get_requests_monthly_sales():
    proxi = proxy_random()
    filename_cookies = os.path.join(cookies_path, '*.json')
    files_json = glob.glob(filename_cookies)
    for item in files_json:
        with open(item, 'r') as f:
            cookies = json.load(f)
        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[1].replace('.json', '')
        session = requests.Session()

        # Добавление кук в сессию
        for name, value in cookies.items():
            session.cookies.set(name, value)

        data = {
            'mvtoken': mvtoken,
            'year': '2023',
        }

        response = session.post('https://www.manyvids.com/includes/get_earnings.php', headers=headers,
                                data=data, proxies=proxi)
        json_data = response.json()
        mvtoken_value = data['mvtoken']
        filterYear_value = data['year']
        filename = os.path.join(monthly_sales_path, f'{mvtoken_value}_{filterYear_value}.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


def get_requests_payout_history():
    proxi = proxy_random()
    filename_cookies = os.path.join(cookies_path, '*.json')
    files_json = glob.glob(filename_cookies)
    for item in files_json:
        with open(item, 'r') as f:
            cookies = json.load(f)
        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[1].replace('.json', '')
        session = requests.Session()

        # Добавление кук в сессию
        for name, value in cookies.items():
            session.cookies.set(name, value)

        data = {
            'mvtoken': mvtoken,
            'year': '2023',
        }
        mvtoken_value = data['mvtoken']
        filterYear_value = data['year']
        filename = os.path.join(payout_history_path, f'{mvtoken_value}_{filterYear_value}.json')
        if not os.path.exists(filename):
            response = session.post(
                'https://www.manyvids.com/includes/get_payperiod_earnings.php',
                headers=headers,
                data=data,
                proxies=proxi
            )

            json_data = response.json()

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


if __name__ == '__main__':
    get_requests_daily_sales()
    get_requests_monthly_sales()
    get_requests_payout_history()
