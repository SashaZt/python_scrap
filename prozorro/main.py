import json
import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

# from selenium import webdriver

current_directory = os.getcwd()
temp_directory = 'temp'
# Создайте полный путь к папке temp
temp_path = os.path.join(current_directory, temp_directory)
json_path = os.path.join(temp_path, 'json')
html_path = os.path.join(temp_path, 'html')

"""Создание временых папок"""


def creative_temp_folders():
    # Убедитесь, что папки существуют или создайте их
    for folder in [temp_path, json_path, html_path]:
        if not os.path.exists(folder):
            os.makedirs(folder)


headers = {
    'authority': 'prozorro.gov.ua',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
    'cache-control': 'no-cache',
    # 'cookie': '_ga=GA1.3.995390387.1707986647; _gat=1',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

"""Получение всех тендеров"""


def get_all_tenders():
    params = {
        'cpv[0]': '39160000-1',
        'status[0]': 'active.enquiries',
        'status[1]': 'active.tendering',
        'filterType': 'tenders',
    }

    response = requests.post('https://prozorro.gov.ua/api/search/tenders', params=params,
                             headers=headers)

    json_data = response.json()
    filename_all_tenders = os.path.join(json_path, 'all_tenders.json')
    with open(filename_all_tenders, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


"""Парсинг всех тендеров"""


def pars_all_tenders():
    filename_all_tenders = os.path.join(json_path, 'all_tenders.json')
    with open(filename_all_tenders, 'r', encoding="utf-8") as f:
        data_json = json.load(f)


"""Получение одного тендера"""


def get_tender():
    response = requests.get('https://prozorro.gov.ua/tender/UA-2024-02-12-015060-a', headers=headers)
    src = response.text
    filename_tender = os.path.join(html_path, 'tender.html')

    with open(filename_tender, "w", encoding='utf-8') as file:
        file.write(src)


"""Парсинг одного тендера и извлечение json файла"""


def parsing_tender():
    filename_tender = os.path.join(html_path, 'tender.html')
    with open(filename_tender, encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    tender_id_full = soup.find('div', {'data-js': 'tender_sign_check'}).get('data-url')
    tender_id = tender_id_full.split('/')[-1]

    return tender_id


def get_json_tender():
    filename_tender = os.path.join(html_path, 'tender.html')
    with open(filename_tender, encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    tender_id_full = soup.find('div', {'data-js': 'tender_sign_check'}).get('data-url')
    tender_id = tender_id_full.split('/')[-1]
    # response = requests.get(tender_id, headers=headers)
    response = requests.get(f"https://public-api.prozorro.gov.ua/api/2.5/tenders/{tender_id}", headers=headers)
    json_data = response.json()
    filename_tender = os.path.join(json_path, 'tender.json')
    with open(filename_tender, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


"""Парсинг одного тендера json"""


def pars_tender():
    tender_id = parsing_tender()
    filename_tender = os.path.join(json_path, 'tender.json')
    with open(filename_tender, 'r', encoding="utf-8") as f:
        data_json = json.load(f)
    json_data = data_json.get('data', {})
    status_tender = json_data.get('status', None)
    url_tender = None
    customer = None
    date_startDate = None
    time_startDate = None
    date_enquiryPeriod_endDate = None
    time_enquiryPeriod_endDate = None
    date_auctionPeriod_auctionPeriod = None
    time_auctionPeriod_auctionPeriod = None
    guarantee_amount = None
    bank_garantiy = None
    award_name_customer = None
    award_value_customer = None
    date_pending = None
    time_pending = None
    tenderID = None
    date_auctionPeriod = None
    time_auctionPeriod = None
    if status_tender == 'active.enquiries':
        status_tender = 'Період уточнень'
        tenderID = json_data.get('tenderID')
        url_tender = f"https://prozorro.gov.ua/tender/{tenderID}"
        customer = json_data.get('procuringEntity', {}).get('name', 'Не указан')
        # "Початок аукціону"
        lots = json_data.get('lots', [{}])
        auctionPeriod = lots[0].get('auctionPeriod', {})
        startDate = auctionPeriod.get('startDate')
        if startDate:
            datetime_obj_startDate = datetime.fromisoformat(startDate)
            date_startDate = datetime_obj_startDate.strftime("%d.%m.%Y")
            time_startDate = datetime_obj_startDate.strftime("%H:%M")
        else:
            date_startDate = time_startDate = None
        # "Звернення за роз’ясненнями"
        enquiryPeriod_endDate = json_data.get('enquiryPeriod', {}).get('endDate')
        if enquiryPeriod_endDate:
            datetime_obj_enquiryPeriod_endDate = datetime.fromisoformat(enquiryPeriod_endDate)

            date_enquiryPeriod_endDate = datetime_obj_enquiryPeriod_endDate - timedelta(days=1)
            date_enquiryPeriod_endDate = date_enquiryPeriod_endDate.strftime("%d.%m.%Y")

            datetime_obj_minus_one_minute = datetime_obj_enquiryPeriod_endDate - timedelta(minutes=1)
            time_enquiryPeriod_endDate = datetime_obj_minus_one_minute.strftime("%H:%M")
        else:
            date_enquiryPeriod_endDate = time_enquiryPeriod_endDate = None



    if status_tender == 'active.tendering':
        status_tender = 'Подання пропозицій'
        tenderID = json_data.get('tenderID')
        url_tender = f"https://prozorro.gov.ua/tender/{tenderID}"
        customer = json_data.get('procuringEntity', {}).get('name', 'Не указан')

        dateCreated = json_data.get('dateCreated', None)

        # "Початок аукціону"
        lots = json_data.get('lots', [{}])
        auctionPeriod = lots[0].get('auctionPeriod', {})
        startDate = auctionPeriod.get('startDate')
        if startDate:
            datetime_obj_startDate = datetime.fromisoformat(startDate)
            date_startDate = datetime_obj_startDate.strftime("%d.%m.%Y")
            time_startDate = datetime_obj_startDate.strftime("%H:%M")
        else:
            date_startDate = time_startDate = None

        # "Очікувана вартість"
        price_tender = json_data.get('value', {}).get('amount', None)

        # "Відкриті торги з особливостями"

        # "Звернення за роз’ясненнями"
        enquiryPeriod_endDate = json_data.get('enquiryPeriod', {}).get('endDate')
        if enquiryPeriod_endDate:
            datetime_obj_enquiryPeriod_endDate = datetime.fromisoformat(enquiryPeriod_endDate)

            date_enquiryPeriod_endDate = datetime_obj_enquiryPeriod_endDate - timedelta(days=1)
            date_enquiryPeriod_endDate = date_enquiryPeriod_endDate.strftime("%d.%m.%Y")

            datetime_obj_minus_one_minute = datetime_obj_enquiryPeriod_endDate - timedelta(minutes=1)
            time_enquiryPeriod_endDate = datetime_obj_minus_one_minute.strftime("%H:%M")
        else:
            date_enquiryPeriod_endDate = time_enquiryPeriod_endDate = None

        # "Кінцевий строк подання тендерних пропозицій"
        auctionPeriod_auctionPeriod = lots[0].get('auctionPeriod', {}).get('shouldStartAfter')
        if auctionPeriod_auctionPeriod:
            datetime_obj_auctionPeriod_auctionPeriod = datetime.fromisoformat(auctionPeriod_auctionPeriod)

            date_auctionPeriod_auctionPeriod = datetime_obj_auctionPeriod_auctionPeriod - timedelta(days=1)
            date_auctionPeriod_auctionPeriod = date_auctionPeriod_auctionPeriod.strftime("%d.%m.%Y")
            datetime_obj_minus_one_minute = datetime_obj_auctionPeriod_auctionPeriod - timedelta(minutes=1)
            time_auctionPeriod_auctionPeriod = datetime_obj_minus_one_minute.strftime("%H:%M")
        else:
            date_auctionPeriod_auctionPeriod = time_auctionPeriod_auctionPeriod = None
    if status_tender == 'active.awarded':
        status_tender = 'Пропозиції розглянуті'
        tenderID = json_data.get('tenderID')
        url_tender = f"https://prozorro.gov.ua/tender/{tenderID}"
        customer = json_data.get('procuringEntity', {}).get('name', 'Не указан')
        """Победитель """
        award_name_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('name', None)
        """Ставка которая победила"""
        award_value_customer = json_data.get('awards', [{}])[0].get('value', [{}]).get('amount', None)

        # award_name = json_data['awards'][0]['suppliers'][0]['name']
        dara_pending = json_data['contracts'][0]['date']
        datetime_obj_pending = datetime.fromisoformat(dara_pending)
        """Дата и время победившей ставки"""
        date_pending = datetime_obj_pending.strftime("%d.%m.%Y")
        time_pending = datetime_obj_pending.strftime("%H:%M")
    if status_tender == 'complete':
        status_tender = 'Завершена'
        tenderID = json_data.get('tenderID')
        url_tender = f"https://prozorro.gov.ua/tender/{tenderID}"
        """Розмір надання забезпечення пропозицій учасників"""
        guarantee_amount = json_data['guarantee']['amount']

        bank_garantiy = json_data['criteria'][10]['requirementGroups'][0]['requirements'][0]['description']
        """забезпечення виконання договору """
        if 'Відповідно до пункту 7 частини першої' in bank_garantiy:
            bank_garantiy = 'Да'
        else:
            bank_garantiy = None
    if status_tender == 'active.pre-qualification.stand-still':
        status_tender = 'Прекваліфікація (період оскарження)'
        tenderID = json_data.get('tenderID')
        url_tender = f"https://prozorro.gov.ua/tender/{tenderID}"
    if status_tender == 'active.auction':
        status_tender = 'Аукціон'
        tenderID = json_data.get('tenderID')
        url_tender = f"https://prozorro.gov.ua/tender/{tenderID}"
        customer = json_data.get('procuringEntity', {}).get('name', 'Не указан')

        # "Початок аукціону"
        lots = json_data.get('lots', [{}])
        auctionPeriod = lots[0].get('auctionPeriod', {})
        # "Кінцевий строк подання тендерних пропозицій"
        auctionPeriod_auctionPeriod = lots[0].get('auctionPeriod', {}).get('startDate')
        if auctionPeriod_auctionPeriod:
            datetime_obj_auctionPeriod = datetime.fromisoformat(auctionPeriod_auctionPeriod)

            date_auctionPeriod = datetime_obj_auctionPeriod.strftime("%d.%m.%Y")
            time_auctionPeriod = datetime_obj_auctionPeriod.strftime("%H:%M")
        else:
            date_auctionPeriod_auctionPeriod = time_auctionPeriod_auctionPeriod = None


    if status_tender == 'active.qualification':
        status_tender = 'Кваліфікація переможця'
        tenderID = json_data.get('tenderID')
        url_tender = f"https://prozorro.gov.ua/tender/{tenderID}"
        award_value = json_data.get('awards', [{}])[0].get('value', [{}]).get('amount', None)
        award_name = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('name', None)

    print(
        f'Ссылка на тендер - {url_tender}'
        f'\nId Тендера {tender_id}'
        f'\nЗаказчик - {customer}'
        f'\nСтатус тендера  - {status_tender}'
        f'\nДата начала тендера - {date_startDate}'
        f'\nВремя начала тендера - {time_startDate}'
        f'\nЗвернення за роз’ясненнями дата - {date_enquiryPeriod_endDate}'
        f'\nЗвернення за роз’ясненнями время - {time_enquiryPeriod_endDate}'
        f'\nКінцевий строк подання тендерних пропозицій дата - {date_auctionPeriod_auctionPeriod}'
        f'\nКінцевий строк подання тендерних пропозицій время - {time_auctionPeriod_auctionPeriod}'
        f'\nАукцион дата - {date_auctionPeriod}'
        f'\nАукцион время - {time_auctionPeriod}'
        f'\nПобедитель - {award_name_customer}'
        f'\nСтавка которая победила - {award_value_customer}'
        f'\nДата победившей ставки - {date_pending}'
        f'\nВремя победившей ставки - {time_pending}'
        f'\nРозмір надання забезпечення пропозицій учасників - {guarantee_amount}'
        f'\nзабезпечення виконання договору - {bank_garantiy}'

    )


def print_key_value_pairs(obj, parent_key=''):
    if isinstance(obj, dict):
        for key, value in obj.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            print_key_value_pairs(value, full_key)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            full_key = f"{parent_key}[{index}]"
            print_key_value_pairs(value, full_key)
    else:
        print(f"{parent_key};{obj}")


if __name__ == '__main__':
    # creative_temp_folders()
    # get_all_tenders()
    # pars_all_tenders()
    # get_tender()
    # get_json_tender()
    pars_tender()

    # filename_tender = os.path.join(json_path, 'tender.json')
    # # Загрузка JSON из файла
    # with open(filename_tender, 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    #
    # print_key_value_pairs(data)
