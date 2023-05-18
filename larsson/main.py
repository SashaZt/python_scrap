import os
import pickle
import time
import pandas as pd
import glob
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv

def get_undetected_chromedriver(use_proxy=False, user_agent=None):
    # Обход защиты
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')

    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument('--headless')
    """Проба"""
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-setuid-sandbox")


    driver = undetected_chromedriver.Chrome()

    return driver


def main_category():
    url = 'https://mike.larsson.pl/pl/'
    driver = get_undetected_chromedriver()
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)
    wait = WebDriverWait(driver, 60)
    button_art_wait = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
    login = driver.find_element(By.NAME, 'username')
    login.send_keys('088087')
    passsss = driver.find_element(By.NAME, 'password')
    passsss.send_keys('jdtvy61')
    passsss.send_keys(Keys.RETURN)
    time.sleep(2)
    try:
        magaz_button = driver.find_element(By.XPATH, '//a[@class="btn btn-primary mr-xs mb-sm btn-lg"]').click()
    except:
        print("")
    try:
        chebox_wait = driver.find_element(By.XPATH, '//span[@class="checkmark "]').click()
        akcetpr_cooki = driver.find_element(By.XPATH, '//div[@class="btnAcceptAll"]').click()
    except:
        print('')
    time.sleep(5)
    with open(f"category.html", "w", encoding='utf-8') as file:
        file.write(driver.page_source)
    driver.close()
    driver.quit()

def get_url_category():
    category_product = []
    with open("category.html", encoding="utf-8") as file:
        src_ru = file.read()
    soup = BeautifulSoup(src_ru, 'lxml')
    # создаем список необходимых значений атрибута num
    num_list = [103, 107, 105, 102, 101, 104, 108, 204, 205, 120, 121]

    # ищем все теги a с атрибутом num
    a_tags = soup.find_all('a', attrs={'num': re.compile('|'.join(map(str, num_list)))})

    # извлекаем значения href из найденных тегов a
    href_list = [a.get('href') for a in a_tags]
    with open('category_product.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\r")
        for href in href_list:
            writer.writerow([href])

def get_url_product():
    driver = get_undetected_chromedriver()

    with open(f'category_product.csv', newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        for url in urls[:1]:
            categoty = url[0].split("/")[-2]

            driver.maximize_window()
            driver.get(url[0])
            time.sleep(2)
            wait = WebDriverWait(driver, 60)
            button_art_wait = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
            login = driver.find_element(By.NAME, 'username')
            login.send_keys('088087')
            passsss = driver.find_element(By.NAME, 'password')
            passsss.send_keys('jdtvy61')
            passsss.send_keys(Keys.RETURN)
            time.sleep(2)
            try:
                magaz_button = driver.find_element(By.XPATH, '//a[@class="btn btn-primary mr-xs mb-sm btn-lg"]').click()
            except:
                print("")
            try:
                chebox_wait = driver.find_element(By.XPATH, '//span[@class="checkmark "]').click()
                akcetpr_cooki = driver.find_element(By.XPATH, '//div[@class="btnAcceptAll"]').click()
            except:
                print('')
            time.sleep(1)
            driver.get(url[0])
            time.sleep(5)
            with open(f"categoty/{categoty}.html", "w", encoding='utf-8') as file:
                file.write(driver.page_source)
        driver.close()
        driver.quit()
def get_to_category():
    url_start = "https://www.larsson.pl/"
    driver = get_undetected_chromedriver()
    driver.maximize_window()
    driver.get(url_start)
    time.sleep(2)
    wait = WebDriverWait(driver, 60)
    button_art_wait = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
    login = driver.find_element(By.NAME, 'username')
    login.send_keys('088087')
    passsss = driver.find_element(By.NAME, 'password')
    passsss.send_keys('jdtvy61')
    passsss.send_keys(Keys.RETURN)
    time.sleep(2)
    try:
        magaz_button = driver.find_element(By.XPATH, '//a[@class="btn btn-primary mr-xs mb-sm btn-lg"]').click()
    except:
        print("")
    try:
        chebox_wait = driver.find_element(By.XPATH, '//span[@class="checkmark "]').click()
        akcetpr_cooki = driver.find_element(By.XPATH, '//div[@class="btnAcceptAll"]').click()
    except:
        print('')
    time.sleep(1)
    with open(f'C:\\scrap_tutorial-master\\larsson\\category_product.csv', newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        for url in urls:
            driver.get(url[0])
            time.sleep(1)
            group = url[0].split('/')[-2]
            wait = WebDriverWait(driver, 10)
            pagina = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'navi_seiten')))
            links = pagina.find_elements(By.TAG_NAME, "a")

            max_number = 0
            for link in links:
                href = link.get_attribute('href')
                if href and 'sr=' in href:
                    number = int(href.split('=')[-1])
                    if number > max_number:
                        max_number = number



            # with open(driver.page_source, encoding="utf-8") as file:
            #     src_ru = file.read()
            # soup = BeautifulSoup(src_ru, 'lxml')
            #
            # pagina = soup.find('div',attrs={'class': 'navi_seiten'})
            # links = pagina.find_all('a')  # Находим все ссылки на странице
            #
            # max_number = 0
            # for link in links:
            #     href = link.get('href')  # Получаем значение атрибута href
            #     if href and 'sr=' in href:  # Проверяем, что в ссылке есть параметр sr
            #         number = int(href.split('=')[-1])  # Извлекаем число из параметра sr
            #         if number > max_number:
            #             max_number = number
            i = 0  # задаем начальное значение i
            while i <= max_number:
                url = f"https://mike.larsson.pl/pl/category/{group}/?sr={i}"
                driver.get(url)
                with open(f"c:\\data_larsoon\\list_data\\{group}_{i}.html", "w", encoding='utf-8') as file:
                    file.write(driver.page_source)
                time.sleep(5)
                i += 30
        driver.close()
        driver.quit()

