import pickle
import zipfile
import os
import json
import csv
import time
import requests
# Нажатие клавиш
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium import webdriver
import random
from fake_useragent import UserAgent

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

useragent = UserAgent()

# Данные для прокси
PROXY_HOST = '141.145.205.4'
PROXY_PORT = 31281
PROXY_USER = 'proxy_alex'
PROXY_PASS = 'DbrnjhbZ88'

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
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    return driver

def save_link_all_product(url):
    driver = get_chromedriver(use_proxy=False,
                              user_agent=f"{useragent.random}")
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    for cookie in pickle.load(open("cookies", "rb")):
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(5)

    clouse_windows = driver.find_element(By.XPATH, '//button[@class="selected-product__container__product__close"]//span[@class="selected-product__container__product__close__title"]')
    if clouse_windows:
        clouse_windows.click()
    time.sleep(1)
    # Листать по страницам ---------------------------------------------------------------------------
    page_product = 0
    isNextDisable = False
    while not isNextDisable:
        try:
            # ----------------------------------------------------------
            # Если необходимо сначала прогрузить все товары тогда открываем все и только потом получаем ссылки
            # Сначала что то ищем на первой странице, а только потом ищем на остальных
            # card_product_url = driver.find_elements(By.XPATH, '//div[@class="catalog-section-item-name"]/a')
            # for item in card_product_url[0:13]:
            #     product_url.append(
            #         {'url_name': item.get_attribute("href")}
            #         # Добавляем в словарь два параметра для дальнейшего записи в json
            #     )
            #     print(item.get_attribute("href"))
            # Если необходимо подождать елемент тогда WebDriverWait
            # next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//i[@class="fa fa-chevron-right"]')))
            driver.implicitly_wait(5)
            next_button = driver.find_element(By.XPATH, '//div[@class="w-100 p-0 m-0 d-flex product-list-navigation__show-btn_container ng-star-inserted"]//button')
            # Проверка на наличие кнопки следующая страница, если есть, тогда листаем!
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            if next_button:
                next_button.click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # if clouse_windows:
                #     clouse_windows.click()
            else:
                isNextDisable = True
        except:
            isNextDisable = True
    print('Pause')
    time.sleep(60)
    # Листать по страницам ---------------------------------------------------------------------------








        # Блок работы с куками-----------------------------------------
        # Создание куки
        # pickle.dump(driver.get_cookies(), open("cookies", "wb"))
        # Читание куки

    driver.close()
    driver.quit()


# def parsing_product():
#     driver = get_chromedriver(use_proxy=True,
#                               user_agent=f"{useragent.random}")
#     with open(f"C:\\scrap_tutorial-master\\11800\\Alfa-Romeo.json") as file:
#         all_site = json.load(file)
#     with open(f"C:\\scrap_tutorial-master\\11800\\Alfa-Romeo.csv", "w", errors='ignore') as file:
#         writer = csv.writer(file, delimiter=";", lineterminator="\r")
#         writer.writerow(
#             (
#                 'name_company',
#                 'adr_company',
#                 'tel_company',
#                 'tel_company_02',
#                 'email_company',
#                 'www_company',
#                 'link_company',
#                 'social_company'
#
#             )
#         )
#     # С json вытягиваем только 'url_name' - это и есть ссылка
#     product_sum = 0
#     for item in all_site:
#         driver.get(item['url_name'])  # 'url_name' - это и есть ссылка
#         try:
#             tel_company = driver.find_element(By.XPATH, '//*[@id="entry"]/div[4]/div[1]/div/div[1]/a/div[2]').text
#             # .replace('"', '').replace('/ №', '').replace('*', '_')  # удаляем из названия следующие символы
#         except:
#             tel_company = 'No phone'
#         try:
#             tel_company_02 = driver.find_element(By.XPATH, '//*[@id="kontakt"]').text.replace("\n", ", ")
#             # .replace('"', '').replace('/ №', '').replace('*', '_')  # удаляем из названия следующие символы
#         except:
#             tel_company_02 = 'No phone additionally'
#         try:
#             name_company = driver.find_element(By.XPATH, '//*[@id="entry"]/div[1]/div[1]/h1').text
#         except:
#             name_company = driver.find_element(By.XPATH, '//*[@id="entry"]/div[2]/div[1]/h1').text
#         try:
#             email_company = driver.find_element(By.XPATH, '//*[@id="box-email-link"]/div[2]').text
#             # .replace("\n", "")  # Убираем перенос с описания
#         except:
#             email_company = "No email"
#         try:
#             www_company = driver.find_element(By.XPATH, '//*[@id="entry"]/div[4]/div[2]/div/div[2]/a/div[2]').text
#
#         except:
#             www_company = driver.find_element(By.XPATH, '//*[@id="entry"]/div[5]/div[2]/div/div[2]/a/div[2]').text
#
#         try:
#             adr_company = driver.find_element(By.XPATH, '//*[@id="entry"]/div[4]/div[1]/div/div[3]/div/div[2]/span').text.replace("\n", "")
#         except:
#            adr_company = driver.find_element(By.XPATH, '//*[@id="entry"]/div[5]/div[1]/div/div[3]/div/div[2]/span').text.replace("\n", "")
#
#         try:
#             social_company = driver.find_element(By.XPATH,
#                                                  '//*[@id="entry"]/div[5]/div[2]/div/div[3]/a').get_attribute("href")
#         except:
#             social_company = 'No social'
#
#
#         with open(f"C:\\scrap_tutorial-master\\11800\\Alfa-Romeo.csv", "a", errors='ignore') as file:
#             writer = csv.writer(file, delimiter=";", lineterminator="\r")
#             writer.writerow(
#                 (
#                     name_company,
#                     adr_company,
#                     tel_company,
#                     tel_company_02,
#                     email_company,
#                     www_company,
#                     item['url_name'],
#                     social_company
#
#                 )
#             )
#
#     driver.close()
#     driver.quit()






if __name__ == '__main__':
    ##Сайт на который переходим
    url = "https://b2b.bm.parts/catalog?warehouses=ACF9000C2947F7AE11E28A2B02C4AD32&warehouses=waiting&warehouses=other&warehouses=81F4005056AC66D611EAD7173350C7AA&warehouses=81EE005056AC66D611EA758E79EBACF9&search_mode=strict&per_page=60&page=1&brands=MERCEDES&brands=FORD"
    # Запускаем первую функцию для сбора всех url на всех страницах
    save_link_all_product(url)
    # parsing_product()

