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
    cookies = {
        'userLang': 'en',
        'nlbi_242093': '3VItFF2VOBoHUUB+JDHybgAAAABsraBHQ9k9WpA8YOPY8dxS',
        'timezone': 'Europe%2FKiev',
        's_ppv': '100',
        'userCategory': 'RPU',
        's_fid': '7B97EB489ACC0C92-3446E08462F183D3',
        'g2usersessionid': '0b4f61da6613900ecce840bc5d774668',
        'search-table-rows': '20',
        'visid_incap_242093': 'UOYi1RRfTzyJ7jo9JOPVyJz6omQAAAAAQkIPAAAAAACAF2utAZJ4uQRFQhFj8qgTt+ndHEwc+Hdu',
        'incap_ses_323_242093': 'aIGEbkfOcxhzexi0wId7BJkrpWQAAAAAOM24/pM9WsAdU7V1mu9xFQ==',
        'G2JSESSIONID': 'DE6C9C9F61E8ED4898A810D7852B0B7B-n1',
        'classicSearchResultsView': 'true',
        'reese84': '3:BnX8RLS4MJQAKxRpmEiwew==:a/Xy1nKWB3+dJVmLWI9/dKkHI1h8Qm4LtK8K71kFiBPmWRc8NR2JqWWUyIpn51d8ZLQZWYzwanKvamK5HAqBamrBIiViE9Z6CkIAShngiOOLGWBAyZxjrQhyejpXZavy+5pKAhTKdQc9FM+CrBqi3ag5nHJiuj8MiSCMWEyQ9xa2oCMXiuaXVYpjpXJsOqicLTEdHs0Jz5GojTl/BKudeLdhI2UMCL2zKtpSjZftUfPPTEmmT4B/COFqxvbOynFZATBPOGenWRkdPBGGF5Fvyszdfin5NnJIKD5oIuQ7UkXqtU7VE0PFCWsbyfiSS+BLtUudPxGcWusy1KDwdza6clRzhkpBLrm8DUknE2t4CkAxBnw6J6tApEeY4uQPes7EqOwb/Z2pJeIAX3/ISJi6bRihja5PYeXEniZO3m911kY89NZ0yK1IxZEipI/9SBS5SCLntrQzudNb7mya3dLaS0QRfHPqbBXSp14UFpwVUBd9yOOFGguR6HmHrK9N2/ywPE67IHsU2pECaNKXJaEu5w==:cVJCouWbe77w+B3nL5fwU+fk5hhX7nR5SzEeuoH9/3k=',
        's_depth': '1',
        's_pv': 'no%20value',
        's_nr': '1688549546977-Repeat',
        's_vnum': '1690995053533%26vn%3D5',
        's_invisit': 'true',
        's_lv': '1688549546978',
        's_lv_s': 'Less%20than%201%20day',
        'copartTimezonePref': '%7B%22displayStr%22%3A%22GMT%2B3%22%2C%22offset%22%3A3%2C%22dst%22%3Atrue%2C%22windowsTz%22%3A%22Europe%2FKiev%22%7D',
        'nlbi_242093_2147483392': 'Jai4SSOlUV/hmPIOJDHybgAAAABEl2Q8SU82VAIBNfgoSSQN',
    }

    headers = {
        'authority': 'www.copart.com',
        'accept': '*/*',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'cache-control': 'no-cache',
        # 'cookie': 'userLang=en; nlbi_242093=3VItFF2VOBoHUUB+JDHybgAAAABsraBHQ9k9WpA8YOPY8dxS; timezone=Europe%2FKiev; s_ppv=100; userCategory=RPU; s_fid=7B97EB489ACC0C92-3446E08462F183D3; g2usersessionid=0b4f61da6613900ecce840bc5d774668; search-table-rows=20; visid_incap_242093=UOYi1RRfTzyJ7jo9JOPVyJz6omQAAAAAQkIPAAAAAACAF2utAZJ4uQRFQhFj8qgTt+ndHEwc+Hdu; incap_ses_323_242093=aIGEbkfOcxhzexi0wId7BJkrpWQAAAAAOM24/pM9WsAdU7V1mu9xFQ==; G2JSESSIONID=DE6C9C9F61E8ED4898A810D7852B0B7B-n1; classicSearchResultsView=true; reese84=3:BnX8RLS4MJQAKxRpmEiwew==:a/Xy1nKWB3+dJVmLWI9/dKkHI1h8Qm4LtK8K71kFiBPmWRc8NR2JqWWUyIpn51d8ZLQZWYzwanKvamK5HAqBamrBIiViE9Z6CkIAShngiOOLGWBAyZxjrQhyejpXZavy+5pKAhTKdQc9FM+CrBqi3ag5nHJiuj8MiSCMWEyQ9xa2oCMXiuaXVYpjpXJsOqicLTEdHs0Jz5GojTl/BKudeLdhI2UMCL2zKtpSjZftUfPPTEmmT4B/COFqxvbOynFZATBPOGenWRkdPBGGF5Fvyszdfin5NnJIKD5oIuQ7UkXqtU7VE0PFCWsbyfiSS+BLtUudPxGcWusy1KDwdza6clRzhkpBLrm8DUknE2t4CkAxBnw6J6tApEeY4uQPes7EqOwb/Z2pJeIAX3/ISJi6bRihja5PYeXEniZO3m911kY89NZ0yK1IxZEipI/9SBS5SCLntrQzudNb7mya3dLaS0QRfHPqbBXSp14UFpwVUBd9yOOFGguR6HmHrK9N2/ywPE67IHsU2pECaNKXJaEu5w==:cVJCouWbe77w+B3nL5fwU+fk5hhX7nR5SzEeuoH9/3k=; s_depth=1; s_pv=no%20value; s_nr=1688549546977-Repeat; s_vnum=1690995053533%26vn%3D5; s_invisit=true; s_lv=1688549546978; s_lv_s=Less%20than%201%20day; copartTimezonePref=%7B%22displayStr%22%3A%22GMT%2B3%22%2C%22offset%22%3A3%2C%22dst%22%3Atrue%2C%22windowsTz%22%3A%22Europe%2FKiev%22%7D; nlbi_242093_2147483392=Jai4SSOlUV/hmPIOJDHybgAAAABEl2Q8SU82VAIBNfgoSSQN',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.copart.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    response = requests.get(
        'https://www.copart.com/public/data/lotdetails/solr/43079133',

        cookies=cookies,
        headers=headers, )
    data = response.json()
    filename = f"c:\\DATA\\copart\\product\\data.json"
    with open(filename, 'w') as f:
        json.dump(data, f)

def parsin():
    with open('c:\\DATA\\copart\\product\\data.json', 'r') as f:
        # Загрузить JSON из файла
        data = json.load(f)
    'https: // www.copart.com / lot / 43079133 / salvage - 2018 - ford - focus - se - fl - miami - south'
    ln = data['data']['lotDetails']['ln']
    url_lot = f"https://www.copart.com/lot/{ln}"
    url_img = data['data']['lotDetails']['tims']
    name_lot = data['data']['lotDetails']['ld']
    price_bnp = data['data']['lotDetails']['bnp']
    odometer_lot = data['data']['lotDetails']['orr']
    drive_lot = data['data']['lotDetails']['drv']
    engine_type_lot = data['data']['lotDetails']['egn']
    vehicle_type_lot = data['data']['lotDetails']['vehTypDesc']


    print(vehicle_type_lot)


if __name__ == '__main__':
    # get_requests()
    # get_cloudscraper()
    # get_selenium()
    # get_id_ad_and_url()
    # get_product()
    parsin()