def parsing_url_product():
    folders = [r"c:\data_larsoon\html_product\*.html"]
    for folder in folders:
        files_html = glob.glob(folder)
        for item in files_html[:1]:
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            table_chart = soup.find('div', {'class': 'mm_details'})
            mm_right_values = [div.text.strip().replace('\xa0', ' ') for div in
                               table_chart.find_all('div', {'class': 'mm_right'})]
            # print(mm_right_values)
            div_img = soup.find('div', {'class': 'mm_images_box'})
            a_img = div_img.find('a')
            href = 'https:' + a_img['href']
            # print(href)
            div_opis_towaru = soup.find('div', {'class': 'goog_trans_cont'})
            opis_towaru_text = div_opis_towaru.get_text(strip=True)
            # print(opis_towaru_text)
            div = soup.find('div', {'id': 'related_articles_werkzeug'})
            table = div.find('table')
            tbody = table.find('tbody')
            tr = tbody.find('tr', {'class': 'tdb'})
            show_history_tips_td = tr.find('td', {'class': 'show_history_tips'})
            value = show_history_tips_td.find("b").get_text()
            print(value)
            mysize_td = tr.find('td', {'class': 'mysize'})
            align_right_tds = tr.find_all('td', {'align': 'right'})
            # print(show_history_tips_td)
            # show_history_tips = show_history_tips_td.text

            mysize = mysize_td.get_text(strip=True)
            align_right_texts = [td.get_text(strip=True).replace('\xa0', ' ') for td in align_right_tds]

            # print(show_history_tips)
            # print( mysize)
            # print(align_right_texts)

