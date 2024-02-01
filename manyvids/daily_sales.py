import csv
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

from config import db_config, use_bd, use_table_daily_sales, use_table_monthly_sales, use_table_payout_history, \
    use_table_login_pass, headers
from proxi import proxies
import glob
import json
import os
import random
from datetime import datetime
import schedule
import time
from datetime import datetime, timedelta

import mysql.connector
import requests

from config import db_config, use_table_daily_sales, headers
from proxi import proxies

current_directory = os.getcwd()
temp_directory = 'temp'
# Создайте полный путь к папке temp
temp_path = os.path.join(current_directory, temp_directory)
cookies_path = os.path.join(temp_path, 'cookies')
login_pass_path = os.path.join(temp_path, 'login_pass')
daily_sales_path = os.path.join(temp_path, 'daily_sales')
monthly_sales_path = os.path.join(temp_path, 'monthly_sales')
payout_history_path = os.path.join(temp_path, 'payout_history')


def get_id_models_csv():
    model_dict = {}

    # Открываем файл
    with open('model_id.csv', mode='r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')  # Используем точку с запятой как разделитель
        for row in reader:
            key = row[0]
            value = row[1]
            model_dict[key] = value

    # Теперь model_dict содержит данные из CSV
    return model_dict

def get_google():
    spreadsheet_id = '145mee2ZsApZXiTnASng4lTzbocYCJWM5EDksTx_FVYY'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\scrap_tutorial-master\\manyvids\\access.json", scope)
    client = gspread.authorize(creds)
    return client, spreadsheet_id

def get_id_models():
    # Подключение к базе данных
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Выполнение запроса для получения уникальных значений
    cursor.execute("SELECT DISTINCT model_fm, mvtoken FROM manyvids.daily_sales")

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


def get_requests(month, filterYear):
    # def get_requests():
    proxi = proxy_random()
    filename_cookies = os.path.join(cookies_path, '*.json')
    files_json = glob.glob(filename_cookies)
    for item in files_json:

        with open(item, 'r') as f:
            cookies_list = json.load(f)

        # # Заполнение словаря cookies

        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}

        session = requests.Session()
        session.cookies.update(cookies_dict)
        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[1].replace('.json', '')
        data = {
            'mvtoken': mvtoken,
            'day': '',
            'month': month,
            'filterYear': filterYear,
        }

        mvtoken_value = data['mvtoken']
        month_value = data['month']
        filterYear_value = data['filterYear']
        filename = os.path.join(daily_sales_path, f'{mvtoken_value}_{month_value}_{filterYear_value}.json')
        if not os.path.exists(filename):
            response = requests.post('https://www.manyvids.com/includes/get_earnings.php', headers=headers,
                                     proxies=proxi, data=data, cookies=cookies_dict)

            json_data = response.json()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
            print(f'Сохранился {mvtoken_value}_{month_value}_{filterYear_value}.json')
            print('Пауза 10сек')
            time.sleep(10)

