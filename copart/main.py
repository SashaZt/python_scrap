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
from selenium.webdriver.chrome.service import Service
import os
from pathlib import Path
import random
import shutil
import tempfile
import os
from proxi import proxies
import concurrent.futures
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import zipfile
import time
# import undetected_chromedriver as webdriver
from selenium import webdriver
import undetected_chromedriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv

proxy = [
    ('185.112.12.122', 2831, '36675', 'g6Qply4q')
]


class ProxyExtension:
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {"scripts": ["background.js"]},
        "minimum_chrome_version": "76.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: %d
            },
            bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        { urls: ["<all_urls>"] },
        ['blocking']
    );
    """

    def __init__(self, host, port, user, password):
        self._dir = os.path.normpath(tempfile.mkdtemp())

        manifest_file = os.path.join(self._dir, "manifest.json")
        with open(manifest_file, mode="w") as f:
            f.write(self.manifest_json)

        background_js = self.background_js % (host, port, user, password)
        background_file = os.path.join(self._dir, "background.js")
        with open(background_file, mode="w") as f:
            f.write(background_js)

    @property
    def directory(self):
        return self._dir

    def __del__(self):
        shutil.rmtree(self._dir)


def get_chromedriver(proxy):
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--disable-extensions') # Отключает использование расширений
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    proxy_extension = ProxyExtension(*proxy)
    chrome_options.add_argument(f"--load-extension={proxy_extension.directory}")
    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })
    return driver


def get_selenium():
    url = 'https://www.copart.com/lotSearchResults?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22FETI%22:%5B%22buy_it_now_code:B1%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D'
    driver = get_chromedriver(proxy[0])
    driver.maximize_window()
    driver.get(url)
    coun = 0
    # next_page = url
    # while next_page:
    #     coun += 1
    #     driver.get(next_page)
    #     time.sleep(1)
    #     pause_time = random.randint(1, 10)
    #     file_name = f"c:\\DATA\\copart\\data_{coun}.html"
    #     if os.path.isfile(file_name):
    #         continue  # Если файл уже существует, переходим к следующей итерации цикла
    #     with open(file_name, "w", encoding='utf-8') as fl:
    #         fl.write(driver.page_source)
    #         time.sleep(pause_time)
    #     try:
    #         next_page = driver.find_element(By.XPATH,
    #                                         '//span[@class="p-paginator-icon pi pi-angle-right"]').click()
    #     except:
    #         next_page = None
    #
    #
    next_up = False
    while not next_up:
        try:
            coun += 1
            driver.execute_script("window.scrollBy(0,200)", "")
            time.sleep(1)
            pause_time = random.randint(1, 5)
            file_name = f"c:\\DATA\\copart\\list\\data_{coun}.html"
            with open(file_name, "w", encoding='utf-8') as fl:
                fl.write(driver.page_source)
                time.sleep(pause_time)
                print(f"Пауза {pause_time}")
            next_page = driver.find_element(By.XPATH, '//span[@class="p-paginator-icon pi pi-angle-right"]').click()
        except:
            break

    #
    # file_name = f"amazon.html"
    # with open(file_name, "w", encoding='utf-8') as fl:
    #     fl.write(driver.page_source)


def get_id_ad_and_url():
    folders_html = r"c:\DATA\copart\list\*.html"
    files_html = glob.glob(folders_html)
    with open(f"id_ad.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for i in files_html[:1]:
            with open(i, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            script_tags = soup.find_all('script')

            json_data = None

            for tag in script_tags:
                content = tag.string
                if content and 'var searchResults =' in content:
                    # Удалить все до начала JSON и после окончания JSON
                    json_str = content.split('var searchResults =', 1)[1].split('}};', 1)[0] + '}}'
                    # Преобразовать строку в JSON
                    # print(json_str)  # Проверка, что содержится в json_str
                    json_data = json.loads(json_str)
            content = json_data['results']['content']
            for c in content:
                id_ad = c['ln']
                # print(type(id_ad))
                writer.writerow([id_ad])

    with open(f"url.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for i in files_html[:1]:
            with open(i, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            script_tags = soup.find_all('script')

            json_data = None

            for tag in script_tags:
                content = tag.string
                if content and 'var searchResults =' in content:
                    # Удалить все до начала JSON и после окончания JSON
                    json_str = content.split('var searchResults =', 1)[1].split('}};', 1)[0] + '}}'
                    # Преобразовать строку в JSON
                    # print(json_str)  # Проверка, что содержится в json_str
                    json_data = json.loads(json_str)
            content = json_data['results']['content']
            for c in content:
                id_ad = f'https://www.copart.com/public/data/lotdetails/solr/{c["ln"]}'
                # print(id_ad)
                writer.writerow([id_ad])

        # print(content)

def get_product():


if __name__ == '__main__':
    # get_requests()
    # get_cloudscraper()
    # get_selenium()
    # get_id_ad_and_url()
    get_product()
