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
    driver.get(url=url)

    driver.maximize_window()
    time.sleep(5)
    # driver.execute_script("window.scrollBy(0,2000)", "")
    categoriy_product_urls = []

    try:
        button_more = driver.find_element(By.XPATH, '//li[@class="listItem_main__8ll0k GridItem_main__33wgr listItem_hasRank__s5vh8 listItem_hasProps__tpE0W listItem_bigGrid__mSpkv GridItem_bigGrid__gcJMW listItem_showInfoIcon__2ZCb5"]//div[@class="container_innerContainer__ulE_r"]//span[text()="more"]').click()
    except:
        button_more = print('Ops!')
    time.sleep(5)
    name_cart = driver.find_element(By.XPATH, '//div[@class="NodeName_nameWrapper__n32Nb"]').text
    namber_card = driver.find_element(By.XPATH, '//div[@class="GridThumbnail_main__EmUPU"]//strong').text
    img_cart = driver.find_element(By.XPATH, '//div[@class="GridThumbnail_main__EmUPU"]//div[@class="GridThumbnail_thumbnailWrapper__007iL"]//img').get_attribute("src")
    try:
        chas = driver.find_elements(By.XPATH, '//div[@class="GridItem_bottomContentWrapper__mgQqL"]//ul[@class="listItem_properties__sFwqE"]//li')
    except:
        chas = ' '
    chars_01 = chas[0].text
    chars_02 = chas[1].text

    try:
        desc_cart = driver.find_element(By.XPATH, '//div[@class="GridItem_bottomContentWrapper__mgQqL"]//div[contains(@class,"container_container")]//span').text.replace("\n", "").replace("\t", "")
    except:
        desc_cart = ' '
    with open(f"C:\\scrap_tutorial-master\\ranker.com\data.csv", "a", errors='ignore') as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\r")
        writer.writerow(
            (
                name_cart, namber_card, img_cart, chars_01, chars_02, desc_cart

            )
        )
    print()
    time.sleep(1)
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
    url = "https://www.ranker.com/list/favorite-male-singers-of-all-time/music-lover?ref=browse_rerank&l=1"
    # Запускаем первую функцию для сбора всех url на всех страницах
    save_link_all_product(url)
    # parsing_product()

