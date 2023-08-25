import re
from bs4 import BeautifulSoup
import random
import glob
import re
from pathlib import Path
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
delta = '''
avtomobilnaya-aptechka
avtomobilnye-kliuchi
buksirovochnyy-tros
distillirovannaya-voda
fm-modulyatory
gruzovye-boksy
gubki-mochalki
kamery-zadnego-vida
klemmi_akkumuliatora
kompressory_avtomobilnye
kreplenie_dlya_velosipeda_na_avto
krepleniya-dlya-lyzh-i-snoubordov
motornoe-maslo-dlya-mototekhniki
nabor-avtomobilista
nabor-instrumentov
nozhi-montazhnye
nozhnicy-po-metallu
ochistiteli_dvigatelya_naruzhnye
ochistiteli_kondicionera
ochistiteli_ruk
ochistiteli_tormoznoy_sistemy
ochistiteli-karbiuratora
ochistiteli-salona
ochki-zashchitnye
perekhodnye-ramki-dlya-magnitol
poliroli-dlya-salona
polirol-dlya-avto
provoda-prikurivaniya
pusko-zaryadnye-ustroystva
restavracionnye-karandashi
schetki-skrebki-vodosgony
siemniki-izolyatsii
signalizatsii-na-avto
sredstva-dlya-ochistki-kuzova-avto
styazhki-dlya-gruza
tormoznaya-zhidkost
tortsevye-golovki
transmissionnoe-maslo
usb-kabeli
videoregistrator-zerkalo
yashchiki-dlya-instrumentov
zhilety-signalnyye
znaki_avarijnoj_ostanovki
'''
delta_list = delta.strip().split("\n")
def parsing():
    for folders in delta_list:
        print(folders)
    # folder = 'kreplenie_dlya_velosipeda_na_avto'
        name_files_ua = folders.replace('-', '_')
        try:
            file_name_ua = f"C:\\scrap_tutorial-master\\archive\\dok.ua\\heandler\\{name_files_ua}.html"
        except:
            file_name_ua = None

        name_files_rus = folders.replace('-', '_') + '_rus'
        file_name_rus = f"C:\\scrap_tutorial-master\\archive\\dok.ua\\heandler\\{name_files_rus}.html"
        try:
            with open(file_name_ua, encoding="utf-8") as file:
                 src = file.read()
        except:
            continue
        soup = BeautifulSoup(src, 'lxml')
        row_id = 1
        hedler_ua = []
        while True:
            element = soup.find('span', {'data-row-id': str(row_id)})
            if element:
                hedler_ua.append(element.text.strip())
                row_id += 1
            else:
                break
        hedler_ua = [re.sub(r',.*$', '', element) for element in hedler_ua]
        with open(file_name_rus, encoding="utf-8") as file:
             src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        row_id = 1
        hedler_rus = []
        while True:
            element = soup.find('span', {'data-row-id': str(row_id)})
            if element:
                hedler_rus.append(element.text.strip())
                row_id += 1
            else:
                break
        hedler_rus = [re.sub(r',.*$', '', element) for element in hedler_rus]
        # Элементы для добавления в начало каждого списка
        art_ua = 'Артикул'
        ser_ua = 'Серія'
        art_rus = 'Артикул'
        ser_rus = 'Серия'

        # Добавляем элементы в начало списков
        hedler_ua.insert(0, ser_ua)
        hedler_ua.insert(0, art_ua)

        hedler_rus.insert(0, ser_rus)
        hedler_rus.insert(0, art_rus)

        # Объединяем списки
        heandler = []
        heandler.extend(hedler_ua)
        heandler.extend(hedler_rus)
        add = ['link_product', 'name_product_ua', 'name_product_rus', 'link_img', 'price_product', 'delivery_product']
        heandler = add + heandler

        # Выводим исходные и объединенные списки для проверки
        # print("hedler_ua:", hedler_ua)
        # print("hedler_rus:", hedler_rus)
        yield folders, heandler
        # return folders, heandler

