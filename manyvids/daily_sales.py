import csv
import datetime
import glob
import json
import os
import random
import time
from datetime import datetime, timedelta
import numpy as np
import gspread
import mysql.connector
import pandas as pd
import requests
import schedule
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from config import db_config, use_table_daily_sales, headers, host, user, password, database, use_table_payout_history,use_table_monthly_sales
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
pending_custom_path = os.path.join(temp_path, 'pending_custom')


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
        data_day = {
            'mvtoken': mvtoken,
            'day': '',
            'month': month,
            'filterYear': filterYear,
        }
        # data_month = {
        #     'mvtoken': mvtoken,
        #     'year': filterYear,
        # }
        data_payout_history = {
            'mvtoken': mvtoken,
            'year': filterYear,
        }

        mvtoken_value = data_day['mvtoken']
        month_value = data_day['month']
        filterYear_value = data_day['filterYear']
        """День"""
        filename_day = os.path.join(daily_sales_path, f'{mvtoken_value}_{month_value}_{filterYear_value}.json')
        response_day = session.post('https://www.manyvids.com/includes/get_earnings.php', headers=headers,
                                    proxies=proxi, data=data_day)  # , cookies=cookies_dict
        json_data_day = response_day.json()
        with open(filename_day, 'w', encoding='utf-8') as f:
            json.dump(json_data_day, f, ensure_ascii=False, indent=4)  # Записываем в файл

        """История"""
        filename_payout_history = os.path.join(payout_history_path, f'{mvtoken_value}_{filterYear_value}.json')
        if not os.path.exists(filename_payout_history):
            time.sleep(5)
            response_payout_history = session.post('https://www.manyvids.com/includes/get_payperiod_earnings.php',
                                                   headers=headers, data=data_payout_history, proxies=proxi
                                                   )
            json_data_payout_history = response_payout_history.json()
            with open(filename_payout_history, 'w', encoding='utf-8') as f:
                json.dump(json_data_payout_history, f, ensure_ascii=False, indent=4)

        """pending"""
        filename_pending_custom = os.path.join(pending_custom_path, f'{mvtoken_value}_{filterYear_value}.html')

        time.sleep(5)
        response_pending_custom = session.get('https://www.manyvids.com/View-my-earnings/', headers=headers)
        src_pending_custom = response_pending_custom.text
        with open(filename_pending_custom, "w", encoding='utf-8') as file:
            file.write(src_pending_custom)

        # filename_month = os.path.join(monthly_sales_path, f'{mvtoken_value}_{filterYear_value}.json')

        # if not os.path.exists(filename_month):
        #     time.sleep(5)
        #     response_month = session.post('https://www.manyvids.com/includes/get_earnings.php', headers=headers,
        #                                   data=data_month, proxies=proxi)
        #     json_data_month = response_month.json()
        #     with open(filename_month, 'w', encoding='utf-8') as f:
        #         json.dump(json_data_month, f, ensure_ascii=False, indent=4)  # Записываем в файл

        print('Пауза 10сек')
        time.sleep(10)


