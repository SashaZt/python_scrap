import csv
import datetime
from pathlib import Path
import mysql.connector
def create_sql():

    # 1. Подключаемся к серверу MySQL
    cnx = mysql.connector.connect(user='python_mysql', password='python_mysql', host='localhost')

    # Создаем объект курсора, чтобы выполнять SQL-запросы
    cursor = cnx.cursor()

    # 2. Создаем базу данных с именем kupypai_com
    cursor.execute("CREATE DATABASE weather")

    # Указываем, что будем использовать эту базу данных
    cursor.execute("USE weather")

    # 3. В базе данных создаем таблицу Zhytomyr
    # 4. Создаем необходимые колонки
    cursor.execute("""
    CREATE TABLE zhytomyr (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        time TIME,
        temp FLOAT
    )
    """)

    # Закрываем соединение
    cnx.close()
if __name__ == '__main__':
    create_sql()


name_files = Path(f'C:/scrap_tutorial-master/Погода/') / 'archive.csv'
with open(name_files, newline='', encoding='utf-8') as files:
    urls = list(csv.reader(files, delimiter=',', quotechar='|'))
    for row in urls[:10]:
        deta = row[0]
        formatted_datetime = datetime.datetime.strptime(deta, "%Y-%m-%dT%H:%M")
        formatted_date = formatted_datetime.date()
        formatted_time = formatted_datetime.time()
        temper = row[1]
        print(temper,formatted_date,formatted_time)