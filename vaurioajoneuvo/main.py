from bs4 import BeautifulSoup
import csv
import glob
import re
import requests
import json
import cloudscraper
import os
import time
import undetected_chromedriver as webdriver
from config import bot_token, chat_id, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS, filter_quoteVolume, time_restart, value_track_type, check_time, inclusion_quote_volume_filter, cookies,headers
import csv

def get_cloudscraper():
    urls = [
    "https://www.vaurioajoneuvo.fi/?model_year_min=1999",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1993&condition=no_demo",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1998",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1981&condition=no_demo",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1976",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1972&condition=no_demo",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1971",
    "https://www.vaurioajoneuvo.fi/?model_year_min=2001&condition=no_demo",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1964",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1984&condition=no_demo",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1962",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1991&condition=no_demo",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1985",
    "https://www.vaurioajoneuvo.fi/?model_year_min=1975&condition=no_demo",
    "https://www.vaurioajoneuvo.fi/?model_year_min=2003"
    ]
    for url in urls[:1]:
        scraper = cloudscraper.create_scraper(browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False

        })
        r = scraper.get(
            url, cookies=cookies, headers=headers)  # , proxies=proxies
        html = r.content
        filename = f"amazon.html"
        with open(filename, "w", encoding='utf-8') as f:
            f.write(html.decode('utf-8'))


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
        for i in item_lift_container:

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
    # get_cloudscraper()
    parsing()
