import zipfile
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import csv
import time

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
    products_all_url = []
    categoriy_product_urls = []
    pod_categoriy_product_urls = []
    card_product_url_all = []
    categoriy_product_url = driver.find_elements(By.XPATH, '//ul[@class="menu-list"]//li[@id="menu-id"]/a')
    for item_categoriy in categoriy_product_url:
        categoriy_product_urls.append(
            {'url_name': item_categoriy.get_attribute("href")}
        )

    for item_pod_categ in categoriy_product_urls:
        driver.get(item_pod_categ['url_name'])
        pod_categ_product_url = driver.find_elements(By.XPATH, '//div[@class="rubric"]//ul[@class="rubric-list"]//a')
        for item_card in pod_categ_product_url:
            pod_categoriy_product_urls.append(
                {'url_name': item_card.get_attribute("href")}
            )

    for item_prod in pod_categoriy_product_urls:
        products_all_url = []
        driver.get(item_prod['url_name'])
        group_product = item_prod['url_name'].split("/")[-1]

        # Листать по страницам ---------------------------------------------------------------------------
        isNextDisable = False
        while not isNextDisable:
            try:
                driver.execute_script("window.scrollBy(0,500)", "")
                next_button = driver.find_element(By.XPATH, '//div[@class="pager add-more-pages"]//button')
                # Проверка на наличие кнопки следующая страница, если есть, тогда листаем!
                if next_button:
                    next_button.click()
                    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                else:
                    isNextDisable = True
            except:
                isNextDisable = True
        # Листать по страницам ---------------------------------------------------------------------------
        products = driver.find_elements(By.XPATH, '//div[@class="catalog__product-list-row"]//div[@class="product-card__layout-inside"]//div[@class="product-card__layout-inside-link"]//div[@class="advanced-tile-on"]//a')
        for href in products:
            products_all_url.append(
                {'url_name': href.get_attribute("href"),
                 'title_group': f'{group_product}'
                 }
            )
        with open(f"C:\\scrap_tutorial-master\\dok.ua\\{group_product}.json", 'w') as file:
            json.dump(products_all_url, file, indent=4, ensure_ascii=False)
    driver.close()
    driver.quit()