def get_sql_data():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    cursor.execute("""
        SELECT buyer_user_id, sales_date, sales_time, seller_commission_price FROM manyvids.daily_sales;
    """)
    data = {(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()}
    cursor.close()
    cnx.close()
    return data
def get_sql():
    # Получение данных из SQL
    sql_data = get_sql_data()

    # Подключение к базе данных
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()


    # # Очистка таблицы перед вставкой новых данных
    # truncate_query = f"TRUNCATE TABLE {use_table_daily_sales}"
    # cursor.execute(truncate_query)
    # cnx.commit()  # Подтверждение изменений

    folder = os.path.join(daily_sales_path, '*.json')
    files_json = glob.glob(folder)
    models_fms = get_id_models_csv()

    # # Очистка таблицы перед вставкой новых данных
    # truncate_query = f"TRUNCATE TABLE {use_table_daily_sales}"
    # cursor.execute(truncate_query)
    # cnx.commit()  # Подтверждение изменений

    for item in files_json:
        with open(item, 'r', encoding="utf-8") as f:
            data_json = json.load(f)

        try:
            dayItems = data_json['dayItems']
        except:
            continue
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

                models_fm = [key for key, value in models_fms.items() if value == model_id]
                try:
                    model_fm = models_fm[0]
                except:
                    model_fm = None

                values = [buyer_username, buyer_stage_name, buyer_user_id, title, type_content, sales_date,
                          sales_time,
                          seller_commission_price, model_id, mvtoken, model_fm]

                json_sales_date_converted = datetime.strptime(sales_date, '%Y-%m-%d').date()

                # Преобразование времени в timedelta
                hours, minutes = map(int, sales_time.split(':'))
                json_sales_time_converted = timedelta(hours=hours, minutes=minutes)

                # Преобразование цены в строку (если это необходимо)
                json_seller_commission_price_converted = str(seller_commission_price)

                # Теперь данные из JSON имеют формат, схожий с данными из SQL
                json_data_tuple = (buyer_user_id, json_sales_date_converted, json_sales_time_converted,
                                   json_seller_commission_price_converted)
                if json_data_tuple in sql_data:
                    continue
                else:
                    # print("Новые данные, нужно добавить в SQL")

                    # SQL-запрос для вставки данных
                    insert_query = f"""
                    INSERT INTO {use_table_daily_sales} (buyer_username, buyer_stage_name, buyer_user_id, title, type_content, sales_date, sales_time,
                              seller_commission_price, model_id, mvtoken,model_fm)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, values)
                    cnx.commit()  # Подтверждение изменений

            except mysql.connector.Error as err:
                print("Ошибка при добавлении данных:", err)
                break  # Прерываем цикл в случае ошибки

    # Закрытие соединения с базой данных
    cursor.close()
    cnx.close()

def get_table_01_to_google():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    cursor.execute("""
        SELECT model_fm, sales_date, ROUND(SUM(seller_commission_price), 2) AS total_seller_commission
        FROM manyvids.daily_sales
        GROUP BY model_fm, sales_date
        ORDER BY model_fm ASC, sales_date ASC
    """)

    # Получение результатов в DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])

    # Преобразование DataFrame
    pivot_df = df.pivot_table(index='model_fm', columns='sales_date', values='total_seller_commission', fill_value=0)

    # Сохранение в CSV
    pivot_df.to_csv('daily_sales.csv')

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()

    """Запись в Google Таблицу"""
    client, spreadsheet_id = get_google()
    sheet_daily_sales = client.open_by_key(spreadsheet_id).worksheet('daily_sales')
    # Читаем CSV файл
    df = pd.read_csv('daily_sales.csv')

    # Конвертируем DataFrame в список списков
    values = df.values.tolist()

    # Добавляем заголовки столбцов в начало списка
    values.insert(0, df.columns.tolist())

    # Очистка всего листа
    sheet_daily_sales.clear()
    # Обновляем данные в Google Sheets
    sheet_daily_sales.update(values, 'A1')
    # Получаем список всех файлов в папке
    files = glob.glob(os.path.join(daily_sales_path, '*'))
    # Удаляем каждый файл
    for f in files:
        if os.path.isfile(f):
            os.remove(f)

def job():
    # Получение текущего месяца и года
    now = datetime.now()
    month = str(now.month)
    filterYear = str(now.year)

    print(f"Запуск задачи для месяца {month} и года {filterYear}.")
    get_requests(month, filterYear)
    get_sql()
    get_table_01_to_google()

# Настройка расписания
schedule.every().hour.at(":59").do(job)  # Запуск каждый час в 00 минут

while True:
    schedule.run_pending()
    time.sleep(1)

# #
# if __name__ == '__main__':
#     # print("Какой месяц парсим от 1 до 12?")
#     # month = input()
#     # print("Какой год парсим? в формате 2024")
#     # filterYear = input()
#     get_requests(month, filterYear)
#     get_sql()
#     get_table_01_to_google()
