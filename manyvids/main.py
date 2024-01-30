import glob
import json
import os
import random
from collections import defaultdict
from datetime import datetime

import gspread
import mysql.connector
import pandas as pd
import requests
from oauth2client.service_account import ServiceAccountCredentials

from config import db_config, use_bd, use_table_daily_sales, use_table_monthly_sales, headers
from proxi import proxies


def get_google():
    spreadsheet_id = '145mee2ZsApZXiTnASng4lTzbocYCJWM5EDksTx_FVYY'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\scrap_tutorial-master\\manyvids\\access.json", scope)
    client = gspread.authorize(creds)
    return client, spreadsheet_id


current_directory = os.getcwd()
temp_directory = 'temp'
# Создайте полный путь к папке temp
temp_path = os.path.join(current_directory, temp_directory)
daily_sales_path = os.path.join(temp_path, 'daily_sales')
monthly_sales_path = os.path.join(temp_path, 'monthly_sales')


def delete_old_data():
    # Убедитесь, что папки существуют или создайте их
    for folder in [temp_path, daily_sales_path, monthly_sales_path]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Удалите файлы из папок list и product
    for folder in [daily_sales_path, monthly_sales_path]:
        files = glob.glob(os.path.join(folder, '*'))
        for f in files:
            if os.path.isfile(f):
                os.remove(f)


def proxy_random():
    proxy = random.choice(proxies)
    proxy_host = proxy[0]
    proxy_port = proxy[1]
    proxy_user = proxy[2]
    proxy_pass = proxy[3]
    formatted_proxy = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    # Возвращаем словарь с прокси
    return {
        "http": formatted_proxy,
        "https": formatted_proxy
    }


"""Скачивание данных"""