# folders = 'bokorezy'
def main():
    for folders, heandler in parsing():
        folders = folders.replace('-', '_')


        folder_ua = fr'c:\DATA\dok_ua\products\{folders}\ua\*.html'
        folder_rus = fr'c:\DATA\dok_ua\products\{folders}\rus\*.html'
        files_html_ua = glob.glob(folder_ua)
        files_html_rus = glob.glob(folder_rus)
        # heandler = ['link_product','name_product_ua','name_product_rus','link_img','price_product','delivery_product','Артикул', 'Серія', 'Довжина', 'Виробник', 'Тип товару', 'Особливості конструкції', 'Артикул', 'Серия', 'Длина', 'Производитель', 'Тип товара', 'Особенности конструкции']
        with open(f'C:\\scrap_tutorial-master\\archive\\dok.ua\\data\\{folders}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=heandler, delimiter=";")
            writer.writeheader()  # Записываем заголовки только один раз
            for item_ua, item_rus in zip(files_html_ua, files_html_rus):
                row_dict = {}  # словарь для текущей строки
                with open(item_ua, encoding="utf-8") as file:
                    src = file.read()
                soup = BeautifulSoup(src, 'lxml')
                try:
                    name_product_ua = soup.find('div', attrs={'class': 'card-title-box'}).find('h1').text.replace("\n", " ")
                except:
                    name_product_ua = None
                try:
                    link_product = soup.find('link', attrs={'hreflang': 'x-default'}).get('href')
                except:
                    link_product = None
                all_link_img = []
                try:
                    images  = soup.select('div.card-gallery-big__item img')
                    for img in images:
                        all_link_img.append(img['data-big-image'])
                except:
                    images = None
                link_img = ",".join(all_link_img)

                try:
                    price_product = soup.find('span', attrs={'itemprop': 'price'}).text

                except:
                    price_product = None
                try:
                    delivery_product = soup.find('span', attrs={'class': 'customer-city-date'}).text

                except:
                    delivery_product = None

                row_dict['link_product'] = link_product
                row_dict['name_product_ua'] = name_product_ua
                row_dict['link_img'] = link_img
                row_dict['price_product'] = price_product
                row_dict['delivery_product'] = delivery_product

                try:
                    rows_ua = soup.select('tr.card-characts-list-item')
                    for row in rows_ua:
                        title_cell = row.select_one('td.card-characts-list-item__title span.mistake-char-title')
                        text_cell = row.select_one('td.card-characts-list-item__text')
                        if title_cell and text_cell:
                            title_text = title_cell.get_text().strip()
                            text_value = text_cell.get_text().strip()
                            if title_text in heandler:
                                row_dict[title_text] = text_value

                except:
                    print("Ошибка в разборе RUS файла")
                # values_rus = []
                with open(item_rus, encoding="utf-8") as file:
                    src = file.read()
                soup = BeautifulSoup(src, 'lxml')
                try:
                    name_product_rus = soup.find('div', attrs={'class': 'card-title-box'}).find('h1').text.replace("\n", " ")
                except:
                    name_product_rus = None

                row_dict['name_product_rus'] = name_product_rus  # Добавляем значение для русского имени продукта

                try:
                    rows_rus = soup.select('tr.card-characts-list-item')
                    for row in rows_rus:
                        title_cell = row.select_one('td.card-characts-list-item__title span.mistake-char-title')
                        text_cell = row.select_one('td.card-characts-list-item__text')
                        if title_cell and text_cell:
                            title_text_rus = title_cell.get_text().strip()
                            text_value_rus = text_cell.get_text().strip()
                            if title_text_rus in heandler:
                                row_dict[title_text_rus] = text_value_rus
                except:
                    print("Ошибка в разборе RUS файла")

                writer.writerow(row_dict)




if __name__ == '__main__':
    main()
