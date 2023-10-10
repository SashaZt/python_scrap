from bs4 import BeautifulSoup
import random
import glob
import re
import requests
import json
import cloudscraper
import os
from playwright.sync_api import sync_playwright
from cf_clearance import sync_cf_retry, sync_stealth
import time
import shutil
import tempfile
# import undetected_chromedriver as webdriver


from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv


def get_chromedriver():
    options = webdriver.ChromeOptions()

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-gpu")
    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # chrome_options.add_argument('--disable-infobars')
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument('--disable-extensions') # Отключает использование расширений
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-setuid-sandbox')
    options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    service = ChromeService(executable_path='C:\\scrap_tutorial-master\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })
    return driver
def get_selenium():
    url = 'https://apnext.eu/pl/koszyk'
    driver = get_chromedriver()
    driver.maximize_window()
    driver.get(url)
    time.sleep(200)

    filename = f"apnext.html"
    with open(filename, "w", encoding='utf-8') as fl:
        fl.write(driver.page_source)

def parsing():
    file = "apnext.html"
    with open(file, encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Code', 'Brand', 'Price', 'Input Value']
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        # Extract '27-0287'
        table = soup.find('div', attrs={'class': 'flex-order-process'})
        all_product = table.find_all('div', attrs={'class': 'cart-content-group pb-4'})
        for i in all_product:

            strong_tag = i.find('strong')
            code = strong_tag.text if strong_tag else "Not found"

            # Extract 'MAXGEAR'
            maxgear_tag = i.find('small')
            maxgear = maxgear_tag.text if maxgear_tag else "Not found"

            # Extract '2,38'
            price_tag = i.select_one('.col-4 > .d-flex > span > small')
            price = price_tag.text.split('/')[0] if price_tag else "Not found"

            # Extract '4' from input field
            input_tag = i.find('input', {'type': 'number'})
            input_value = input_tag['value'] if input_tag else "Not found"
            writer.writerow({'Code': code, 'Brand': maxgear, 'Price': price, 'Input Value': input_value})
            # # Display extracted data
            # print(f"Code: {code}")
            # print(f"Brand: {maxgear}")
            # print(f"Price: {price}")
            # print(f"Input Value: {input_value}")


if __name__ == '__main__':
    # get_requests()
    # get_cloudscraper()
    # get_selenium()
    parsing()