def get_requests_daily_sales():
    proxi = proxy_random()
    cookies = {
        'KGID': 'o80cgt04fte',
        'userPreferredContent': '1p2p3p',
        'dataSectionTemp': '0',
        'contentPopup': 'false',
        'fp_token_7c6a6574-f011-4c9a-abdd-9894a102ccef': 'zqYNeuNq+n2916euUK3gXOFHg4G1WNhLPHLjgeszP+I=',
        '_hjSessionUser_665482': 'eyJpZCI6IjA3NjI1MWZmLWY5MDMtNThjYy04NjNmLTkwMjk5YTQwYzlkNyIsImNyZWF0ZWQiOjE2OTkyMDAxMDY1MDAsImV4aXN0aW5nIjp0cnVlfQ==',
        '_gat': '1',
        '_ga': 'GA1.1.2086640919.1699200083',
        'privacyPolicyRead': '1',
        'MSG_LEG_TKN': 'nIosQT4UW5EOiuumof3ONw==',
        'manyvh': 'bt6T3y7uGGOPmR086VFJyegqq0BsAwvwBJIi',
        '_gat_UA-45103406-1': '1',
        'timezone': 'Europe%2FAmsterdam',
        '_hjIncludedInSessionSample_665482': '0',
        'KGID': '2e3fcde2-6671-5bf6-896a-8743cecda114',
        '_ga_K93D8HD50B': 'deleted',
        '_hjSessionUser_665482': 'eyJpZCI6IjA3NjI1MWZmLWY5MDMtNThjYy04NjNmLTkwMjk5YTQwYzlkNyIsImNyZWF0ZWQiOjE2OTkyMDAxMDY1MDAsImV4aXN0aW5nIjp0cnVlfQ==',
        '_hjAbsoluteSessionInProgress': '1',
        '_hjIncludedInSessionSample_665482': '0',
        '_hjAbsoluteSessionInProgress': '1',
        '_gid': 'GA1.2.1554863151.1702850273',
        '_gid': 'GA1.1.1554863151.1702850273',
        '_ga_K93D8HD50B': 'deleted',
        'seenWarningPage': 'eyJpdiI6IjlHWVBpMEZ4NjAxSXFHV21MQ2dVY1E9PSIsInZhbHVlIjoidXNnQ0FFMmRJbTNRQktBTHlkdFNZUT09IiwibWFjIjoiNjllZGFiMmE1MmU2ZDRhZDZiOWE3NzM3M2I1YmY3YmE3NDg0MGFiOThmMWYzZjNjMjE4ZWQ2NDBlMTU4MWVlNSJ9',
        'API_KEY': 'EB1chmbGUzvVF%2Bbd0KzZGh3K2vnZBgSeNcIFkzDzsA%2B7gKI%2FEl%2BgOVSFVZzgHyLq',
        'preview': '0',
        'seenWarningPage': 'true',
        'PHPSESSID': 'nlvkp8c0fv168vuobkfhmjdvk4b3o3kjqal2fnrp',
        'mvAnnouncement': 'fGYXzXk7Iu58%3AJWyKCvZPRv1W',
        '_hjSession_665482': 'eyJpZCI6IjU0ZjMyODQ4LTYzZjAtNGNiOC1hNWQ1LTAzNWQ2ZjNhYzBlYyIsImMiOjE3MDY2MjI2Njk5ODgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        'XSRF-TOKEN': 'eyJpdiI6InpoNkduaUkrNkxcL0M2b0luTU1teStBPT0iLCJ2YWx1ZSI6Ikt6N1NqdmFzd0wwUXUxaXIrRVwvSjBEUGF3ODlybVwvUWg5Z0x5S0wrbUNuR3hvTUxiYnBsSk9jXC83dEY1eWpOajQiLCJtYWMiOiI5YmUwY2RlNzU3ODIzNDdkOWM4MTRkNzM3MjE1MDY1N2NiMjFhM2E5NjAxYWQyYWIyMDFhZTJkYzRkMjAyZWM1In0%3D',
        '_hjSession_665482': 'eyJpZCI6IjcxZjdlY2RhLWU5NzgtNGI0Ny1iYzFjLTAwZjA3NDI2MDkyOSIsImMiOjE3MDY2MzczNjAxNTYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
        'AWSALB': 'LsRiwKEH9Jf35c3WXS5M1/XiqxFzayJBkp+9Ijo4kg9FruONxl0eHLnAMZA9+lge6Vm/3tSjFWJz0MokajTR6ksMN46cB3blq9zCJOq20Pz6f4NmK8c0/SMgmemN3LL9OE713uEve4Ozem1RoTTvwxd0vbnAH8LJyZpq1y6+vymU0nbrJTNnqULpfVKFqw==',
        'AWSALBCORS': 'LsRiwKEH9Jf35c3WXS5M1/XiqxFzayJBkp+9Ijo4kg9FruONxl0eHLnAMZA9+lge6Vm/3tSjFWJz0MokajTR6ksMN46cB3blq9zCJOq20Pz6f4NmK8c0/SMgmemN3LL9OE713uEve4Ozem1RoTTvwxd0vbnAH8LJyZpq1y6+vymU0nbrJTNnqULpfVKFqw==',
        '_ga': 'GA1.2.2086640919.1699200083',
        '_ga_K93D8HD50B': 'GS1.1.1706637351.39.1.1706637380.31.0.0',
        '_dd_s': 'logs=1&id=3d2c7a36-ac92-42cf-bbea-0ccf1716eafc&created=1706637351457&expire=1706638283820',
    }

    data = {
        'mvtoken': '65b5d5a4977f5536834414',
        'day': '',
        'month': '11',
        'filterYear': '2023',
    }
    mvtoken_value = data['mvtoken']
    month_value = data['month']
    filterYear_value = data['filterYear']
    filename = os.path.join(daily_sales_path, f'{mvtoken_value}_{month_value}_{filterYear_value}.json')
    if not os.path.exists(filename):
        response = requests.post('https://www.manyvids.com/includes/get_earnings.php', cookies=cookies, headers=headers,
                                 data=data, proxies=proxi)

        json_data = response.json()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


