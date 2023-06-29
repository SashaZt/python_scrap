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
from selenium.common.exceptions import TimeoutException
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv

PROXY_HOST = '37.233.3.100'
PROXY_PORT = 9999
PROXY_USER = 'proxy_alex'
PROXY_PASS = 'DbrnjhbZ88'
# proxies = {
#     'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
#     'https': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'
# }
proxies = {"http": f"http://{PROXY_HOST}:{PROXY_PORT}", f"https": f"http://{PROXY_HOST}:{PROXY_PORT}"}


def get_undetected_chromedriver():
    # Обход защиты
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--proxy-server=45.14.174.253:80")
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-setuid-sandbox')
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_requests():
    import requests

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Origin': 'https://youcontrol.com.ua',
        'Referer': 'https://youcontrol.com.ua/sign_in/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        '_csrf-frontend': 'q5kAWYsUJNFhGGBupQzQJOYEH6DBdSudGXkI5NAXDSzt4Uo3w3hJnCZTTSeXdOYXjltLxPk3HttJMCW2oHVHeg==',
        'LoginForm[login]': 'fincar.marketing@gmail.com',
        'LoginForm[previousUrl]': '',
        'LoginForm[password]': '299466',
        'LoginForm[rememberMe]': [
            '0',
            '1',
        ],
        'login-button': '',
    }

    response = requests.post('https://youcontrol.com.ua/dashboard/', headers=headers, data=data)
    src = response.text
    filename = f"amazon.html"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(src)


def parsing():
    file = 'avto.html'
    with open(file, encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')

    table_row = soup.find('div', attrs={'class': 'cars-list'})
    regex_containr = re.compile('.*(?=item-lift-container)')
    item_lift_container = table_row.find_all('div', attrs={'class':regex_containr})
    for i in item_lift_container[:1]:
        print(i)



def get_cloudscraper():
    cookies = {
        'svt-buyers': '384bbf1a1bed4a7c1614936795d4d4a1495e7058',
        'cf_clearance': 'zuXdvfq_0dnbSwrap3Yt7q2LyhUVLranDf2asOF5LKE-1688035391-0-150',
    }

    headers = {
        'authority': 'www.vaurioajoneuvo.fi',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'cache-control': 'no-cache',
        # 'cookie': 'svt-buyers=384bbf1a1bed4a7c1614936795d4d4a1495e7058; cf_clearance=zuXdvfq_0dnbSwrap3Yt7q2LyhUVLranDf2asOF5LKE-1688035391-0-150',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.vaurioajoneuvo.fi/?__cf_chl_tk=i_f5HW4kRkuDVtn245h2rak2TncY1kQNOfRfpp4wr3k-1688035391-0-gaNycGzNDXs',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False

    })
    r = scraper.get(
        'https://www.vaurioajoneuvo.fi/', cookies=cookies, headers=headers)  # , proxies=proxies
    html = r.content
    filename = f"amazon.html"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(html.decode('utf-8'))




if __name__ == '__main__':
    # get_cloudscraper()
    parsing()
