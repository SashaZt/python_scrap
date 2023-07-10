import re
import glob
import json
import os
from bs4 import BeautifulSoup
import shutil
import pickle
import tempfile
import zipfile
import time
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv


def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--disable-extensions') # Отключает использование расширений
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })
    return driver


def get_selenium():
    url = 'https://tripoli.land/users/sign_in?sign_in_source=%2Ffarmers'

    driver = get_chromedriver()
    driver.maximize_window()
    driver.get(url)
    wait = WebDriverWait(driver, 60)
    time.sleep(1)
    wait_email = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="user[email]"]')))
    email = driver.find_element(By.XPATH, '//input[@name="user[email]"]')
    email.send_keys('stepan.onyskiv@gmail.com')
    passwords = driver.find_element(By.XPATH, '//input[@name="user[password]"]')
    passwords.send_keys('Stepan9472')
    passwords.send_keys(Keys.RETURN)
    time.sleep(1)
    coun = 0
    with open('ХМ.csv', 'a', newline='', encoding='utf-8') as file_data:
        writer = csv.writer(file_data, delimiter=';')
        writer.writerow(['', '', '', '', '', '', '', ''])
        for i in range(39, 49): #Будет 48 страниц

            pause_time = random.randint(1, 3)
            driver.get(
                f'https://tripoli.land/farmers/proizvoditeli-zerna/hmelnitskaya?page={i}&q%5Bcategories_id_eq%5D=2&q%5Bdistrict_region_id_eq%5D=24')
            wait_company = wait.until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="call-popup"]')))
            company = driver.find_element(By.XPATH, '//span[@class="call-popup"]')
            company.click()
            for j in range(1, 41):
                coun += 1
                # file_name = f"c:\\data_tripoli_land\\farmers_{coun}.html"
                # if not os.path.exists(file_name):
                time.sleep(1)
                # driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                # with open(os.path.join('data', file_name), "w", encoding='utf-8') as fl:
                #     fl.write(driver.page_source)
                time.sleep(pause_time)
                company_nex = driver.find_element(By.XPATH,
                                                  '//button[@class="non-fluid right modal-action-btn tips-tooltip ng-scope"]')
                soup = BeautifulSoup(driver.page_source, 'lxml')
                regex_all = re.compile('beige-hover ng-scope.*')
                telephoni_company = soup.find('table', attrs={'ng-if': '!isMobile()'}).find_all('tbody')[0].find_all(
                    'tr', attrs={'class': regex_all})
                contacts = []
                for i in range(0, len(telephoni_company)):
                    regex_one = re.compile('same-phone-widt.*')
                    try:

                        telef = telephoni_company[i].find('a', attrs={'class': regex_one}).get('ng-href')
                    except AttributeError:
                        telef = ""
                    try:
                        names = telephoni_company[i].find('span', attrs={
                            'class': 'phone-comment phone-comment-edit-pencil tablink-correct tablink-correct hide-hover tips-tooltip ng-binding ng-scope'}).text.strip()
                    except AttributeError:
                        names = ""
                    try:
                        job = telephoni_company[i].find('span', attrs={
                            'class': 'dropdown-toggle position-title tips-tooltip ng-binding'}).text.strip()
                    except AttributeError:
                        job = ""
                    if not telef == "":
                        contacts.append(telef)
                    if not names == "":
                        contacts.append(names)
                    if not job == "":
                        contacts.append(job)
                contacts_email = []

                regex_email = re.compile('beige-hover ng-scope.*')
                try:
                    tables_email = soup.find_all('table', {'class': 'web-phones ng-scope'})
                    # email_company = soup.find_all('table', attrs={'class': 'web-phones ng-scope'})[1].find_all('tbody')[0].find_all(
                    #     'tr', attrs={'class': regex_email})
                except:
                    tables_email = None
                    # email_company = None
                try:
                    table = tables_email[1]

                except:
                    table = None
                if not table is None:
                    rows = table.find_all('tr')
                    for row in rows:
                        # Ищем теги 'span' с классом 'ng-binding'
                        spans = row.find_all('span', {'class': 'ng-binding'})
                        for span in spans:
                            # Извлекаем текст из каждого 'span' и добавляем в список
                            contacts_email.append(span.text)

                #
                # for i in range(0, len(email_company)):
                #     regex_one = re.compile('same-phone-widt.*')
                #     try:
                #
                #         email = email_company[i].find('span', attrs={'class': 'ng-binding'}).text
                #     except AttributeError:
                #         email = ""
                #     # try:
                #     #     names = email_company[i].find('span', attrs={
                #     #         'class': 'phone-comment phone-comment-edit-pencil tablink-correct tablink-correct hide-hover tips-tooltip ng-binding ng-scope'}).text.strip()
                #     # except AttributeError:
                #     #     names = ""
                #     # try:
                #     #     job = email_company[i].find('span', attrs={
                #     #         'class': 'dropdown-toggle position-title tips-tooltip ng-binding'}).text.strip()
                #     # except AttributeError:
                #     #     job = ""
                #     if not email == "":
                #         contacts_email.append(email)
                    # if not names == "":
                    #     contacts.append(names)
                    # if not job == "":
                    #     contacts.append(job)
                # print(contacts_email)

                edrpo = soup.find('div', attrs={'ng-if': 'org.erdpou'}).find('div',
                                                                             attrs={'class': 'ng-binding'}).text
                address = soup.find('div', attrs={'ng-bind': 'org.address_label'}).text.split(',')
                try:
                    address_company_01 = address[0]
                except:
                    address_company_01 = ""
                try:
                    address_company_02 = address[1]
                except:
                    address_company_02 = ""
                try:
                    address_company_03 = address[2]
                except:
                    address_company_03 = ""
                try:
                    address_company_04 = address[3]
                except:
                    address_company_04 = ""
                try:
                    address_company_05 = address[4]
                except:
                    address_company_05 = ""
                try:
                    address_company_06 = address[5]
                except:
                    address_company_06 = ""
                try:
                    address_company_07 = address[6]
                except:
                    address_company_07 = ""
                try:
                    address_company_08 = address[7]
                except:
                    address_company_08 = ""
                name_company = soup.find('p', attrs={
                    'class': 'modal-title display-inline-block farmer-modal-name ng-binding'}).text
                try:
                    landing_area_sum = soup.find('div',
                                                 attrs={'ng-bind': 'org.landing_area_sum | splitThousands'}).text
                except:
                    landing_area_sum = ""
                try:
                    director = soup.find('div', attrs={'ng-bind': 'org.director'}).text
                except:
                    director = ""
                datas = [address_company_01, address_company_02, address_company_03, address_company_04,
                         address_company_05, address_company_06, address_company_07, address_company_08,
                         name_company, edrpo, director, contacts, contacts_email, landing_area_sum
                         ]
                writer.writerow(
                    datas
                )

                company_nex.click()
            # clouse_button = driver.find_element(By.XPATH, '//div[@class="s-close-btn"]')
            # clouse_button.click()

        driver.close()
        driver.quit()


