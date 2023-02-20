import glob
import urllib.request
from urllib.request import urlretrieve
from PIL import Image
import PIL
import re
import zipfile
import os
import json
import csv
import time
import requests
from bs4 import BeautifulSoup
import lxml
# Нажатие клавиш
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

'''
Нужно тестировать
pip install -U 'requests[socks]'
import requests

resp = requests.get('http://go.to', 
                    proxies=dict(http='socks5://user:pass@host:port',
                                 https='socks5://user:pass@host:port'))


'''

'''
Тестировать
proxies = [
    {
        'addr': '123.123.123.123:1234',
        'auth': 'admin:admin'
    },
    {
        'addr': '200.2.2.2:7868',
        'auth': 'foo:bar'
    },
]

for proxy in proxies:
    service_args = ['--proxy=' + proxy['addr'], '--proxy-type=socks5', '--proxy-auth=' + proxy['auth']]
    driver = webdriver.Chrome(executable_path=path_to_chrome_webdriver, 
                              service_args=service_args)
    driver.get('https://2ip.ru/')
    driver.close()

'''



from selenium import webdriver
import random
from fake_useragent import UserAgent

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

useragent = UserAgent()


def proxy():
    driver_service = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    username = 'alex'
    password = 'DbrnjhbZ88'
    ip = '37.233.3.100'
    port = 30808
    proxy = f'{username}:{password}@{ip}:{port}'
    # options = webdriver.ChromeOptions()
    options = {

        'proxy': {
            'https': f'https://{proxy}',
        }

    }

    service_args = [
        '--proxy=37.233.3.100:30808',
        '--proxy-type=socks5',
        '--proxy-auth=alex:DbrnjhbZ88',

    ]

    driver = webdriver.Chrome(
        service=driver_service,
        options=options,
        service_args=service_args
    )
    driver.get('https://2ip.ua/ru/')
    time.sleep(20)
    driver.close()
    driver.quit()




    proxies = [
        {
            'addr': '37.233.3.100:30808',
            'auth': 'alex:DbrnjhbZ88'
        }
        # {
        #     'addr': '200.2.2.2:7868',
        #     'auth': 'foo:bar'
        # },
    ]

    # for proxy in proxies:
    #     service_args = ['--proxy=' + proxy['addr'], '--proxy-type=socks5', '--proxy-auth=' + proxy['auth']]
    #     driver_service = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    #     driver = webdriver.Chrome(
    #         service=driver_service,
    #         options=options,
    #         service_args=service_args
    #     )
    #     driver.get('https://2ip.ua/ru/')
    #     time.sleep(20)
    #     driver.close()



if __name__ == '__main__':
    proxy()