def get_requests_monthly_sales():
    proxi = proxy_random()
    cookies = {
        'KGID': 'o80cgt04fte',
        'userPreferredContent': '1p2p3p',
        'dataSectionTemp': '0',
        'contentPopup': 'false',
        'fp_token_7c6a6574-f011-4c9a-abdd-9894a102ccef': 'zqYNeuNq+n2916euUK3gXOFHg4G1WNhLPHLjgeszP+I=',
        '_hjSessionUser_665482': 'eyJpZCI6IjA3NjI1MWZmLWY5MDMtNThjYy04NjNmLTkwMjk5YTQwYzlkNyIsImNyZWF0ZWQiOjE2OTkyMDAxMDY1MDAsImV4aXN0aW5nIjp0cnVlfQ==',
        '_gat': '1',
        '_ga': 'GA1.1.2086640919.1699200083',
        'privacyPolicyRead': '1',
        'MSG_LEG_TKN': 'nIosQT4UW5EOiuumof3ONw==',
        'manyvh': 'bt6T3y7uGGOPmR086VFJyegqq0BsAwvwBJIi',
        '_gat_UA-45103406-1': '1',
        'timezone': 'Europe%2FAmsterdam',
        '_hjIncludedInSessionSample_665482': '0',
        'KGID': '2e3fcde2-6671-5bf6-896a-8743cecda114',
        '_ga_K93D8HD50B': 'deleted',
        '_hjSessionUser_665482': 'eyJpZCI6IjA3NjI1MWZmLWY5MDMtNThjYy04NjNmLTkwMjk5YTQwYzlkNyIsImNyZWF0ZWQiOjE2OTkyMDAxMDY1MDAsImV4aXN0aW5nIjp0cnVlfQ==',
        '_hjAbsoluteSessionInProgress': '1',
        '_hjIncludedInSessionSample_665482': '0',
        '_hjAbsoluteSessionInProgress': '1',
        '_gid': 'GA1.2.1554863151.1702850273',
        '_gid': 'GA1.1.1554863151.1702850273',
        '_ga_K93D8HD50B': 'deleted',
        'seenWarningPage': 'eyJpdiI6IjlHWVBpMEZ4NjAxSXFHV21MQ2dVY1E9PSIsInZhbHVlIjoidXNnQ0FFMmRJbTNRQktBTHlkdFNZUT09IiwibWFjIjoiNjllZGFiMmE1MmU2ZDRhZDZiOWE3NzM3M2I1YmY3YmE3NDg0MGFiOThmMWYzZjNjMjE4ZWQ2NDBlMTU4MWVlNSJ9',
        'API_KEY': 'EB1chmbGUzvVF%2Bbd0KzZGh3K2vnZBgSeNcIFkzDzsA%2B7gKI%2FEl%2BgOVSFVZzgHyLq',
        'preview': '0',
        'seenWarningPage': 'true',
        'PHPSESSID': 'nlvkp8c0fv168vuobkfhmjdvk4b3o3kjqal2fnrp',
        'mvAnnouncement': 'fGYXzXk7Iu58%3AJWyKCvZPRv1W',
        '_hjSession_665482': 'eyJpZCI6IjU0ZjMyODQ4LTYzZjAtNGNiOC1hNWQ1LTAzNWQ2ZjNhYzBlYyIsImMiOjE3MDY2MjI2Njk5ODgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        'XSRF-TOKEN': 'eyJpdiI6InpoNkduaUkrNkxcL0M2b0luTU1teStBPT0iLCJ2YWx1ZSI6Ikt6N1NqdmFzd0wwUXUxaXIrRVwvSjBEUGF3ODlybVwvUWg5Z0x5S0wrbUNuR3hvTUxiYnBsSk9jXC83dEY1eWpOajQiLCJtYWMiOiI5YmUwY2RlNzU3ODIzNDdkOWM4MTRkNzM3MjE1MDY1N2NiMjFhM2E5NjAxYWQyYWIyMDFhZTJkYzRkMjAyZWM1In0%3D',
        '_ga': 'GA1.2.2086640919.1699200083',
        '_hjSession_665482': 'eyJpZCI6IjU0ZjMyODQ4LTYzZjAtNGNiOC1hNWQ1LTAzNWQ2ZjNhYzBlYyIsImMiOjE3MDY2MjI2Njk5ODgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        '_ga_K93D8HD50B': 'GS1.1.1706647640.40.0.1706647640.60.0.0',
        'AWSALB': 'KCEKBpQjqQUHOsP3Lhw2lrtT5ti0VcjcIkzsS1KWaEtGF5JrFmgr1RiToZDfL41bDZxxwm7gzHUGsrIdP6Rsq2XmEgjLb8Np1vK5aIxaBRfJ1/Pvm6qcsUeq3uiqp6tLDmReaRYqtrVkKWFKrsfYfDYOTHPmJjRL0YnCdCeIU0y9NDApb5JUfmQlqNGn3A==',
        'AWSALBCORS': 'KCEKBpQjqQUHOsP3Lhw2lrtT5ti0VcjcIkzsS1KWaEtGF5JrFmgr1RiToZDfL41bDZxxwm7gzHUGsrIdP6Rsq2XmEgjLb8Np1vK5aIxaBRfJ1/Pvm6qcsUeq3uiqp6tLDmReaRYqtrVkKWFKrsfYfDYOTHPmJjRL0YnCdCeIU0y9NDApb5JUfmQlqNGn3A==',
        '_dd_s': 'logs=1&id=f0c3e95f-ee2b-4222-83bb-ec06804681ec&created=1706647640602&expire=1706648544705',
    }

    data = {
        'mvtoken': '65b5d5a4977f5536834414',
        'year': '2024',
    }

    response = requests.post('https://www.manyvids.com/includes/get_earnings.php', cookies=cookies, headers=headers,
                             data=data, proxies=proxi)
    json_data = response.json()
    mvtoken_value = data['mvtoken']
    filterYear_value = data['year']
    filename = os.path.join(monthly_sales_path, f'{mvtoken_value}_{filterYear_value}.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


"""Загрузка данных в БД"""


def parsing_daily_sales():
    # Подключение к базе данных
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    folder = os.path.join(daily_sales_path, '*.json')
    files_json = glob.glob(folder)

    for item in files_json:
        with open(item, 'r', encoding="utf-8") as f:
            data_json = json.load(f)

        dayItems = data_json['dayItems']
        try:
            buyer_username = dayItems[0]['buyer_username']
        except IndexError:

            print(f"dayItems пустой в файле {item}.")
            continue

        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[0]

        for day in dayItems:
            try:
                buyer_stage_name = day['buyer_stage_name']
                buyer_user_id = day['buyer_user_id']
                title = day['title']
                type_content = day['type']
                sales_date = day['sales_date'].replace('/', '.')
                sales_date = datetime.strptime(sales_date, '%d.%m.%Y').strftime('%Y-%m-%d')
                sales_time = day['sales_time']
                seller_commission_price = day['seller_commission_price']
                model_id = day['model_id']
                values = [buyer_username, buyer_stage_name, buyer_user_id, title, type_content, sales_date, sales_time,
                          seller_commission_price, model_id, mvtoken]

                # SQL-запрос для вставки данных
                insert_query = f"""
                INSERT INTO {use_table_daily_sales} (buyer_username, buyer_stage_name, buyer_user_id, title, type_content, sales_date, sales_time,
                          seller_commission_price, model_id, mvtoken)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, values)
                cnx.commit()  # Подтверждение изменений

            except mysql.connector.Error as err:
                print("Ошибка при добавлении данных:", err)
                break  # Прерываем цикл в случае ошибки

    # Закрытие соединения с базой данных
    cursor.close()
    cnx.close()


def parsing_monthly_sales():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    # Инициализация словаря для хранения сумм по месяцам
    monthly_sums = defaultdict(float)

    # Получение словаря id_models
    id_models = get_id_models()

    folder = os.path.join(monthly_sales_path, '*.json')
    files_json = glob.glob(folder)

    for item in files_json:
        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[0]

        # Ищем, какому ключу соответствует mvtoken
        models_id = [key for key, value in id_models.items() if value == mvtoken]
        try:
            model_id = models_id[0]
        except:
            model_id = None
        with open(item, 'r', encoding="utf-8") as f:
            data_json = json.load(f)

        monthItems = data_json['monthItems']

        for month in monthItems:
            sales_date = month['sales_date'].replace('/', '.')
            sales_date = datetime.strptime(sales_date, '%d.%m.%Y')
            sales_month = sales_date.month
            sales_year = sales_date.year

            seller_commission_price = float(month['seller_commission_price'])

            # Формирование ключа в формате "(model_id, Месяц Год)"
            # month_year = sales_date.strftime("%b %Y")
            key = (model_id, sales_month, sales_year)
            monthly_sums[key] += seller_commission_price

        # Вывод суммы по каждой модели и месяцу

    for (model_id, sales_month, sales_year), total_sum in monthly_sums.items():
        formatted_total_sum = "{:.2f}".format(total_sum)
        values = [model_id, sales_month, sales_year, formatted_total_sum]
        # SQL-запрос для вставки данных
        insert_query = f"""
                        INSERT INTO {use_table_monthly_sales} (model_id, sales_month,sales_year, total_sum)
                        VALUES (%s,%s, %s, %s)
                        """
        cursor.execute(insert_query, values)
        cnx.commit()  # Подтверждение изменений


"""Создание БД"""


def create_sql_daily_sales():
    # 1. Подключаемся к серверу MySQL
    cnx = mysql.connector.connect(**db_config)

    # Создаем объект курсора, чтобы выполнять SQL-запросы
    cursor = cnx.cursor()

    # 2. Создаем базу данных с именем kupypai_com
    # cursor.execute("CREATE DATABASE vpromo2_usa")

    # Указываем, что будем использовать эту базу данных
    cursor.execute(f"USE {use_bd}")

    # 3. В базе данных создаем таблицу ad
    # 4. Создаем необходимые колонки

    cursor.execute(f"""
        CREATE TABLE {use_table_daily_sales} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    buyer_username VARCHAR(255),
                    model_id VARCHAR(255),
                    buyer_stage_name VARCHAR(255),
                    buyer_user_id VARCHAR(255),
                    title VARCHAR(255),
                    type_content VARCHAR(255),
                    sales_date DATE,
                    sales_time TIME,
                    seller_commission_price VARCHAR(255),
                    mvtoken VARCHAR(255)    )
        """)
    # """Добавить колонку в текущую БД"""
    # cursor.execute(f"""
    #     ALTER TABLE {use_table}
    #     ADD COLUMN Kod_części_zamiennej TEXT
    # """)
    # Закрываем соединение
    cnx.close()


