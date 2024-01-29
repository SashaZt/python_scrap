import json
import random
from datetime import datetime

import mysql.connector
import requests

from config import db_config, use_bd, use_table, headers
from proxi import proxies


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


def get_requests_daily_sales():
    proxi = proxy_random()
    cookies = {
        'KGID': 'vw81enngnq',
        'contentPopup': 'false',
        'fp_token_7c6a6574-f011-4c9a-abdd-9894a102ccef': 'oix6rQRGBtS6uFahjigPvPhEKbgJi3Tr5BC8yJsspR8=',
        '_hjSessionUser_665482': 'eyJpZCI6ImJkMWRiNzI1LWNhNzItNWNiNS1hYjlmLTA2ODU1MGE3ZTc4ZCIsImNyZWF0ZWQiOjE2OTg3NDg4Mjg5NDQsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga': 'GA1.1.1303883953.1698748820',
        'privacyPolicyRead': '1',
        '_gat': '1',
        'userPreferredContent': '1p2p3p',
        'dataSectionTemp': '0',
        'MSG_LEG_TKN': 'IS6Q61g8WwFJn9vjnRwKqA==',
        '_gat_UA-45103406-1': '1',
        '_hjSessionUser_665482': 'eyJpZCI6ImJkMWRiNzI1LWNhNzItNWNiNS1hYjlmLTA2ODU1MGE3ZTc4ZCIsImNyZWF0ZWQiOjE2OTg3NDg4Mjg5NDQsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga_K93D8HD50B': 'deleted',
        '_hjIncludedInSessionSample_665482': '0',
        'KGID': '28b938dd-8db9-57a6-b5d9-6d96c6b8af21',
        '_hjAbsoluteSessionInProgress': '0',
        '_hjDonePolls': '977734%2C977740',
        'timezone': 'Europe%2FAmsterdam',
        '_gid': 'GA1.2.79581497.1705419542',
        '_hjIncludedInSessionSample_665482': '0',
        'seenWarningPage': 'eyJpdiI6ImpycUVnWWxzWkRoZW1FZ0tBQlJPRlE9PSIsInZhbHVlIjoibXVlUnBHOGRmXC8renhublI0SWZHMUE9PSIsIm1hYyI6IjhmZWZhZjJkZTUwNGZkZGI2YzhlYWVjMWQwNTczZWM5YTEzZmYzOWU4N2E0YTU2ZjhhZDM4MDExYjZlOTBiZjMifQ%3D%3D',
        'API_KEY': 'FWfDdyNjdYgqDDr7b61HVUV%2Fec7fc3BuZRJ0zDzRQaZe15QDNnO3%2FlzV59AdirEm',
        'manyvh': 'th7WJdHKAwbYHEUUwWYGGaWfahAob0Lh0sem',
        'PHPSESSID': '63i286ueif1ikoe4aslol56cg24frvb3aelip72b',
        '_gid': 'GA1.1.79581497.1705419542',
        'mvAnnouncement': 'kVZfGcleqyVt',
        '_ga_K93D8HD50B': 'deleted',
        '_hjSession_665482': 'eyJpZCI6ImYxMmZhNTliLTczYzUtNDE4My05YzQzLWI5NjIzMzNmY2UxZCIsImMiOjE3MDY1Mzk5ODEyNDcsInMiOjAsInIiOjAsInNiIjoxLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        'XSRF-TOKEN': 'eyJpdiI6InBHVTBINzJGVjdZRGI4dyttSVdhbFE9PSIsInZhbHVlIjoiZEZkXC9Ma2lHMVFQMm9uYXRlaXEraXVMdEVxaU1DSGdTUUFCSVphTlwvd2VyMzRuVzBJajVxSEJsOFBtbmF1bFlLIiwibWFjIjoiMmRkOTNhOGFjYTg5YjQ2YjlmMzc4NWUxNTM3M2VjNWFjYjY1ZTYyYjMwNWM2Y2VmZjc5NjE3OGVjNjYwZjhkZiJ9',
        'AWSALB': 'xCR1IhfrFYrIK6C4YCrHAl5fz9HgPERtcHKUMyDBso61KiLvolWk0tZ5FoFw2UwUW5awuSbjq+DoR3PW3KPeBJ8NW0iOtopEkzOnF2ritFs2xjlIiNwkF3bW4+0cLTPlcBAV5ALfTUoxEpN9mZPVw8Ai9SEMkMhKQCqrQ9QLOtWp5lA+04JvGyHMqxS/fg==',
        'AWSALBCORS': 'xCR1IhfrFYrIK6C4YCrHAl5fz9HgPERtcHKUMyDBso61KiLvolWk0tZ5FoFw2UwUW5awuSbjq+DoR3PW3KPeBJ8NW0iOtopEkzOnF2ritFs2xjlIiNwkF3bW4+0cLTPlcBAV5ALfTUoxEpN9mZPVw8Ai9SEMkMhKQCqrQ9QLOtWp5lA+04JvGyHMqxS/fg==',
        '_ga': 'GA1.2.1303883953.1698748820',
        '_ga_K93D8HD50B': 'GS1.1.1706539974.2.1.1706541444.31.0.0',
        '_dd_s': 'logs=1&id=9c9c1aa6-5d06-470e-9872-a28131751e24&created=1706539901243&expire=1706542363950',
    }


    data = {
        'mvtoken': '65af8f4235331358595768',
        'day': '',
        'month': '11',
        'filterYear': '2023',
    }

    response = requests.post('https://www.manyvids.com/includes/get_earnings.php', cookies=cookies, headers=headers,
                             data=data, proxies=proxi)
    mvtoken_value = data['mvtoken']
    filename = f'{mvtoken_value}_daily_sales.json'
    json_data = response.json()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл

