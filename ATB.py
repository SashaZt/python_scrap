import zipfile
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import csv
import time
import glob

# Нажатие клавиш

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium import webdriver

from fake_useragent import UserAgent

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

useragent = UserAgent()

# Данные для прокси
PROXY_HOST = 'IP'
PROXY_PORT = 'PORT' #Без кавычек
PROXY_USER = 'LOGIN'
PROXY_PASS = 'PASS'

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
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
    driver.get(url=url)

    driver.maximize_window()
    check_boot = driver.find_elements(By.XPATH, '//span[@class="b-checkbox-light__visible-checkbox"]')
    check_boot[0].click()
    time.sleep(1)
    button = driver.find_element(By.XPATH, '//div[@class="stores__buttons"]//button[@class="btn btn--green"]').click()
    time.sleep(5)
    # zoom_out = driver.find_element(By.XPATH, '//div[@class="leaflet-top leaflet-left"]//a[@class="leaflet-control-zoom-out"]').click()
    # driver.execute_script("window.scrollBy(0,300)", "")
    generals = driver.find_elements(By.XPATH, '//div[@class="leaflet-pane leaflet-marker-pane"]//img')
    for i in generals[0:]:
        time.sleep(5)
        i.click()
        time.sleep(5)
        desc_atb = i.find_element(By.XPATH, '//div[@class="leaflet-popup-content-wrapper"]').get_attribute('outerText').replace("\n", " ")
        print(desc_atb)

    driver.close()
    driver.quit()




if __name__ == '__main__':
    # # Собираем все ссылки на категории товаров
    url = "https://www.atbmarket.com/store-map"
    save_link_all_product(url)
    #Парсим все товары из файлов с
    # parsing_product()