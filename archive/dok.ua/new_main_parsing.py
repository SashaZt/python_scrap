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


folders = 'maslo_motornoe'
def main():
    folder_ua = fr'c:\DATA\dok_ua\products\{folders}\ua\*.html'
    folder_rus = fr'c:\DATA\dok_ua\products\{folders}\rus\*.html'
    files_html_ua = glob.glob(folder_ua)
    files_html_rus = glob.glob(folder_rus)
    heandler = ['link_product','name_product_ua','name_product_rus','link_img','price_product','delivery_product','Серія','Артикул', "В'язкість за SAE", 'Ємність, л', 'Виробник', 'Тип', 'Тип двигуна', 'Підходить для генераторів', 'Допуск OEM VAG (VW, Audi, Seat, Skoda)', 'Класифікація ACEA', 'Класифікація API', 'Допуск OEM General Motors', 'Допуск OEM Renault', 'Допуск OEM BMW', 'Класифікація ILSAC', 'Допуск OEM Mercedes Benz', 'Допуск OEM Peugeot, Citroen', 'Допуск OEM Ford', 'Допуск OEM Chrysler', 'Допуск OEM Fiat', 'Допуск OEM Volvo', 'Допуск OEM Porsche', 'Допуск OEM Jaguar, Land Rover', 'Допуск OEM Detroit Diesel', 'Класифікація JASO', 'Допуск OEM MAN', 'Допуск OEM Allison', 'Допуск OEM Caterpillar', 'Допуск OEM Cummins', 'Допуск OEM Deutz', 'Допуск OEM Iveco', 'Допуск OEM Mack', 'Допуск OEM MTU', 'Допуск OEM Scania', 'Допуск OEM ZF', 'Допуск OEM Valtra', 'Допуск OEM Voith', 'Допуск OEM John Deere', 'Допуск OEM DAF','Серия','Артикул','Вязкость по SAE', 'Емкость, л', 'Производитель', 'Тип', 'Тип двигателя', 'Подходит для генераторов', 'Допуск OEM VAG (VW, Audi, Seat, Skoda)', 'Классификация ACEA', 'Классификация API', 'Допуск OEM General Motors', 'Допуск OEM Renault', 'Допуск OEM BMW', 'Классификация ILSAC', 'Допуск OEM Mercedes Benz', 'Допуск OEM Peugeot, Citroen', 'Допуск OEM Ford', 'Допуск OEM Chrysler', 'Допуск OEM Fiat', 'Допуск OEM Volvo', 'Допуск OEM Porsche', 'Допуск OEM Jaguar, Land Rover', 'Допуск OEM Detroit Diesel', 'Классификация JASO', 'Допуск OEM MAN', 'Допуск OEM Allison', 'Допуск OEM Caterpillar', 'Допуск OEM Cummins', 'Допуск OEM Deutz', 'Допуск OEM Iveco', 'Допуск OEM Mack', 'Допуск OEM MTU', 'Допуск OEM Scania', 'Допуск OEM ZF', 'Допуск OEM Valtra', 'Допуск OEM Voith', 'Допуск OEM John Deere', 'Допуск OEM DAF']
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=heandler, delimiter=";")
        writer.writeheader()  # Записываем заголовки только один раз
        for item_ua, item_rus in zip(files_html_ua[:10], files_html_rus[:10]):
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





        #
        #
        #
        #
        # values_ua = []
        # for item in files_html_ua[:10]:
        #     with open(item, encoding="utf-8") as file:
        #         src = file.read()
        #     soup = BeautifulSoup(src, 'lxml')
        #     try:
        #         name_product_ua = soup.find('div', attrs={'class': 'card-title-box'}).find('h1').text.replace("\n", " ")
        #     except:
        #         name_product_ua = None
        #     try:
        #         link_product = soup.find('link', attrs={'hreflang': 'x-default'}).get('href')
        #     except:
        #         link_product = None
        #     all_link_img = []
        #     try:
        #         images  = soup.select('div.card-gallery-big__item img')
        #         for img in images:
        #             all_link_img.append(img['data-big-image'])
        #     except:
        #         images = None
        #     link_img = ",".join(all_link_img)
        #
        #     try:
        #         price_product = soup.find('span', attrs={'itemprop': 'price'}).text
        #
        #     except:
        #         price_product = None
        #     try:
        #         delivery_product = soup.find('span', attrs={'class': 'customer-city-date'}).text
        #
        #     except:
        #         delivery_product = None
        #
        #     csv_data_ua = []
        #     try:
        #         rows_ua = soup.select('tr.card-characts-list-item')
        #
        #         for row in rows_ua:
        #             title_cell = row.select_one('td.card-characts-list-item__title span.mistake-char-title')
        #             text_cell = row.select_one('td.card-characts-list-item__text')
        #
        #             if title_cell and text_cell:
        #                 title_text = title_cell.get_text().strip()
        #                 text_value = text_cell.get_text().strip()
        #                 csv_data_ua.append(title_text)
        #                 csv_data_ua.append(text_value)
        #     except:
        #         rows_ua = None
        #     values_ua.extend([link_product, name_product_ua, link_img, price_product, delivery_product])
        #     values_ua.extend(csv_data_ua)
        #
        # values_rus = []
        # for item in files_html_rus[:10]:
        #     with open(item, encoding="utf-8") as file:
        #         src = file.read()
        #     soup = BeautifulSoup(src, 'lxml')
        #     try:
        #         name_product_rus = soup.find('div', attrs={'class': 'card-title-box'}).find('h1').text.replace("\n", " ")
        #     except:
        #         name_product_rus = None
        #
        #     csv_data_rus = []
        #     try:
        #         rows_rus = soup.select('tr.card-characts-list-item')
        #
        #         for row in rows_rus:
        #             title_cell = row.select_one('td.card-characts-list-item__title span.mistake-char-title')
        #             text_cell = row.select_one('td.card-characts-list-item__text')
        #
        #             if title_cell and text_cell:
        #                 title_text = title_cell.get_text().strip()
        #                 text_value = text_cell.get_text().strip()
        #                 csv_data_rus.append(title_text)
        #                 csv_data_rus.append(text_value)
        #     except:
        #         rows = None
        #     values_rus.extend([name_product_rus])
        #     values_rus.extend(csv_data_rus)
        # values = values_ua[:2] + [values_rus[0]] + values_ua[2:] + values_rus[1:]
        # with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        #     writer = csv.writer(file, delimiter=";")
        #     writer.writerow(values)




if __name__ == '__main__':
    main()