def get_requests_monthly_sales():
    proxi = proxy_random()
    cookies = {
        'KGID': 'vw81enngnq',
        'contentPopup': 'false',
        'fp_token_7c6a6574-f011-4c9a-abdd-9894a102ccef': 'oix6rQRGBtS6uFahjigPvPhEKbgJi3Tr5BC8yJsspR8=',
        '_hjSessionUser_665482': 'eyJpZCI6ImJkMWRiNzI1LWNhNzItNWNiNS1hYjlmLTA2ODU1MGE3ZTc4ZCIsImNyZWF0ZWQiOjE2OTg3NDg4Mjg5NDQsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga': 'GA1.1.1303883953.1698748820',
        'privacyPolicyRead': '1',
        '_gat': '1',
        'userPreferredContent': '1p2p3p',
        'dataSectionTemp': '0',
        'MSG_LEG_TKN': 'IS6Q61g8WwFJn9vjnRwKqA==',
        '_gat_UA-45103406-1': '1',
        '_hjSessionUser_665482': 'eyJpZCI6ImJkMWRiNzI1LWNhNzItNWNiNS1hYjlmLTA2ODU1MGE3ZTc4ZCIsImNyZWF0ZWQiOjE2OTg3NDg4Mjg5NDQsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga_K93D8HD50B': 'deleted',
        '_hjIncludedInSessionSample_665482': '0',
        'KGID': '28b938dd-8db9-57a6-b5d9-6d96c6b8af21',
        '_hjAbsoluteSessionInProgress': '0',
        '_hjDonePolls': '977734%2C977740',
        'timezone': 'Europe%2FAmsterdam',
        '_gid': 'GA1.2.79581497.1705419542',
        '_hjIncludedInSessionSample_665482': '0',
        'seenWarningPage': 'eyJpdiI6ImpycUVnWWxzWkRoZW1FZ0tBQlJPRlE9PSIsInZhbHVlIjoibXVlUnBHOGRmXC8renhublI0SWZHMUE9PSIsIm1hYyI6IjhmZWZhZjJkZTUwNGZkZGI2YzhlYWVjMWQwNTczZWM5YTEzZmYzOWU4N2E0YTU2ZjhhZDM4MDExYjZlOTBiZjMifQ%3D%3D',
        'API_KEY': 'FWfDdyNjdYgqDDr7b61HVUV%2Fec7fc3BuZRJ0zDzRQaZe15QDNnO3%2FlzV59AdirEm',
        'manyvh': 'th7WJdHKAwbYHEUUwWYGGaWfahAob0Lh0sem',
        'PHPSESSID': '63i286ueif1ikoe4aslol56cg24frvb3aelip72b',
        '_gid': 'GA1.1.79581497.1705419542',
        'mvAnnouncement': 'kVZfGcleqyVt',
        '_ga_K93D8HD50B': 'deleted',
        'XSRF-TOKEN': 'eyJpdiI6ImZcL2RMOTc0VDlXb0ZhK2hcL2IzeW1sUT09IiwidmFsdWUiOiJROVhMdVVVd1lJTnQ0ZXBSanRLNkdPWVVyZWhoWG45KzVkVCt3T0dqcHh5eFVjaWpZSWdlXC9xU3AzTXNYQUk3QSIsIm1hYyI6IjI3MGE0NWZkMzgwMTBmY2NiOWJhMzcyY2JjZDViMjI3OGNmOGNkMDJjYTQ4NWQ1MzNmOTNkOTZjNWQyMjI0OTkifQ%3D%3D',
        '_hjSession_665482': 'eyJpZCI6IjNmZDNkODMyLTU3ZWQtNDAzZS05Yjg1LTlkZGRlOTc0N2U2MCIsImMiOjE3MDY1NTc4NTc4MTAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        '_ga': 'GA1.2.1303883953.1698748820',
        '_ga_K93D8HD50B': 'GS1.1.1706557313.5.1.1706557985.52.0.0',
        'AWSALB': 'EPQtEkWseI4/v245Ywl86NAjtFUVH47mN7vohKdsnKmnC49LjLdNFD2y7ZusqeIMrx96eHN75VPacTw4Ua5I2JOGKvVpTDZ26HSzLnCvK7133rbDVOq2GcOcfHuwiDGB3CqzDeY7TRQogBQQqUc+QXJj78pJeJhS8pwxjlp/pE4zeI7+F63syEjTmrhJ/A==',
        'AWSALBCORS': 'EPQtEkWseI4/v245Ywl86NAjtFUVH47mN7vohKdsnKmnC49LjLdNFD2y7ZusqeIMrx96eHN75VPacTw4Ua5I2JOGKvVpTDZ26HSzLnCvK7133rbDVOq2GcOcfHuwiDGB3CqzDeY7TRQogBQQqUc+QXJj78pJeJhS8pwxjlp/pE4zeI7+F63syEjTmrhJ/A==',
        '_dd_s': 'logs=1&id=57a5760d-0b18-4b63-99fb-dcdbaee78db9&created=1706557313718&expire=1706558895825',
    }


    data = {
        'mvtoken': '65af8f4235331358595768',
        'year': '2023',
    }

    response = requests.post('https://www.manyvids.com/includes/get_earnings.php', cookies=cookies, headers=headers,
                             data=data, proxies=proxi)
    json_data = response.json()
    mvtoken_value = data['mvtoken']
    filename = f'{mvtoken_value}_monthly_sales.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл



