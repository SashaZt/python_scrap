import re
from bs4 import BeautifulSoup
import random
import glob
import re
from pathlib import Path
import requests
import json
import cloudscraper
import os
from playwright.sync_api import sync_playwright
from cf_clearance import sync_cf_retry, sync_stealth
import time
import shutil
import tempfile
# import undetected_chromedriver as webdriver


from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv


def get_chromedriver():
    options = webdriver.ChromeOptions()

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-gpu")
    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # chrome_options.add_argument('--disable-infobars')
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument('--disable-extensions') # Отключает использование расширений
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-setuid-sandbox')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    # proxy_extension = ProxyExtension(*proxy)
    # options.add_argument(f"--load-extension={proxy_extension.directory}")
    service = ChromeService(executable_path='C:\\scrap_tutorial-master\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })
    return driver


def get_selenium():
    name_files = Path('C:/scrap_tutorial-master/archive/dok.ua') / 'url.csv'
    with open(name_files, newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        for row in urls:
            url = row[0]
            folder_path = f"c:/DATA/dok_ua/list/{url.split('/')[-1].replace('-', '_')}/"
            # os.makedirs(folder_path, exist_ok=True)
            # folder_path = f"c:/DATA/dok_ua/products/{url.split('/')[-1].replace('-', '_')}/rus/"
            # os.makedirs(folder_path, exist_ok=True)


            # # Создание папки, если её нет
            # os.makedirs(folder_path, exist_ok=True)
            driver = get_chromedriver()
            driver.maximize_window()
            driver.get(url)
            time.sleep(1)
            last_page = None
            try:
                last_page = int(driver.find_element(By.XPATH, '//li[@class="last"]').text)
            except:
                div = driver.find_element(By.XPATH, '//div[@class="add-more-info"]').text
                match = re.search(r'з (\d+) товарів', div)
                if match:
                    last_page = int(match.group(1)) // 12
            count = 0
            for p in range(1, last_page + 2):
                count +=1
                new_url = f'{url}?page={p}'
                driver.get(new_url)
                time.sleep(1)
                file_name = f"{folder_path}data_0{count}.html"
                with open(file_name, "w", encoding='utf-8') as fl:
                    fl.write(driver.page_source)



def get_url_product():
    folder = r'c:\DATA\dok_ua\list\*.html'
    files_html = glob.glob(folder)
    with open('url_products.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        for item in files_html:
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            urls = soup.find_all('div', attrs={'class': 'product-card-packaging__item'})
            for u in urls:
                url = u.get("data-link")
                url = f'https://dok.ua{url}'
                writer.writerow([url])



if __name__ == '__main__':
    get_selenium()
    # get_url_product()
