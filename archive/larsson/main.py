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

def filter_classes(tag):
    return tag and tag.name == 'tr' and tag.has_attr('class') and ('tda' in tag['class'] or 'tdb' in tag['class'])

def parsing():
    with open("larsson.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    # Находим первую таблицу
    table = soup.find('table')
    # all_specifications_table = []
    # all_specifications_history = []
    if table:
        # Используем CSS-селекторы для выбора элементов с классами 'tda' или 'tdb'
        row_all = table.select('tr.tda, tr.tdb')

        all_specifications_table = []
        all_specifications_history = []
        for row_td in row_all:
    # Извлекаем все строки таблицы
    # row_all = table.find_all('tr', class_=filter_classes)
    #
    #
    #
    #
    # for row_td in row_all:
            key_table = ('Model', 'Kod roku', 'Typ', 'VIN_od', 'VIN_do', 'Rocznik', 'Il. cyl.', 'Moc silnika')

            values_table = [a.find('a').get_text(strip=True) for a in row_td]
            specifications_table = dict(zip(key_table, values_table))
            all_specifications_table.append(specifications_table)

            history = row_td.find('td', attrs={'class': 'show_history_tips'})
            table = history.find('table')
            rows_tr = table.find_all('tr')

            specifications_history = {}
            for row in rows_tr:
                tds = row.find_all('td')
                if len(tds) == 2:
                    key = tds[0].get_text(strip=True)
                    value = tds[1].get_text(strip=True)
                    specifications_history[key] = value

            all_specifications_history.append(specifications_history)


    # Объединяем данные из обоих списков
    combined_data = []
    for table, history in zip(all_specifications_table, all_specifications_history):
        combined_dict = {**table, **history}  # Объединяем два словаря
        combined_data.append(combined_dict)

    # Определяем заголовки для CSV
    # Возьмем ключи из первого элемента списка (предполагая, что все элементы имеют одинаковые ключи)
    headers = combined_data[0].keys() if combined_data else []

    # Запись данных в CSV
    with open('specifications.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")

        # Записываем заголовки
        writer.writeheader()

        # Записываем строки данных
        for data in combined_data:
            writer.writerow(data)

    print("Данные записаны в файл 'specifications.csv'")


if __name__ == '__main__':
    # get_requests()
    # get_cloudscraper()
    # get_selenium()
    parsing()
