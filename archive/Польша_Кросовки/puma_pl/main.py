from selenium.webdriver.chrome.service import Service
import os
import shutil
import tempfile
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
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--disable-extensions') # Отключает использование расширений
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    # chrome_options.add_argument("--incognito")  # Открытие в режиме инкогнито
    chrome_options.add_argument("--disable-cache")  # Отключение кэширования
    chrome_options.add_argument("--disable-cookies")  # Отключение использования куков
    # proxy = ("195.201.161.3", 20561, "zBoGZh5PqsrQ", "AIILgcGVH0")
    # proxy_extension = ProxyExtension(*proxy)
    # chrome_options.add_argument(f"--load-extension={proxy_extension.directory}")
    s = Service(
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )
    return driver

def main():

    urls = [
        "https://eu.puma.com/pl/pl/mezczyzni/buty",
        "https://eu.puma.com/pl/pl/kobiety/buty",
        "https://eu.puma.com/pl/pl/dzieciece/produkty/buty"
    ]
    for url in urls[:1]:
        driver = get_chromedriver()
        group = url.split("/")[-2]

        driver.get(url)


if __name__ == '__main__':
    main()
