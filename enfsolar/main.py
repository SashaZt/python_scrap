import json
import os
from multiprocessing import Pool
import csv
import lxml
import time
# Нажатие клавиш
from selenium.webdriver.common.keys import Keys
from random import randint
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import csv
from selenium import webdriver
import pickle

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
# Отключение режима WebDriver
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
)
driver_service = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
driver = webdriver.Chrome(
    service=driver_service,
    options=options
)
# Окно браузера на весь экран
driver.maximize_window()


# Для работы webdriver____________________________________________________

def get_content(url):
    # Создание файла отчета
    # with open("soft.csv", "w") as file:
    #     writer = csv.writer(file, delimiter=";", lineterminator="\r")
    #     writer.writerow(
    #         (
    #             "Ссылка",
    #             "Просмотры",
    #             "Город"
    #         )
    #     )
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 "
    }

    try:
        url_country = []
        url_firma = []
        resp = requests.get(url, headers=header)
        soup = BeautifulSoup(resp.text, 'lxml')
        table = soup.find('div', class_='mk-body')
        table_continent = table.find_all('div', class_='clearfix mk-section')
        for i in table_continent:
            driver.implicitly_wait(5)
            country_list = i.find_all('li', class_='pull-left')
            for j in country_list:
                href = 'https://www.enfsolar.com' + j.find_next('a').get("href")
                url_country.append(href)

        for item in url_country[0:1]:
            driver.implicitly_wait(5)
            driver.get(f'{item}')
            #Листать по страницам ---------------------------------------------------------------------------
            isNextDisable = False
            while not isNextDisable:
                try:
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    table_firma = soup.find('table', attrs={'class': 'enf-list-table'})
                    # Получаем таблицу всех фирм на странице
                    firma_url = table_firma.find('tbody').find_all('tr')
                    # Получаем ссылку на каждую фирму
                    for href in firma_url:
                        url = href.find_next('td').find('a').get("href")
                        # Добавляем ссылки на фирмы в список
                        url_firma.append(url)
                    time.sleep(5)
                    try:
                        next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//i[@class="fa fa-chevron-right"]')))
                        # next_page = driver.find_element(By.XPATH, '//i[@class="fa fa-chevron-right"]').click()
                        # next_page_class = next_page.get_attribute('protocol')
                        if next_button:
                            print('Есть')
                            next_button.click()
                        else:
                            isNextDisable = True
                        time.sleep(1)
                    except Exception as ex:
                        print(ex)



                except:
                    isNextDisable = True
            # Листать по страницам ---------------------------------------------------------------------------












    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


def parse_content():
    url = "https://www.enfsolar.com/directory/installer"
    get_content(url)


if __name__ == '__main__':
    parse_content()
