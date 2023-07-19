import random
from bs4 import BeautifulSoup
import csv
import requests
import glob
import json
import os
import time
from datetime import datetime
from dateutil import parser


def course_dollars():
    import requests

    cookies = {
        'locale': 'ua',
        '__cf_bm': 'bpW6G9IMs2e.Nqlg2axi5OIGdfYsHR5iDtqNrJy9nAA-1689742731-0-AaT4syoOIZxDAxNKGrQGvfxabRgS0pR9K1NVDi7G5aHarGOwo9aAFY69rQ8nh4lg4zjLgjZTEvFj/zxiIeQ/JLU=',
    }

    headers = {
        'authority': 'bank.gov.ua',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'cache-control': 'no-cache',
        # 'cookie': 'locale=ua; __cf_bm=bpW6G9IMs2e.Nqlg2axi5OIGdfYsHR5iDtqNrJy9nAA-1689742731-0-AaT4syoOIZxDAxNKGrQGvfxabRgS0pR9K1NVDi7G5aHarGOwo9aAFY69rQ8nh4lg4zjLgjZTEvFj/zxiIeQ/JLU=',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    response = requests.get('https://bank.gov.ua/ua/markets/exchangerates', cookies=cookies, headers=headers)
    src = response.text
    soup = BeautifulSoup(src, 'lxml')
    scripts = soup.find_all('script')

    json_str = scripts[2].string.split('window.results = JSON.parse(', 1)[1].rsplit(')', 1)[0].strip("'")
    json_data = json.loads(json_str)  # Преобразовываем строку JSON в словарь Python
    course_dollars = json_data[7]['rate']
    return course_dollars


def get_url_ad():

    cookies = {
        'current_currency': 'UAH',
        '_ga': 'GA1.2.905147567.1689674622',
        '_gid': 'GA1.2.555662714.1689674622',
        'csrftoken': 'K5uPBwwPeP67R82c5M5y2OTFiKChd4hKBCxR7b5PIUyYBNAXMveyjTHptqaimZiO',
        'sessionid': 'nz041h2nmtl03vyfdjuf3jvgwzyvky3m',
        '_gat_UA-200319004-1': '1',
        '_ga_MD7LGRXX6R': 'GS1.2.1689689658.4.1.1689691128.60.0.0',
    }

    headers = {
        'authority': 'kupypai.com',
        'accept': '*/*',
        'accept-language': 'uk',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        # 'cookie': 'current_currency=UAH; _ga=GA1.2.905147567.1689674622; _gid=GA1.2.555662714.1689674622; csrftoken=K5uPBwwPeP67R82c5M5y2OTFiKChd4hKBCxR7b5PIUyYBNAXMveyjTHptqaimZiO; sessionid=nz041h2nmtl03vyfdjuf3jvgwzyvky3m; _gat_UA-200319004-1=1; _ga_MD7LGRXX6R=GS1.2.1689689658.4.1.1689691128.60.0.0',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://kupypai.com/profile/announcement/list/client',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-csrftoken': 'K5uPBwwPeP67R82c5M5y2OTFiKChd4hKBCxR7b5PIUyYBNAXMveyjTHptqaimZiO',
        'x-requested-with': 'XMLHttpRequest',
    }
    offset = 100
    with open('url_products.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for page_list in range(1, 10):
            if page_list == 1:
                params = {
                    'limit': '100',
                }
                response = requests.get(
                    'https://kupypai.com/api/v1/announcement/list/%3Bsort%3Dcreated_at_up/',
                    params=params,
                    cookies=cookies,
                    headers=headers,
                )
                json_data = response.json()
                with open(f'json_list/data_0{page_list}.json', 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
                # id_ads = json_data['data']['items']
                # for i in range(101):
                #     id_ad = id_ads[i]['id']
                #     writer.writerow([id_ad])
            if page_list > 1:
                params = {
                    'limit': '100',
                    'offset': offset,
                }
                response = requests.get(
                    'https://kupypai.com/api/v1/announcement/list/%3Bsort%3Dcreated_at_up/',
                    params=params,
                    cookies=cookies,
                    headers=headers,
                )
                json_data = response.json()
                with open(f'json_list/data_0{page_list}.json', 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
                # id_ads = json_data['data']['items']
                # for i in range(101):
                #     id_ad = id_ads[i]['id']
                #     writer.writerow([id_ad])
                offset += 100
            time.sleep(10)


def get_id_ad():
    """Получаем список всех объявлений"""
    folders_json = fr"C:\scrap_tutorial-master\kupypai\json_list\*.json"
    files_json = glob.glob(folders_json)
    with open('id_ad.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|')
        for j in files_json:
            with open(j, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            id_ads = json_data['data']
            for item in id_ads['items']:
                id_ad = item['id']
                data_ad = item['createdAt']
                dt = parser.parse(data_ad)

                # Приведите объект datetime к нужному формату
                formatted_time = dt.strftime('%H:%M')
                formatted_date = dt.strftime('%d.%m.%Y')
                writer.writerow([id_ad,formatted_time,formatted_date])


def get_ad():
    data = []

    with open('id_ad.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    cookies = {
        'current_currency': 'UAH',
        '_ga': 'GA1.2.905147567.1689674622',
        '_gid': 'GA1.2.555662714.1689674622',
        'csrftoken': 'K5uPBwwPeP67R82c5M5y2OTFiKChd4hKBCxR7b5PIUyYBNAXMveyjTHptqaimZiO',
        'sessionid': 'nz041h2nmtl03vyfdjuf3jvgwzyvky3m',
        '_ga_MD7LGRXX6R': 'GS1.2.1689689658.4.1.1689691463.60.0.0',
    }

    headers = {
        'authority': 'kupypai.com',
        'accept': '*/*',
        'accept-language': 'uk',
        'content-type': 'application/json',
        # 'cookie': 'current_currency=UAH; _ga=GA1.2.905147567.1689674622; _gid=GA1.2.555662714.1689674622; csrftoken=K5uPBwwPeP67R82c5M5y2OTFiKChd4hKBCxR7b5PIUyYBNAXMveyjTHptqaimZiO; sessionid=nz041h2nmtl03vyfdjuf3jvgwzyvky3m; _ga_MD7LGRXX6R=GS1.2.1689689658.4.1.1689691463.60.0.0',
        'dnt': '1',
        'referer': 'https://kupypai.com/profile/announcement/2181/client',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-csrftoken': 'K5uPBwwPeP67R82c5M5y2OTFiKChd4hKBCxR7b5PIUyYBNAXMveyjTHptqaimZiO',
        'x-requested-with': 'XMLHttpRequest',
    }
    page = 0
    for d in data:
        page += 1
        name_files = f'json_ad/{d[0]}.json'
        pause_time = random.randint(5, 10)
        if not os.path.exists(name_files):
            response = requests.get(f'https://kupypai.com/api/v1/announcement/{d[0]}/retrieve-update/', cookies=cookies,
                                    headers=headers)
            json_data = response.json()
            with open(name_files, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
            time.sleep(pause_time)
        print(f'{len(data) - page}')


def parsing_ad():
    folders_json = fr"C:\scrap_tutorial-master\kupypai\json_ad\*.json"
    files_json = glob.glob(folders_json)
    dollars = course_dollars().replace(",", ".")
    dollars = float(dollars)
    data_row = []

    with open('id_ad.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data_row.append(row)
    data_dict = {}

    for row in data_row:
        id_ad_row, formatted_time_row, formatted_date_row = row[0].split(';')
        data_dict[int(id_ad_row)] = (formatted_time_row, formatted_date_row)
    heandler = ['Дата публікації', 'Час публікації',
        'Id', 'Статус', 'Оголошення ID', 'Кадастровий номер', 'Ціна ділянки UAH', 'Ціна ділянки $',
        'Ціна за 1 га UAH', 'Ціна за 1 га $', 'Термін оренди', 'Орендна плата, за рік UAH', 'Орендна плата, за рік $',
        'Річний орендний дохід після податків UAH', 'Річний орендний дохід після податків $', 'Площа', 'Призначення', 'Дохідність',
        'Населений пункт', "", "Район", "Область", "Країна", 'Координати', "Власник ЄДРПО", "Власник", "Телефон",
        "Назва компанії", 'ЄДРПО Компаніїї', "ПІБ", 'Контакти компанії', 'email'

    ]
    with open('ad.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|')
        writer.writerow(heandler)
        for j in files_json[:21]:
            with open(j, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            id_ad = json_data['data']['item']['id']
            formatted_time_row = ''
            formatted_date_row = ''
            if id_ad in data_dict:
                formatted_time_row, formatted_date_row = data_dict[id_ad]
            status_ad = json_data['data']['item']['statusDisplay']
            currency_ad = json_data['data']['item']['currency']  # Валюта
            identifier_ad = json_data['data']['item']['identifier']  # Индификатор
            cadastre_ad = json_data['data']['item']['cadastre']  # Кадастровий номер
            price_ad = f"{json_data['data']['item']['price']} {currency_ad}"  # Ціна ділянки:
            price_ad_dol = round(int(json_data['data']['item']['price']) / dollars)  # Ціна ділянки $:
            pricePerOne_ad = f"{json_data['data']['item']['pricePerOne']} {currency_ad}"  # Ціна за 1 га
            pricePerOne_ad_dol = round(int(json_data['data']['item']['pricePerOne']) / dollars)  # Ціна за 1 га $
            rentPeriod_ad = json_data['data']['item']['rentPeriod']  # Термін оренди:
            rentRate_ad_dol = round(int(json_data['data']['item']['rentRate']) / dollars)  # Орендна плата, за рік $
            rentRate_ad = f"{json_data['data']['item']['rentRate']} {currency_ad}"  # Орендна плата, за рік
            rentRateClean_ad = f"{json_data['data']['item']['rentRateClean']} {currency_ad}"  # Річний орендний дохід після податків
            rentRateClean_ad_dol = round(int(json_data['data']['item']['rentRateClean'])  / dollars) # Річний орендний дохід після податків $
            area_ad = json_data['data']['item']['rentalYield'].replace('.', ',')  # Площа:
            purpose_ad = json_data['data']['item']['purpose']  # Призначення
            rentalYield_ad = json_data['data']['item']['rentalYield']  # Дохідність:
            koatuuLocation_ad = json_data['data']['item']['koatuuLocation']  # Адреса
            locations_list = koatuuLocation_ad.split(", ")
            if len(locations_list) == 4:
                locations_list.insert(0, None)
            locations_list += [None] * (5 - len(locations_list))
            geoCoordinates_ad = json_data['data']['item']['geoCoordinates']  # Координати
            ownerEdrpou_ad = json_data['data']['item']['ownerEdrpou']  # ЕДРПО
            ownerName_ad = json_data['data']['item']['ownerName']  # Назва
            ownerPhone_ad = json_data['data']['item']['ownerPhone']  # Телефон
            title_ad = json_data['data']['item']['renterCompany']['title']  # Назва фирми
            edrpou_ad = json_data['data']['item']['renterCompany']['edrpou']  # Фирми ЕДРПО
            contactName_ad = json_data['data']['item']['renterCompany']['contactName']  # Фирми ЕДРПО
            contactPhone_ad = json_data['data']['item']['renterCompany']['contactPhone']  # Фирми ЕДРПО
            email_ad = json_data['data']['item']['renterCompany']['email']  # Фирми ЕДРПО
            data = [
                       formatted_date_row, formatted_time_row, id_ad, status_ad, identifier_ad, cadastre_ad, price_ad, price_ad_dol, pricePerOne_ad,
                       pricePerOne_ad_dol, rentPeriod_ad, rentRate_ad, rentRate_ad_dol, rentRateClean_ad, rentRateClean_ad_dol, area_ad, purpose_ad,
                       rentalYield_ad] + locations_list + [geoCoordinates_ad, ownerEdrpou_ad, ownerName_ad,
                                                           ownerPhone_ad, title_ad, edrpou_ad, contactName_ad,
                                                           contactPhone_ad, email_ad
                                                           ]

            writer.writerow(data)


def update_ad():
    data_old = []

    with open('id_ad.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data_old.append(row)
    cookies = {
        'current_currency': 'UAH',
        '_ga': 'GA1.2.905147567.1689674622',
        '_gid': 'GA1.2.555662714.1689674622',
        'csrftoken': 'K5uPBwwPeP67R82c5M5y2OTFiKChd4hKBCxR7b5PIUyYBNAXMveyjTHptqaimZiO',
        'sessionid': 'nz041h2nmtl03vyfdjuf3jvgwzyvky3m',
        '_gat_UA-200319004-1': '1',
        '_ga_MD7LGRXX6R': 'GS1.2.1689689658.4.1.1689691128.60.0.0',
    }

    headers = {
        'authority': 'kupypai.com',
        'accept': '*/*',
        'accept-language': 'uk',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        # 'cookie': 'current_currency=UAH; _ga=GA1.2.905147567.1689674622; _gid=GA1.2.555662714.1689674622; csrftoken=K5uPBwwPeP67R82c5M5y2OTFiKChd4hKBCxR7b5PIUyYBNAXMveyjTHptqaimZiO; sessionid=nz041h2nmtl03vyfdjuf3jvgwzyvky3m; _gat_UA-200319004-1=1; _ga_MD7LGRXX6R=GS1.2.1689689658.4.1.1689691128.60.0.0',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://kupypai.com/profile/announcement/list/client',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-csrftoken': 'K5uPBwwPeP67R82c5M5y2OTFiKChd4hKBCxR7b5PIUyYBNAXMveyjTHptqaimZiO',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        'limit': '100',
    }
    response = requests.get(
        'https://kupypai.com/api/v1/announcement/list/%3Bsort%3Dcreated_at_up/',
        params=params,
        cookies=cookies,
        headers=headers,
    )


if __name__ == '__main__':
    # get_url_ad()
    # get_id_ad()
    # get_ad()
    # parsing_ad()
    update_ad()
