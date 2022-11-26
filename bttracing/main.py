import select
import time
import pickle
import csv
import re
import time
from random import randint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
# Нажатие клавиш
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
)
# Отключение режима WebDriver
options.add_argument("--disable-blink-features=AutomationControlled")


def get_content(url):
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    # Перебираем все ссылки
    resp = requests.get(url, headers=header)

    # Настройка WEB драйвера
    driver_service = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(
        service=driver_service,
        options=options
    )
    # Окно браузера на весь экран
    driver.maximize_window()
    driver.get(url=url)
    driver.implicitly_wait(5)
    # Находим выпадающий списко №1
    avto = driver.find_elements(By.XPATH, '//select[@class="jet-select__control depth-0"]')
    # Находим выпадающий списко №1
    avto_year = driver.find_elements(By.XPATH, '//select[@class="jet-select__control depth-1"]')
    # Если Xpath несколько выбираем необходимый
    select_avto = avto[1]
    # Если Xpath несколько выбираем необходимый
    select_avto_year = avto_year[1]
    # Делаем выбор через Select
    drp_select_avto = Select(select_avto)
    # Делаем выбор через Select
    drp_select_avto_year = Select(select_avto_year)
    for item in range(1, 2):
        time.sleep(5)
        # Черезе цикл выбираем поочереди каждый пункт выпадающего списка
        drp_select_avto.select_by_index(item)
        # Получаем название каждого выпадающего из списка названия
        name_avto = drp_select_avto.first_selected_option.text
        # Ставим обезательно время что-бы прогрузилась страница

        print(name_avto)
        for i in range(1, 2):
            time.sleep(5)
            driver.implicitly_wait(5)
            drp_select_avto_year.select_by_index(i)
            driver.implicitly_wait(5)
            name_year = drp_select_avto_year.first_selected_option.text
            print(name_year)

            #Даем время прогрузится странице
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            table = soup.find('div', attrs={'data-id': 'c7fb3b8'})
            tale_card = table.find_all('div', attrs={'class': re.compile('^jet-listing-grid__.*')})

            for j in tale_card:
                href = j.find_next('h3', attrs={'class': 'elementor-heading-title elementor-size-default'}).find('a').get("href")
                print(href)



def parse_content():
    url = "https://www.bttracing.com/"
    get_content(url)


if __name__ == '__main__':
    parse_content()
