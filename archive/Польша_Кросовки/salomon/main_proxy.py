import os
import shutil
import tempfile

import time
import random
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv
wait_time = random.uniform(5, 10)
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
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    proxy_extension = ProxyExtension(*proxy)
    chrome_options.add_argument(f"--load-extension={proxy_extension.directory}")
    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    """Рабочая настройка для обхода Cloudflare """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })
    return driver
def check_file_exists(file_path):
    return os.path.isfile(file_path)

# Функция для получения прокси-серверов
def get_proxies():
    from proxies import proxies
    return proxies

# Функция для загрузки HTML-страницы
def load_html(url, proxy, category, counter):
    driver = get_chromedriver(proxy)  # Получаем настроенный драйвер Chrome
    driver.get(url)  # Загрузка страницы
    time.sleep(wait_time)
    wait = WebDriverWait(driver, 3)
    try:
        button_clouse_wait = wait.until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="popin_close popin-pushs-close"]')))
        button_clouse = driver.find_elements(By.XPATH, '//button[@class="popin_close popin-pushs-close"]')[
            0].click()
    except:
        return
    try:
        button_cookies_wait = wait.until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="cookie-accept-all"]')))
        button_cookies = driver.find_element(By.XPATH, '//button[@class="cookie-accept-all"]').click()
    except:
        return
    driver.execute_script("window.scrollBy(0,3000)", "")
    time.sleep(wait_time)
    filename = f"c:\\salomon_pl\\html_product\\{category}\\0_{counter}.html"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    driver.close()
    driver.quit()


# Основная функция для обработки категорий и загрузки страниц
def process_categories(categories, max_workers=2):
    for category in categories:
        urls_file_path = f"c:\\salomon_pl\\csv_url\\{category}\\url.csv"
        html_dir_path = f"c:\\salomon_pl\\html_product\\{category}"
        counter = 0

        with open(urls_file_path, 'r') as urls_file:
            urls = urls_file.read().splitlines()

        proxies = get_proxies()
        proxy_urls = list(zip(urls, random.choices(proxies, k=len(urls))))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for url, proxy in proxy_urls:
                counter += 1
                file_path = os.path.join(html_dir_path, f"0_{counter}.html")
                if check_file_exists(file_path):
                    continue

                executor.submit(load_html, url, proxy, category, counter)

# Пример использования
categories = ['kids', 'men', 'women']
max_workers = 1

process_categories(categories, max_workers)