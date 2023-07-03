import schedule
import time
from datetime import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs
import glob
import re
from playwright.sync_api import sync_playwright
from cf_clearance import sync_cf_retry, sync_stealth
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

def process_urls_and_send_messages(bot_token, chat_id, list_urls):
    while True:
        url = 'https://www.vaurioajoneuvo.fi/?model_year_min=1999'
        # not use cf_clearance, cf challenge is fail
        # proxies = {
        #     "all": "socks5://localhost:7890"
        # }
        res = requests.get(url)
        if '<title>Just a moment...</title>' in res.text:
            print("cf challenge fail")
        # get cf_clearance
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            sync_stealth(page, pure=True)
            page.goto(url)
            res = sync_cf_retry(page)
            if res:
                cookies = page.context.cookies()
                for cookie in cookies:
                    if cookie.get('name') == 'cf_clearance':
                        cf_clearance_value = cookie.get('value')
                        # print(cf_clearance_value)
                ua = page.evaluate('() => {return navigator.userAgent}')
                # print(ua)
                # get_cloudscraper(ua, cf_clearance_value)

            else:
                print("cf challenge fail")

            browser.close()
            # return ua, cf_clearance_value  # Возвращаем значения
        for url in list_urls:  # Убрать срез тут список url
            headers = {"user-agent": ua}
            cookies = {"cf_clearance": cf_clearance_value}
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
                with open(file_name, 'a', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)

            table_row = soup.find('div', attrs={'class': 'cars-list'})
            regex_containr = re.compile('.*(?=item-lift-container)')
            item_lift_container = table_row.find_all('div', attrs={'class': regex_containr})
            for i in item_lift_container[:1]: #Тут срез не убирать!

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
                details_all = [span.text for span in i.find_all('span')]
                details = f"{details_all[0]} {details_all[1]} {details_all[2]}"
                message = f"Title: {title}\nLink: {link}\nPrice: {price}\nDetails: {details}"
                # print(message)  # print to console

                # send the same message to telegram
                asyncio.run(send_message(bot_token, chat_id, message))
        time.sleep(30)
        print('Паузка 30сек')
process_urls_and_send_messages(bot_token, chat_id, list_urls)