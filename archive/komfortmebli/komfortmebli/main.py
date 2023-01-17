import datetime
import json
import csv
import os
import pickle
import lxml
import time
# Нажатие клавиш
from selenium.webdriver.common.keys import Keys
from random import randint
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import csv
from selenium import webdriver
import random
from fake_useragent import UserAgent
# Библиотеки для Асинхронного парсинга
import asyncio
import aiohttp
# Библиотеки для Асинхронного парсинга

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

useragent = UserAgent()
options = webdriver.ChromeOptions()
# Отключение режима WebDriver
options.add_experimental_option('useAutomationExtension', False)
# # Работа в фоновом режиме
options.headless = True
options.add_argument(
    # "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    f"user-agent={useragent.random}"
)
driver_service = Service(executable_path="C:\scrap_tutorial-master\chromedriver.exe")
driver = webdriver.Chrome(
    service=driver_service,
    options=options
)


# # Окно браузера на весь экран
# driver.maximize_window()
# driver.set_window_size(1400, 3000)


# Для работы webdriver____________________________________________________


# Для работы undetected_chromedriver ---------------------------------------

# import undetected_chromedriver as uc
# driver = uc.Chrome()


# Для работы undetected_chromedriver ---------------------------------------


# "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"

def get_content(url):
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": f"{useragent.random}"

    }
    data = []
    data_2 = []
    driver.get(url=url)
    product_url = []
    time.sleep(2)
    # Прокрутка до конца страницы
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Обезательно ждем
    time.sleep(2)
    # Повторяем сколько необходимо
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    card_product_url = driver.find_elements(By.XPATH,
                                            '//div[@class="catalog-section bx-red"]//div[@class="product-item"]/a[@itemprop="url"]')

    for item in card_product_url:
        product_url.append(
            {'url_name': item.get_attribute("href")}  # Добавляем в словарь два параметра для дальнейшего записи в json
        )

    for item in product_url:
        driver.get(item['url_name'])  # 'url_name' - это и есть ссылка
        time.sleep(2)
        try:
            name_product = driver.find_element(By.XPATH, '//div[@class="workarea"]//div[@class="col-xs-12"]//h1').text
        except:
            name_product = 'Нет названия'
        try:
            old_price = driver.find_element(By.XPATH, '//div[@class="product-item-detail-price-old"]').text
        except:
            old_price = "Нет старой цены"
        try:
            new_price = driver.find_element(By.XPATH, '//div[@class="product-item-detail-price-current"]').text
        except:
            new_price = "Нет новой цены"

        try:
            xapac_tovar = driver.find_elements(By.XPATH,
                                               '//div[@class="product-item-detail-tab-content"]//dl[@class="product-item-detail-properties"]/dt')
            title_tovar = driver.find_elements(By.XPATH,
                                               '//div[@class="product-item-detail-tab-content"]//dl[@class="product-item-detail-properties"]/dd')

            charac_01 = xapac_tovar[0].text

            charac_02 = xapac_tovar[1].text
            if charac_02 == 'Ціновий діапазон':
                charac_02 = xapac_tovar[1].text
            else:
                charac_02 = 'Ширина'
            print(charac_02)
            # charac_03 = xapac_tovar[2].text
            # if charac_03 == 'Серія':
            #     charac_03 = xapac_tovar[2].text
            # else:
            #     charac_03 = 'Глибина'
            # charac_04 = xapac_tovar[3].text
            # charac_05 = xapac_tovar[4].text
            # charac_06 = xapac_tovar[5].text
            # charac_07 = xapac_tovar[6].text
            # charac_08 = xapac_tovar[7].text
            # charac_09 = xapac_tovar[8].text
            # charac_10 = xapac_tovar[9].text
            # charac_11 = xapac_tovar[10].text

            # tovar_01 = title_tovar[0].text
            # tovar_02 = title_tovar[1].text
            # tovar_03 = title_tovar[2].text
            # tovar_04 = title_tovar[3].text
            # tovar_05 = title_tovar[4].text
            # tovar_06 = title_tovar[5].text
            # tovar_07 = title_tovar[6].text
            # tovar_08 = title_tovar[7].text
            # tovar_09 = title_tovar[8].text
            # tovar_10 = title_tovar[9].text
            # tovar_11 = title_tovar[10].text
        except:
            j = "header"
            k = 'title'
        try:
            text_product = driver.find_element(By.XPATH, '//div[@class="product-item-detail-tab-content active"]').text
        except:
            text_product = "Нет описания"

        # data.append(
        #     [name_product, old_price, new_price, tovar_01, tovar_02, tovar_03, tovar_04, tovar_05, tovar_06,
        #      tovar_07, tovar_08, tovar_09, tovar_10, tovar_11, text_product]
        # )
        #
        # with open("doctor.csv", "w") as file:
        #     writer = csv.writer(file, delimiter=";", lineterminator="\r")
        #     writer.writerow(
        #         (
        #             "Название",
        #             "Старая цена",
        #             "Новая цена",
        #             charac_01,
        #             charac_02,
        #             charac_03,
        #             charac_04,
        #             charac_05,
        #             charac_06,
        #             charac_07,
        #             charac_08,
        #             charac_09,
        #             charac_10,
        #             charac_11,
        #             'Описание'
        #
        #         )
        #     )
        #     writer.writerows(
        #         data
        #     )

    driver.close()
    driver.quit()


def parse_content():
    url = "https://komfortmebli.com.ua/catalog/gotovye_komplekty_krashenuy/"
    get_content(url)


if __name__ == '__main__':
    parse_content()
