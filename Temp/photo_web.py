import csv
import os
import time

import requests

# имя CSV-файла
csv_filename = "products.csv"

# создаем папку photos, если ее еще нет
if not os.path.exists("photos"):
    os.makedirs("photos")

# открываем CSV-файл и читаем его построчно
with open(csv_filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        # получаем идентификатор продукта и его название
        product_id = row[0]
        product_name = row[1]

        # получаем ссылки на фотографии
        photo_urls = [url for url in row[2:] if url]
        # print(f"Total number of photo URLs for product {product_id}: {len(photo_urls)}")

        # для каждой ссылки скачиваем фотографию и сохраняем ее в папку photos
        for i, url in enumerate(photo_urls):
            if not url.startswith("http"):
                url = "https://" + url

            # получаем имя файла из ссылки на фото
            filename = f"{product_id}_{product_name}_{i + 1:02d}.jpg"

            # проверяем, существует ли файл в папке photos
            if os.path.exists(f"photos/{filename}"):
                print(f"File {filename} already exists, skipping")
                continue

            response = requests.get(url)
            if response.ok:
                with open(f"photos/{filename}", "wb") as f:
                    f.write(response.content)
                print(f"Скачан {product_id} и пауза 1 сек")
                time.sleep(1)
            else:
                print(f"Failed to download image from {url}")