def get_url_from_html():
    folders = [r"c:\data_larsoon\*.html"]

    with open('url_product.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for folder in folders:
            files_html = glob.glob(folder)
            for item in files_html:

                with open(item, encoding="utf-8") as file:
                    src = file.read()
                soup = BeautifulSoup(src, 'lxml')
                all_urls = []
                try:
                    galery = soup.find('div', attrs={'class': 'gallery'})
                    for div_yellow in galery.find_all('div', {'class': 'availability part_available show_history_tips'}):
                        link_yellow = div_yellow.find_next('a')['href']
                        all_urls.append(link_yellow)
                    for div_green in galery.find_all('div', {'class': 'availability available show_history_tips'}):
                        link_green = div_green.find_next('a')['href']
                        all_urls.append(link_green)
                    # Записываем URL-адреса в файл по одному на каждой строке
                    for url in all_urls:
                        writer.writerow([url])
                except:
                    print(item)

    #
    #
    #
    # folders = [r"c:\data_larsoon\*.html"]
    # urls = []
    # for folder in folders:
    #     files_html = glob.glob(folder)
    #     for item in files_html:
    #         with open(item, encoding="utf-8") as file:
    #             src = file.read()
    #         soup = BeautifulSoup(src, 'lxml')
    #         all_urls = []
    #         galery = soup.find('div', attrs={'class': 'gallery'})
    #         for div_yellow in galery.find_all('div', {'class': 'availability part_available show_history_tips'}):
    #             link_yellow = div_yellow.find_next('a')['href']
    #             all_urls.append(link_yellow)
    #         for div_green in galery.find_all('div', {'class': 'availability available show_history_tips'}):
    #             link_green = div_green.find_next('a')['href']
    #             all_urls.append(link_green)
    #         with open('url_product.csv', 'a', newline='') as csvfile:
    #             # Создаем объект writer для записи данных в файл csv
    #             writer = csv.writer(csvfile)
    #             # Записываем URL-адреса в файл по одному на каждой строке
    #             for url in all_urls:
    #                 writer.writerow([url])
def drop_duplicates():
    csv_files = 'url_product.csv'
    df = pd.read_csv(csv_files)

    # удалить дубликаты строк и сохранить уникальные строки в новом DataFrame
    df_unique = df.drop_duplicates()

    # сохранить уникальные строки в CSV-файл
    df_unique.to_csv(f'{csv_files}', index=False)
    print("Дубликты удалили, переходим к обработке main_asio")

def save_html_product():
    """Один поток"""
    url_start = "https://www.larsson.pl/"
    driver = get_undetected_chromedriver()
    driver.maximize_window()
    driver.get(url_start)
    time.sleep(2)
    wait = WebDriverWait(driver, 60)
    button_art_wait = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
    login = driver.find_element(By.NAME, 'username')
    login.send_keys('088087')
    passsss = driver.find_element(By.NAME, 'password')
    passsss.send_keys('jdtvy61')
    passsss.send_keys(Keys.RETURN)
    time.sleep(2)
    try:
        magaz_button = driver.find_element(By.XPATH, '//a[@class="btn btn-primary mr-xs mb-sm btn-lg"]').click()
    except:
        print("")
    try:
        chebox_wait = driver.find_element(By.XPATH, '//span[@class="checkmark "]').click()
        akcetpr_cooki = driver.find_element(By.XPATH, '//div[@class="btnAcceptAll"]').click()
    except:
        print('')
    time.sleep(1)
    with open(f'url_product.csv', newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        for url in urls[:5]:
            group = url[0].split('/')[-2]
            driver.get(url[0])
            time.sleep(1)
            with open(f"c:\\data_larsoon\\html_product\\{group}.html", "w", encoding='utf-8') as file:
                file.write(driver.page_source)
            # folder_path = "c:\\data_larsoon\\html_product"
            # # пробегаемся по всем файлам в папке
            # for filename in os.listdir(folder_path):
            #     # проверяем, что имя файла начинается с числа, а затем идет "_171849.html"
            #     if not re.match(f'{group}.html$', filename):
            #         driver.get(url[0])
            #         time.sleep(1)
            #         with open(f"c:\\data_larsoon\\html_product\\{group}.html", "w", encoding='utf-8') as file:
            #             file.write(driver.page_source)
            #     else:
            #         # файл найден, пропускаем итерацию
            #         print("файл найден, пропускаем итерацию")
            #         continue








if __name__ == '__main__':
    # main_category()
    # get_url_category()
    # get_url_product()
    # get_to_category()
    # get_url_from_html()
    # drop_duplicates()
    # save_html_product()
    parsing_url_product()