def create_sql_monthly_sales():
    # 1. Подключаемся к серверу MySQL
    cnx = mysql.connector.connect(**db_config)

    # Создаем объект курсора, чтобы выполнять SQL-запросы
    cursor = cnx.cursor()

    # 2. Создаем базу данных с именем kupypai_com
    # cursor.execute("CREATE DATABASE vpromo2_usa")

    # Указываем, что будем использовать эту базу данных
    cursor.execute(f"USE {use_bd}")

    # 3. В базе данных создаем таблицу ad
    # 4. Создаем необходимые колонки

    cursor.execute(f"""
            CREATE TABLE {use_table_monthly_sales} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        model_id VARCHAR(255),
                        sales_month INT,
                        sales_year INT,
                        total_sum VARCHAR(255)
                        )
            """)
    # """Добавить колонку в текущую БД"""
    # cursor.execute(f"""
    #     ALTER TABLE {use_table}
    #     ADD COLUMN Kod_części_zamiennej TEXT
    # """)
    # Закрываем соединение
    cnx.close()


"""Формирование отчетов"""


def get_id_models():
    # Подключение к базе данных
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Выполнение запроса для получения уникальных значений
    cursor.execute("SELECT DISTINCT model_id, mvtoken FROM manyvids.daily_sales")

    dict_models = {}
    # Получение и вывод результатов
    results = cursor.fetchall()
    for row in results:
        model_id, mvtoken = row
        dict_models[model_id] = mvtoken
    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()
    return dict_models


