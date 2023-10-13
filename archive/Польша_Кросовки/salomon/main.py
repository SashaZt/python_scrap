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
import cloudscraper
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv
wait_time = random.uniform(5, 10)
scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })
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
cookies = {
    'form_key': 'Yv9mTf1bQx5qEH2r',
    'PHPSESSID': '1feea8e2974359c3cfd2632e35bd4a17',
    '_pxhd': 's8-ny9JSej4MU3SwnyRd9S8v8RZnIJJnbAaNEtm3DDxizC/zipZrWOoXbs2Y5sSmWMOkadBE3RpcwQA/kDlkZQ==:yApEOv-5kHz3xj0AvXPQrhPpFRCAQWylay/DJ5a2GvVgJL0JNsC/7CPnhWVFSef3q066c2w8M0Uz25XE4xMpqpF-4qRFldYfSko4hEIbofk=',
    'UUID': 'e0629043-ff2a-41c9-985d-d271f3e0fb51',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+May+24+2023+12^%^3A47^%^3A43+GMT^%^2B0300+(^%^D0^%^92^%^D0^%^BE^%^D1^%^81^%^D1^%^82^%^D0^%^BE^%^D1^%^87^%^D0^%^BD^%^D0^%^B0^%^D1^%^8F+^%^D0^%^95^%^D0^%^B2^%^D1^%^80^%^D0^%^BE^%^D0^%^BF^%^D0^%^B0^%^2C+^%^D0^%^BB^%^D0^%^B5^%^D1^%^82^%^D0^%^BD^%^D0^%^B5^%^D0^%^B5+^%^D0^%^B2^%^D1^%^80^%^D0^%^B5^%^D0^%^BC^%^D1^%^8F)&version=202302.1.0&isIABGlobal=false&hosts=&genVendors=V8^%^3A0^%^2CV28^%^3A0^%^2CV18^%^3A0^%^2CV10^%^3A0^%^2CV4^%^3A0^%^2CV26^%^3A0^%^2CV12^%^3A0^%^2CV19^%^3A0^%^2CV11^%^3A0^%^2CV21^%^3A0^%^2CV22^%^3A0^%^2CV23^%^3A0^%^2CV7^%^3A0^%^2CV2^%^3A0^%^2CV25^%^3A0^%^2CV16^%^3A0^%^2CV14^%^3A0^%^2CV9^%^3A0^%^2CV27^%^3A0^%^2CV3^%^3A0^%^2CV13^%^3A0^%^2CV15^%^3A0^%^2CV6^%^3A0^%^2CV24^%^3A0^%^2CV5^%^3A0^%^2CV17^%^3A0^%^2C&consentId=4df5be68-cae1-45bd-9f32-a60e71262328&interactionCount=1&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0003^%^3A1^%^2CC0002^%^3A1^%^2CC0004^%^3A1&geolocation=UA^%^3B18&AwaitingReconsent=false',
    'pxcts': '02d81152-fa18-11ed-955b-44504c784759',
    '_pxvid': '016fb9c1-fa18-11ed-9fb2-522cb1e0961f',
    'geoIp_country_code': '^%^7B^%^22country_code^%^22^%^3A^%^22PL^%^22^%^7D',
    '_px2': 'eyJ1IjoiMDc1ZTQwZDAtZmExOC0xMWVkLWE5MDQtMGZiZWE2NmM2NWQ0IiwidiI6IjAyOGNhYjUzLWZhMTgtMTFlZC1iMDhkLWNiOTk5ZTM3YjUxOCIsInQiOjE2ODQ5MjM2NDk1OTksImgiOiI3ZTZhYTU4OTdkOGRiNjhhNjg1MDY3ODdhODc4ZTRlMWRhZjIwN2ZiYTdiYTM1Mzk2NWRiNDA5M2Q4Y2E2NjUyIn0=',
    'OptanonAlertBoxClosed': '2023-05-24T09:47:37.536Z',
    'AMCV_DFBF2C1653DA80920A490D4B^%^40AdobeOrg': '179643557^%^7CMCMID^%^7C65575658457533855045850372181627544039^%^7CMCAID^%^7CNONE^%^7CMCOPTOUT-1684928867s^%^7CNONE^%^7CvVersion^%^7C5.5.0',
    's_ecid': 'MCMID^%^7C65575658457533855045850372181627544039',
    'AMCVS_DFBF2C1653DA80920A490D4B^%^40AdobeOrg': '1',
    'at_check': 'true',
    'mbox': 'session^#69d3dbd9083045f082671c0978c46545^#1684923527',
    's_cc': 'true',
    '_ga_Y9PJ3VZ8E4': 'GS1.1.1684921661.1.1.1684921666.55.0.0',
    '_ga': 'GA1.1.831945971.1684921661',
    '_gcl_au': '1.1.1607385794.1684921661',
    '_ga_Q3HF4EKNG8': 'GS1.1.1684921661.1.0.1684921667.0.0.0',
    '_cs_c': '0',
    '_cs_cvars': '^%^7B^%^7D',
    '_cs_id': 'b6812439-e872-a182-fbdb-a1541d8e871a.1684921661.1.1684921667.1684921661.1.1719085661596',
    '_cs_s': '2.0.0.1684923467258',
    'FPLC': 'HKK^%^2FnizTq7UyU7w5kbXuHSrQUpgU0QnUUDBxEWQ46rqYOxBLxfa0g3ahyyEvgFZivWpMjHtZdZAWWh0IKNzPMLLgf7hMmYVRUyxQYBe8Uf^%^2FieLR5iOzvtlAtkdCQ5Q^%^3D^%^3D',
    'FPID': 'FPID2.2.8R5Xrz7uQH637YWAsSq6SD6Hri6jd0b8SOMc^%^2BrIRISk^%^3D.1684921661',
    '_uetsid': '0a5507b0fa1811edb8802dc6a6385f61',
    '_uetvid': '0a551f60fa1811ed951be3497a805e75',
    '_pin_unauth': 'dWlkPVpHTTFPRFl6TjJNdE0yWXpNQzAwTVRnM0xXSXhNMlF0TlRsa1pXTXpaVE5sTVRVeQ',
}

