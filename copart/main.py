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
from proxi import proxies

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
    time.sleep(1)
    coun = 0
    next_up = False
    while not next_up:
        try:
            coun += 1
            driver.execute_script("window.scrollBy(0,200)", "")
            pause_time = random.randint(1, 5)
            file_name = f"c:\\DATA\\copart\\list\\data_{coun}.html"
            with open(file_name, "w", encoding='utf-8') as fl:
                fl.write(driver.page_source)
                time.sleep(pause_time)
                print(f"Пауза {pause_time}")
            next_page = driver.find_element(By.XPATH, '//span[@class="p-paginator-icon pi pi-angle-right"]').click()
        except:
            break


def get_request():
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
        's_pv': 'no%20value',
        's_vnum': '1690995053533%26vn%3D6',
        's_invisit': 'true',
        's_lv_s': 'Less%20than%201%20day',
        'classicSearchResultsView': 'false',
        'reese84': '3:j3nWFM5DfXwSWpXQE+uoBQ==:dBTMeIC1FPWMt7ed8gzdXQmPzxabSuoYU9f6tTddmYoiCW9Cvph95nLaMsVHpZ2d1+sYYQwjhxxHNRm9K4TYBCFW0HfgQhS1jF7QHpVErnNIDK+TcF3zWJYQ3RRAR9fvZLFJqm1cEIx7lao3/R+8RS/tU/my2R3WZBxsYE717gjup2I2npfWSAXcczd+IHryVBb6RzL63MA1qqB4nJJqqHftHQHSXzTRuoF1ZfvWwUbycffpj+CkyKrYkmY7OQb4vZvvVu5A3v27J8LmPw7qAeSQmuIXLuUJ4Zht5fUb/xTk8fvLCSN5vTFRdK6jb9gl/zXyrz/I4pwi8ESp6uFX9rKlKx/yGAXarkIEeSucQzrv6ofjYXkWa13hIk6C3qty9wrrc7LHEwwg3/wB4WqjGvGZvy/CrWv50YUvtXbUwgvXYO9/BX54kHut+W+3DPLVxA/10mA1Y80Detk9pbO0bIKC/wavLOoMH6zJW+SGh7stNbWykGpprfn40vnlV8iDpXtLUF1BqkqpuDkZiKMjlA==:Uet8RctMMVSxOXRArZflaN8YVnhCtvO8rZ+vZ+1cwgY=',
        'nlbi_242093_2147483392': 'Ed2TSwo/TD7HvHMJJDHybgAAAACisH3S/7tajAF69TWPKcU6',
        'copartTimezonePref': '%7B%22displayStr%22%3A%22GMT%2B3%22%2C%22offset%22%3A3%2C%22dst%22%3Atrue%2C%22windowsTz%22%3A%22Europe%2FKiev%22%7D',
        's_depth': '4',
        's_nr': '1688559453085-Repeat',
        's_lv': '1688559453086',
    }

    headers = {
        'authority': 'www.copart.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'access-control-allow-headers': 'Content-Type, X-XSRF-TOKEN',
        'content-type': 'application/json',
        # 'cookie': 'userLang=en; nlbi_242093=3VItFF2VOBoHUUB+JDHybgAAAABsraBHQ9k9WpA8YOPY8dxS; timezone=Europe%2FKiev; s_ppv=100; userCategory=RPU; s_fid=7B97EB489ACC0C92-3446E08462F183D3; g2usersessionid=0b4f61da6613900ecce840bc5d774668; search-table-rows=20; visid_incap_242093=UOYi1RRfTzyJ7jo9JOPVyJz6omQAAAAAQkIPAAAAAACAF2utAZJ4uQRFQhFj8qgTt+ndHEwc+Hdu; incap_ses_323_242093=aIGEbkfOcxhzexi0wId7BJkrpWQAAAAAOM24/pM9WsAdU7V1mu9xFQ==; G2JSESSIONID=DE6C9C9F61E8ED4898A810D7852B0B7B-n1; s_pv=no%20value; s_vnum=1690995053533%26vn%3D6; s_invisit=true; s_lv_s=Less%20than%201%20day; classicSearchResultsView=false; reese84=3:j3nWFM5DfXwSWpXQE+uoBQ==:dBTMeIC1FPWMt7ed8gzdXQmPzxabSuoYU9f6tTddmYoiCW9Cvph95nLaMsVHpZ2d1+sYYQwjhxxHNRm9K4TYBCFW0HfgQhS1jF7QHpVErnNIDK+TcF3zWJYQ3RRAR9fvZLFJqm1cEIx7lao3/R+8RS/tU/my2R3WZBxsYE717gjup2I2npfWSAXcczd+IHryVBb6RzL63MA1qqB4nJJqqHftHQHSXzTRuoF1ZfvWwUbycffpj+CkyKrYkmY7OQb4vZvvVu5A3v27J8LmPw7qAeSQmuIXLuUJ4Zht5fUb/xTk8fvLCSN5vTFRdK6jb9gl/zXyrz/I4pwi8ESp6uFX9rKlKx/yGAXarkIEeSucQzrv6ofjYXkWa13hIk6C3qty9wrrc7LHEwwg3/wB4WqjGvGZvy/CrWv50YUvtXbUwgvXYO9/BX54kHut+W+3DPLVxA/10mA1Y80Detk9pbO0bIKC/wavLOoMH6zJW+SGh7stNbWykGpprfn40vnlV8iDpXtLUF1BqkqpuDkZiKMjlA==:Uet8RctMMVSxOXRArZflaN8YVnhCtvO8rZ+vZ+1cwgY=; nlbi_242093_2147483392=Ed2TSwo/TD7HvHMJJDHybgAAAACisH3S/7tajAF69TWPKcU6; copartTimezonePref=%7B%22displayStr%22%3A%22GMT%2B3%22%2C%22offset%22%3A3%2C%22dst%22%3Atrue%2C%22windowsTz%22%3A%22Europe%2FKiev%22%7D; s_depth=4; s_nr=1688559453085-Repeat; s_lv=1688559453086',
        'dnt': '1',
        'origin': 'https://www.copart.com',
        'referer': 'https://www.copart.com/lotSearchResults?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22FETI%22:%5B%22buy_it_now_code:B1%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': 'c6fc2bbf-5f17-499f-b6e9-4b7e8b065c7c',
    }

    ad = 19209
    page_ad = ad // 20
    start = 0
    page = 0
    for i in range(page_ad + 1):

        json_data = {
            'query': [
                '*',
            ],
            'filter': {
                'FETI': [
                    'buy_it_now_code:B1',
                ],
            },
            'sort': [
                'member_damage_group_priority asc',
                'auction_date_type desc',
                'auction_date_utc asc',
            ],
            'page': 0,
            'size': 20,
            'start': 0,
            'watchListOnly': False,
            'freeFormSearch': False,
            'hideImages': False,
            'defaultSort': False,
            'specificRowProvided': False,
            'displayName': '',
            'searchName': '',
            'backUrl': '',
            'includeTagByField': {},
            'rawParams': {},
        }

        response = requests.post('https://www.copart.com/public/lots/search-results', cookies=cookies, headers=headers,
                                 json=json_data)
        src = response.text


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
    with open("url.csv", newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        counter = 0
        for url in urls:
            proxy = random.choice(proxies)
            proxy_host = proxy[0]
            proxy_port = proxy[1]
            proxy_user = proxy[2]
            proxy_pass = proxy[3]

            proxi = {
                'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
                'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
            }
            counter += 1
            response = requests.get(url[0], cookies=cookies, headers=headers, proxies=proxi)
            data = response.json()
            filename = f"c:\\DATA\\copart\\product\\data_{counter}.json"
            with open(filename, 'w') as f:
                json.dump(data, f)


def parsin():
    with open('c:\\DATA\\copart\\product\\data.json', 'r') as f:
        # Загрузить JSON из файла
        data_json = json.load(f)
    'https: // www.copart.com / lot / 43079133 / salvage - 2018 - ford - focus - se - fl - miami - south'
    ln = data_json['data']['lotDetails']['ln']
    url_lot = f"https://www.copart.com/lot/{ln}"
    url_img = data_json['data']['lotDetails']['tims']
    name_lot = data_json['data']['lotDetails']['ld']
    price_bnp = data_json['data']['lotDetails']['bnp']
    odometer_lot = data_json['data']['lotDetails']['orr']
    drive_lot = data_json['data']['lotDetails']['drv']
    engine_type_lot = data_json['data']['lotDetails']['egn']
    vehicle_type_lot = data_json['data']['lotDetails']['vehTypDesc']
    highlights_lot = data_json['data']['lotDetails']['lcd']
    sale_location = data_json['data']['lotDetails']['yn']
    data = [url_lot, url_img, name_lot, price_bnp, odometer_lot, drive_lot, engine_type_lot, vehicle_type_lot,
            highlights_lot, sale_location]
    print(data)


if __name__ == '__main__':
    get_selenium()
    get()
    # get_id_ad_and_url()
    # get_product()
    # parsin()
