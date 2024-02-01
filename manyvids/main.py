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

from config import db_config, use_bd, use_table_daily_sales, use_table_monthly_sales, use_table_payout_history, headers
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


def get_google():
    spreadsheet_id = '145mee2ZsApZXiTnASng4lTzbocYCJWM5EDksTx_FVYY'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\scrap_tutorial-master\\manyvids\\access.json", scope)
    client = gspread.authorize(creds)
    return client, spreadsheet_id


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
                    mvtoken VARCHAR(255),
                    model_fm  VARCHAR(255)
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


def create_sql_payout_history():
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
                CREATE TABLE {use_table_payout_history} (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            model_id VARCHAR(255),
                            payment_date DATE,
                            paid VARCHAR(255)
                            )
                """)
    # """Добавить колонку в текущую БД"""
    # cursor.execute(f"""
    #     ALTER TABLE {use_table}
    #     ADD COLUMN Kod_części_zamiennej TEXT
    # """)
    # Закрываем соединение
    cnx.close()


"""Скачивание данных"""


def get_requests_daily_sales():
    proxi = proxy_random()
    filename_cookies = os.path.join(cookies_path, '*.json')
    files_json = glob.glob(filename_cookies)
    for item in files_json:
        with open(item, 'r') as f:
            cookies = json.load(f)
        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[1].replace('.json', '')
        # Создание сессии
        session = requests.Session()

        # Добавление кук в сессию
        for name, value in cookies.items():
            session.cookies.set(name, value)

        data = {
            'mvtoken': mvtoken,
            'day': '',
            'month': '1',
            'filterYear': '2024',
        }
        # proxy_host = '85.237.196.5'
        # proxy_port = 51523
        # proxy_user = 'locomgmt'
        # proxy_pass = 'ogzj4wAZnz'
        # proxi = {
        #     'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
        #     'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
        # }
        mvtoken_value = data['mvtoken']
        month_value = data['month']
        filterYear_value = data['filterYear']
        filename = os.path.join(daily_sales_path, f'{mvtoken_value}_{month_value}_{filterYear_value}.json')
        if not os.path.exists(filename):
            response = session.post('https://www.manyvids.com/includes/get_earnings.php', headers=headers,
                                    proxies=proxi, data=data)

            json_data = response.json()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


