import datetime
import json
import csv
import os
import pickle
import lxml
import time
from random import randint
import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import random
from fake_useragent import UserAgent
# Библиотеки для Асинхронного парсинга
import asyncio
import aiohttp
# Библиотеки для Асинхронного парсинга

start_time = datetime.datetime.now()
table_product = []
url_product = []
async def get_page_data(session, page) :

    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    url = f"https://shop.moderngroup.com/fleetguard/?sort=bestselling&page={page}"
    async with session.get(url=url, headers=header) as response:
        resp = await response.text()
        soup = BeautifulSoup(resp, 'lxml')
        table = soup.find('ul', attrs={'class': 'productGrid visible'}).find_all("li")

        for item in table[0:20]:
            href = item.find('a').get("href")
            url_product.append(href)

        for i in url_product:
            resp_url = requests.get(i, headers=header)
            soup = BeautifulSoup(resp_url.text, 'lxml')
            try:
                product_name = soup.find('div', attrs={'class': 'productView-product'}).find("h1").text
            except:
                product_name = "Нет названия"
            try:
                product_sky = soup.find('dl', attrs={'class': "productView-info"}).find('dd', attrs={
                    'class': "productView-info-value"}).text
            except:
                product_sky = "Нет кода"
            try:
                product_katalog = soup.find('h2', attrs={'class': 'productView-brand'}).find("span").text
            except:
                product_katalog = "Нет каталога"
            try:
                product_price = soup.find('div', attrs={'class': 'productView-price'}).find('span', attrs={
                    'class': 'price price--withoutTax'}).text
            except:
                product_price = "Нет цены"
            try:
                product_img = soup.find('figure', attrs={'class': 'productView-image fancy-gallery'}).get("href")
            except:
                product_img = "нет изображения"
            table_product.append(
                {
                    "product_name": product_name,
                    "product_sky": product_sky,
                    "product_katalog": product_katalog,
                    "product_price": product_price,
                    "product_img": product_img
                }
            )







async def gather_data():
    url = "https://shop.moderngroup.com/fleetguard/?sort=bestselling"
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(10):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())

    url = f"https://shop.moderngroup.com/fleetguard/?sort=bestselling"
    group = url.split("/")[-2]
    with open(f"C:\\scrap_tutorial-master\\moderngroup\\{group}.csv", "w", errors='ignore') as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\r")
        writer.writerow(
            (
                'Название',
                'Каталожный номер',
                'Название группы',
                'Цена',
                'Ссылка на изображение'
            )
        )
    for product in table_product:
        with open(f"C:\\scrap_tutorial-master\\moderngroup\\{group}.csv", "a", errors='ignore') as file:
            writer = csv.writer(file, delimiter=";", lineterminator="\r")
            writer.writerow(
                (
                    product["product_name"],
                    product["product_sky"],
                    product["product_katalog"],
                    product["product_price"],
                    product["product_img"]
                )
            )

    diff_time = datetime.datetime.now() - start_time
    print(diff_time)
if __name__ == '__main__':
    main()
