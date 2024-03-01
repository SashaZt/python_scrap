import json
import os
import random
from io import BytesIO
import time
import requests
from PIL import Image
from bs4 import BeautifulSoup

from config import cookies, headers, time_a, time_b

current_directory = os.getcwd()
image_directory = 'image'
image_path = os.path.join(current_directory, image_directory)


def get_img():
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    with open('list.csv', encoding='utf-8') as file:
        # Проходим по каждой строке файла
        for line in file:
            # Убираем пробельные символы в начале и конце строки, например, перевод строки
            line = line.strip()
            # Разделяем строку на части по символу ";"
            parts = line.split(';')
            # Первая часть - это name, вторая часть - это url
            name, url = parts
            response = requests.get(url, cookies=cookies, headers=headers)
            src = response.text
            soup = BeautifulSoup(src, 'lxml')
            scripts_json = soup.find_all('script', type="application/ld+json")
            for script in scripts_json:
                try:
                    # Преобразуем текст скрипта в словарь
                    data = json.loads(script.text)

                    # Проверяем, есть ли ключ 'image'
                    if 'image' in data:
                        url_image = data['image']
                        # Загрузка изображения
                        filename = os.path.join(image_directory, f"{name}.jpeg")
                        if not os.path.exists(filename):
                            response = requests.get(url_image)
                            if response.status_code == 200:

                                # Открываем изображение из памяти
                                image = Image.open(BytesIO(response.content))

                                # Конвертируем в JPEG
                                # Для сохранения в JPEG, изображение должно быть в режиме RGB
                                if image.mode != 'RGB':
                                    image = image.convert('RGB')
                                image.save(filename, "JPEG")
                                sleep_time = random.randint(time_a, time_b)
                                time.sleep(sleep_time)
                except:
                    continue


if __name__ == '__main__':
    get_img()
