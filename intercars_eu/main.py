import glob
import re
import os
import shutil
import tempfile
import zipfile
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
from selenium.webdriver.common.keys import Keys


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

    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--disable-extensions') # Отключает использование расширений
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    # proxy_extension = ProxyExtension(*proxy)
    # chrome_options.add_argument(f"--load-extension={proxy_extension.directory}")
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


def get_chromedriver_parsing():
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-extensions')  # Отключает использование расширений
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver


def get_category():
    cookies = {
        'BTID': '4C54089E-29F3-4B81-9FFE-47F1678DF42D',
        'JSESSIONID': 'Y22-747f3ca0-b336-4efe-acdc-f3540d172c43.app22',
    }
    url = 'https://ua.e-cat.intercars.eu/ru/'
    driver = get_chromedriver()
    driver.get(url)
    driver.maximize_window()
    # for cookie_name, cookie_value in cookies.items():
    #     cookie_dict = {'name': cookie_name, 'value': cookie_value}
    #     driver.add_cookie(cookie_dict)
    # time.sleep(1)
    # driver.refresh()
    # # for cookie_name, cookie_value in cookies.items():
    # #     cookie_dict = {'name': cookie_name, 'value': cookie_value}
    # #     driver.add_cookie(cookie_dict)
    # time.sleep(10)

    try:
        wait = WebDriverWait(driver, 60)
        wait_email = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="loginForm:username"]')))
        email = driver.find_element(By.XPATH, '//input[@id="loginForm:username"]')
        email.send_keys('logisticamotoprox@gmail.com')
        passwords = driver.find_element(By.XPATH, '//input[@id="loginForm:password"]')
        passwords.send_keys('GEkz54x!')
        passwords.send_keys(Keys.RETURN)
        time.sleep(10)
        driver.get('https://ua.e-cat.intercars.eu/ru/motorcycles')
        time.sleep(10)
        urls = driver.find_elements(By.XPATH,
                                    '//div[@class="yCmsContentSlot"]//div[@class="yCmsComponent categorytiles__item"]//a')
        with open('url_category.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for u in urls:
                category = u.get_attribute("href")
                writer.writerow([category])

        # file_name = f"motorcycles.html"
        # with open(file_name, "w", encoding='utf-8') as fl:
        #     fl.write(driver.page_source)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def get_product():
    urls = [
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9F%D1%80%D0%B8%D0%B2%D0%BE%D0%B4/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D0%B5%D1%82%D0%BD%D0%B8%D0%B9-%D0%BF%D1%80%D0%B8%D0%B2%D1%96%D0%B4/%D0%A6%D0%B5%D0%BF%D1%8C-%D0%A0%D0%B5%D0%BC%D0%B5%D0%BD%D1%8C/c/tecdoc-6500000-5010888-6515040?q=%3Adefault%3AbranchAvailability%3AALL%3Amarket%3AMOT",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%90%D0%BA%D0%BA%D1%83%D0%BC%D1%83%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D1%8B-%D0%B8-%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA-%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8F/c/tecdoc-5090003?q=%3Adefault%3Aicgoods_35545%3Aall_markets%3AbranchAvailability%3AALL%3Amarket%3AMOT",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%A2%D0%BE%D1%80%D0%BC%D0%BE%D0%B7%D0%BD%D0%B0%D1%8F-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0/%D0%94%D0%B8%D1%81%D0%BA%D0%BE%D0%B2%D1%8B%D0%B9-%D1%82%D0%BE%D1%80%D0%BC%D0%BE%D0%B7/%D0%A2%D0%BE%D1%80%D0%BC%D0%BE%D0%B7%D0%BD%D0%B0%D1%8F-%D0%BA%D0%BE%D0%BB%D0%BE%D0%B4%D0%BA%D0%B0-%D0%B4%D0%B8%D1%81%D0%BA%D0%BE%D0%B2%D0%BE%D0%B3%D0%BE-%D1%82%D0%BE%D1%80%D0%BC%D0%BE%D0%B7%D0%B0/c/tecdoc-6600000-6611000-6611010?q=:default:market:MOT",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%B0%D1%81%D0%BB%D0%B0-%D0%A1%D0%BC%D0%B0%D0%B7%D0%BA%D0%B8-%D0%9C%D0%BE%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F-%D1%85%D0%B8%D0%BC%D0%B8%D1%8F/c/tecdoc-5090009?q=%3adefault:icgoods_38683:icgoods_366384:icgoods_25999:icgoods_289274",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%90%D0%BC%D0%BE%D1%80%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F-%D0%B0%D0%B2%D1%82%D0%BE%D1%82%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%BD%D0%BE%D0%B3%D0%BE-%D1%81%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B2a/%D0%90%D0%BC%D0%BE%D1%80%D1%82%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80%D1%8B/%D0%90%D0%BC%D0%BE%D1%80%D1%82%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F-%D0%B6%D0%B8%D0%B4%D0%BA%D0%BE%D1%81%D1%82%D1%8C/c/tecdoc-6400000-6411000-genart_9563?q=:default",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%B0%D1%81%D0%BB%D0%B0-%D0%A1%D0%BC%D0%B0%D0%B7%D0%BA%D0%B8-%D0%9C%D0%BE%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F-%D1%85%D0%B8%D0%BC%D0%B8%D1%8F/c/tecdoc-5090009?q=%3adefault:icgoods_38683:icgoods_366384:icgoods_25999:icgoods_289280",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%B0%D1%81%D0%BB%D0%B0-%D0%A1%D0%BC%D0%B0%D0%B7%D0%BA%D0%B8-%D0%9C%D0%BE%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F-%D1%85%D0%B8%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BC%D0%B0%D0%B7%D0%BA%D0%B8/%D0%A1%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D1%81%D0%BC%D0%B0%D0%B7%D0%BA%D0%B0/%D0%96%D0%B8%D0%B4%D0%BA%D0%BE%D1%81%D1%82%D1%8C-%D0%B4%D0%BB%D1%8F-%D1%86%D0%B5%D0%BF%D0%B8/c/tecdoc-5090009-5010183-5010190-genart_3201?q=:default",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9E%D1%85%D0%BB%D0%B0%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5/%D0%90%D0%BD%D1%82%D0%B8%D1%84%D1%80%D0%B8%D0%B7/c/tecdoc-6900000-6923000?q=:default:branchAvailability:ALL:market:MOT",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%B0%D1%81%D0%BB%D0%B0-%D0%A1%D0%BC%D0%B0%D0%B7%D0%BA%D0%B8-%D0%9C%D0%BE%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F-%D1%85%D0%B8%D0%BC%D0%B8%D1%8F/%D0%A2%D0%BE%D1%80%D0%BC%D0%BE%D0%B7%D0%BD%D1%8B%D0%B5-%D0%B6%D0%B8%D0%B4%D0%BA%D0%BE%D1%81%D1%82%D0%B8/c/tecdoc-5090009-5010195?q=%3Adefault%3AbranchAvailability%3AALL",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9E%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0-%D0%B8-%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9A%D0%BE%D0%BC%D0%B1%D0%B8%D0%BD%D0%B5%D0%B7%D0%BE%D0%BD%D1%8B/c/tecdoc-5090012-5010763-5010753",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9E%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0-%D0%B8-%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%92%D0%BD%D0%B5%D0%B4%D0%BE%D1%80%D0%BE%D0%B6%D0%BD%D1%8B%D0%B9/%D0%A4%D1%83%D1%82%D0%B1%D0%BE%D0%BB%D0%BA%D0%B0-%D0%B4%D0%BB%D1%8F-%D0%B1%D0%B5%D0%B7%D0%B4%D0%BE%D1%80%D0%BE%D0%B6%D1%8C%D1%8F/c/tecdoc-5090012-5010763-5010771-genart_92452",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9E%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0-%D0%B8-%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9A%D1%83%D1%80%D1%82%D0%BA%D0%B8/c/tecdoc-5090012-5010763-5010750",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9E%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0-%D0%B8-%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D0%B5%D1%82%D0%BD%D1%8B%D0%B5-%D0%B1%D0%BE%D1%82%D0%B8%D0%BD%D0%BA%D0%B8/c/tecdoc-5090012-5010763-5010754",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9E%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0-%D0%B8-%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%97%D0%B0%D1%89%D0%B8%D1%82%D0%BD%D0%B8%D0%BA%D0%B8/c/tecdoc-5090012-5010763-5010759",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9E%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0-%D0%B8-%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D0%B5%D1%82%D0%BD%D1%8B%D0%B5-%D0%BF%D0%B5%D1%80%D1%87%D0%B0%D1%82%D0%BA%D0%B8/c/tecdoc-5090012-5010763-5010755",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9E%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0-%D0%B8-%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D0%B5%D1%82%D0%BD%D1%8B%D0%B5-%D1%88%D1%82%D0%B0%D0%BD%D1%8B/c/tecdoc-5090012-5010763-5010752",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%A8%D0%BB%D0%B5%D0%BC%D1%8B/c/tecdoc-5090012-5010749",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%A8%D0%BB%D0%B5%D0%BC%D1%8B/%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B-%D0%B4%D0%BB%D1%8F-%D1%88%D0%BB%D0%B5%D0%BC%D0%B0/c/tecdoc-5090012-5010749-genart_92440",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%9C%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B-%D0%B4%D0%BB%D1%8F-%D0%BC%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%B2/%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B-%D0%B4%D0%BB%D1%8F-%D0%BC%D0%BE%D1%82%D0%BE%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%B2/%D0%9F%D1%83%D1%82%D0%B5%D1%88%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D0%B5-%D0%B8-%D0%B1%D0%B0%D0%B3%D0%B0%D0%B6/c/tecdoc-5090012-5010858-5010515-genart_92446",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%A8%D0%B8%D0%BD%D1%8B-%D0%9A%D0%BE%D0%BB%D1%91%D1%81%D0%B0-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/c/tecdoc-5090008?q=:default:icgoods_63966:icgoods_1028752:branchAvailability:ALL:icgoods_64319:icgoods_1028756",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%A8%D0%B8%D0%BD%D1%8B-%D0%9A%D0%BE%D0%BB%D1%91%D1%81%D0%B0-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/c/tecdoc-5090008?q=:default:icgoods_63966:icgoods_1028752:branchAvailability:ALL:icgoods_64319:icgoods_1056313",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%A8%D0%B8%D0%BD%D1%8B-%D0%9A%D0%BE%D0%BB%D1%91%D1%81%D0%B0-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/c/tecdoc-5090008?q=:default:icgoods_63966:icgoods_1028752:branchAvailability:ALL:icgoods_64319:icgoods_1056314",
        "https://ua.e-cat.intercars.eu/ru/%D0%92%D1%81%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8/%D0%A8%D0%B8%D0%BD%D1%8B-%D0%9A%D0%BE%D0%BB%D1%91%D1%81%D0%B0-%D0%90%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B/c/tecdoc-5090008?q=:default:icgoods_63966:icgoods_1028752:branchAvailability:ALL:icgoods_64319:icgoods_1056315"
    ]
    cookies = {
        'BTID': '4C54089E-29F3-4B81-9FFE-47F1678DF42D',
        'JSESSIONID': 'Y22-747f3ca0-b336-4efe-acdc-f3540d172c43.app22',
    }
    url = 'https://ua.e-cat.intercars.eu/ru/'
    driver = get_chromedriver()
    driver.get(url)
    driver.maximize_window()
    try:
        wait = WebDriverWait(driver, 60)
        wait_email = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="loginForm:username"]')))
        email = driver.find_element(By.XPATH, '//input[@id="loginForm:username"]')
        email.send_keys('logisticamotoprox@gmail.com')
        passwords = driver.find_element(By.XPATH, '//input[@id="loginForm:password"]')
        passwords.send_keys('GEkz54x!')
        passwords.send_keys(Keys.RETURN)
        time.sleep(5)

        for i in urls[1:]:
            coun = 0
            next_page = i
            while next_page:
                coun += 1
                driver.get(next_page)
                time.sleep(1)

                category = driver.find_element(By.XPATH, '//a[@data-test="parentCategoryName"]').get_attribute(
                    "title").replace("/", "_")
                file_name = f"c:\\DATA\\intercars_eu\\{category}_{coun}.html"
                if os.path.isfile(file_name):
                    continue  # Если файл уже существует, переходим к следующей итерации цикла
                with open(file_name, "w", encoding='utf-8') as fl:
                    fl.write(driver.page_source)
                # table_product = driver.find_element(By.XPATH, '//table[@class="listingcollapsed__wrapper"]')
                # products = table_product.find_elements(By.XPATH, "//tbody[contains(@class, 'listingcollapsed__item')]")
                #
                # with open(f"{category}.csv", 'a', newline='',
                #           encoding='utf-8') as csvfile:  # Используем 'a' чтобы добавлять в файл, а не перезаписывать
                #     writer = csv.writer(csvfile, delimiter=";")
                #     for product in products:
                #         name_product = product.find_element(By.XPATH,
                #                                             ".//a[@data-test='activenumber,search-result-row-title']").get_attribute(
                #             "data-id")
                #         date_product = product.find_element(By.XPATH, './/div[@class="productdelivery__date"]').text
                #         price_product = product.find_element(By.XPATH,
                #                                              './/div[@class, "quantity quantity--pricesmall"]//div[@class="quantity__amount"]').text
                #         datas = [name_product, date_product, price_product]
                #         writer.writerow(datas)

                try:
                    next_page = driver.find_element(By.XPATH,
                                                    '//li[@class="pagination__item pagination__item--smallmargin"][2]//a').get_attribute(
                        "href")  # Получаем ссылку на следующую страницу
                except:
                    next_page = None  # Если следующей страницы нет, завершаем цикл while
        # for i in urls[:1]:
        #     driver.get(i)
        #     time.sleep(1)
        #
        #     category = driver.find_element(By.XPATH, '//a[@data-test="parentCategoryName"]').get_attribute(
        #         "title").replace("/",
        #                          "_")
        #     table_product = driver.find_element(By.XPATH, '//table[@class="listingcollapsed__wrapper"]')
        #     products = table_product.find_elements(By.XPATH, "//tbody[contains(@class, 'listingcollapsed__item')]")
        #     with open(f"{category}.csv", 'w', newline='', encoding='utf-8') as csvfile:
        #         writer = csv.writer(csvfile, delimiter=";")
        #         for i in products:
        #             name_product = i.find_element(By.XPATH,
        #                                           ".//a[@data-test='activenumber,search-result-row-title']").get_attribute(
        #                 "data-id")
        #             date_product = i.find_element(By.XPATH, './/div[@class="productdelivery__date"]').text
        #             price_product = i.find_element(By.XPATH,
        #                                            './/div[@class="quantity quantity--pricesmall productpricetoggle__gross  productpricetoggle__wholesale  js-product-wholesale-toggle"]//div[@class="quantity__amount"]').text
        #             datas = [name_product, date_product, price_product]
        #             writer.writerow(datas)
        #
        #         try:
        #             pagin_next = driver.find_element(By.XPATH,
        #                                              '//li[@class="pagination__item pagination__item--smallmargin"][2]//a').get_attribute(
        #                 "href")
        #             driver.get(pagin_next)
        #         except:
        #             continue
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def parsing():
    driver = get_chromedriver_parsing()
    folders_html = fr"c:\DATA\intercars_eu\*.html"
    files_html = glob.glob(folders_html)
    coun = 0
    with open(f"data.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for i in files_html:
            driver.get(i)
            coun += 1
            category = driver.find_element(By.XPATH, '//a[@data-test="parentCategoryName"]').get_attribute(
                "title").replace("/",
                                 "_")
            table_product = driver.find_element(By.XPATH, '//table[@class="listingcollapsed__wrapper"]')
            products = table_product.find_elements(By.XPATH, "//tbody[contains(@class, 'listingcollapsed__item')]")
            for i in products:
                name_product = i.find_element(By.XPATH,
                                              ".//a[@data-test='activenumber,search-result-row-title']").get_attribute(
                    "data-id")
                try:
                    date_product = i.find_element(By.XPATH, './/div[@class="productdelivery__date"]').text
                except:
                    date_product = None
                try:
                    price_product = i.find_element(By.XPATH,
                                                   './/div[@class="quantity quantity--pricesmall productpricetoggle__gross  productpricetoggle__wholesale  js-product-wholesale-toggle"]//div[@class="quantity__amount"]').text
                except:
                    price_product = None
                datas = [name_product, date_product, price_product]
                writer.writerow(datas)
            print(f"Осталось {len(files_html) - coun}")


if __name__ == '__main__':
    # get_category()
    # get_product()
    parsing()