def parsing_daily_sales():
    # Подключение к базе данных
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    filename = f'manyvids.json'
    with open(filename, 'r', encoding="utf-8") as f:
        data_json = json.load(f)

    dayItems = data_json['dayItems']
    buyer_username = dayItems[0]['buyer_username']

    try:
        for day in dayItems:
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
                      seller_commission_price, model_id]

            # SQL-запрос для вставки данных
            insert_query = f"""
            INSERT INTO {use_table} (buyer_username, buyer_stage_name, buyer_user_id, title, type_content, sales_date, sales_time, seller_commission_price, model_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, values)
            cnx.commit()  # Подтверждение изменений
            # print("Данные успешно добавлены.")

    except mysql.connector.Error as err:
        print("Ошибка при добавлении данных:", err)
    finally:
        # Закрытие соединения с базой данных
        cursor.close()
        cnx.close()

def parsing_monthly_sales():
    filename = f'65af8f4235331358595768_monthly_sales.json'
    with open(filename, 'r', encoding="utf-8") as f:
        data_json = json.load(f)
    monthItems = data_json['monthItems']
    for month in monthItems:
        type_content = month['type']
        sales_date = month['sales_date'].replace('/', '.')
        sales_date = datetime.strptime(sales_date, '%d.%m.%Y').strftime('%Y-%m-%d')
        seller_commission_price = month['seller_commission_price']
        values = [type_content, sales_date, seller_commission_price]
        print(values)

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
        CREATE TABLE {use_table} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    buyer_username VARCHAR(255),
                    buyer_stage_name VARCHAR(255),
                    buyer_user_id VARCHAR(255),
                    title VARCHAR(255),
                    type_content VARCHAR(255),
                    sales_date DATE,
                    sales_time TIME,
                    seller_commission_price VARCHAR(255),
                    model_id VARCHAR(255)
                    
    )
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
            CREATE TABLE {use_table} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        buyer_username VARCHAR(255),
                        buyer_stage_name VARCHAR(255),
                        buyer_user_id VARCHAR(255),
                        title VARCHAR(255),
                        type_content VARCHAR(255),
                        sales_date DATE,
                        sales_time TIME,
                        seller_commission_price VARCHAR(255),
                        model_id VARCHAR(255)

        )
            """)
    # """Добавить колонку в текущую БД"""
    # cursor.execute(f"""
    #     ALTER TABLE {use_table}
    #     ADD COLUMN Kod_części_zamiennej TEXT
    # """)
    # Закрываем соединение
    cnx.close()

if __name__ == '__main__':
    # create_sql_daily_sales()
    # create_sql_monthly_sales()
    # get_requests_daily_sales()
    # get_requests_monthly_sales()
    # parsing_daily_sales()
    # parsing_monthly_sales()
