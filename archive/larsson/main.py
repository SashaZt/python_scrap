from bs4 import BeautifulSoup
import csv
import glob
from selenium.webdriver.common.keys import Keys
import re
import requests
import json
import cloudscraper
import os
import time

def get_requests():

    cookies = {
        'PHPSESSID_MIKE': 'cu48ap0n218a14pi0v9fee11rd',
        'ActiveBasket': '1',
        'dv_consent': '{"accepted":[{"uid":"1"},{"uid":"6"}],"ts":1701674208}',
    }

    headers = {
        'authority': 'mike.larsson.pl',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        # 'cookie': 'PHPSESSID_MIKE=cu48ap0n218a14pi0v9fee11rd; ActiveBasket=1; dv_consent={"accepted":[{"uid":"1"},{"uid":"6"}],"ts":1701674208}',
        'dnt': '1',
        'referer': 'https://mike.larsson.pl/pl/faction/select_vehicle/ftype/1/type/99/Marke/Honda/Verkaufsbezeichnung/CBR/Feldx/600/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    params = {
        'ftype': '1',
        'type': '99',
        'Marke': 'Honda',
        'Verkaufsbezeichnung': 'CBR',
        'Feldx': '600',
        'vsr': 'all',
    }

    response = requests.get(
        'https://mike.larsson.pl/pl/faction/select_vehicle/ftype/1/type/99/Marke/Honda/Verkaufsbezeichnung/CBR/Feldx/600/',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    # json_data = response.json()
    # with open(f'Hannover.json', 'w', encoding='utf-8') as f:
    #     json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
    src = response.text
    filename = f"larsson.html"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(src)


def parsing():

    with open("larsson.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    # Находим первую таблицу
    table = soup.find('table')

    # Извлекаем все строки таблицы
    row_all = table.find_all('tr', class_='tda')
    specifications = {}
    # Перебираем строки таблицы
    for row_td in row_all[:1]:
        for i in row_td:
            print(i.find('a').get_text(strip=True))
        history = row_td.find('td', attrs={'class': 'show_history_tips'})
        table = history.find('table')
        rows_tr = table.find_all('tr')

        # Для каждой строки извлекаем ключ и значение
        for row in rows_tr:

            tds = row.find_all('td')
            if len(tds) == 2:  # Убедитесь, что в строке две ячейки
                key = tds[0].get_text(strip=True)
                value = tds[1].get_text(strip=True)
                specifications[key] = value




        print(specifications)

        # row_data = []
        #
        # # Перебираем все дочерние элементы в строке
        # for element in row.contents:
        #     # Проверяем, является ли элемент тегом <td> или <th> и не имеет ли он класса "show_history_tips"
        #     if element.name in ['td'] and 'show_history_tips' not in element.get('class', []):
        #         row_data.append(element.get_text(strip=True))
        #
        # # Выводим данные каждой строки, если она содержит данные
        # if row_data:
        #     print(row_data)


if __name__ == '__main__':
    # get_requests()
    # get_cloudscraper()
    # get_selenium()
    parsing()
