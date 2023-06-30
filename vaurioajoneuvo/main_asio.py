import asyncio
import aiohttp
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

async def send_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    async with aiohttp.ClientSession() as session:
        await session.post(url, data=data)

for url in list_urls[:1]: #Убрать срез!
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    params = {k: v[0] for k, v in params.items()}
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True,
            'mobile': False}

    )

    response = scraper.get(url, cookies=cookies, headers=headers, params=params)  # , proxies=proxies
    html = response.content
    src = response.text
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
        message = f"Title: {title}\nLink: {link}\nPrice: {price}\nDetails: {details[:3]}"
        message = f"Title: {title}\nLink: {link}\nPrice: {price}\nDetails: {details[:3]}"
        print(message)  # print to console

        # send the same message to telegram
        asyncio.run(send_message(bot_token, chat_id, message))