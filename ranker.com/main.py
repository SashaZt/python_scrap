import urllib.request
from urllib.request import urlretrieve
from PIL import Image
import PIL
import re
import zipfile
import os
import json
import csv
import time
import requests
from bs4 import BeautifulSoup
import lxml
# Нажатие клавиш
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium import webdriver
import random
from fake_useragent import UserAgent

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    # for b in range(30):
    #     try:
    #         button_more_card= driver.find_element(By.XPATH,
    #                                           '//li[@class="listItem_main__8ll0k GridItem_main__33wgr listItem_hasRank__s5vh8 listItem_hasProps__tpE0W listItem_bigGrid__mSpkv GridItem_bigGrid__gcJMW listItem_showInfoIcon__2ZCb5"]//div[@class="container_innerContainer__ulE_r"]//span[text()="more"]').click()
    #     except:
    #         button_more_card = print('Not description')
    more_ = False
    while not more_:
        try:
            driver.find_element(By.XPATH, '//span[text() = "more"]').click()
            driver.execute_script("window.scrollBy(0,50)", "")
            time.sleep(1)

        except:
            break

    next_up = False
    while not next_up:
        try:
            driver.execute_script("window.scrollBy(0,200)", "")
            time.sleep(1)
            button_load_more = driver.find_element(By.XPATH,
                                                   '//button[@class="sc-81a1fbb4-0 copewu button_main__b1K6d button_large__mns0w button_tertiary__jtYJm button_isFullWidth__bQMs4 paginationButton_paginationButton__gTe3k"]').click()
            driver.execute_script("window.scrollBy(0,500)", "")




        except:
            break
    # load_more = True
    # while not load_more:
    #     try:
    #         # driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    #         button_load_more = driver.find_element(By.XPATH,'//button[@class="sc-81a1fbb4-0 copewu button_main__b1K6d button_large__mns0w button_tertiary__jtYJm button_isFullWidth__bQMs4 paginationButton_paginationButton__gTe3k"]')
    #         if button_load_more:
    #             button_load_more.click()
    #             time.sleep(1)
    #         else:
    #             button_load_more.click()
    #     except:
    #         load_more = True



    with open("C:\\scrap_tutorial-master\\ranker.com\\data.html", "w", encoding='utf-8') as file:
        file.write(driver.page_source)

    print("Скачал страницу")
    driver.close()
    driver.quit()
def get_items(file_path):
    with open(f"C:\\scrap_tutorial-master\\ranker.com\\data.csv", "w", errors='ignore') as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\r")
        writer.writerow(
            (
                'Name', 'Number', "Albums", "Labels", "description","description_2"

            )
        )
    with open(file_path, encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    table = soup.find('ul', attrs={'data-testid': 'list-item-ul'})
    # cart_table = table.find_all('li', attrs={'class': 'listItem_main__'})
    #Найти класс который содержит часть текста
    regex_cart = re.compile('listItem_main__.*')
    cart_table = table.find_all('li', attrs={'class': regex_cart})
    for i in cart_table:
        name_card = i.find('div', attrs={'class': 'NodeName_nameWrapper__n32Nb'}).text
        namber_card = i.find('div', attrs={'class': 'GridThumbnail_rankContainer__vE6_I GridThumbnail_hasImage__kNLG_ GridThumbnail_bigGrid__UiCVo'}).text
        regex_img = re.compile('Media_main__ex93e.*')
        if i.find('figure', attrs={'class': regex_img}).find('img').get("data-src"):
            img_card = i.find('figure', attrs={'class': regex_img}).find('img').get("data-src").replace("q=60&fit=crop&fm=pjpg&dpr=2&crop=faces&h=150&w=150", "q=100&fit=crop&fm=pjpg&dpr=2&crop=faces&h=250&w=250")
        else:
            img_card =i.find('figure', attrs={'class': regex_img}).find('img').get("src").replace("q=60&fit=crop&fm=pjpg&dpr=2&crop=faces&h=150&w=150", "q=100&fit=crop&fm=pjpg&dpr=2&crop=faces&h=250&w=250")
        #Выкачка фото
        img_data = requests.get(img_card)
        with open(
                f"C:\\scrap_tutorial-master\\ranker.com\\img\\{namber_card}.jpg",'wb') as file_img:
            file_img.write(img_data.content)
        try:
            albums_card = i.find('ul', attrs={'class': 'listItem_properties__sFwqE'}).find_all('li', attrs={'class': 'properties_item__STYON'})
        except:
            albums_card = "not alboms"
        try:
            Albums = albums_card[0].text
        except:
            Albums = "Not Albums"
        try:
            Labels = albums_card[1].text
        except:
            Labels = "Not Labels"
        try:
            dest_card = i.find('div', attrs={'class': 'container_container__53t32'}).text.replace("\n", "")
        except:
            dest_card = "Not description"
        try:
            dest_card_2 = i.find('div', attrs={'class': 'richText_container__p5dag listItem_itemDescription__jxHkE listItem_blather__v_A3E'}).find('span').text.replace("\n", "")
        except:
            dest_card_2 = "Not description"
        # print(img_card)

        with open(f"C:\\scrap_tutorial-master\\ranker.com\\data.csv", "a", errors='ignore') as file:
            writer = csv.writer(file, delimiter=";", lineterminator="\r")
            writer.writerow(
                (
                    name_card, namber_card, Albums, Labels, dest_card, dest_card_2

                )
            )



if __name__ == '__main__':
    # print("Вставьте ссылку")
    # url = input()
    # # # # # ##Сайт на который переходим
    # # # # # # url = "https://www.ranker.com/list/favorite-male-singers-of-all-time/music-lover?ref=browse_rerank&l=1"
    # # # # # # Запускаем первую функцию для сбора всех url на всех страницах
    save_link_all_product('https://www.ranker.com/list/hottest-asian-men/calistylie?ref=browse_ranking&l=1')
    get_items('C:\\scrap_tutorial-master\\ranker.com\\data.html')
    # parsing_product()

