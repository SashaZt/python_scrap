import zipfile
import os
import time
import undetected_chromedriver

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv
from selenium.webdriver.chrome.service import Service

# def get_undetected_chromedriver():
#     PROXY = "37.233.3.100:9999"
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument(
#         '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
#
#     chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument('--proxy-server=%s' % PROXY)
#     # chrome_options.add_argument('--headless')
#     """Проба"""
#     #chrome_options.add_argument("--disable-dev-shm-usage")
#     #chrome_options.add_argument("--disable-setuid-sandbox")
#     #chrome_options.add_argument('--proxy-server=37.233.3.100:9999')
#
#
#     driver = undetected_chromedriver.Chrome()
#
#     return driver

"""Рабочий на один прокси"""

# def get_chromedriver():
#     PROXY = "37.233.3.100:9999"
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--proxy-server=%s' % PROXY)
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument(
#         '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
#
#     chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--start-maximized")
#     s = Service(
#         executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
#     )
#     driver = webdriver.Chrome(
#         service=s,
#         options=chrome_options
#     )
#
#     return driver


PROXY_HOST = '195.201.161.3'
PROXY_PORT = 20561
PROXY_USER = 'zBoGZh5PqsrQ'
PROXY_PASS = 'AIILgcGVH0'

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



def get_chromedriver():

    # Создаем объект chrome_options и добавляем настройки
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')

    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-gpu")
    plugin_file = 'proxy_auth_plugin.zip'
    if not os.path.exists('proxy_auth_plugin.zip'):
        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr('manifest.json', manifest_json)
            zp.writestr('background.js', background_js)
    chrome_options.add_extension(plugin_file)
    # Создаем объект webdriver.Chrome
    s = Service(
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )
    return driver

def main():
    url = "https://combomed.ru/antigrippin-dolak"
    driver = get_chromedriver()
    driver.maximize_window()
    driver.get(url)
    time.sleep(10)

if __name__ == '__main__':
    main()
