from datetime import datetime
import requests
import re
import random
import json
from bs4 import BeautifulSoup
from lxml import html
import glob
from selenium.webdriver.chrome.service import Service
import os
import shutil
import tempfile
from selenium.webdriver.common.action_chains import ActionChains
import zipfile
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv


def parsing_html():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Необходимо для работы в фоновом режиме (без отображения окна браузера)
    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    folders_html = [r"c:\salomon_pl\html_product\kids\*.html",
                    r"c:\salomon_pl\html_product\men\*.html",
                    r"c:\salomon_pl\html_product\women\*.html"
                    ]
    for file in folders_html[1:2]:  # Убарть срез для категории!
        group = file.split('\\')[3]
        files_json = glob.glob(file)
        for item in files_json[:1]:




            driver.get(item)
            html_content = driver.page_source
            soup_img = BeautifulSoup(html_content, 'lxml')
            alls_photo = []
            try:
                product_image_divs = soup_img.find('div', attrs={'class': 'product-slider_nav'}).find_all('img')
                # product_image_divs = driver.find_elements(By.XPATH, '//div[@class="product-slider_nav"]//img')
                for i in product_image_divs:
                    src = i.get('src')
                    if src and re.search(r'https://www.salomon.com/pl-pl/shop-emea/media', src):
                        alls_photo.append(src.split('.png')[0] + '.png')

            except:
                alls_photo_set = set()
                product_image_divs = soup_img.find_all('ul', attrs={'class': 'layout-pdp-media-grid slider-scroll_wrapper'})[0].find_all('source')
                # product_image_divs = driver.find_elements(By.XPATH, '//div[@class="product-slider_nav"]//img')
                for i in product_image_divs:
                    src = i.get('data-srcset')
                    if src and re.search(r'https://www.salomon.com/pl-pl/shop-emea/media', src):
                        urls = src.split('.png')[0] + '.png'
                        alls_photo_set.add(urls)
                alls_photo = list(alls_photo_set)






if __name__ == '__main__':
    parsing_html()