def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    # Установка параметров headers
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    chrome_options.add_argument(
        '--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    chrome_options.add_argument('--accept-language=ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6')
    chrome_options.add_argument('--dnt=1')
    chrome_options.add_argument('--authority=www.salomon.com')
    chrome_options.add_argument('--cache-control=max-age=0')
    chrome_options.add_argument('--Connection=keep-alive')
    chrome_options.add_argument('--Upgrade-Insecure-Requests=1')
    chrome_options.add_argument('--sec-ch-ua=Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"')
    chrome_options.add_argument('--sec-ch-ua-platform=Windows')
    chrome_options.add_argument('--sec-fetch-mode=navigate')
    chrome_options.add_argument('--sec-fetch-site=same-origin')

    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--disable-extensions') # Отключает использование расширений
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-setuid-sandbox')
    # chrome_options.add_argument("--incognito")  # Открытие в режиме инкогнито
    # chrome_options.add_argument("--disable-cache")  # Отключение кэширования
    # chrome_options.add_argument("--disable-cookies")  # Отключение использования куков
    # proxy = ("195.123.193.74", 2831, "36507", "E6KMONDv")
    # proxy_extension = ProxyExtension(*proxy)
    # chrome_options.add_argument(f"--load-extension={proxy_extension.directory}")
    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    # """Рабочая настройка для обхода Cloudflare """
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     'source': '''
    #            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    #            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    #            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    #      '''
    # })
    return driver

def get_urls_products():
    urls = [
        "https://www.salomon.com/pl-pl/shop-emea/men/shoes.html",
        "https://www.salomon.com/pl-pl/shop-emea/women/shoes.html",
        "https://www.salomon.com/pl-pl/shop-emea/kids/shoes.html"
    ]
    for url in urls:
        group = url.split("/")[-2]
        html = scraper.get(url).content  # , proxies=proxies
        soup = BeautifulSoup(html, 'lxml')
        all_col = int(soup.find('div', class_='segmented-product-list_total').text.replace('Produkty: ', "").strip())
        col_range = all_col // 10
        urls_product = []
        for i in range(1, col_range + 1):
            time.sleep(5)
            page_url = f"{url}?p={i}"
            request = scraper.get(page_url).content
            soup = BeautifulSoup(request, 'lxml')
            url_product = soup.find_all('a', attrs={'ref': 'linkHead'})
            for u in url_product:
                if "https://www.salomon.com/pl-pl/shop-emea/product" in u['href']:
                    urls_product.append(u['href'])

        with open(f"csv_url/{group}/url.csv", "w", newline="", encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[url] for url in urls_product])


    #     driver.get(url)
    #     # for name, value in cookies.items():
    #     #     driver.add_cookie({'name': name, 'value': value})
    #     # time.sleep(5)
    #     driver.refresh()
    #     # time.sleep(60)
    #     wait = WebDriverWait(driver, 30)
    #     try:
    #         button_clouse_wait = wait.until(
    #             EC.presence_of_element_located((By.XPATH, '//button[@class="popin_close popin-pushs-close"]')))
    #         button_clouse = driver.find_elements(By.XPATH, '//button[@class="popin_close popin-pushs-close"]')[0].click()
    #         time.sleep(wait_time)
    #     except:
    #         continue
    #     try:
    #         button_cookies_wait = wait.until(
    #             EC.presence_of_element_located((By.XPATH, '//button[@class="cookie-accept-all"]')))
    #         button_cookies = driver.find_element(By.XPATH, '//button[@class="cookie-accept-all"]').click()
    #         time.sleep(wait_time)
    #     except:
    #         continue
    #     urls_product = []
    #     for k in range(60):
    #         driver.execute_script("window.scrollBy(0,500)","")
    #         time.sleep(wait_time)
    #     time.sleep(wait_time)
    #     url_product = driver.find_elements(By.XPATH, '//a[@ref="linkHead"]')
    #     for u in url_product:
    #         urls_product.append(u.get_attribute("href"))
    #     with open(f"csv_url/{group}/url.csv", "w", newline="", encoding='utf-8') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerows([[url] for url in urls_product])
    # driver.close()
    # driver.quit()

