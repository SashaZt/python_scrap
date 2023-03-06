import mysql.connector
import csv

# Установить соединение с базой данных
db = mysql.connector.connect(
  host="localhost",
  user="python_mysql",
  password="<julfY19",
  database="intercars"
)

# Создать объект курсора для выполнения запросов к базе данных
cursor = db.cursor()

# Выполнить запрос
cursor.execute("SELECT sku, brand FROM intercars.ax_product_no_image;")

# Получить результаты запроса
results = cursor.fetchall()

# запись результатов запроса в CSV файл

# for row in results[:1]:
#     print(row[0].replace(',', '_'), row[1].replace(',', '_'))


with open('C:\\scrap_tutorial-master\\webshop-ua.intercars.eu\\csv\\output.csv', mode='w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file, quotechar='|')
    for row in results:
        writer.writerow(row)


# Закрыть соединение с базой данных
db.close()