def get_requests_monthly_sales():
    proxi = proxy_random()
    filename_cookies = os.path.join(cookies_path, '*.json')
    files_json = glob.glob(filename_cookies)
    for item in files_json:
        with open(item, 'r') as f:
            cookies = json.load(f)
        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[1].replace('.json', '')
        session = requests.Session()

        # Добавление кук в сессию
        for name, value in cookies.items():
            session.cookies.set(name, value)

        data = {
            'mvtoken': mvtoken,
            'year': '2023',
        }

        response = session.post('https://www.manyvids.com/includes/get_earnings.php', headers=headers,
                                data=data, proxies=proxi)
        json_data = response.json()
        mvtoken_value = data['mvtoken']
        filterYear_value = data['year']
        filename = os.path.join(monthly_sales_path, f'{mvtoken_value}_{filterYear_value}.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


def get_requests_payout_history():
    proxi = proxy_random()
    filename_cookies = os.path.join(cookies_path, '*.json')
    files_json = glob.glob(filename_cookies)
    for item in files_json:
        with open(item, 'r') as f:
            cookies = json.load(f)
        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[1].replace('.json', '')
        session = requests.Session()

        # Добавление кук в сессию
        for name, value in cookies.items():
            session.cookies.set(name, value)

        data = {
            'mvtoken': mvtoken,
            'year': '2023',
        }
        mvtoken_value = data['mvtoken']
        filterYear_value = data['year']
        filename = os.path.join(payout_history_path, f'{mvtoken_value}_{filterYear_value}.json')
        if not os.path.exists(filename):
            response = session.post(
                'https://www.manyvids.com/includes/get_payperiod_earnings.php',
                headers=headers,
                data=data,
                proxies=proxi
            )

            json_data = response.json()

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


"""Загрузка данных в БД"""


def parsing_daily_sales():
    # Подключение к базе данных
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    folder = os.path.join(daily_sales_path, '*.json')
    files_json = glob.glob(folder)
    models_fms = get_id_models_csv()
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

                models_fm = [key for key, value in models_fms.items() if value == model_id]
                try:
                    model_fm = models_fm[0]
                except:
                    model_fm = None

                values = [buyer_username, buyer_stage_name, buyer_user_id, title, type_content, sales_date, sales_time,
                          seller_commission_price, model_id, mvtoken, model_fm]

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


def parsing_payout_history():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    folder = os.path.join(payout_history_path, '*.json')
    files_json = glob.glob(folder)
    id_models = get_id_models()
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
        try:
            payPeriodItems = data_json['payPeriodItems']
        except:
            continue
        for item in payPeriodItems:
            payment_date = item['end_period_date']
            paid = item['paid']
            values = [model_id, payment_date, paid]
            # print(values)

            # SQL-запрос для вставки данных
            insert_query = f"""
                            INSERT INTO {use_table_payout_history} (model_id, payment_date, paid)
                            VALUES (%s, %s, %s)
                            """
            cursor.execute(insert_query, values)
        cnx.commit()  # Подтверждение изменений
    cursor.close()
    cnx.close()


"""Формирование отчетов"""


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


def get_table_03_to_google():
    # Подключение к базе данных
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    cursor.execute("""
        SELECT model_id,  payment_date, paid FROM manyvids.payout_history
        ORDER BY model_id, payment_date;

    """)

    # Получение результатов в DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])
    pivot_df = df.pivot(index='model_id', columns='payment_date', values='paid')
    pivot_df.to_csv('payout_history.csv')

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()
    """Запись в Google Таблицу"""

    client, spreadsheet_id = get_google()
    sheet_payout_history = client.open_by_key(spreadsheet_id).worksheet('payout_history')

    # Читаем CSV файл
    df = pd.read_csv('payout_history.csv')
    df.fillna(0, inplace=True)
    df = df.astype(str)
    # Конвертируем DataFrame в список списков
    values = df.values.tolist()

    # Добавляем заголовки столбцов в начало списка
    values.insert(0, df.columns.tolist())

    # Очистка всего листа
    sheet_payout_history.clear()
    # Обновляем данные в Google Sheets
    sheet_payout_history.update(values, 'A1')


def get_table_04_to_google():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    cursor.execute("""
           SELECT 
    buyer_stage_name, 
    buyer_user_id, 
    ROUND(SUM(seller_commission_price), 2) AS total_commission, 
    COUNT(*) AS total_count, 
    ROUND(AVG(seller_commission_price), 2) AS average_commission,
    GROUP_CONCAT(DISTINCT model_fm SEPARATOR ', ') AS all_buyer_usernames
FROM manyvids.daily_sales
GROUP BY buyer_stage_name, buyer_user_id;



        """)

    # Получение результатов в DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])
    # Запись DataFrame в CSV файл
    df.to_csv('withdrawals.csv', index=False)
    """Запись в Google Таблицу"""

    client, spreadsheet_id = get_google()
    sheet_payout_history = client.open_by_key(spreadsheet_id).worksheet('clients')

    # Читаем CSV файл
    df = pd.read_csv('withdrawals.csv')
    df.fillna(0, inplace=True)
    df = df.astype(str)
    # Конвертируем DataFrame в список списков
    values = df.values.tolist()

    # Добавляем заголовки столбцов в начало списка
    values.insert(0, df.columns.tolist())

    # Очистка всего листа
    sheet_payout_history.clear()
    # Обновляем данные в Google Sheets
    sheet_payout_history.update(values, 'A1')


def get_to_google():
    proxi = proxy_random()
    import requests
    import json

    with open('cookies.json', 'r') as f:
        cookies = json.load(f)

    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Выполнение запроса с использованием сессии, кук, заголовков и прокси
    response = session.get('https://www.manyvids.com/View-my-earnings/', headers=headers, proxies=proxi)
    src = response.text

    # Сохранение ответа в файл
    filename = "cookies.html"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(src)


if __name__ == '__main__':
    # delete_old_data()
    # create_sql_daily_sales()
    # create_sql_monthly_sales()
    # create_sql_payout_history()
    # get_requests_daily_sales()
    # get_requests_monthly_sales()
    get_requests_payout_history()
    # parsing_daily_sales()
    # parsing_monthly_sales()
    # parsing_payout_history()
    # get_id_models()
    # get_table_01_to_google()
    # get_table_02_to_google()
    # get_table_03_to_google()
    # get_table_04_to_google()
    # get_to_google()
