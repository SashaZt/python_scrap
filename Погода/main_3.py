import csv
import datetime
from pathlib import Path

import mysql.connector


def create_sql():
    # 1. Подключаемся к серверу MySQL
    cnx = mysql.connector.connect(user='python_mysql', password='python_mysql', host='localhost')

    # Создаем объект курсора, чтобы выполнять SQL-запросы
    cursor = cnx.cursor()

    # # 2. Создаем базу данных с именем kupypai_com
    # cursor.execute("CREATE DATABASE weather")

    # Указываем, что будем использовать эту базу данных
    cursor.execute("USE weather")

    # 3. В базе данных создаем таблицу Zhytomyr
    # 4. Создаем необходимые колонки
    cursor.execute("""
    CREATE TABLE lutsk (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        time TIME,
        temp FLOAT
    )
    """)

    # Закрываем соединение
    cnx.close()


def updates_data():
    cnx = mysql.connector.connect(
        host="localhost",  # ваш хост, например "localhost"
        user="python_mysql",  # ваше имя пользователя
        password="python_mysql",  # ваш пароль
        database="weather"  # имя вашей базы данных
    )
    cursor = cnx.cursor()

    name_files = Path(f'/home/alex/PycharmProjects/scrap_tutorial-master/Погода/') / 'archive.csv'
    with open(name_files, newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=',', quotechar='|'))
        for row in urls:
            deta = row[0]
            formatted_datetime = datetime.datetime.strptime(deta, "%Y-%m-%dT%H:%M")
            formatted_date = formatted_datetime.date()
            formatted_time = formatted_datetime.time()
            temper = row[1]
            data = [formatted_date, formatted_time, temper]
            insert_query = """
                INSERT INTO zhytomyr (
                    date, time, temp
                ) VALUES (
                    %s, %s, %s
                )
            """

            cursor.execute(insert_query, data)
    cnx.commit()
    cnx.close()


def check_data_sql():
    cnx = mysql.connector.connect(
        host="localhost",  # ваш хост, например "localhost"
        user="python_mysql",  # ваше имя пользователя
        password="python_mysql",  # ваш пароль
        database="weather"  # имя вашей базы данных
    )
    cursor = cnx.cursor()

    # Пример запроса на выборку данных
    select_query = "SELECT * FROM zhytomyr"
    cursor.execute(select_query)

    # Получение результатов
    results = cursor.fetchall()

    # Вывод результатов
    for row in results:
        print(row)

    # Закрытие cursor и соединения
    cnx.commit()
    cnx.close()


if __name__ == '__main__':
    updates_data()
    check_data_sql()