def get_table_01_to_google():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    cursor.execute("""
        SELECT model_id, sales_date, ROUND(SUM(seller_commission_price), 2) AS total_seller_commission
        FROM manyvids.daily_sales
        GROUP BY model_id, sales_date
        ORDER BY model_id ASC, sales_date ASC
    """)

    # Получение результатов в DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])

    # Преобразование DataFrame
    pivot_df = df.pivot_table(index='model_id', columns='sales_date', values='total_seller_commission', fill_value=0)

    # Сохранение в CSV
    pivot_df.to_csv('daily_sales.csv')

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()

    """Запись в Google Таблицу"""
    client, spreadsheet_id = get_google()
    sheet01 = client.open_by_key(spreadsheet_id).get_worksheet(0)  # Первый лист в книге daily_sales

    # Читаем CSV файл
    df = pd.read_csv('daily_sales.csv')

    # Конвертируем DataFrame в список списков
    values = df.values.tolist()

    # Добавляем заголовки столбцов в начало списка
    values.insert(0, df.columns.tolist())

    # Очистка всего листа
    sheet01.clear()
    # Обновляем данные в Google Sheets
    sheet01.update(values, 'A1')


def get_table_02_to_google():
    # Подключение к базе данных
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    cursor.execute("""
        SELECT model_id, sales_month,sales_year,total_sum FROM manyvids.monthly_sales
        ORDER BY model_id, sales_year, sales_month;

    """)

    # Получение результатов в DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])
    df['sales_month'] = df['sales_month'].astype(int)
    # df['sales_year'] = df['sales_year'].astype(str)
    # df['month_year'] = pd.to_datetime(df['sales_month'] + '.' + df['sales_year'], format='%m.%Y')
    df['total_sum'] = pd.to_numeric(df['total_sum'])
    # # Создание сводной таблицы
    pivot_df = df.pivot_table(index='model_id', columns='sales_month', values='total_sum', fill_value=0)
    #
    # # Вывод результата
    #
    # # Сохранение в CSV
    pivot_df.to_csv('monthly_sales.csv')

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()
    """Запись в Google Таблицу"""
    client, spreadsheet_id = get_google()
    df = pd.read_csv('monthly_sales.csv')
    columns_to_check = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]  # Список колонок для проверки

    for col in columns_to_check:
        if col in df.columns:
            # Определяем индекс листа на основе номера колонки
            sheet_index = int(col) if col.isdigit() else 0
            sheet = client.open_by_key(spreadsheet_id).get_worksheet(sheet_index)

            # Выбираем только колонки 'model_id' и текущую колонку
            df_subset = df[['model_id', col]]

            # Преобразуем DataFrame в список списков и вставляем заголовки колонок
            values = [df_subset.columns.tolist()] + df_subset.values.tolist()

            # Очищаем лист и записываем данные
            sheet.clear()
            sheet.update(values, 'A1')
    # # Проверяем наличие колонки с названием "1" и выбираем соответствующий лист
    # if "1" in df.columns:
    #     sheet02 = client.open_by_key(spreadsheet_id).get_worksheet(1)  # Первый лист для daily_sales
    #     # Выбираем только колонки 'model_id' и '1'
    #     df_subset = df[['model_id', '1']]
    #     # Преобразуем DataFrame в список списков и вставляем заголовки колонок
    #     values = [df_subset.columns.tolist()] + df_subset.values.tolist()
    #
    #     # Очищаем лист и записываем данные
    #     sheet02.clear()
    #     sheet02.update(values, 'A1')
    # if "11" in df.columns:
    #     sheet11 = client.open_by_key(spreadsheet_id).get_worksheet(11)  # Первый лист для daily_sales
    #     # Выбираем только колонки 'model_id' и '1'
    #     df_subset = df[['model_id', '11']]
    #     # Преобразуем DataFrame в список списков и вставляем заголовки колонок
    #     values = [df_subset.columns.tolist()] + df_subset.values.tolist()
    #
    #     # Очищаем лист и записываем данные
    #     sheet11.clear()
    #     sheet11.update(values, 'A1')
    # if "12" in df.columns:
    #     sheet12 = client.open_by_key(spreadsheet_id).get_worksheet(12)  # Первый лист для daily_sales
    #     # Выбираем только колонки 'model_id' и '1'
    #     df_subset = df[['model_id', '12']]
    #     # Преобразуем DataFrame в список списков и вставляем заголовки колонок
    #     values = [df_subset.columns.tolist()] + df_subset.values.tolist()
    #
    #     # Очищаем лист и записываем данные
    #     sheet12.clear()
    #     sheet12.update(values, 'A1')

    # client, spreadsheet_id = get_google()
    #
    # sheet = client.open_by_key(spreadsheet_id).sheet1  # Первый лист в книге daily_sales
    #
    # # Читаем CSV файл
    # df = pd.read_csv('daily_sales.csv')
    #
    # # Конвертируем DataFrame в список списков
    # values = df.values.tolist()
    #
    # # Добавляем заголовки столбцов в начало списка
    # values.insert(0, df.columns.tolist())
    # # Очистка всего листа
    #
    # sheet.clear()
    # # Обновляем данные в Google Sheets
    # sheet.update(values, 'A1')


def get_to_google():
    spreadsheet_id = '145mee2ZsApZXiTnASng4lTzbocYCJWM5EDksTx_FVYY'
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\scrap_tutorial-master\\manyvids\\access.json", scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.sheet1
    sheet.update_cell(1, 1, "Привет, мир!")


if __name__ == '__main__':
    # delete_old_data()
    # create_sql_daily_sales()
    # create_sql_monthly_sales()
    # get_requests_daily_sales()
    # get_requests_monthly_sales()
    # parsing_daily_sales()
    # parsing_monthly_sales()
    # get_id_models()
    # get_table_01_to_google()
    get_table_02_to_google()
    # get_to_google()
