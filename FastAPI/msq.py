from config import db_config, use_bd, use_table
import mysql.connector

def create_sql():

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
    cursor.execute("""
        CREATE TABLE copart (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url_lot VARCHAR(500),
            url_img_full VARCHAR(1000),
            url_img_high VARCHAR(1000),
            name_lot VARCHAR(255),
            lot_number INT,
            title_code VARCHAR(255),
            odometer FLOAT,
            `keys` VARCHAR(255), -- Используем обратные кавычки для ключевого слова "keys"
            transmission VARCHAR(255),
            price FLOAT,
            primary_damage VARCHAR(255),
            cylinders INT,
            body_style VARCHAR(255),
            drive VARCHAR(255),
            engine_type VARCHAR(255),
            vehicle_type VARCHAR(255),
            fuel VARCHAR(255),
            color VARCHAR(255),
            highlights VARCHAR(255),
            sale_status VARCHAR(255),
            current_bid FLOAT,
            sale_location VARCHAR(255),
            sale_date DATE,  -- Изменим на DATETIME, если нужно хранить и время
            last_updated DATE, -- Изменим на DATETIME, если нужно хранить и время
            parsing_date DATE  -- Изменим на DATETIME, если нужно хранить и время
        )
    """)

    # Закрываем соединение
    cnx.close()