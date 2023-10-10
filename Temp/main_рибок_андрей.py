import shutil
import glob
import cloudscraper
import urllib.parse
import pandas as pd
import zipfile
import os
import shutil
import tempfile
import shutil
from lxml import html
from main_asio import *
import re
import json
from bs4 import BeautifulSoup

import undetected_chromedriver
import csv
import shutil
import time
import requests
from datetime import datetime, timedelta
# Нажатие клавиш
import glob
import shutil
import zipfile
import os
from lxml import html
import re
import json
import csv
import time
import requests
# Нажатие клавиш
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from selenium import webdriver
import random

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
# Настройка для requests чтобы использовать прокси
# proxies = {'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}/'}

proxies = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--disable-extensions') # Отключает использование расширений
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-setuid-sandbox')
    
    # proxy_extension = ProxyExtension(*proxy)
    # chrome_options.add_argument(f"--load-extension={proxy_extension.directory}")
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def proba_scrape():
    """Рабочий, только 10тыс в месяц бесплатно
    https://app.scrapingant.com/dashboard"""
    import requests
    import urllib.parse
    from bs4 import BeautifulSoup

    sa_key = 'YOUR_API_TOKEN'  # paste here
    sa_api = 'https://api.scrapingant.com/v2/general'
    qParams = {'url': 'https://coinsniper.net/new', 'x-api-key': sa_key}
    reqUrl = f'{sa_api}?{urllib.parse.urlencode(qParams)}'

    r = requests.get(reqUrl)
    # print(r.text) # --> html
    soup = BeautifulSoup(r.content, 'html.parser')







