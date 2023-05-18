import zipfile
import os
import time
import undetected_chromedriver

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv
from selenium.webdriver.chrome.service import Service

# def get_undetected_chromedriver():
#     PROXY = "37.233.3.100:9999"
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument(
#         '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
#
#     chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument('--proxy-server=%s' % PROXY)
#     # chrome_options.add_argument('--headless')
#     """Проба"""
#     #chrome_options.add_argument("--disable-dev-shm-usage")
#     #chrome_options.add_argument("--disable-setuid-sandbox")
#     #chrome_options.add_argument('--proxy-server=37.233.3.100:9999')
#
#
#     driver = undetected_chromedriver.Chrome()
#
#     return driver

"""Рабочий на один прокси"""

# def get_chromedriver():
#     PROXY = "37.233.3.100:9999"
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--proxy-server=%s' % PROXY)
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument(
#         '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
#
#     chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--start-maximized")
#     s = Service(
#         executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
#     )
#     driver = webdriver.Chrome(
#         service=s,
#         options=chrome_options
#     )
#
#     return driver



# Список прокси-серверов
proxies = [
    "37.233.3.100:9999",
    "203.142.76.114:3128",
    "95.216.198.156:8080",
    # Добавьте свои прокси-сервера сюда
]

# Индекс текущего прокси-сервера
current_proxy_index = 0

def get_chromedriver():
    global current_proxy_index

    # Выбираем следующий прокси-сервер
    current_proxy = proxies[current_proxy_index]

    # Создаем объект chrome_options и добавляем настройки
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % current_proxy)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')

    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-gpu")

    # Создаем объект webdriver.Chrome
    s = Service(
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    # Увеличиваем индекс для следующего вызова
    current_proxy_index = (current_proxy_index + 1) % len(proxies)

    return driver

def main():
    url = "https://combomed.ru/antigrippin-yunispaz"
    driver = get_chromedriver()
    driver.maximize_window()
    driver.get(url)
    time.sleep(10)

if __name__ == '__main__':
    main()
