import os
import asyncio
import glob
import requests
from bs4 import BeautifulSoup
import csv
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}


def parsing_url_category_in_html():
    folder_path_data = "C:/Data_olekmotocykle/"

    files_data = glob.glob(folder_path_data + "*.html")

    for file_data in files_data:
        os.remove(file_data)
    folder_path_img = "C:/Data_olekmotocykle/img/"

    files_img = glob.glob(folder_path_img + "*.html")

    for file_img in files_img:
        os.remove(file_img)

    url = "https://shop.olekmotocykle.com/"
    response = requests.get(url, headers=header)  # , proxies=proxies
    url_ = 'https://shop.olekmotocykle.com/'
    category_product = []
    if response.content:
        soup = BeautifulSoup(response.content, 'lxml')

        for link in soup.select('.category-links-ui a'):
            href = link.get('href')
            if 'produkty/' in href:
                category_product.append(url_ + href)

        with open('category_product.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=";", lineterminator="\r")
            for item in category_product:
                writer.writerow([item])
    else:
        print("No content received")


def main_download_url():
    import main_url_asio
    asyncio.run(main_url_asio.main())


if __name__ == '__main__':
    print("Собираем категории товаров")
    parsing_url_category_in_html()
    print("Скачиваем все ссылки")
    main_download_url()
    print("Следующая обработка main_asio.py")
