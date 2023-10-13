import boto3

# Установка учетных данных AWS
ACCESS_KEY = 'AKIAQWBRT2HZZFWLS5EJ'
SECRET_KEY = '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'

# Создание клиента S3
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Отправка файла на S3 бакет
bucket_name = 'probaloket'
file_path = r'C:\\salomon_pl\\data_img\\img_kids\\LG3725$_6.webp'
destination_filename = 'LG3725$_6.webp'

s3.upload_file(file_path, bucket_name, destination_filename)


import os
import boto3
import requests

# Установка учетных данных AWS
ACCESS_KEY = 'AKIAQWBRT2HZZFWLS5EJ'
SECRET_KEY = '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'

# Создание клиента S3
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Настройка параметров
bucket_name = 'имя_вашего_бакета'
img_group_folder = 'папка_группы_изображений'
id_product = 'идентификатор_продукта'
coun = 'номер_изображения'
img_url = 'URL_изображения'

# Формирование путей к файлам
file_path = f"{img_group_folder}/{id_product}_{coun}.webp"
new_file_path = f"c:\\adidas_pl\\csv_data\\{img_group_folder}\\{id_product}_{coun}.webp"

# Проверка наличия файла в S3 бакете
try:
    s3.head_object(Bucket=bucket_name, Key=file_path)
    print(f"Файл {file_path} уже существует в S3 бакете. Пропуск загрузки.")
except:
    # Загрузка файла из удаленного источника
    print(f"Файл {file_path} отсутствует в S3 бакете. Загрузка из удаленного источника.")
    img_data = requests.get(img_url, headers=header, proxies=proxies)
    with open(new_file_path, 'wb') as file_img:
        file_img.write(img_data.content)

    # Загрузка файла в S3 бакет
    s3.upload_file(new_file_path, bucket_name, file_path)
    print(f"Файл {file_path} успешно загружен в S3 бакет.")