def get_sql_data_data_day():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    cursor.execute("""
        SELECT buyer_user_id, sales_date, sales_time, seller_commission_price FROM manyvids.daily_sales;
    """)
    data = {(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()}
    cursor.close()
    cnx.close()
    return data



def get_sql_data_payout_history():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    cursor.execute("""
        SELECT model_id,payment_date,paid  FROM manyvids.payout_history;
    """)
    data = {(row[0], row[1], row[2]) for row in cursor.fetchall()}
    cursor.close()
    cnx.close()
    return data


def get_sql_data_day():
    # Получение данных из SQL
    sql_data = get_sql_data_data_day()

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


def parsing_monthly_sales_in_daily():
    # Подключение к базе данных и выполнение запроса
    # cnx = mysql.connector.connect(**db_config)
    database_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"

    # Создание движка SQLAlchemy
    engine = create_engine(database_uri)

    # Выполнение запроса и чтение данных в DataFrame
    query = """
            SELECT model_fm,
                EXTRACT(YEAR FROM sales_date) AS year, 
                EXTRACT(MONTH FROM sales_date) AS month, 
                ROUND(SUM(seller_commission_price), 2) AS total_seller_commission
            FROM 
                manyvids.daily_sales
            GROUP BY 
                model_fm, year, month
            ORDER BY 
                model_fm ASC, year ASC, month ASC;
        """
    df = pd.read_sql_query(query, engine)

    # Создание сводной таблицы
    pivot_df = df.pivot_table(index='model_fm', columns='month', values='total_seller_commission', fill_value=0)

    # Округление значений до двух знаков после запятой
    pivot_df = pivot_df.round(2)

    pivot_df.to_csv('monthly_sales.csv')
    engine.dispose()

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
            df_subset = df[['model_fm', col]]

            # Преобразуем DataFrame в список списков и вставляем заголовки колонок
            values = [df_subset.columns.tolist()] + df_subset.values.tolist()

            # Очищаем лист и записываем данные
            sheet.clear()
            sheet.update(values, 'A1')

def get_pending_to_google():
    spreadsheet_id = '145mee2ZsApZXiTnASng4lTzbocYCJWM5EDksTx_FVYY'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\scrap_tutorial-master\\manyvids\\access.json", scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    database_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"

    # Создание движка SQLAlchemy
    engine = create_engine(database_uri)
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    cursor.execute("""
                  SELECT model_fm,
                EXTRACT(YEAR FROM sales_date) AS year,
                EXTRACT(MONTH FROM sales_date) AS month,
                ROUND(SUM(seller_commission_price), 2) AS total_seller_commission
            FROM
                manyvids.daily_sales
            GROUP BY
                model_fm, year, month
            ORDER BY
                model_fm ASC, year ASC, month ASC;




                """)
    # Получение результатов в DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])
    # Запись DataFrame в CSV файл
    df.to_csv('monthly_sales.csv', index=False)
    # Чтение CSV файла
    df = pd.read_csv('monthly_sales.csv')

    # Переименование столбцов в DataFrame для соответствия таблице в БД
    df.rename(columns={
        'model_fm': 'model_id',
        'year': 'sales_year',
        'month': 'sales_month',  # Убедитесь, что названия столбцов соответствуют вашему CSV файлу
        'total_seller_commission': 'total_sum'
    }, inplace=True)

    # # Создание строки подключения
    # connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'

    # Создание движка SQLAlchemy

    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()


    # Очистка таблицы перед вставкой новых данных
    truncate_query = f"TRUNCATE TABLE {use_table_monthly_sales}"
    cursor.execute(truncate_query)
    cnx.commit()  # Подтверждение изменений
    cursor.close()
    cnx.close()

    # Запись DataFrame в таблицу MySQL
    df.to_sql(name='monthly_sales', con=engine, if_exists='append', index=False)
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    now = datetime.now()  # Текущие дата и время
    month = str(now.month)
    clear_pending_query = """
            UPDATE manyvids.monthly_sales
            SET pending_custom = NULL
            WHERE sales_month != %s;
        """
    cursor.execute(clear_pending_query, (month,))
    cnx.commit()
    id_models = get_id_models()
    folder = os.path.join(pending_custom_path, '*.html')

    files_html = glob.glob(folder)
    for item in files_html:
        filename = os.path.basename(item)
        parts = filename.split("_")
        mvtoken = parts[0]
        # Ищем, какому ключу соответствует mvtoken
        models_id = [key for key, value in id_models.items() if value == mvtoken]
        try:
            model_id = models_id[0]
        except:
            model_id = None
        with open(item, encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        custom_vids_body = soup.find_all('div', id="customVidsBody")
        for c in custom_vids_body:
            # Извлекаем все строки таблицы внутри найденного div
            rows = c.find_all('tr')

            # Проходимся по каждой строке и извлекаем содержимое шестой ячейки с элементом strong
            for row in rows:
                # Предполагая, что каждая строка содержит как минимум 6 ячеек
                if len(row.find_all('td')) >= 6:
                    strong_tag = row.find_all('td')[5].find(
                        'strong')  # Индексация начинается с 0, поэтому шестая ячейка это индекс 5
                    if strong_tag:
                        pending = strong_tag.get_text(strip=True).replace('$', '')
                        values = [model_id, month, pending]
                        # Убедитесь, что 'pending' преобразуется в числовой формат, если колонка 'pending_custom' ожидает число
                        try:
                            pending_value = float(pending)
                            # Подготовка и выполнение SQL запроса на обновление
                            update_query = """
                                                    UPDATE manyvids.monthly_sales
                                                    SET pending_custom = %s
                                                    WHERE model_id = %s AND sales_month = %s;
                                                """
                            cursor.execute(update_query, (pending_value, model_id, month))
                            cnx.commit()
                        except ValueError:
                            print(
                                f"Невозможно преобразовать '{pending}' в число для model_id {model_id} и месяца {month}.")
                    else:
                        print("Strong tag not found in the 6th cell")
    """Запись в Google Таблицу"""
    # Подключение к базе данных и выполнение запроса
    # cnx = mysql.connector.connect(**db_config)
    # database_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"



    # Выполнение запроса и чтение данных в DataFrame
    query = """
        SELECT model_id, sales_month, total_sum, pending_custom FROM manyvids.monthly_sales;
    """
    df = pd.read_sql_query(query, engine)

    # Преобразование DataFrame
    df_pivot = df.pivot_table(index='model_id',
                              columns='sales_month',
                              values=['total_sum', 'pending_custom'],
                              aggfunc='first').reset_index()

    df_pivot.columns = ['_'.join(str(i) for i in col).strip() for col in df_pivot.columns.values]

    # Вывод преобразованного DataFrame для проверки
    # Запись в CSV
    csv_file_path = 'pending_custom.csv'
    df_pivot.to_csv(csv_file_path, index=False)

    # # Создание сводной таблицы
    # pivot_df = df.pivot_table(index='model_id', columns='sales_month', values='total_sum', fill_value=0)
    #
    # # Округление значений до двух знаков после запятой
    # pivot_df = pivot_df.round(2)
    #
    # pivot_df.to_csv('monthly_sales.csv')


    """Запись в Google Таблицу"""
    # client, spreadsheet = get_google()
    df = pd.read_csv('pending_custom.csv')
    # Список месяцев для проверки
    months = range(1, 13)  # От 1 до 12
    for month in months:
        sheet_name = f'{month:02}_monthly_sales'

        # Подготовка данных для записи
        columns = ['model_id_']
        data_columns = []

        # Добавляем колонки в список, если они существуют в DataFrame
        pending_custom_col = f'pending_custom_{month}'
        total_sum_col = f'total_sum_{month}'
        if pending_custom_col in df.columns:
            columns.append(pending_custom_col)
            data_columns.append(pending_custom_col)
        if total_sum_col in df.columns:
            columns.append(total_sum_col)
            data_columns.append(total_sum_col)

        # Если нет ни одной из специфичных колонок для месяца, пропускаем итерацию
        if not data_columns:
            continue

        df_subset = df[columns].copy()
        df_subset.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

        # Получаем или создаем лист для текущего месяца
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")

        values = [df_subset.columns.tolist()] + df_subset.values.tolist()

        worksheet.clear()
        worksheet.update(values,'A1')
    engine.dispose()
def get_sql_payout_history():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # # Очистка таблицы перед вставкой новых данных
    # truncate_query = f"TRUNCATE TABLE {use_table_payout_history}"
    # cursor.execute(truncate_query)
    # cnx.commit()  # Подтверждение изменений

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

    sql_data = get_sql_data_payout_history()

    # Подключение к базе данных
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
            json_sales_date_converted = datetime.strptime(payment_date, '%Y-%m-%d').date()
            json_seller_commission_price_converted = str(paid)
            json_data_tuple = (model_id, json_sales_date_converted, json_seller_commission_price_converted)
            if json_data_tuple in sql_data:
                continue
            else:
                # SQL-запрос для вставки данных
                insert_query = f"""
                                            INSERT INTO {use_table_payout_history} (model_id, payment_date, paid)
                                            VALUES (%s, %s, %s)
                                            """
                cursor.execute(insert_query, values)
            cnx.commit()  # Подтверждение изменений
    cursor.close()
    cnx.close()

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
FROM 
    manyvids.daily_sales
GROUP BY 
    buyer_stage_name, 
    buyer_user_id
ORDER BY 
    total_commission DESC;




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
def job():
    now = datetime.now()  # Текущие дата и время
    month = str(now.month)
    filterYear = str(now.year)
    currentTime = now.strftime("%H:%M:%S")  # Форматирование текущего времени

    print(f"[{currentTime}] Запуск задачи для месяца {month} и года {filterYear}.")

    # Ваши функции здесь
    get_requests(month, filterYear)
    get_sql_data_day()
    get_table_01_to_google()
    get_sql_payout_history()
    get_table_04_to_google()
    get_pending_to_google()
    print(f'Все выполнено, ждем 30мин')


# Вызов функции для немедленного выполнения задачи при запуске скрипта
job()

# Настройка расписания
# schedule.every().hour.at(":25").do(job)  # Запуск каждый час в 00 минут
# Настройка расписания на выполнение каждые 30 минут
schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

# if __name__ == '__main__':
#     print("Какой месяц парсим от 1 до 12?")
#     month = input()
#     print("Какой год парсим? в формате 2024")
#     filterYear = input()
#     get_requests(month, filterYear)
#     get_sql_data_day()
#     get_table_01_to_google()
