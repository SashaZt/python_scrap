import os
import pickle
import json
import csv
import re
import time
import requests
from bs4 import BeautifulSoup
import lxml
# Нажатие клавиш
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


from selenium import webdriver
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
    time.sleep(60)
    # Блок работы с куками-----------------------------------------
    # Создание куки
    pickle.dump(driver.get_cookies(), open("cookies", "wb"))
    time.sleep(5)
    # Читание куки
    # for cookie in pickle.load(open("cookies", "rb")):
    #     driver.add_cookie(cookie)
    # Блок работы с куками-----------------------------------------

    # try:
    #     actions = ActionChains(driver)
    #     actions.move_to_element(driver.find_element(By.XPATH, '//span[text()="Human Challenge требует проверки. Нажмите и удерживайте кнопку до окончания проверки"]')).perform()
    #     actions.click_and_hold(driver.find_element(By.XPATH, '//span[text()="Human Challenge требует проверки. Нажмите и удерживайте кнопку до окончания проверки"]'))
    #     time.sleep(10)
    #     actions.release()
    # except:
    #     print('!')
    # try:
    #     driver.find_element(By.XPATH, '//span[text()="Log In"]').click()
    # except:
    #     print("Not LogIn")
    # try:
    #     driver.find_element(By.XPATH, '//input[@data-placeholder="E-mail Address"]').send_keys('a.zinchyk83@gmail.com')
    # except:
    #     print('Not E-mail')


    driver.close()
    driver.quit()
def get_items(file_path):
    pass


if __name__ == '__main__':
    # print("Вставьте ссылку")
    # url = input()
    # # # # # ##Сайт на который переходим
    # # # # # # url = "https://www.ranker.com/list/favorite-male-singers-of-all-time/music-lover?ref=browse_rerank&l=1"
    # # # # # # Запускаем первую функцию для сбора всех url на всех страницах
    save_link_all_product('https://www.crunchbase.com')
    # get_items('C:\\scrap_tutorial-master\\ranker.com\\data.html')
    # parsing_product()

