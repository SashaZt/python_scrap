import csv
import glob
import json
import time

import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Данные для прокси
PROXY_HOST = 'IP'
PROXY_PORT = 'PORT'  # Без кавычек
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


def get_undetected_chromedriver(use_proxy=False, user_agent=None):
    # Обход защиты
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-gpu")

    driver = undetected_chromedriver.Chrome()

    return driver


# Получаем все ссылки на необходимый товар
def save_link_all_product(url):
    product_url = []
    driver = get_undetected_chromedriver()
    driver.get(url)
    isNextDisable = False
    while not isNextDisable:
        try:
            # Ждем пока появится элемент, как только появляется, выполняем следующие действия
            button_find = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-default-highlight btn-find"]')))
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            card_product_url = driver.find_elements(By.XPATH,
                                                    '//li[@class="result-list-entry result-list-entry--clickable result-list-entry--hoverable search-result-list-item search-result-entry-item"]//div[@class="result-list-entry-wrapper mb-3 mb-md-3"]//a')
            for item in card_product_url:
                product_url.append(
                    {'url_name': item.get_attribute("href")}
                )

            next_button = driver.find_element(By.XPATH, '//button[@class="link icon-right"]')
            # driver.execute_script("window.scrollBy(0,1500)", "")
            if next_button:
                next_button.click()
                button_find = WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-default-highlight btn-find"]')))
            else:
                isNextDisable = True
        except:
            isNextDisable = True

    with open(f"C:\\scrap_tutorial-master\\archive\\11800\\url\\Alfa-Romeo\\url_firm.json", 'w') as file:
        json.dump(product_url, file, indent=4, ensure_ascii=False)
    driver.close()
    driver.quit()


# Сохраняем товар в html файл
def save_html():
    driver = get_undetected_chromedriver()

    with open(f"C:\\scrap_tutorial-master\\archive\\11800\\url\\Alfa-Romeo\\url_firm.json") as file:
        all_site = json.load(file)

    # С json вытягиваем только 'url_name' - это и есть ссылка
    count = 0
    for item in all_site:
        count += 1
        driver.get(item['url_name'])  # 'url_name' - это и есть ссылка
        try:
            next_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-default-highlight btn-find"]')))
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            time.sleep(1)
            with open(f"C:\\scrap_tutorial-master\\archive\\11800\\data\\Alfa-Romeo\\data_{count}.html", "w",
                      encoding='utf-8') as fl:
                fl.write(driver.page_source)
        except:
            continue

    driver.close()
    driver.quit()


# Парсим html файл
def pasing_html():
    datas = []
    targetPattern = r"C:\\scrap_tutorial-master\\archive\\11800\\data\\Alfa-Romeo\\*.html"
    files_html = glob.glob(targetPattern)

    for item in files_html:
        data_csv = []
        with open(item, encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        try:
            brand_firn = soup.find('span', attrs={'class': 'trades-list'}).text.strip()
        except:
            brand_firn = ""

        script = soup.find_all('script', type="application/ld+json")[0]
        # script = soup.find_all('script', type="application/json")[1].text.strip()[4:-3]
        data_json = json.loads(script.string)
        name_firm = data_json['name']
        telef_firm = data_json['telephone'][0]
        try:
            email_firm = data_json['email']
        except:
            email_firm = ""
        try:
            url_firm = data_json['url']
        except:
            url_firm = ""
        try:
            postalCode = data_json['address']['postalCode']
        except:
            postalCode = ""
        try:
            addressLocality = data_json['address']['addressLocality']
        except:
            addressLocality = ""
        try:
            addressRegion = data_json['address']['addressRegion']
        except:
            addressRegion = ""
        try:
            streetAddress = data_json['address']['streetAddress']
        except:
            streetAddress = ""
        adress_firma = f"{postalCode}, {addressLocality}, {addressRegion}, {streetAddress}"

        try:
            servises_firma_1 = soup.find_all('div', attrs={'class': 'term-box__panel-content'})[0].find('div', attrs={
                'class': 'row'}).find_all('div')
        except:
            servises_firma_1 = ""

        try:
            servises_firma_2 = soup.find_all('div', attrs={'class': 'term-box__panel-content'})[1].find('div', attrs={
                'class': 'row'}).find_all('div')
        except:
            servises_firma_2 = ""
        all_s1 = []
        for s1 in servises_firma_1:
            all_s1.append(s1.text)
        servises_firma_01 = ",".join(all_s1)
        all_s2 = []
        for s2 in servises_firma_2:
            all_s2.append(s2.text)
        servises_firma_02 = ",".join(all_s2)
        servise = f'{servises_firma_01}, {servises_firma_02}'
        with open(f"C:\\scrap_tutorial-master\\archive\\11800\\data\\Alfa-Romeo\\data.csv", "a",
                  errors='ignore') as file:
            writer = csv.writer(file, delimiter=";", lineterminator="\r")
            writer.writerow(
                (
                    brand_firn, name_firm, adress_firma, telef_firm, email_firm, url_firm, servise
                )
            )


if __name__ == '__main__':
    url = "https://www.11880.com/suche/Kfz-Reparaturen/deutschland?page=1110&query=cmxXakxKcWNvelMwbko5aFZ3YzdWemtjb0p5MFZ3YmtBRmp2b1RTbXFSOXZuekl3cVBWNnJsV3NuSkR2QnZWMlpUQXVMR1YwQXdxd1pKSXVaR3l5WlFOME1UWjVMbVJ2WVBXc3BUeXhWd2JrQlFFOXNGanZwMkl1cHpBYkczTzBuSjlocGxWNnIzMGZWYVd1b3pFaW9JQXlNSkR2Qno1MW9Uazk="
    save_link_all_product(url)
    # save_html()
    # pasing_html()
