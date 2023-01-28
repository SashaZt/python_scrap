# -*- coding: utf-8 -*-
# Parser Hyatt hotels Corp codes 
# 1.3 - fix cookie
# 1.31 - added csv
# 1.32 - fix selenium
# 1.33 - added exception on cookies
# 1.5 - fix selenium
# 1.6 - added exception in cycle

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import xlsxwriter as xl
import re

START = 2420
END = 2500
SEND_MES = False
# false if exception
verify = True
PATH = 'chromedriver.exe'
# TOKEN = botXXXXXXXXXXXXXXXXXXXX
TOKEN = 'botXXXXXXXXXXXXXXXXX'
chat_id = 00000000
URL = 'https://www.hyatt.com/en-US/shop/rates/mosrm?rooms=1&adults=1&location=Bangkok%2C%20Thailand&checkinDate=2023-12-11&checkoutDate=2023-12-12&kids=0&rateFilter=standard&corp_id='

hotel = URL.split('/')[-1].split('?')[0]
filename_csv = 'result-' + hotel + '_' + time.strftime('%Y-%m-%d-%H-%M') + '.csv'

print(f'Hotel "{hotel}"; Start {START}; End {END}')
print(f'To force stop press Ctrl+C')

headers = {
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
}


def to_int(price):
    price = int(''.join(re.findall(r'\d', price)))
    return price


def get_cookies(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument('headless')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36')

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    driver.get(url)
    time.sleep(5)
    cookies_list = driver.get_cookies()
    print(cookies_list)
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    # print(cookies_dict)
    try:
        cooke_raw = f'tkrm_alpekz={cookies_dict["tkrm_alpekz_s1.3"]}; source-country=RU;'
        # cooke_raw = f'tkrm_alpekz={cookies_dict["tkrm_alpekz_s1.3"]}; source-country=RU; _dst_lnn={cookies_dict["_dst_lnn"]}'
    except KeyError:
        cooke_raw = f'tkrm_alpekz={cookies_dict["tkrm_alpekz_s1.3"]}; source-country=RU'
    cookiesdict = {}
    for i in cooke_raw.split('; '):
        cookiesdict[i.split('=')[0]] = i.split('=')[1]
    driver.close()
    return cookiesdict


def get_exc():
    soup = BeautifulSoup(requests.get(URL, verify=verify, headers=headers, cookies=cookiesdict).text, 'html.parser')
    exc = soup.find('span', 'b-text_copy-2 b-text_weight-bold b-d-none b-d-inline@md').text
    return exc


def parse(id, cookiesdict):
    url = URL + (str(i))
    req = requests.get(url, verify=verify, headers=headers, cookies=cookiesdict)
    soup = BeautifulSoup(req.text, 'html.parser')
    name = soup.find('span', 'b-text_copy-2 b-text_weight-bold b-d-none b-d-inline@md')
    price = soup.find('div', 'b-text_weight-bold rate-pricing')
    return [name, price]


def write_csv(id_, name, price):
    with open(filename_csv, 'a') as csv_file:
        csv_file.write(f'{id_},{name},{price}\n')


cookiesdict = get_cookies(URL)
data = {"id": [], "name": [], "price": []}
EXCEPT = ' '.join(get_exc().split(' ')[:2])
print(f'Mark Exception "{EXCEPT}"')
try:
    for i in range(START, END + 1):
        try:
            dataparse = parse(i, cookiesdict)
            if dataparse[0].text.startswith(EXCEPT):
                print(f'id {i} -- exception')
                continue
            else:
                price = to_int(dataparse[1].text)
                print(f'id {i} -- {dataparse[0].text} -- {price}')
                data["id"].append(i)
                data["name"].append(dataparse[0].text)
                data["price"].append(price)
                write_csv(i, dataparse[0].text, price)
        except KeyboardInterrupt:
            print(f'id {i} -- Forced termination...')
            break
        except Exception:
            print(f'id {i} -- Invalid Cookies...')
            try:
                cookiesdict = get_cookies(URL + (str(i)))
                dataparse = parse(i, cookiesdict)
                if dataparse[0].text.startswith(EXCEPT):
                    print(f'id {i} -- exception')
                else:
                    price = to_int(dataparse[1].text)
                    print(f'id {i} -- {dataparse[0].text} -- {price}')
                    data["id"].append(i)
                    data["name"].append(dataparse[0].text)
                    data["price"].append(price)
                    write_csv(i, dataparse[0].text, price)
            except Exception as err:
                print(err)
                print('Opened unusual page...')
except Exception as err:
    if SEND_MES:
        mes = requests.get(
            f'https://api.telegram.org/{TOKEN}/sendMessage?chat_id={chat_id}&text=Error id {i}, parser stopped working')

if SEND_MES:
    mes = requests.get(
        f'https://api.telegram.org/{TOKEN}/sendMessage?chat_id={chat_id}&text=The {hotel} is done; Start {START}, End {END}, Total found: {len(data["id"])}')

price_sort = {}
for i, j in enumerate(data["price"]):
    price_sort[i] = j
price_sort = list(price_sort.items())
price_sort.sort(key=lambda i: i[1])
data_sort = {'id': [], 'name': [], 'price': []}
for i in price_sort:
    data_sort["price"].append(i[1])
    data_sort["id"].append(data["id"][i[0]])
    data_sort["name"].append(data["name"][i[0]])
print(data_sort)

filename = 'result-' + hotel + '_' + time.strftime('%Y-%m-%d-%H-%M') + '.xlsx'
title = ['ID', 'Name', 'Price']
workbook = xl.Workbook(filename)
worksheet = workbook.add_worksheet()
worksheet.write_row('A1', title)
worksheet.write_column('A2', data_sort["id"])
worksheet.write_column('B2', data_sort["name"])
worksheet.write_column('C2', data_sort["price"])
print(f"Sorted data exported, {filename} written")
workbook.close()
