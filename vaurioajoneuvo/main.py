from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs
import glob
import re
import requests
import json
import cloudscraper
import random
import os
import time
import undetected_chromedriver as webdriver
from config import bot_token, chat_id, proxies, list_urls, cookies, headers
import csv


def get_cloudscraper():
    while True:
        for url in list_urls: #Убрать срез!
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            params = {k: v[0] for k, v in params.items()}

            # print(url)
            """Настройка прокси серверов случайных"""
            proxy = random.choice(proxies)
            proxy_host = proxy[0]
            proxy_port = proxy[1]
            proxy_user = proxy[2]
            proxy_pass = proxy[3]

            proxi = {
                'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
                'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
            }
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'firefox',
                    'platform': 'windows',
                    'mobile': False}
            )
            response = scraper.get(url, cookies=cookies, headers=headers, params=params)  # , proxies=proxies
            # print(proxi)
            print(response.status_code)
            """Для теста"""
            html = response.content
            # filename = f"avto_{coun}.html"
            # with open(filename, "w", encoding='utf-8') as f:
            #     f.write(html.decode('utf-8'))
            """Для теста"""
            src = response.text
            """ТЕСТИРОВАНИЕ"""
            soup = BeautifulSoup(src, 'lxml')
            file_name = 'id_ad.csv'
            try:
                with open(file_name, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    id_list = [row[0] for row in reader]
            except:
                with open(file_name, 'w', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)

            table_row = soup.find('div', attrs={'class': 'cars-list'})
            regex_containr = re.compile('.*(?=item-lift-container)')
            item_lift_container = table_row.find_all('div', attrs={'class': regex_containr})
            for i in item_lift_container[:1]:

                id_avto = i.find('div', {'class': 'item-lift'}).get('data-auction-id')
                if id_avto in id_list:
                    print('Объявление есть')
                    continue
                time.sleep(1)
                with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([id_avto])
                link = 'https://www.vaurioajoneuvo.fi' + i.find('a').get('href')
                # Извлечь текст из блока с названием
                title = i.find('strong').text
                # Извлечь текст из блока с информацией о цене
                regex_price = re.compile('item-lift-price-now auction-price-now.*')
                try:
                    price = i.find('strong', {'class': regex_price}).text
                except:
                    price = None
                details = [span.text for span in i.find_all('span')]

                print(f"Title: {title}")
                print(f"Link: {link}")
                print(f"Price: {price}")
                print(f"Details: {details[:3]}")


        # html = r.content
        # filename = f"amazon.html"
        # with open(filename, "w", encoding='utf-8') as f:
        #     f.write(html.decode('utf-8'))


def get_id_ad():
    file = 'avto.html'
    with open(file, encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    file_name = 'id_ad.csv'
    table_row = soup.find('div', attrs={'class': 'cars-list'})
    regex_containr = re.compile('.*(?=item-lift-container)')
    item_lift_container = table_row.find_all('div', attrs={'class': regex_containr})
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for i in item_lift_container[:1]:

            id_avto = i.find('div', {'class': 'item-lift'}).get('data-auction-id')
            writer.writerow([id_avto])


def parsing():
    file = 'avto.html'
    with open(file, encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    file_name = 'id_ad.csv'
    with open(file_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        id_list = [row[0] for row in reader]

    table_row = soup.find('div', attrs={'class': 'cars-list'})
    regex_containr = re.compile('.*(?=item-lift-container)')
    item_lift_container = table_row.find_all('div', attrs={'class': regex_containr})
    for i in item_lift_container:

        id_avto = i.find('div', {'class': 'item-lift'}).get('data-auction-id')
        if id_avto in id_list:
            continue
        with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([id_avto])
        link = 'https://www.vaurioajoneuvo.fi' + i.find('a').get('href')
        # Извлечь текст из блока с названием
        title = i.find('strong').text
        # Извлечь текст из блока с информацией о цене
        regex_price = re.compile('item-lift-price-now auction-price-now.*')
        try:
            price = i.find('strong', {'class': regex_price}).text
        except:
            price = None
        details = [span.text for span in i.find_all('span')]

        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Price: {price}")
        print(f"Details: {details[:3]}")


if __name__ == '__main__':
    get_cloudscraper()
    # parsing()
