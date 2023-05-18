import os
import zipfile
import time
import undetected_chromedriver
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv
proxies = [{'ip': '193.124.190.63', 'port': '9317', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '194.67.201.189', 'port': '9874', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '194.67.202.219', 'port': '9973', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '194.67.200.169', 'port': '9485', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '194.67.202.109', 'port': '9013', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '194.67.201.44', 'port': '9798', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '194.67.201.206', 'port': '9707', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '193.124.191.145', 'port': '9587', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '194.67.201.205', 'port': '9292', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '194.67.200.64', 'port': '9821', 'user': 'rdZvZY', 'pass': '4hB2v9'},
                   {'ip': '194.67.202.181', 'port': '9851', 'user': 'QWyoUo', 'pass': 'nRTyzY'},
                   {'ip': '194.67.202.134', 'port': '9450', 'user': 'QWyoUo', 'pass': 'nRTyzY'},
                   {'ip': '194.67.202.205', 'port': '9319', 'user': 'QWyoUo', 'pass': 'nRTyzY'},
                   {'ip': '194.67.202.203', 'port': '9417', 'user': 'QWyoUo', 'pass': 'nRTyzY'},
                   {'ip': '194.67.202.108', 'port': '9223', 'user': 'QWyoUo', 'pass': 'nRTyzY'},
                   {'ip': '193.124.191.159', 'port': '9233', 'user': 'QWyoUo', 'pass': 'nRTyzY'},
                   {'ip': '194.67.202.29', 'port': '9387', 'user': 'QWyoUo', 'pass': 'nRTyzY'},
                   {'ip': '194.67.202.198', 'port': '9839', 'user': 'QWyoUo', 'pass': 'nRTyzY'},
                   {'ip': '194.67.201.2', 'port': '9043', 'user': 'QWyoUo', 'pass': 'nRTyzY'},
                   {'ip': '194.67.201.51', 'port': '9636', 'user': 'QWyoUo', 'pass': 'nRTyzY'}]
PROXY_HOST = '193.124.190.63'
PROXY_PORT = 9317
PROXY_USER = 'rdZvZY'
PROXY_PASS = '4hB2v9'


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

def process_url(url):
    try:
        name_file = url.split('/')[-1]
        file_name = f"{name_file}.html"
        if os.path.exists(os.path.join('data', file_name)):
            return
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-setuid-sandbox')
        for i, background_js in enumerate(background_js_list):
            plugin_file = f'proxy_auth_plugin_{i}.zip'
            with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr('manifest.json', manifest_json)
                zp.writestr('background.js', background_js)
            chrome_options.add_extension(plugin_file)

        driver = undetected_chromedriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get('https://2ip.ua/ru/')
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="navbar-brand"]')))
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        driver.stop_client()
        driver.set_page_load_timeout(1)
        driver.set_script_timeout(1)
        time.sleep(1)
        with open(os.path.join('data', file_name), "w", encoding='utf-8') as fl:
            fl.write(driver.page_source)
    except TimeoutException:
        print(f"Timeout exception occurred while loading {url}")
    finally:
        driver.close()
        driver.quit()


def save_html():
    """Рабочий код"""
    with open('url.csv', newline='', encoding='utf-8') as files:
        csv_reader = list(csv.reader(files, delimiter=' ', quotechar='|'))
        urls = [row[0] for row in csv_reader]

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(process_url, urls)


if __name__ == '__main__':
    save_html()
