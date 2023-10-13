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

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor

PROXY_HOST = '37.233.3.100'
PROXY_PORT = 9999
PROXY_USER = 'proxy_alex'
PROXY_PASS = 'DbrnjhbZ88'
# proxies = {
#     'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
#     'https': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'
# }
proxies = {"http": f"http://{PROXY_HOST}:{PROXY_PORT}", f"https": f"http://{PROXY_HOST}:{PROXY_PORT}"}
cookies = {
    'session-id': '142-4156051-2826849',
    'ubid-main': '135-0200416-6965265',
    'at-main': 'Atza|IwEBIHLENpvSo6IYU2heB7riylOu6be5vQagD_ucLEFt2UfXHgiQHVZ7xRfVcAYadFi8ib8mt-fhd1yegmao8hSuX5vcEWP8gg3vLHxTzmg5uzXvxGSyEUmjGKPMaxpfVxS7lmPJiL-CS44B4NsqT3lDkNv6PSHdresvfJ2HRvm-T13KHKaJx7EG7_tIDqQQSQF_zUIUzVgqprv7DJYz47K6FNZ-YNdpZMXNnl5PJXOmHXuXBSQDNOCBi8-KIab0HR2n0mEpcJcICzFoEJouFusIupwKR7CXC3KtMWfF78u8schavw',
    'sess-at-main': '"IdhMzuGhPU5e0XmtHASAFlgyp5zJI6ZHWIaM0QVTITM="',
    'sst-main': 'Sst1|PQGEmNiYL84BFT_awTvcUbA4CQR9fQwYZi3ZP9Zj2zJ9OuZEEcAWcba5pfE9rwjuJf8cPTsosQ1pJDbvcLNoNOc8e6FNYtKBjuzLH0rlVIxNYnTsBR40DzEDWTPe8aCEmgEBOKkg-q4dys-q8YuJVZMSSd8p1xMFDqpKz9GDYngmqPY4ahBksaFRFYToIt1Opvj6OgEoJVG8m_WzcCxiIezIFTm5TOYtpYdnvCuStLOWwhmDI-aiUU6JKLIDsyQTMnuLUL91ciNgFFve9HyJL_nuD9iip3LdNdvOa6ZcOcUnE-w',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'skin': 'noskin',
    'sp-cdn': '"L5Z9:UA"',
    'lc-main': 'en_US',
    'session-token': '"055TzHoT+uUJhMJxd/kR7PGDhkhW6CEFgHhJCQBFx5VubASmBtMoeKEE/HaJ/PaERrxeVX4fxw6sfyex1Z1kBPPY2PXJZAxdeVst+sQUU0tgk6wOb9+y72D0jR2xzO0NfBkqVjbcLnMwdJ+XhMhD8oG74qNhBQkH8H6jGk3xLquT+1+js/E6jCK166CFyrK+A6dBCSd0q2FA8XpByaXWOu6eLPGrZ4UEEbJrnNxOzy8="',
    'csm-hit': 'adb:adblk_no&t:1687247536508&tb:QCF6R5T7WFZ4R58FKXWX+sa-TZ7PKAZ4SSGZNHQ5QJ5X-7HB88RE8AF4W86G1Q5Y8|1687247536508',
}

headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'session-id=142-4156051-2826849; ubid-main=135-0200416-6965265; at-main=Atza|IwEBIHLENpvSo6IYU2heB7riylOu6be5vQagD_ucLEFt2UfXHgiQHVZ7xRfVcAYadFi8ib8mt-fhd1yegmao8hSuX5vcEWP8gg3vLHxTzmg5uzXvxGSyEUmjGKPMaxpfVxS7lmPJiL-CS44B4NsqT3lDkNv6PSHdresvfJ2HRvm-T13KHKaJx7EG7_tIDqQQSQF_zUIUzVgqprv7DJYz47K6FNZ-YNdpZMXNnl5PJXOmHXuXBSQDNOCBi8-KIab0HR2n0mEpcJcICzFoEJouFusIupwKR7CXC3KtMWfF78u8schavw; sess-at-main="IdhMzuGhPU5e0XmtHASAFlgyp5zJI6ZHWIaM0QVTITM="; sst-main=Sst1|PQGEmNiYL84BFT_awTvcUbA4CQR9fQwYZi3ZP9Zj2zJ9OuZEEcAWcba5pfE9rwjuJf8cPTsosQ1pJDbvcLNoNOc8e6FNYtKBjuzLH0rlVIxNYnTsBR40DzEDWTPe8aCEmgEBOKkg-q4dys-q8YuJVZMSSd8p1xMFDqpKz9GDYngmqPY4ahBksaFRFYToIt1Opvj6OgEoJVG8m_WzcCxiIezIFTm5TOYtpYdnvCuStLOWwhmDI-aiUU6JKLIDsyQTMnuLUL91ciNgFFve9HyJL_nuD9iip3LdNdvOa6ZcOcUnE-w; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; sp-cdn="L5Z9:UA"; lc-main=en_US; session-token="055TzHoT+uUJhMJxd/kR7PGDhkhW6CEFgHhJCQBFx5VubASmBtMoeKEE/HaJ/PaERrxeVX4fxw6sfyex1Z1kBPPY2PXJZAxdeVst+sQUU0tgk6wOb9+y72D0jR2xzO0NfBkqVjbcLnMwdJ+XhMhD8oG74qNhBQkH8H6jGk3xLquT+1+js/E6jCK166CFyrK+A6dBCSd0q2FA8XpByaXWOu6eLPGrZ4UEEbJrnNxOzy8="; csm-hit=adb:adblk_no&t:1687247536508&tb:QCF6R5T7WFZ4R58FKXWX+sa-TZ7PKAZ4SSGZNHQ5QJ5X-7HB88RE8AF4W86G1Q5Y8|1687247536508',
    'device-memory': '8',
    'dnt': '1',
    'downlink': '10',
    'dpr': '1',
    'ect': '4g',
    'referer': 'https://www.amazon.com/s?i=stripbooks&rh=n%3A283155&dc&fs=true&ds=v1%3AFW8FzwCBmo65EzoRsz1El3Z1rFWVVXAAYR6kFuYqSyk&qid=1687247019&ref=sr_ex_n_1',
    'rtt': '50',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '1100',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'viewport-width': '1100',
}

params = {
    'i': 'stripbooks',
    'rh': 'n%3A283155%2Cn%3A1',
    'dc': '',
    'fs': 'true',
    'page': 2,
    'qid': '1687247117',
    'rnid': '283155',
    'ref': 'sr_pg_2',
}


# url = 'https://www.g2g.com/categories/diablo-4-boosting-service?seller=AMELIBOOST'


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

    # cookies = {
    #     'sessionid': 'mrqjw8vnilh44diz8aryq5jrodokxq2f',
    #     'cf_clearance': 'V4_Zy99exclmqrs8.cC4ve77WHggd.XueZk2zXkN5Wc-1697135038-0-1-d29a0353.7d7311cd.859b5cb3-0.2.1697135038',
    #     'csrftoken': 'WSZtemNOAzSQPwzxwR5wyfn7flUj4wj3RSTiNoo3A4hohELJtB9WKEZW62v78dRY',
    #     'crisp-client%2Fsession%2F980759c4-00d9-4b4b-85e6-c48036807fc0': 'session_1b713c7a-4fba-4d1f-a801-b184ce903e57',
    #     'catalog_page_size': '50',
    #     'crisp-client%2Fsocket%2F980759c4-00d9-4b4b-85e6-c48036807fc0': '0',
    # }

    headers = {
        'authority': 'exist.ua',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'cache-control': 'no-cache',
        # 'cookie': 'sessionid=mrqjw8vnilh44diz8aryq5jrodokxq2f; cf_clearance=V4_Zy99exclmqrs8.cC4ve77WHggd.XueZk2zXkN5Wc-1697135038-0-1-d29a0353.7d7311cd.859b5cb3-0.2.1697135038; csrftoken=WSZtemNOAzSQPwzxwR5wyfn7flUj4wj3RSTiNoo3A4hohELJtB9WKEZW62v78dRY; crisp-client%2Fsession%2F980759c4-00d9-4b4b-85e6-c48036807fc0=session_1b713c7a-4fba-4d1f-a801-b184ce903e57; catalog_page_size=50; crisp-client%2Fsocket%2F980759c4-00d9-4b4b-85e6-c48036807fc0=0',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'https://exist.ua/uk/kyb-kayaba-brand/amortyzator-pidvisky-perednoji-gazomasljanyj-kyb-excel-g-335808-14866668/',
        # cookies=cookies,
        headers=headers,
    )


    # json_data = response.json()
    # with open(f'test.json', 'w', encoding='utf-8') as f:
    #     json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
    src = response.text
    filename = f"amazon.html"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(src)


