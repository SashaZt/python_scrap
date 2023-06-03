import math
import pickle
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import re
import json
import time


def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    s = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    """Рабочая настройка для обхода Cloudflare """
    return driver


def get_url_category(url):
    driver = get_chromedriver()
    driver.get(url)
    driver.maximize_window()
    try:
        counter_wait_url = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="text-secondary"]')))
    except:
        print('Не загрузилась')
        return
    # # # Читание куки
    for cookie in pickle.load(open("cookies", "rb")):
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(10)

    about_results = driver.find_element(By.XPATH, '//div[@class="text-secondary"]').text
    result_number = int(re.search(r'\d+', about_results).group())
    url_in_page = 48
    list_url = math.ceil(result_number / url_in_page)

    product_url = []
    for i in range(0, list_url + 1):
        if i == 1:
            driver.get(url)
            time.sleep(5)
            card_product = driver.find_elements(By.XPATH,
                                                '//div[@class="row q-col-gutter-sm-md q-px-sm-md"]//div[@class="full-height full-width position-relative"]/a')
            for i in card_product:
                href = i.get_attribute('href')
                product_url.append(
                    {
                        'url_name': href
                    }
                )
            driver.execute_script("window.scrollBy(0,1800)", "")


        elif i > 1:
            driver.get(f'{url}&page={i}')
            time.sleep(5)
            card_product = driver.find_elements(By.XPATH,
                                                '//div[@class="row q-col-gutter-sm-md q-px-sm-md"]//div[@class="full-height full-width position-relative"]/a')
            for i in card_product:
                href = i.get_attribute('href')
                product_url.append(
                    {
                        'url_name': href
                    }
                )
            driver.execute_script("window.scrollBy(0,1800)", "")

    with open("car_url.json", 'w') as file:
        json.dump(product_url, file, indent=4, ensure_ascii=False)
    print(len(product_url))

    driver.close()
    driver.quit()


def get_url_product(url):
    driver = get_chromedriver()
    with open(f"car_url.json") as file:
        all_site = json.load(file)
    counter_url = len(all_site)
    products_all = []
    driver.get(url)
    for cookie in pickle.load(open("cookies", "rb")):
        driver.add_cookie(cookie)
    driver.refresh()
    for item in all_site:
        driver.get(item['url_name'])  # 'url_name' - это и есть ссылка
        # time.sleep(1)
        counter_wait_url = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="seller__title"]')))
        counter_wait_url = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="seller__title"]')))
        try:
            if driver.find_element(By.XPATH, '//div[@class="m-l-sm seller__info-items seller-details"]'):
                counter_wait_url = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="seller__title"]')))
                try:
                    name_server = driver.find_element(By.XPATH,
                                                      '//h1[@class="main__title-skin"]').text
                except:
                    name_server = ""

                try:
                    server_regions = driver.find_elements(By.XPATH,
                                                          '//div[@class="seller_details-region-main"]//div[@class="region_right-detail"]')
                except:
                    server_regions = ""
                try:
                    sr = driver.find_elements(By.XPATH,
                                              '//div[@class="seller_details-region-main"]//div[@class="region_left-detail"]')
                except:
                    sr = ''

                price_server = driver.find_element(By.XPATH,
                                                   '//div[@class="price_section-section"]//span[@class="amount__section-main"]').text.replace(
                    ".", ",")
                try:
                    server_region = server_regions[0].text
                except:
                    server_region = None
                try:
                    server_Platform = server_regions[1].text
                except:
                    server_Platform = None
                try:
                    server_ServiceType = server_regions[2].text
                except:
                    server_ServiceType = None
                try:
                    stock = driver.find_element(By.XPATH, '//span[@id="precheckout_offer_stock"]').text
                except:
                    stock = ""
                try:
                    checkout_devlivery = driver.find_element(By.XPATH, '//div[@class="checkout-plus-minus-main-section"]').find_element(By.XPATH, '//input[@type="number"]').get_attribute('value')
                except:
                    checkout_devlivery = ""

                # Создаем список
                products_all.append(
                    {
                        'price': price_server,
                        'name': name_server,
                        'region': server_region,
                        'Platform': server_Platform,
                        'ServiceType': server_ServiceType,
                        'Stock': stock,
                        'checkout_devlivery': checkout_devlivery

                    }
                )
                #
                # В панду загоняем наш список и сохраняем в csv

        except:
            continue
    df = pd.DataFrame(products_all)
    # df_sort = df.sort_values(['server_region', 'server_Platform', 'server_ServiceType'])
    df.to_csv("data.csv",
              # encoding='utf-8',
              mode='w',
              header=True,
              index=False,
              sep=';'
              )
    print('Все сделал')
    driver.close()
    driver.quit()


def parse_content():
    print("Вставьте ссылку")
    url = input()
    get_url_category(url)
    get_url_product(url)


if __name__ == '__main__':
    parse_content()