"""Сохраняем все json"""
def save_json_product():
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })
    """mezczyzni"""
    url_men = "https://www.reebok.eu/en-pl/shopping/men-shoes"
    scraper_get_men = scraper.get(url_men).content
    time.sleep(10)
    soup = BeautifulSoup(scraper_get_men, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_mezczyzni = data['numberOfItems'] // 48
    counter_mezczyzni = 0
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\html_data\\men-shoes'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    for page in range(1, totalResources_mezczyzni + 2):
        if page == 1:
            counter_mezczyzni += 1
            scraper_get_men = scraper.get(url_men).content
            soup = BeautifulSoup(scraper_get_men, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\men-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(10)
        if page > 1:
            counter_mezczyzni += 1
            url_mezczyzni_api = f'https://www.reebok.eu/en-pl/shopping/men-shoes?pageindex={counter_mezczyzni}'
            scraper_get_men = scraper.get(url_mezczyzni_api).content
            soup = BeautifulSoup(scraper_get_men, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\men-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(f"men-shoes {counter_mezczyzni} из {totalResources_mezczyzni + 1 }")
    print(f"Собрал men-shoes")

    """women"""
    url_women = "https://www.reebok.eu/en-pl/shopping/women-shoes"
    scraper_get_women = scraper.get(url_women).content
    soup = BeautifulSoup(scraper_get_women, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_women = data['numberOfItems'] // 48
    counter_women = 1
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\html_data\\women-shoes'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for page in range(1, totalResources_women + 2):
        if page == 1:
            url_women = "https://www.reebok.eu/en-pl/shopping/women-shoes"
            scraper_get_women = scraper.get(url_women).content
            soup = BeautifulSoup(scraper_get_women, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\women-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(1)
        if page > 1:
            counter_women += 1
            url_women_api = f'https://www.reebok.eu/en-pl/shopping/women-shoes?pageindex={counter_women}'
            scraper_get_women = scraper.get(url_women_api).content
            soup = BeautifulSoup(scraper_get_women, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\women-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(f"women-shoes {counter_women} из {totalResources_women + 1}")
    print(f"Собрал women-shoes")

    """kids_youth_9_14"""
    url_kids_youth_9_14 = "https://www.reebok.eu/en-pl/shopping/kids-youth-9-14"
    scraper_get_kids_youth_9_14 = scraper.get(url_kids_youth_9_14).content
    soup = BeautifulSoup(scraper_get_kids_youth_9_14, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_kids_youth_9_14 = data['numberOfItems'] // 48
    counter_kids_youth_9_14 = 1
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\html_data\\kids-youth-9-14'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for page in range(0, totalResources_kids_youth_9_14 + 2):
        if page == 1:
            url_kids_youth_9_14 = "https://www.reebok.eu/en-pl/shopping/kids-youth-9-14"
            scraper_get_kids_youth_9_14 = scraper.get(url_kids_youth_9_14).content
            soup = BeautifulSoup(scraper_get_kids_youth_9_14, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\kids-youth-9-14\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(1)
        if page > 1:
            counter_kids_youth_9_14 += 1
            url_kids_youth_9_14_api = f'https://www.reebok.eu/en-pl/shopping/kids-youth-9-14?pageindex={counter_kids_youth_9_14}'
            scraper_get_kids_youth_9_14 = scraper.get(url_kids_youth_9_14_api).content
            soup = BeautifulSoup(scraper_get_kids_youth_9_14, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\kids-youth-9-14\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(f"kids_youth_9_14 {counter_kids_youth_9_14} из {totalResources_kids_youth_9_14 + 1 }")
    print(f"Собрал kids_youth_9_14")

    """kids_kids_5_8"""
    url_kids_kids_5_8_years_kids_shoes = "https://www.reebok.eu/en-pl/shopping/kids-kids-5-8-years-kids-shoes"
    scraper_get_kids_kids_5_8_years_kids_shoes = scraper.get(url_kids_kids_5_8_years_kids_shoes).content
    soup = BeautifulSoup(scraper_get_kids_kids_5_8_years_kids_shoes, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_kids_kids_5_8_years_kids_shoes = data['numberOfItems'] // 48
    counter_kids_kids_5_8_years_kids_shoes = 1
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\html_data\\kids-kids-5-8-years-kids-shoes'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for page in range(0, totalResources_kids_kids_5_8_years_kids_shoes + 2):
        if page == 1:
            url_kids_kids_5_8_years_kids_shoes = "https://www.reebok.eu/en-pl/shopping/kids-kids-5-8-years-kids-shoes"
            scraper_get_kids_kids_5_8_years_kids_shoes = scraper.get(url_kids_kids_5_8_years_kids_shoes).content
            soup = BeautifulSoup(scraper_get_kids_kids_5_8_years_kids_shoes, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\kids-kids-5-8-years-kids-shoes\\0_{page}.json", "w",
                      encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(1)
        if page > 1:
            counter_kids_kids_5_8_years_kids_shoes += 1
            url_kids_kids_5_8_years_kids_shoes_api = f'https://www.reebok.eu/en-pl/shopping/kids-kids-5-8-years-kids-shoes?pageindex={counter_kids_kids_5_8_years_kids_shoes}'
            scraper_get_kids_kids_5_8_years_kids_shoes = scraper.get(url_kids_kids_5_8_years_kids_shoes_api).content
            soup = BeautifulSoup(scraper_get_kids_kids_5_8_years_kids_shoes, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\kids-kids-5-8-years-kids-shoes\\0_{page}.json", "w",
                      encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(
            f"kids-kids-5-8-years-kids-shoes {counter_kids_kids_5_8_years_kids_shoes} из {totalResources_kids_kids_5_8_years_kids_shoes + 1}")
    print(f"Собрал kids-kids-5-8-years-kids-shoes")

    """_kids_baby_0_4"""
    url_kids_baby_0_4_years_baby_shoes = "https://www.reebok.eu/en-pl/shopping/kids-baby-0-4-years-baby-shoes"
    scraper_get_kids_baby_0_4_years_baby_shoes = scraper.get(url_kids_baby_0_4_years_baby_shoes).content
    soup = BeautifulSoup(scraper_get_kids_baby_0_4_years_baby_shoes, 'lxml')
    script = soup.find_all('script', {'type': 'application/ld+json'})
    json_text = script[1].text
    data = json.loads(json_text)
    totalResources_kids_baby_0_4_years_baby_shoes = data['numberOfItems'] // 48
    counter_kids_baby_0_4_years_baby_shoes = 1
    """Очистка папки с старыми данными"""
    dir_path = f'c:\\reebok_pl\\html_data\\kids-baby-0-4-years-baby-shoes'
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for page in range(0, totalResources_kids_baby_0_4_years_baby_shoes + 2):
        if page == 1:
            url_kids_baby_0_4_years_baby_shoes = "https://www.reebok.eu/en-pl/shopping/kids-baby-0-4-years-baby-shoes"
            scraper_get_kids_baby_0_4_years_baby_shoes = scraper.get(url_kids_baby_0_4_years_baby_shoes).content
            soup = BeautifulSoup(scraper_get_kids_baby_0_4_years_baby_shoes, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\kids-baby-0-4-years-baby-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            time.sleep(1)
        if page > 1:
            counter_kids_baby_0_4_years_baby_shoes += 1
            url_kids_baby_0_4_years_baby_shoes_api = f'https://www.reebok.eu/en-pl/shopping/kids-baby-0-4-years-baby-shoes?pageindex={counter_kids_baby_0_4_years_baby_shoes}'
            scraper_get_kids_baby_0_4_years_baby_shoes = scraper.get(url_kids_baby_0_4_years_baby_shoes_api).content
            soup = BeautifulSoup(scraper_get_kids_baby_0_4_years_baby_shoes, 'lxml')
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text = script[1].text
            data = json.loads(json_text)
            with open(f"c:\\reebok_pl\\html_data\\kids-baby-0-4-years-baby-shoes\\0_{page}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(1)
        print(f"kids-baby-0-4-years-baby-shoes {counter_kids_baby_0_4_years_baby_shoes} из {totalResources_kids_baby_0_4_years_baby_shoes + 1}")
    print(f"Собрал kids-baby-0-4-years-baby-shoes")


"""Собираем все ссылки на товары"""
def parsing_url_json():
    folders = [r"c:\reebok_pl\html_data\kids-baby-0-4-years-baby-shoes\*.json",
               r"c:\reebok_pl\html_data\kids-kids-5-8-years-kids-shoes\*.json",
               r"c:\reebok_pl\html_data\kids-youth-9-14\*.json",
               r"c:\reebok_pl\html_data\women-shoes\*.json",
               r"c:\reebok_pl\html_data\men-shoes\*.json"
               ]
    for folder in folders:
        urls = []
        files_json = glob.glob(folder)
        group = files_json[0].split("\\")[-2]
        for item in files_json:
            with open(item, encoding='utf-8') as f:
                data = json.load(f)
                all_products = data['itemListElement']
                coun = 0
                for url in all_products:
                    coun +=1
                    urls.append(url['url'])
        with open(f'c:\\reebok_pl\\csv_url\\{group}\\url.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
            writer.writerow(urls)
    print("Собрали все url")

def parsin_contact_html():
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })
    today = datetime.today()
    date_str = today.strftime('%d/%m')
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    folders_html = [r"c:\reebok_pl\html_product\men-shoes\*.html",
               r"c:\reebok_pl\html_product\women-shoes\*.html",
               r"c:\reebok_pl\html_product\kids-youth-9-14\*.html",
               r"c:\reebok_pl\html_product\kids-kids-5-8-years-kids-shoes\*.html",
               r"c:\reebok_pl\html_product\kids-baby-0-4-years-baby-shoes\*.html"
               ]

    response = requests.get('https://myfin.by/currency/minsk')
    root = html.fromstring(response.text)
    value = root.xpath('//div[@class="c-best-rates"]//table//tbody//tr[4]//td[4]/text()')
    """Курс Беларуских"""
    bel = (float(value[0])) / 10
    # print(bel)
    for file in folders_html[4:]: # Убарть срез выбор папки!
        group = file.split('\\')[3]
        # print(group)
        with open(f"c:\\reebok_pl\\csv_data\\{group}.csv", "w",
                  errors='ignore', encoding="utf-8") as file_csv:
            writer = csv.writer(file_csv, delimiter=",", lineterminator="\r")
            writer.writerow(
                (
                    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags', 'Published',
                    'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name',
                    'Option3 Value',
                    'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
                    'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                    'Variant Compare At Price',
                    'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src',
                    'Image Position',
                    'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
                    'Google Shopping / Google Product Category', 'Google Shopping / Gender',
                    'Google Shopping / Age Group',
                    'Google Shopping / MPN', 'Google Shopping / AdWords Grouping',
                    'Google Shopping / AdWords Labels',
                    'Google Shopping / Condition', 'Google Shopping / Custom Product',
                    'Google Shopping / Custom Label 0',
                    'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2',
                    'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4', 'Variant Image',
                    'Variant Weight Unit', 'Variant Tax Code', 'Cost per item', 'Included / Belarus',
                    'Included / International', 'Price / International', 'Compare At Price / International',
                    'Status'
                )
            )
        files_json = glob.glob(file)

        for item in files_json: # Убарть срез выбор файла!
            with open(item, 'r', encoding='utf-8') as file:
                html_content = file.read()
            counter = 0
            sizes = []
            soup = BeautifulSoup(html_content, 'lxml')
            try:
                table_size = soup.find('div', class_='css-4sx26k')
            except:
                continue

            try:
                div_elements = table_size.find_all('div', class_='css-19xoysq')
            except:
                continue

            for div in div_elements:
                disabled_attr = div.find('input', disabled=True)
                if disabled_attr is not None:
                    continue  # Пропускаем элемент, если атрибут "disabled" присутствует
                label = div.find('label', class_='css-zcfdzo')

                if label is not None:
                    extracted_value = label.text.strip()
                    sizes.append(extracted_value)
            script = soup.find_all('script', {'type': 'application/ld+json'})
            json_text_1 = script[1].text.replace("\\'n\\'", ' ')
            data_1 = json.loads(json_text_1)
            Handle = data_1['productID']
            Title = "Reebok " + soup.find('h2', class_="css-1wx06p0").text
            #
            id_product = data_1['productID']
            category_product_old = soup.find('p', class_="css-18y5zfz").text
            if category_product_old == 'Classics':
                category_product = 'Lifestyle/Повседневные'
            else:
                category_product = 'Спорт/Зал'
            Vendor = "Reebok"
            picture_dicts = data_1['image']
            alls_photo = []
            for i, photo_url in enumerate(picture_dicts):
                index = i + 1
                photo_link = photo_url.replace("_200.jpg", "_1000.jpg")
                alls_photo.append(photo_link)
            color_old = data_1['color']
            color = ''
            try:
                color_old = data_1['color'].split('/')[0].strip()
                with open(r'c:\\reebok_pl\\colors.csv', newline='', encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    for row in reader:
                        if row[0] == color_old:
                            color = row[1]
                            break
                        else:
                            color = color_old
            except:
                color = None

            coun = 0
            pfoto_site = []
            # for img in alls_photo:
            #     coun += 1
            img_groups = {
                "kids-baby-0-4-years-baby-shoes": "img_kids-baby-0-4-years-baby-shoes",
                "kids-kids-5-8-years-kids-shoes": "img_kids-kids-5-8-years-kids-shoes",
                "kids-youth-9-14t": "img_kids-youth-9-14",
                "men-shoes": "img_men-shoes",
                "women-shoes": "img_women-shoes"
            }


            for coun, img in enumerate(alls_photo, 1):
                img_group_folder = img_groups.get(group)
                if img_group_folder:
                    pfoto_site.append(
                        f"https://loketsneakers.s3.eu-central-1.amazonaws.com/{img_group_folder}/{id_product}_{coun}.webp")
                    file_path = f"c:\\reebok_pl\\data_img\\{img_group_folder}\\{id_product}_{coun}.webp"
                    new_file_path = f"c:\\reebok_pl\\csv_data\\{img_group_folder}\\{id_product}_{coun}.webp"
                    if not os.path.exists(file_path):
                        img_data = scraper.get(img, stream=True)
                        with open(new_file_path, "wb") as f:
                            img_data.raw.decode_content = True
                            shutil.copyfileobj(img_data.raw, f)

            table_price = soup.find('section', class_="css-a5s3hw")
            try:
                sell_price = table_price.find('span', attrs={'data-test': 'product-salePrice'}).text.replace(" z\\xc5\\x82", "")
            except:
                sell_price = 0
            base_price = table_price.find('span', attrs={'data-test': 'product-price'}).text.replace(" z\\xc5\\x82", "")
            if not base_price:
                base_price = 0
            # print(f"{type(base_price)} - {base_price} - Файл {item}")
            # print(sell_price, base_price)
            """Формирование цены с курсом"""
            Variant_Price = 0
            Variant_Compare_At_Price = 0
            if sell_price > 0:
                Variant_Price = round(((float(sell_price) + 60.0) * 1.1) * bel, 1)  # два знака после запятой
                Variant_Price = str(Variant_Price).replace('.', ',')
                Variant_Compare_At_Price = round(((float(base_price) + 60.0) * 1.1) * bel,
                                                 1)  # два знака после запятой
                Variant_Compare_At_Price = str(Variant_Compare_At_Price).replace('.', ',')
            elif sell_price == 0:
                Variant_Price = round(((float(base_price) + 60.0) * 1.1) * bel, 1)  # два знака после запятой
                Variant_Price = str(Variant_Price).replace('.', ',')
                Variant_Compare_At_Price = ""
            index_photo = 1  # Initialize photo index

            for i, size in enumerate(sizes):
                if i < len(pfoto_site):
                    photo = pfoto_site[i]
                    index_photo_str = str(index_photo)  # convert index to string
                    index_photo += 1  # Increment photo index for each iteration
                else:
                    photo = ""
                    index_photo_str = ""  # leave index_photo_str empty
                data_dict = [Handle, Title, "", Vendor, 'Apparel & Accessories > Shoes', category_product,
                        f'{color}, {date_str}', 'TRUE',
                        'Размер', size, "", "", "", "", "", "", "", "999", "continue", "manual", Variant_Price,
                        Variant_Compare_At_Price, "TRUE", "TRUE", "", photo, index_photo_str, "", "", "", "",
                        "", "", "",
                        "",
                        "", "", "", "", "", "", "", "", "", "", "kg", "", "", "TRUE", "TRUE", "", "", "Active"]
                with open(f"c:\\reebok_pl\\csv_data\\{group}.csv", "a",
                          errors='ignore', encoding="utf-8") as file:
                    writer = csv.writer(file, delimiter=",", lineterminator="\r")
                    writer.writerow((data_dict))

            # If there are more photos than sizes, fill in the remaining rows with empty data except for photo and index
            if len(pfoto_site) > len(sizes):
                alls_photo = []
                for picture_dict in picture_dicts:
                    # print(picture_dict)
                    photo_url =picture_dict.replace("_200.jpg", "_1000.jpg")
                    alls_photo.append(photo_url)
                for j in range(len(sizes), len(pfoto_site)):
                    photo = pfoto_site[j]
                    index_photo_str = str(index_photo)  # convert index to string
                    data_d = [Handle, Title, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '',
                            '', '', '', '', '', photo, index_photo_str, '', '', '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '', '', ""]
                    with open(f"c:\\reebok_pl\\csv_data\\{group}.csv", "a",
                              errors='ignore', encoding="utf-8") as file:
                        writer = csv.writer(file, delimiter=",", lineterminator="\r")
                        writer.writerow((data_d))
                    index_photo += 1

def move_img():
    folders = {
        r'c:\reebok_pl\csv_data\img_kids-baby-0-4-years-baby-shoes': r'c:\reebok_pl\data_img\img_kids-baby-0-4-years-baby-shoes',
        r'c:\reebok_pl\csv_data\img_kids-kids-5-8-years-kids-shoes': r'c:\reebok_pl\data_img\img_kids-kids-5-8-years-kids-shoes',
        r'c:\reebok_pl\csv_data\img_kids-youth-9-14': r'c:\reebok_pl\data_img\img_kids-youth-9-14',
        r'c:\reebok_pl\csv_data\img_men-shoes': r'c:\reebok_pl\data_img\img_men-shoes',
        r'c:\reebok_pl\csv_data\img_women-shoes': r'c:\reebok_pl\data_img\img_women-shoes'
    }

    for src, dest in folders.items():
        for root, dirs, files in os.walk(src):
            dest_root = root.replace(src, dest)
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_root, file)
                shutil.move(src_path, dest_path)

def del_files_html_product():
    folders_del = [r"c:\reebok_pl\html_data\kids-baby-0-4-years-baby-shoes",
               r"c:\reebok_pl\html_data\kids-kids-5-8-years-kids-shoes",
               r"c:\reebok_pl\html_data\kids-youth-9-14",
               r"c:\reebok_pl\html_data\men-shoes",
               r"c:\reebok_pl\html_data\women-shoes"
               ]
    for folder in folders_del:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")





if __name__ == '__main__':
    # move_img()
    # print('Переместили изображение в папку с БД')
    # del_files_html_product()
    # print("Удалили старые файлы HTML")
    # save_json_product()
    # print("Сохранили все JSON")
    # parsing_url_json()
    # print('Собрали все ссылки')
    # print('Переходим к скрипту main_asio.py')

    parsin_contact_html()
    print("Все получили")


""""Запуск по времени"""
# def job():
#     # Ваш код здесь
#     if __name__ == '__main__':
#         """Перемещаем изображение в папку с БД"""
#         move_img()
#         """Удаляем старые файлы HTML"""
#         del_files_html_product()
#         save_json_product()
#         parsing_url_json()
#         main_asio()
#         parsin_contact_html()
#
# schedule.every().day.at("07:00").do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
