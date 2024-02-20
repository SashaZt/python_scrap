import sqlite3


def crative_sql_bd():
    # Подключение к базе данных (файлу). Если файла нет, он будет создан.
    conn = sqlite3.connect('prozorro.db')
    c = conn.cursor()

    # Создание таблицы tender
    c.execute(
        """CREATE TABLE IF NOT EXISTS tender (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Автоинкрементный ID
            tender_id TEXT UNIQUE,                 -- Уникальный ID тендера
            customer TEXT,                         -- Заказчик
            status_tender TEXT,                    -- Статус тендера
            date_auction TEXT,                     -- Дата аукциона
            time_auction TEXT,                     -- Время аукциона
            date_enquiryPeriod TEXT,               -- Звернення за роз’ясненнями дата
            time_enquiryPeriod TEXT,               -- Звернення за роз’ясненнями время
            date_auctionPeriod_auctionPeriod TEXT, -- Кінцевий строк подання тендерних пропозицій дата
            time_auctionPeriod_auctionPeriod TEXT, -- Кінцевий строк подання тендерних пропозицій время
            award_name_customer TEXT,              -- Победитель
            award_value_customer TEXT,             -- Ставка которая победила
            date_pending TEXT,                     -- Дата победившей ставки
            time_pending TEXT,                     -- Время победившей ставки
            guarantee_amount TEXT,                 -- Розмір надання забезпечення пропозицій учасників
            bank_garantiy TEXT,                    -- забезпечення виконання договору
            award_value TEXT,                      -- Пропозиція переможця
            award_name TEXT                        -- Имя переможця 
            )"""
)


    # Сохранение (коммит) изменений
    conn.commit()

    # Закрытие соединения
    conn.close()


if __name__ == '__main__':
    crative_sql_bd()