def get_html_products():
    categories = ['kids', 'men', 'women']
    driver = get_chromedriver()
    for category in categories: #Убрать срез
        counter = 0
        with open(f'c:\\salomon_pl\\csv_url\\{category}\\url.csv', newline='', encoding='utf-8') as files:
            urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
            if os.path.isfile(f'c:\\salomon_pl\\csv_url\\{category}\\url.csv'):
                with open(f'c:\\salomon_pl\\csv_url\\{category}\\url.csv', newline='', encoding='utf-8') as files:
                    urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
            for url in urls: #Убрать срез
                counter += 1
                filename = f"c:\\salomon_pl\\html_product\\{category}\\0_{counter}.html"
                if os.path.isfile(filename):
                    continue  # Если файл уже существует, переходим к следующей итерации цикл
                driver.get(url[0])
                time.sleep(wait_time)
                wait = WebDriverWait(driver, 30)
                try:
                    button_clouse_wait = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//button[@class="popin_close popin-pushs-close"]')))
                    button_clouse = driver.find_elements(By.XPATH, '//button[@class="popin_close popin-pushs-close"]')[
                        0].click()
                except:
                    continue
                try:
                    button_cookies_wait = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//button[@class="cookie-accept-all"]')))
                    button_cookies = driver.find_element(By.XPATH, '//button[@class="cookie-accept-all"]').click()
                except:
                    continue
                driver.execute_script("window.scrollBy(0,3000)", "")
                time.sleep(wait_time)
                filename = f"c:\\salomon_pl\\html_product\\{category}\\0_{counter}.html"
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(driver.page_source)
        driver.close()
        driver.quit()

def move_img():
    folders = {
        r'c:\salomon_pl\csv_data\img_kids': r'c:\salomon_pl\data_img\img_kids',
         r'c:\salomon_pl\csv_data\img_men': r'c:\salomon_pl\data_img\img_men',
        r'c:\salomon_pl\csv_data\img_women': r'c:\salomon_pl\data_img\img_women'
    }

    for src, dest in folders.items():
        for root, dirs, files in os.walk(src):
            dest_root = root.replace(src, dest)
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_root, file)
                shutil.move(src_path, dest_path)


def del_files_html_product():
    folders_del = [r"c:\salomon_pl\html_product\kids",
                   r"c:\salomon_pl\html_product\men",
                   r"c:\salomon_pl\html_product\women"
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
    print("Переносим файлы с изображением")
    move_img()
    print("Удаляем старые данные")
    del_files_html_product()
    print('Собираем все ссылки на товары')
    get_urls_products()
    print('Запускаем обработку main_proxy.py')
