import json
import math
import re
import time
import zipfile
import pickle

import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.chrome.service import Service
# Нажатие клавиш
from selenium.webdriver.common.by import By

# Библиотеки для Асинхронного парсинга


# options = webdriver.ChromeOptions()
# # Отключение режима WebDriver
# options.add_experimental_option('useAutomationExtension', False)
# # # Работа в фоновом режиме
# # options.headless = True
# options.add_argument(
#     # "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
#     f"user-agent={useragent.random}"
# )
# driver_service = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
# driver = webdriver.Chrome(
#     service=driver_service,
#     options=options
# )
#
# # # Окно браузера на весь экран
# driver.maximize_window()

# Для работы webdriver____________________________________________________


# Для работы undetected_chromedriver ---------------------------------------

# import undetected_chromedriver as uc
# driver = uc.Chrome()


# Для работы undetected_chromedriver ---------------------------------------


# "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"


# Данные для прокси
PROXY_HOST = ''
PROXY_PORT = 31281
PROXY_USER = ' '
PROXY_PASS = ' '

# Настройка для requests чтобы использовать прокси
proxies = {'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}/'}

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
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"76.0.0"
}
"""

background_js = """
let config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
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
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()

    if use_proxy:
        plugin_file = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr('manifest.json', manifest_json)
            zp.writestr('background.js', background_js)

        chrome_options.add_extension(plugin_file)

    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')

    s = Service(
        executable_path="C:\\Users\\msi\\Desktop\\g2g\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    return driver


def get_url_category(url):
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'

    }
    driver = get_chromedriver(use_proxy=False,
                              user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
    driver.get(url)
    driver.maximize_window()
    counter_wait_url = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="text-secondary"]')))

    # time.sleep(5)
    # # # Блок работы с куками-----------------------------------------
    # # # Создание куки
    # time.sleep(30)
    # pickle.dump(driver.get_cookies(), open("cookies", "wb"))
    # # # Читание куки
    for cookie in pickle.load(open("cookies", "rb")):
        driver.add_cookie(cookie)
    driver.refresh()
    counter_wait_url = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="text-secondary"]')))
    # time.sleep(10)

    counets_url = driver.find_element(By.XPATH, '//div[@class="text-secondary"]').text.replace(",", "")
    count_url = int(re.search(r"(\d+)", counets_url).group(0))
    url_in_page = 48
    list_url = math.ceil(count_url / url_in_page)

    product_url = []
    for i in range(0, list_url + 1):
        if i == 1:
            driver.get(url)
            counter_wait_url = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="text-secondary"]')))
            card_product = driver.find_elements(By.XPATH,
                                                '//div[@class="row q-col-gutter-sm-md q-px-sm-md"]//div[@class="full-height full-width position-relative"]/a')
            for i in card_product:
                href = i.get_attribute('href')
                product_url.append(
                    {
                        'url_name': href
                    }
                )
            driver.execute_script("window.scrollBy(0,1800)", "")
            

        elif i > 1:
            driver.get(f'{url}&page={i}')
            counter_wait_url = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="text-secondary"]')))
            card_product = driver.find_elements(By.XPATH,
                                                '//div[@class="row q-col-gutter-sm-md q-px-sm-md"]//div[@class="full-height full-width position-relative"]/a')
            for i in card_product:
                href = i.get_attribute('href')
                product_url.append(
                    {
                        'url_name': href
                    }
                )
            driver.execute_script("window.scrollBy(0,1800)", "")
            
    with open("car_url.json", 'w') as file:
        json.dump(product_url, file, indent=4, ensure_ascii=False)
    print(len(product_url))

    driver.close()
    driver.quit()


def get_url_product(url):
    driver = get_chromedriver(use_proxy=False,
                              user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
    with open(f"car_url.json") as file:
        all_site = json.load(file)
    counter_url = len(all_site)
    products_all = []
    driver.get(url)
    for cookie in pickle.load(open("cookies", "rb")):
        driver.add_cookie(cookie)
    driver.refresh()
    for item in all_site:
        driver.get(item['url_name'])  # 'url_name' - это и есть ссылка
        # time.sleep(1)
        counter_wait_url = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="seller__title"]')))
        counter_wait_url = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="seller__title"]')))
        try:
            if driver.find_element(By.XPATH, '//div[@class="m-l-sm seller__info-items seller-details"]'):
                counter_wait_url = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="seller__title"]')))
                try:
                    name_server = driver.find_element(By.XPATH,
                                                      '//h1[@class="main__title-skin"]').text
                except:
                    name_server = ""

                try:
                    server_regions = driver.find_elements(By.XPATH,
                                                          '//div[@class="seller_details-region-main"]//div[@class="region_right-detail"]')
                except:
                    server_regions = ""
                try:
                    sr = driver.find_elements(By.XPATH,
                                              '//div[@class="seller_details-region-main"]//div[@class="region_left-detail"]')
                except:
                    sr = ''

                price_server = driver.find_element(By.XPATH,
                                                   '//div[@class="price_section-section"]//span[@class="amount__section-main"]').text.replace(
                    ".", ",")
                try:
                    server_region = server_regions[0].text
                except:
                    server_region = None
                try:
                    server_Platform = server_regions[1].text
                except:
                    server_Platform = None
                try:
                    server_ServiceType = server_regions[2].text
                except:
                    server_ServiceType = None

                # Создаем список
                products_all.append(
                    {
                        'price': price_server,
                        'name': name_server,
                        'region': server_region,
                        'Platform': server_Platform,
                        'ServiceType': server_ServiceType

                    }
                )
                #
                # В панду загоняем наш список и сохраняем в csv

        except:
            continue
    df = pd.DataFrame(products_all)
    # df_sort = df.sort_values(['server_region', 'server_Platform', 'server_ServiceType'])
    df.to_csv("data.csv",
              # encoding='utf-8',
              mode='w',
              header=True,
              index=False,
              sep=';'
              )
    print('Все сделал')
    driver.close()
    driver.quit()


def parse_content():
    print("Вставьте ссылку")
    url = input()
    get_url_category(url)
    get_url_product(url)


if __name__ == '__main__':
    parse_content()