def parsing():
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        file_path = r"C:\scrap_tutorial-master\Temp\shcool.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        # Теперь переменная 'data' содержит данные из файла в формате JSON
        list_sclool = data['search']['data']['schools-kyivska-kyiv']
        for i in list_sclool:
            try:
                phone = i['phone']
            except:
                phone = None
            try:
                ua = i['ua']
            except:
                ua = None
            try:
                shortTitle = ua['shortTitle']
            except:
                shortTitle = None
            try:
                title = ua['title']
            except:
                title = None
            try:
                address = ua['address']
            except:
                address = None
            try:
                search = ua['search']
            except:
                search = None
            values = [phone, shortTitle, title, address, search]
            # print(values)
            writer.writerow(values)  # Дописываем значения из values



    # soup = BeautifulSoup(src, 'lxml')
    # script_tag = soup.find_all('script')  # находим все теги script
    #
    # json_data = None
    # pattern = re.compile(r'window\["__PRELOADED_STATE__"\]=(.*?);')
    #
    # # Поиск JSON данных
    # for tag in script_tag[2]:
    #     # print(tag)
    #     match = pattern.search(tag.string or "")
    #     if match:
    #         json_data = match.group()
    #         break
    # # Сохранение данных в файл
    # if json_data:
    #     # Используйте регулярное выражение, чтобы отрезать лишние символы в начале и в конце строки
    #     json_data = re.sub(r'^window\["__PRELOADED_STATE__"\]=|;$', '', json_data)
    #
    #     with open("output.json", "w", encoding="utf-8") as f:
    #         try:
    #             # Попробуйте десериализовать JSON данные
    #             data = json.loads(json_data)
    #
    #             # Сериализуйте данные обратно в JSON с экранированными кавычками
    #             json_str = json.dumps(data, ensure_ascii=False, indent=4)
    #
    #             # Замените неэкранированные кавычки на экранированные
    #             json_str = json_str.replace('"', r'\"')
    #
    #             # Запишите данные в файл
    #             f.write(json_str)
    #         except json.JSONDecodeError as e:
    #             # print(json_data[186750:186800])
    #             print(f"Failed to decode JSON data due to: {e.msg}")
    #             print(f"Error occurs at line {e.lineno}, column {e.colno}")
    # else:
    #     print("JSON data not found.")



def get_cloudscraper():
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False

    })
    tokens, user_agent = cloudscraper.get_tokens('https://www.vaurioajoneuvo.fi')
    print(tokens)
    # r = scraper.get(
    #     'https://sellercentral.amazon.com/skucentral?mSku=AV-QNMH-TN28&ref=myi_skuc', params=params, cookies=cookies, headers=headers
    # )  # , proxies=proxies
    # html = r.content
    # filename = f"amazon.html"
    # with open(filename, "w", encoding='utf-8') as f:
    #     f.write(html.decode('utf-8'))


def get_chromedriver():
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
    driver = get_chromedriver()
    driver.get('https://schoolhub.com.ua/ua/catalog/schools/kyivska/kyiv/53')

    time.sleep(10)
    filename = f"amazon.html"
    with open(filename, "w", encoding='utf-8') as fl:
        fl.write(driver.page_source)



if __name__ == '__main__':
    get_requests()
    # get_cloudscraper()
    # get_selenium()
    # parsing()
