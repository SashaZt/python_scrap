from datetime import datetime
import requests
import re
import random
import json
from bs4 import BeautifulSoup
from lxml import html
import glob
from selenium.webdriver.chrome.service import Service
import os
import shutil
import tempfile
from selenium.webdriver.common.action_chains import ActionChains
import zipfile
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv
wait_time = random.uniform(5, 10)
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


def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")
    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    """Рабочая настройка для обхода Cloudflare """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
               delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
               delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
               delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
         '''
    })
    return driver

def parsing_html():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Необходимо для работы в фоновом режиме (без отображения окна браузера)
    s = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

    today = datetime.today()
    date_str = today.strftime('%d/%m')
    folders_html = [r"c:\salomon_pl\html_product\kids\*.html",
                    r"c:\salomon_pl\html_product\men\*.html",
                    r"c:\salomon_pl\html_product\women\*.html"
                    ]
    """Курс Беларуских"""
    url_myfin_by = "https://myfin.by/bank/kursy_valjut_nbrb/pln"
    response = requests.get(url_myfin_by, headers=header)
    root = html.fromstring(response.text)
    value = root.xpath('//div[@class="h1"][1]/text()')[0]
    bel = float(value) / 10
    for file in folders_html:  # Убарть срез для категории!
        group = file.split('\\')[3]

        with open(f"c:\\salomon_pl\\csv_data\\{group}.csv", "w",
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
        coun = 0
        files_json = glob.glob(file)
        for item in files_json:  # Убарть срез для файла!
            counter = 0
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')


            table_size = soup.find('div', attrs={'class': 'size-selection_sizes'})
            try:
                all_size = table_size.find_all('li', attrs={'class': 'input-size'})
            except:
                continue
            sizes = []
            for s in all_size:
                size_one = s.find('span', attrs={'class': 'label'}).text.strip()
                if ' ' not in size_one:
                    continue  # Пропустить итерацию, если нет пробела в size_one
                whole_number, fraction = size_one.split(' ')
                if fraction == '1/2':
                    fraction = '.5'
                elif fraction == '2/3':
                    fraction = '.6'
                elif fraction == '1/3':
                    fraction = '.3'
                elif fraction == '⅓':
                    fraction = '.3'
                elif fraction == '⅔':
                    fraction = '.6'
                size_decimal = round(float(whole_number) + float(fraction), 1)
                sizes.append(size_decimal)

            scripts = soup.find_all('script', {'type': 'application/ld+json'})
            # print(scripts)
            if 'name' in json.loads(scripts[0].string):
                json_data = json.loads(scripts[0].string)
            elif 'name' in json.loads(scripts[2].string):
                json_data = json.loads(scripts[2].string)

            Title = "Salomon " + json_data['name']
            Handle = json_data['sku']

            """Открыть когда разберемся с курсом"""
            base_price_float = float(soup.find('div', attrs={'class': 'product-price -pdp'}).find('span', attrs={'class': 'price'}).text.replace("zł", "").replace("\xa0", "").replace(",", "."))


            base_price_round = round(base_price_float)
            base_price = int(base_price_round)
            Variant_Price = round(((float(base_price) + 60.0) * 1.1) * bel, 1)  # два знака после запятой
            Variant_Price = str(Variant_Price).replace('.', ',')
            Variant_Compare_At_Price = ""
            category_product_old = json_data['category']
            category_product = category_product_old

            with open('c:\\salomon_pl\\dict.csv', newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for row in reader:
                    if row[0] == category_product_old:
                        category_product = row[1]
                        break

            div_tag = soup.find('div', attrs={'class': 'swatch-opt magepack-swatches'})

            json_data_01 = json.loads(div_tag['data-json-config'])

            Vendor = "Salomon"

            """Блок получение изображения"""
            driver.get(item)
            html_content = driver.page_source
            soup_img = BeautifulSoup(html_content, 'lxml')
            alls_photo = []
            try:
                product_image_divs = soup_img.find('div', attrs={'class': 'product-slider_nav'}).find_all('img')
                # product_image_divs = driver.find_elements(By.XPATH, '//div[@class="product-slider_nav"]//img')
                for i in product_image_divs:
                    src = i.get('src')
                    if src and re.search(r'https://www.salomon.com/pl-pl/shop-emea/media', src):
                        alls_photo.append(src.split('.png')[0] + '.png')

            except:
                alls_photo_set = set()
                product_image_divs = \
                soup_img.find_all('ul', attrs={'class': 'layout-pdp-media-grid slider-scroll_wrapper'})[0].find_all(
                    'source')
                # product_image_divs = driver.find_elements(By.XPATH, '//div[@class="product-slider_nav"]//img')
                for i in product_image_divs:
                    src = i.get('data-srcset')
                    if src and re.search(r'https://www.salomon.com/pl-pl/shop-emea/media', src):
                        urls = src.split('.png')[0] + '.png'
                        alls_photo_set.add(urls)
                alls_photo = list(alls_photo_set)

            coun = 0
            pfoto_site = []
            # for img in alls_photo:
            #     coun += 1
            img_groups = {
                "kids": "img_kids",
                "men": "img_men",
                "women": "img_women"
            }
            id_product = Handle
            for coun, img in enumerate(alls_photo, 1):
                img_group_folder = img_groups.get(group)
                if img_group_folder:
                    pfoto_site.append(
                        f"https://loketsneakers.s3.eu-central-1.amazonaws.com/{img_group_folder}/{id_product}_{coun}.webp")
                    file_path = f"c:\\salomon_pl\\data_img\\{img_group_folder}\\{id_product}_{coun}.webp"
                    new_file_path = f"c:\\salomon_pl\\csv_data\\{img_group_folder}\\{id_product}_{coun}.webp"
                    if not os.path.exists(file_path):
                        img_data = requests.get(img, headers=header)
                        with open(new_file_path, 'wb') as file_img:
                            file_img.write(img_data.content)
            color = ''
            try:
                color_old = soup.find('div', class_='product-options_selected').text.split('/')[0].strip()
                with open('colors.csv', newline='', encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    for row in reader:
                        if row[0] == color_old:
                            color = row[1]
                            break
                        else:
                            color = color_old
            except:
                color = None
            index_photo = 1  # Initialize photo index
            for i, size in enumerate(sizes):
                if i < len(pfoto_site):
                    photo = pfoto_site[i]
                    index_photo_str = str(index_photo)  # convert index to string
                    index_photo += 1  # Increment photo index for each iteration
                else:
                    photo = ""
                    index_photo_str = ""  # leave index_photo_str empty
                data = [Handle, Title, "", Vendor, 'Apparel & Accessories > Shoes', category_product,
                        f'{color}, {date_str}', 'TRUE',
                        'Размер', size, "", "", "", "", "", "", "", "999", "continue", "manual", Variant_Price,
                        "", "TRUE", "TRUE", "", photo, index_photo_str, "", "", "", "",
                        "", "", "",
                        "",
                        "", "", "", "", "", "", "", "", "", "", "kg", "", "", "TRUE", "TRUE", "", "", "Active"]
                with open(f"c:\\salomon_pl\\csv_data\\{group}.csv", "a",
                          errors='ignore', encoding="utf-8") as file:
                    writer = csv.writer(file, delimiter=",", lineterminator="\r")
                    writer.writerow((data))

            if len(pfoto_site) > len(sizes):
                for j in range(len(sizes), len(pfoto_site)):
                    photo = pfoto_site[j]
                    index_photo_str = str(index_photo)  # convert index to string
                    data = [Handle, Title, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '',
                            '', '', '', '', '', photo, index_photo_str, '', '', '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '', '', ""]
                    with open(f"c:\\salomon_pl\\csv_data\\{group}.csv", "a",
                              errors='ignore', encoding="utf-8") as file:
                        writer = csv.writer(file, delimiter=",", lineterminator="\r")
                        writer.writerow((data))
                    index_photo += 1



if __name__ == '__main__':
    parsing_html()
