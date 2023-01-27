import csv
import glob
import time

import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
# Нажатие клавиш
from selenium.webdriver.chrome.service import Service

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки

useragent = UserAgent()


def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()

    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')

    s = Service(
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    return driver


def save_link_all_product(url):
    driver = get_chromedriver(use_proxy=False,
                              user_agent=f"{useragent.random}")
    driver.get(url=url)
    driver.maximize_window()
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    time.sleep(1)
    with open("data.html", "w", encoding='utf-8') as file:
        file.write(driver.page_source)
    time.sleep(1)
    driver.close()
    driver.quit()


def pandas_html():
    html_data = pd.read_html('data.html')
    # for idx, table in enumerate(html_data):
    #     print(idx)
    #     print(table)
    # Сохраняем таблицу с характеристикам
    for i in range(1, len(html_data)):
        html_data[i].to_csv('data.csv', sep=';', mode="a", encoding='cp1251')


def get_items():
    with open(f"C:\\scrap_tutorial-master\\discord\\data.csv", "w", errors='ignore') as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\r")
        writer.writerow(
            (
                'Name', 'ID'

            )
        )
    targetPattern = "C:\\scrap_tutorial-master\\discord\\data\\*.html"
    files_html = glob.glob(targetPattern)
    for item in files_html:
        with open(item, encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")
        table = soup.find('table', attrs={'class': 'table serversList'})
        table_tbody = table.find('tbody')
        cart_table = table_tbody.find_all('tr', attrs={'class': 'tr'})
        for i in cart_table:
            name_card = i.find('a', attrs={'class': 'serverName'}).text
            id_card = i.find('span', attrs={'class': 'members'}).text
            print(item, ";", name_card, ";", id_card)

            # with open(f"C:\\scrap_tutorial-master\\ranker.com\\data.csv", "a", errors='ignore') as file:
            #     writer = csv.writer(file, delimiter=";", lineterminator="\r")
            #     writer.writerow(
            #         (
            #             name_card, id_card
            #
            #         )
            #     )


if __name__ == '__main__':
    # print("Вставьте ссылку")
    # url = input()
    # # # # # ##Сайт на который переходим
    # # # # # # url = "https://www.ranker.com/list/favorite-male-singers-of-all-time/music-lover?ref=browse_rerank&l=1"
    # # # # # # Запускаем первую функцию для сбора всех url на всех страницах
    # save_link_all_product('https://setevuha.ua/mikrotik-ccr1016-ccr1016-12g.html')
    pandas_html()
    # get_items()
    # parsing_product()