def parsing():
    files_htmls = f"c:\\data_tripoli_land\\Льовськая\\*.html"
    files_html = glob.glob(files_htmls)

    with open('Ровно.csv', 'w', newline='', encoding='utf-8') as file_data:
        writer = csv.writer(file_data, delimiter=';')
        writer.writerow(['', '', '', '', '', '', ''])

        for item in files_html[150:160]:
            print(item)
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            regex_all = re.compile('beige-hover ng-scope.*')
            telephoni_company = soup.find('table', attrs={'ng-if': '!isMobile()'}).find_all('tbody')[0].find_all('tr',
                                                                                                                 attrs={
                                                                                                                     'class': regex_all})
            contacts = []
            for i in range(0, len(telephoni_company)):
                regex_one = re.compile('same-phone-widt.*')
                try:

                    telef = telephoni_company[i].find('a', attrs={
                        'class': regex_one}).get(
                        'ng-href')
                except AttributeError:
                    telef = ""
                try:
                    names = telephoni_company[i].find('span', attrs={
                        'class': 'phone-comment phone-comment-edit-pencil tablink-correct tablink-correct hide-hover tips-tooltip ng-binding ng-scope'}).text.strip()
                except AttributeError:
                    names = ""
                try:
                    job = telephoni_company[i].find('span', attrs={
                        'class': 'dropdown-toggle position-title tips-tooltip ng-binding'}).text.strip()
                except AttributeError:
                    job = ""
                if not telef == "":
                    contacts.append(telef)
                if not names == "":
                    contacts.append(names)
                if not job == "":
                    contacts.append(job)
            edrpo = soup.find('div', attrs={'ng-if': 'org.erdpou'}).find('div', attrs={'class': 'ng-binding'}).text
            address = soup.find('div', attrs={'ng-bind': 'org.address_label'}).text.split(',')
            try:
                address_company_01 = address[0]
            except:
                address_company_01 = ""
            try:
                address_company_02 = address[1]
            except:
                address_company_02 = ""
            try:
                address_company_03 = address[2]
            except:
                address_company_03 = ""
            try:
                address_company_04 = address[3]
            except:
                address_company_04 = ""
            try:
                address_company_05 = address[4]
            except:
                address_company_05 = ""
            try:
                address_company_06 = address[5]
            except:
                address_company_06 = ""
            try:
                address_company_07 = address[6]
            except:
                address_company_07 = ""
            try:
                address_company_08 = address[7]
            except:
                address_company_08 = ""
            name_company = soup.find('p', attrs={
                'class': 'modal-title display-inline-block farmer-modal-name ng-binding'}).text
            try:
                landing_area_sum = soup.find('div', attrs={'ng-bind': 'org.landing_area_sum | splitThousands'}).text
            except:
                landing_area_sum = ""
            try:
                director = soup.find('div', attrs={'ng-bind': 'org.director'}).text
            except:
                director = ""
            datas = [address_company_01, address_company_02, address_company_03, address_company_04,
                     address_company_05, address_company_06, address_company_07, address_company_08,
                     name_company, edrpo, director, contacts, landing_area_sum
                     ]
            writer.writerow(
                datas
            )

            # writer.writerow([contacts, edrpo])
            # script_json = soup.find_all('script', type="application/json")[4]
            # data_json = json.loads(script_json.string)
            # list_company = len(data_json)
            # for i in range(len(data_json)):
            #     if i < len(data_json):
            #         address_company = data_json[i]['address']
            #         if address_company is None:
            #             address_company = ''
            #         else:
            #             address_company = address_company.split(',')
            #         try:
            #             address_company_01 = address_company[0]
            #         except:
            #             address_company_01 = None
            #         try:
            #             address_company_02 = address_company[1]
            #         except:
            #             address_company_02 = None
            #         try:
            #             address_company_03 = address_company[2]
            #         except:
            #             address_company_03 = None
            #         try:
            #             address_company_04 = address_company[3]
            #         except:
            #             address_company_04 = None
            #         try:
            #             address_company_05 = address_company[4]
            #         except:
            #             address_company_05 = None
            #         try:
            #             address_company_06 = address_company[5]
            #         except:
            #             address_company_06 = None
            #         try:
            #             address_company_07 = address_company[6]
            #         except:
            #             address_company_07 = None
            #         try:
            #             address_company_08 = address_company[7]
            #         except:
            #             address_company_08 = None
            #
            #         name_company = data_json[i]['name']
            #         landing_area_sum = data_json[i]['landing_area_sum']
            #         director = data_json[i]['director']
            #         erdpou = data_json[i]['erdpou']
            #         phone_mobile = data_json[i]['phone_mobile']
            #         phone_mobile_additional = data_json[i]['phone_mobile_additional']
            #         if phone_mobile is None:
            #             phone_mobile = ''
            #         if phone_mobile_additional is None:
            #             phone_mobile_additional = ''
            #         phone_list = phone_mobile + phone_mobile_additional
            #
            #         datas = [address_company_01, address_company_02, address_company_03, address_company_04,
            #                  address_company_05, address_company_06, address_company_07, address_company_08,
            #                  name_company, erdpou, director, landing_area_sum]
            #         writer.writerow(
            #             datas
            #         )

    # print(f'Адресс - {address_company}')
    # print(f'Название компании -  {name_company}')
    # print(f'Земля - {landing_area_sum}')
    # print(f'Директор {director}')
    # print(f'ЕДРПО - {erdpou}')
    # print(f'Номер телефона - {phone_mobile}')
    # print(f'Дополнительный номер  - {phone_mobile_additional}')
    # # with open("output.json", "w", encoding='utf-8') as write_file:
    #     json.dump(data_json, write_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    get_selenium()
    # parsing()
