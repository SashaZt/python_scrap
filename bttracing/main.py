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
# Работа с БД sqlite
import sqlite3
from sqlite3 import Error
# Работа с БД sqlite


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
    avto = driver.find_elements(By.XPATH, '//select[@class="jet-select__control depth-0"]')
    avto_year = driver.find_elements(By.XPATH, '//select[@class="jet-select__control depth-1"]')
    select_avto = avto[1]
    select_avto_year = avto_year[1]
    drp_select_avto = Select(select_avto)
    drp_select_avto_year = Select(select_avto_year)
    for item in range(1, 2):
        drp_select_avto.select_by_index(item)
        driver.implicitly_wait(2)
        for i in range(5):
            drp_select_avto_year.select_by_index(i)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            table = soup.find('div', attrs={'data-id': 'c7fb3b8'})
            driver.implicitly_wait(5)








def parse_content():
    url = "https://www.bttracing.com/"
    get_content(url)


if __name__ == '__main__':
    parse_content()
