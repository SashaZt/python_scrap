# import subprocess
import mysql.connector
#
# def dump_database(username, password, database_name, output_file):
#     dump_cmd = f"mysqldump -u {username} -p{password} {database_name} > {output_file}"
#     process = subprocess.Popen(dump_cmd, shell=True)
#     output, error = process.communicate()
#
# # Используйте параметры из mysql.connector для mysqldump
# username = 'python_mysql'
# password = 'python_mysql'
# database_name = 'kupypai_com'
# output_file = 'dump.sql'
#
# dump_database(username, password, database_name, output_file)


# import subprocess
# import os
#
# username = "python_mysql"
# password = "python_mysql"
# database_name = "kupypai_com"
#
# dumpcmd = '"c:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump" -u' + username + ' -p' + password + ' ' + database_name + ' > ' + os.getcwd() + "\\dump.sql"
# subprocess.call(dumpcmd, shell=True)

# import mysql.connector
#
# # Создание соединения
# cnx = mysql.connector.connect(
#     host="185.65.245.79",  # ваш хост, например "localhost"
#     user="python_mysql",  # ваше имя пользователя
#     password="4tz_{4!r%x8~E@W",  # ваш пароль
#     database="kupypai_com"  # имя вашей базы данных
# )
#
# # Создание объекта курсора
# cursor = cnx.cursor()
#
# # Подготовка запроса SQL
# query = "DELETE FROM ad WHERE id = %s"
#
# # Запрос на удаление
# cursor.execute(query, (851,))
#
# # Подтверждение изменений
# cnx.commit()
#
# # Закрытие соединения
# cnx.close()



# # 1. Подключаемся к серверу MySQL
# cnx = mysql.connector.connect(user='python_mysql', password='python_mysql', host='localhost', database='kupypai_com')
# # cnx = mysql.connector.connect(user='python_mysql', password='4tz_{4!r%x8~E@W', host='185.65.245.79', database='kupypai_com')
#
# # Создаем объект курсора, чтобы выполнять SQL-запросы
# cursor = cnx.cursor()
#
# # Указываем, что будем использовать эту базу данных
# cursor.execute("USE kupypai_com")
#
# # Добавляем новую колонку delta_time в таблицу my_table
# cursor.execute("ALTER TABLE ad MODIFY delta_time INT")
#
# cnx.commit()  # сохраняем изменения
# cnx.close()  # закрываем соединение
# Подключаемся к серверу MySQL
# cnx = mysql.connector.connect(user='python_mysql', password='python_mysql', host='localhost', database='kupypai_com')
cnx = mysql.connector.connect(user='python_mysql', password='4tz_{4!r%x8~E@W', host='185.65.245.79', database='kupypai_com')

# Создаем объект курсора, чтобы выполнять SQL-запросы
cursor = cnx.cursor()

# Указываем, что будем использовать эту базу данных
cursor.execute("USE kupypai_com")

# Изменяем тип колонки delta_time на INT
cursor.execute("ALTER TABLE ad MODIFY delta_time INT")

# Обновляем значение status_ad для записи с id = 830
cursor.execute("UPDATE ad SET status_ad = 'В процесі укладання угоди купівлі-продажу' WHERE id = 258")

# Делаем commit для сохранения изменений
cnx.commit()
