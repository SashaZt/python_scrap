import time
import pickle
import csv
import time
from random import randint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
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


# # Работа в фоновом режиме
# options.headless = True
# # Настройка WEB драйвера
# driver_service = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
# driver = webdriver.Chrome(
#     service=driver_service,
#     options=options
# )
# # Окно браузера на весь экран
# driver.maximize_window()


def get_content(url):
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    # Создаем сначала файл куда будем записывать информацию
    with open("doctor.csv", "w") as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\r")
        writer.writerow(
            (
                "Имя",
                "Специальность",
                "Телефон"
            )
        )
    for i in range(1, 3):
        # Перебираем все ссылки
        resp = requests.get(url + f"&page={i}", headers=header)
        time.sleep(randint(1, 5))
        try:
            # Настройка WEB драйвера
            driver_service = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
            driver = webdriver.Chrome(
                service=driver_service,
                options=options
            )
            # Окно браузера на весь экран
            driver.maximize_window()
            soup = BeautifulSoup(resp.text, 'lxml')
            table = soup.find('div', attrs={'data-id': 'search-left-column'})
            table_card = table.find_all('div', attrs={'class': 'card-body p-0'})
            url_doctor = []

            for item in table_card:
                href = item.find_next('a').get("href")
                url_doctor.append(href)

            for href in url_doctor:
                time.sleep(randint(1, 5))

                driver.get(f"{href}")
                for cookie in pickle.load(open("cookies", "rb")):
                    driver.add_cookie(cookie)
                # driver.implicitly_wait(5)
                driver.refresh()
                driver.implicitly_wait(5)
                specialty_doctor_list = driver.find_elements(By.XPATH, '//a[@class="text-muted"]')
                # Получаем специальность доктора
                specialty_doctor = specialty_doctor_list[0].text.strip()
                # Получаем имя доктора
                name_doctor = driver.find_element(By.XPATH, '//div[@data-id="profile-fullname-wrapper"]').text.strip()
                # # Закрыть всплывающее окно
                # windows_close = driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
                # driver.implicitly_wait(5)
                # windows_close.click()
                # driver.implicitly_wait(5)
                # Открываем телефон
                phone_show = driver.find_element(By.XPATH, '//a[@data-id="show-phone-number-modal"]')
                if phone_show.is_displayed():
                    driver.implicitly_wait(5)
                    phone_show = driver.find_element(By.XPATH, '//a[@data-id="show-phone-number-modal"]')
                    phone_show.click()
                    driver.implicitly_wait(5)
                    driver.implicitly_wait(5)
                    # Если есть похожие елементы, тогда находим все елементы find_elements
                    checkbox = driver.find_elements(By.XPATH, '//input[@data-id="gdpr-number-terms-button"]')
                    # Нажимаем на N елемент
                    checkbox[1].click()
                    driver.implicitly_wait(5)
                    # Получаем номер телефона
                    phone_doctor = driver.find_element(By.XPATH,
                                                       '//a[@data-patient-app-event-name="dp-call-phone"]').text.strip()
                else:
                    phone_doctor = 'Нет номера телефона'
                with open("doctor.csv", "a", errors='ignore') as file:
                    writer = csv.writer(file, delimiter=";", lineterminator="\r")
                    writer.writerow(
                        (
                            name_doctor,
                            specialty_doctor,
                            phone_doctor
                        )
                    )
                # print(name_doctor, specialty_doctor, phone_doctor)
        except Exception as ex:
            print({href})
        finally:
            driver.close()
            driver.quit()


def parse_content():
    url = "https://www.znanylekarz.pl/szukaj?q=&loc=Warszawa"
    get_content(url)


if __name__ == '__main__':
    parse_content()