def parsing_product():
    with open(f"C:\\scrap_tutorial-master\\dok.ua\\maslo-motornoe.json") as file:
        all_site = json.load(file)

    driver = get_chromedriver(use_proxy=False,
                              user_agent=f"{useragent.random}")


    # driver.maximize_window()
    with open(f"C:\\scrap_tutorial-master\\dok.ua\\data.csv", "w", errors='ignore') as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\r")
        writer.writerow(
            (
                '', '', '',

            )
        )
    for item in all_site[:2]:
        data_table = []
        driver.get(item['url_name'])  # 'url_name' - это и есть ссылка
        driver.maximize_window()
        # char = driver.find_element(By.XPATH, '//div[@class="col-sm-8 col-md-9"]//li[@class="product-item-detail-tab"]').click()
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # # Обезательно ждем
        # time.sleep(30)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # driver.implicitly_wait(5)
        block_all_price = driver.find_element(By.XPATH, '//div[@class="card-packaging"]')
        all_price = driver.find_elements(By.XPATH, '//div[@class="card-packaging__wrap"]//div[@class="card-packaging__col"]//a')
        table_price = []
        if block_all_price:
            for i in all_price:
                table_price.append(
                    {'url_name': i.get_attribute("href")}
                )
            for href in table_price:
                driver.get(href['url_name'])
                time.sleep(3)

                try:
                    name_product = driver.find_element(By.XPATH, '//div[@class="card-title-box"]//h1').get_attribute("textContent").replace("\n", " ")
                except:
                    name_product = 'Not title'
                try:
                    categ_product = driver.find_elements(By.XPATH, '//ol[@class="breadcrumblist horizontal"]//li')
                    bread = categ_product[-2].text

                except:
                    categ_product = "Not cat"
                try:
                    price_new = driver.find_element(By.XPATH, '//div[@class="card-price-box__price"]').get_attribute("outerText")
                except:
                    price_new = 'no price_old'
                try:
                    images = driver.find_element(By.XPATH,'//div[@class="slick-list draggable"]//div[@class="slick-track"]//img').get_attribute("src")
                except:
                    images = 'No images'
                # Получаем ссылки на все фото и добавляем их в словарь
                all_link_img =[]
                image = driver.find_elements(By.XPATH,'//div[@class="card-gallery"]//div[@class="card-gallery-big slick-initialized slick-slider"]//div[@class="slick-list draggable"]//img')
                for h in image:
                    all_link_img.append(h.get_attribute("src"))
                # Обьеденяим их в одну сроку, разделитель указываем в начале
                link_img = " ; ".join(all_link_img)



                try:
                    n_01 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][1]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_01 = 'No n_01'
                try:
                    n_02 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][2]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_02 = 'No n_02'
                try:
                    n_03 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][3]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_03 = 'No n_03'
                try:
                    n_04 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][4]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_04 = 'No n_04'
                try:
                    n_05 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][5]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_05 = 'No n_05'
                try:
                    n_06 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][6]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_06 = 'No n_06'
                try:
                    n_07 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][7]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_07 = 'No n_07'
                try:
                    n_08 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][8]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_08 = 'No n_08'
                try:
                    n_09 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][9]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_09 = 'No n_09'
                try:
                    n_10 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][10]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_10 = 'No n_10'
                try:
                    n_11 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][11]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
                except:
                    n_11 = 'No n_11'
                with open(f"C:\\scrap_tutorial-master\\dok.ua\\data.csv", "a", errors='ignore') as file:
                    writer = csv.writer(file, delimiter=";", lineterminator="\r")
                    writer.writerow(
                        (
                            name_product, bread, price_new, n_01, n_02, n_03, n_04, n_05, n_06, n_07, n_08, n_09, n_10, n_11,
                            link_img

                        )
                    )
        else:
            time.sleep(5)
            try:
                name_product = driver.find_element(By.XPATH, '//div[@class="card-title-box"]//h1').get_attribute("textContent").replace("\n", " ")
            except:
                name_product = 'Not title'
            try:
                categ_product = driver.find_elements(By.XPATH, '//ol[@class="breadcrumblist horizontal"]//li')
                bread = categ_product[-2].text

            except:
                categ_product = "Not cat"
            try:
                price_new = driver.find_element(By.XPATH, '//div[@class="card-price-box__price"]').get_attribute("outerText")
            except:
                price_new = 'no price_old'
            try:
                images = driver.find_element(By.XPATH,'//div[@class="slick-list draggable"]//div[@class="slick-track"]//img').get_attribute("src")
            except:
                images = 'No images'
            try:
                n_01 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][1]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_01 = 'No n_01'
            try:
                n_02 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][2]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_02 = 'No n_02'
            try:
                n_03 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][3]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_03 = 'No n_03'
            try:
                n_04 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][4]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_04 = 'No n_04'
            try:
                n_05 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][5]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_05 = 'No n_05'
            try:
                n_06 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][6]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_06 = 'No n_06'
            try:
                n_07 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][7]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_07 = 'No n_07'
            try:
                n_08 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][8]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_08 = 'No n_08'
            try:
                n_09 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][9]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_09 = 'No n_09'
            try:
                n_10 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][10]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_10 = 'No n_10'
            try:
                n_11 = driver.find_element(By.XPATH, '//div[@class="card-characts-list"]//div[@class="card-characts-list-item"][11]').get_attribute("outerText").replace("\n", " ").replace(" ? ", " ")
            except:
                n_11 = 'No n_11'

            with open(f"C:\\scrap_tutorial-master\\dok.ua\\data.csv", "a", errors='ignore') as file:
                writer = csv.writer(file, delimiter=";", lineterminator="\r")
                writer.writerow(
                    (
                        name_product, bread, price_new,n_01, n_02, n_03, n_04, n_05, n_06, n_07, n_08, n_09, n_10, n_11, images

                    )
                )
        # # Дописываем данные из списка data в файл
        # writer.writerows(
        #     data_table
        # )


if __name__ == '__main__':
    # #Сайт на который переходим
    # url = "https://dok.ua/"
    # Запускаем первую функцию для сбора всех url на всех страницах
    # save_link_all_product(url)
    parsing_product()
