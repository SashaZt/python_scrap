import datetime
import lxml
import time
from bs4 import BeautifulSoup

# Библиотеки для Асинхронного парсинга
import asyncio
import aiohttp
import aiofiles
from aiocsv import AsyncWriter


async def get_page_data():
    start_time = datetime.datetime.now()
    async with aiohttp.ClientSession() as session:
        for page in range(1):
            url = f"https://shop.moderngroup.com/fleetguard/?sort=bestselling&page={page}"
            # group = url.split("/")[-2]
        header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
        response = await session.get(url=url, headers=header)
        soup = BeautifulSoup(await response.text(), 'lxml')
        table = soup.find('ul', attrs={'class': 'productGrid visible'}).find_all("li")
        url_product = []
        for item in table[0:20]:
            href = item.find('a').get("href")
            url_product.append(href)

        data = []
        for i in url_product:
            resp_url = await session.get(i, headers=header)
            soup = BeautifulSoup(await resp_url.text(), 'lxml')
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
            data.append(
                [product_name, product_sky, product_katalog, product_price, product_img]
            )
    async with aiofiles.open(f"C:\\scrap_tutorial-master\\moderngroup\\{product_katalog}.csv", "w",
                             errors='ignore') as file:
        writer = AsyncWriter(file, delimiter=";", lineterminator="\r")
        await writer.writerow(
            (
                'Название',
                'Каталожный номер',
                'Название группы',
                'Цена',
                'Ссылка на изображение'
            )
        )
        await writer.writerows(
            data
        )
    diff_time = datetime.datetime.now() - start_time
    print(diff_time)


async def main():
    await get_page_data()


if __name__ == '__main__':
    asyncio.run(main())
