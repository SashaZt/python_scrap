import random
from typing import Optional
import csv
import time
import os
import asyncio
import aiofiles
import aiohttp
# import main_asio_photo


import pandas as pd
import glob
import json
import html
import re

import requests
from bs4 import BeautifulSoup
import csv
def urls_photo():
    targetPattern = f"c:\\Data_olekmotocykle\\*.html"
    files_html = glob.glob(targetPattern)

    result_dict = {}
    for item in files_html:
        with open(item, encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, 'html.parser')
        try:
            div = soup.find_all("div", {"class": "lazyslider-container-lq"})[0]
        except:
            print(f'Ошибка в {item}')
            continue
        id_product = soup.find('div', {'class': 'product-code-ui product-code-lq'}).text.strip()
        imgs = div.find_all("img", {"class": "open-gallery-lq"})

        item_dict = {}
        for i, img in enumerate(imgs):
            url_photo = 'https://' + img["data-src"].replace("//", "")
            item_dict[f"url_{i + 1}"] = url_photo
            item_dict[f"id_{i + 1}"] = id_product

        result_dict[item.replace("c:\\Data_olekmotocykle\\", "")] = item_dict

    # записываем результат в файл JSON
    with open("result.json", "w") as json_file:
        json.dump(result_dict, json_file)
    print('Переходим к обработке main_asio_photo.py')

if __name__ == '__main__':
    urls_photo()
