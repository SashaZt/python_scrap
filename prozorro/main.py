import glob
import json
import os
import sqlite3
import time
from datetime import datetime, timedelta
import csv
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# from selenium import webdriver

current_directory = os.getcwd()
temp_directory = 'temp'
# Создайте полный путь к папке temp
temp_path = os.path.join(current_directory, temp_directory)
json_path = os.path.join(temp_path, 'json')
html_path = os.path.join(temp_path, 'html')

spreadsheet_id = '167BcAUM74pqhlC1Xl4MD6yKRN0OlG05cbAjF4JeYjMA'


def get_google():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    creds_file = os.path.join(current_directory, 'access.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    client = gspread.authorize(creds)
    return client, spreadsheet_id


"""Создание временых папок"""


def creative_temp_folders():
    # Убедитесь, что папки существуют или создайте их
    for folder in [temp_path, json_path, html_path]:
        if not os.path.exists(folder):
            os.makedirs(folder)


dict_comany_edrpo = {
    'ТОВ ГАМАЮНГРУП': '45159370',
    'ТОВ Гамаюн': '31610879',
    'ТОВ Гамаюн-Груп': '39537875',
    'ТОВ Компанія Гамаюн»': '37726414',
    'ФОП Волкова Наталія Іванівна': '2677614784',
    'ФОП Копошинська Алла Володимирівна': '3067116849',
    'ФОП Кушнарьов Дмитро Віталійович': '2632314232',
    'ФОП Кушнарьова Віолета Віталіївна': '2895702346',
    'ФОП Кушнарьова Олена Лоранівна': '2877203246',
    'ФОП Нєдвига Олена Русланівна': '3375108225',
    'ФОП Пальчиковська Наталія Олександрівна': '2635603285'
}

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
    url = 'https://prozorro.gov.ua/tender/UA-2023-11-09-008503-a'
    id_url = url.split('/')[-1]
    response = requests.get(url, headers=headers)
    src = response.text
    filename_tender = os.path.join(html_path, f'tender_{id_url}.html')

    with open(filename_tender, "w", encoding='utf-8') as file:
        file.write(src)


"""Парсинг одного тендера и извлечение json файла"""


def parsing_tender(tenderID):
    filename_tender = os.path.join(html_path, f'tender_{tenderID}.html')
    with open(filename_tender, encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    tender_id_full = soup.find('div', {'data-js': 'tender_sign_check'}).get('data-url')
    tender_id = tender_id_full.split('/')[-1]

    return tender_id


def get_json_tender():
    filename_tender = os.path.join(html_path, 'tender_*.html')
    filenames = glob.glob(filename_tender)
    all_objects = []
    for filename in filenames:
        with open(filename, encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        tender_id_full = soup.find('div', {'data-js': 'tender_sign_check'}).get('data-url')
        tender_id = tender_id_full.split('/')[-1]
        # response = requests.get(tender_id, headers=headers)
        response = requests.get(f"https://public-api.prozorro.gov.ua/api/2.5/tenders/{tender_id}", headers=headers)
        json_data = response.json()
        filename_tender = os.path.join(json_path, f'tender_{tender_id}.json')
        with open(filename_tender, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
        time.sleep(10)


"""Парсинг одного тендера json"""


def pars_tender():
    dick_tender = get_all_tender_records_as_dicts()

    filename_tender = os.path.join(json_path, 'tender*.json')
    filenames = glob.glob(filename_tender)
    for filename in filenames:
        with open(filename, 'r', encoding="utf-8") as f:
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
        tenderID = json_data.get('tenderID')
        tender_id = parsing_tender(tenderID)
        date_auctionPeriod = None
        time_auctionPeriod = None
        award_status = None
        bids_amount = None
        url_tender = f"https://prozorro.gov.ua/tender/{tenderID}"
        customer = json_data.get('procuringEntity', {}).get('name', None)

        """Період уточнень"""
        if status_tender == 'active.enquiries':
            status_tender = 'Період уточнень'

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

        """Подання пропозицій"""
        if status_tender == 'active.tendering':
            status_tender = 'Подання пропозицій'

            dateCreated = json_data.get('dateCreated', None)

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

        """"Пропозиції розглянуті"""
        if status_tender == 'active.awarded':
            status_tender = 'Пропозиції розглянуті'
            """Победитель ЕДРПО"""
            edrpo_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('identifier').get('id',
                                                                                                              None)
            """Победитель """
            award_name_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('name', None)
            """Ставка которая победила"""
            award_value_customer = json_data.get('awards', [{}])[0].get('value', [{}]).get('amount', None)

            """Дата и время победившей ставки"""
            dara_pending = json_data['awards'][0]['date']
            datetime_obj_pending = datetime.fromisoformat(dara_pending)
            """Дата и время победившей ставки"""
            date_pending = datetime_obj_pending.strftime("%d.%m.%Y")
            time_pending = datetime_obj_pending.strftime("%H:%M")
            award_status = json_data.get('awards', [{}])[0].get('status', None)
            if edrpo_customer in dict_comany_edrpo.values():
                if award_status == 'pending':
                    award_status = 'Очікує рішення'
                if award_status == 'active':
                    award_status = 'Переможець'
            else:
                award_status = None

        """Завершена"""
        if status_tender == 'complete':
            status_tender = 'Завершена'

            """Остаточна пропозиція"""
            # Получаем список bids из json_data
            bids = json_data.get('bids', [])
            # Проходим по каждому bid в списке
            for bid_index in range(len(bids)):
                # Получаем текущий bid по индексу
                current_bid = bids[bid_index]

                # Проверяем, есть ли 'tenderers' и это список
                tenderers = current_bid.get('tenderers', [])

                # Теперь итерируем по каждому tenderer
                for tenderer in tenderers:
                    # Извлекаем EDRPOU код tenderer
                    edrpou = tenderer.get('identifier', {}).get('id', None)

                    # Проверяем, есть ли edrpou в вашем словаре dict_comany_edrpo
                    if edrpou and edrpou in dict_comany_edrpo.values():
                        # print(f'+ Найден EDRPOU код: {edrpou}')

                        # После нахождения EDRPOU, получаем значение amount из lotValues
                        if 'lotValues' in current_bid:
                            for lotValue in current_bid['lotValues']:
                                bids_amount = lotValue.get('value', {}).get('amount', None)
                                if bids_amount is not None:
                                    continue
                                    # print(f'Сумма ставки: {bids_amount}')
                                else:
                                    continue
                                    # print('Сумма ставки не указана')
                        else:
                            continue
                            # print('Информация о lotValues отсутствует в данном bid')

                    else:
                        continue
            """Победитель """
            award_name_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('name', None)
            """Победитель ЕДРПО"""
            edrpo_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('identifier').get('id',
                                                                                                              None)
            # edrpo_customer = json_data['awards'][0]['suppliers'][0]['identifier']['id']

            """Ставка которая победила"""
            award_value_customer = json_data.get('awards', [{}])[0].get('value', [{}]).get('amount', None)
            dara_pending = json_data['awards'][0]['date']
            datetime_obj_pending = datetime.fromisoformat(dara_pending)
            """Дата и время победившей ставки"""
            date_pending = datetime_obj_pending.strftime("%d.%m.%Y")
            time_pending = datetime_obj_pending.strftime("%H:%M")
            award_status = json_data.get('awards', [{}])[0].get('status', None)
            if edrpo_customer in dict_comany_edrpo.values():
                if award_status == 'pending':
                    award_status = 'Очікує рішення'
                if award_status == 'active':
                    award_status = 'Переможець'
            else:
                award_status = None
            """Розмір надання забезпечення пропозицій учасників"""
            guarantee_amount = json_data['guarantee']['amount']
            if len(json_data.get('criteria', [])) > 10:
                criteria = json_data.get('criteria')[10]  # Теперь безопасно получаем элемент с индексом 10
                requirementGroups = criteria.get('requirementGroups', [{}])[
                    0]  # Безопасно получаем первый элемент списка
                requirements = requirementGroups.get('requirements', [{}])[0]  # Снова безопасно получаем первый элемент
                bank_garantiy = requirements.get('description', None)  # И, наконец, получаем 'description'
                """забезпечення виконання договору """
                if 'Відповідно до пункту 7 частини першої' in bank_garantiy:
                    bank_garantiy = 'Да'
                else:
                    bank_garantiy = None
            else:
                bank_garantiy = None  # Если элементов в списке 'criteria' меньше 11, возвращаем None

        """Прекваліфікація (період оскарження)"""
        if status_tender == 'active.pre-qualification.stand-still':
            status_tender = 'Прекваліфікація (період оскарження)'

        """Аукціон"""
        if status_tender == 'active.auction':
            status_tender = 'Аукціон'

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

        """Кваліфікація переможця"""
        if status_tender == 'active.qualification':
            status_tender = 'Кваліфікація переможця'

            """Победитель """
            award_name_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('name', None)
            """Ставка которая победила"""
            award_value_customer = json_data.get('awards', [{}])[0].get('value', [{}]).get('amount', None)
            dara_pending = json_data['awards'][0]['date']
            datetime_obj_pending = datetime.fromisoformat(dara_pending)
            """Дата и время победившей ставки"""
            date_pending = datetime_obj_pending.strftime("%d.%m.%Y")
            time_pending = datetime_obj_pending.strftime("%H:%M")
            """Победитель ЕДРПО"""
            edrpo_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('identifier').get('id',
                                                                                                              None)
            award_status = json_data.get('awards', [{}])[0].get('status', None)
            if edrpo_customer in dict_comany_edrpo.values():
                if award_status == 'pending':
                    award_status = 'Очікує рішення'
                if award_status == 'active':
                    award_status = 'Переможець'
            else:
                award_status = None
        """Пока поставлю для всех award_value_customer = None"""
        award_name_customer = None
        # Данные для вставки
        tender_data = {
            'tender_id': tender_id,
            'url_tender': url_tender,
            'customer': customer,
            'status_tender': status_tender,
            'date_auction': date_auctionPeriod,
            'time_auction': time_auctionPeriod,
            'bids_amount': bids_amount,
            'date_enquiryPeriod': date_enquiryPeriod_endDate,
            'time_enquiryPeriod': time_enquiryPeriod_endDate,
            'date_auctionPeriod_auctionPeriod': date_auctionPeriod_auctionPeriod,
            'time_auctionPeriod_auctionPeriod': time_auctionPeriod_auctionPeriod,
            'award_name_customer': award_name_customer,
            'award_value_customer': award_value_customer,
            'date_pending': date_pending,
            'time_pending': time_pending,
            'award_status': award_status,
            'guarantee_amount': guarantee_amount,
            'bank_garantiy': bank_garantiy

        }
        conn = sqlite3.connect('prozorro.db')
        c = conn.cursor()
        # Проверяем, существует ли уже запись с таким tender_id
        c.execute("SELECT 1 FROM tender WHERE tender_id = ?", (tender_id,))
        exists = c.fetchone()

        if not exists:
            # Если записи не существует, выполняем вставку
            sql = '''INSERT INTO tender (
                        tender_id, url_tender, customer, status_tender, date_auction, time_auction,bids_amount, date_enquiryPeriod,
                        time_enquiryPeriod, date_auctionPeriod_auctionPeriod, time_auctionPeriod_auctionPeriod,
                        award_name_customer, award_value_customer, date_pending, time_pending, award_status, guarantee_amount,
                        bank_garantiy
                     ) VALUES (
                        :tender_id, :url_tender, :customer, :status_tender, :date_auction, :time_auction, :bids_amount, :date_enquiryPeriod,
                        :time_enquiryPeriod, :date_auctionPeriod_auctionPeriod, :time_auctionPeriod_auctionPeriod,
                        :award_name_customer, :award_value_customer, :date_pending, :time_pending, :award_status, :guarantee_amount,
                        :bank_garantiy
                     )'''
            c.execute(sql, tender_data)
            conn.commit()
        else:
            print(f"Запись с tender_id {tender_id} уже существует. Пропускаем...")

        conn.close()
        # sql = '''INSERT INTO tender (
        #             tender_id, url_tender, customer, status_tender, date_auction, time_auction, date_enquiryPeriod,
        #             time_enquiryPeriod, date_auctionPeriod_auctionPeriod, time_auctionPeriod_auctionPeriod,
        #             award_name_customer, award_value_customer, date_pending, time_pending, award_status, guarantee_amount,
        #             bank_garantiy
        #          ) VALUES (
        #             :tender_id, :url_tender, :customer, :status_tender, :date_auction, :time_auction, :date_enquiryPeriod,
        #             :time_enquiryPeriod, :date_auctionPeriod_auctionPeriod, :time_auctionPeriod_auctionPeriod,
        #             :award_name_customer, :award_value_customer, :date_pending, :time_pending, :award_status, :guarantee_amount,
        #             :bank_garantiy
        #          )'''
        #
        # # Выполняем запрос
        # c.execute(sql, tender_data)
        #
        # # Сохраняем изменения
        # conn.commit()
        #
        # # Закрываем соединение с базой данных
        # conn.close()


"""Обновление БД"""


def update_tenders_from_json():
    # Получение списка текущих тендеров из базы данных
    dick_tender = get_all_tender_records_as_dicts()
    # Словарь для перевода статусов из json в читаемый вид
    dict_status_tenders = {
        'active.auction': 'Аукціон',
        'complete': 'Завершена',
        'active.qualification': 'Кваліфікація переможця',
        'active.tendering': 'Подання пропозицій',
        'active.awarded': 'Пропозиції розглянуті',
        'active.enquiries': 'Період уточнень'
    }

    filenames = glob.glob(os.path.join(json_path, 'tender*.json'))
    db_path = 'prozorro.db'
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        for filename in filenames:
            with open(filename, 'r', encoding="utf-8") as f:
                data_json = json.load(f)
            json_data = data_json.get('data', {})
            tenderID = json_data.get('tenderID')
            tender_id_json = parsing_tender(tenderID)
            status_tender_json = json_data.get('status', None)

            # Преобразование статуса и проверка на необходимость обновления
            new_status = dict_status_tenders.get(status_tender_json, "Неизвестный статус")
            for tender in dick_tender:
                if tender['tender_id'] == tender_id_json and tender['status_tender'] != new_status:

                    """Аукціон"""
                    if new_status == 'Аукціон':

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
                            # Обновление статуса и даты аукциона в базе данных
                        cursor.execute("""
                                UPDATE tender
                                SET status_tender = ?, date_auctionPeriod = ?, time_auctionPeriod = ?
                                WHERE tender_id = ?
                            """, (new_status, date_auctionPeriod, time_auctionPeriod, tender_id_json))

                        print(
                            f"Статус тендера {tender_id_json} обновлен на '{new_status}' с датой аукциона {date_auctionPeriod} и временем {time_auctionPeriod}.")

                    """Кваліфікація переможця"""
                    if new_status == 'Кваліфікація переможця':

                        """Победитель """
                        award_name_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('name',
                                                                                                             None)
                        """Ставка которая победила"""
                        award_value_customer = json_data.get('awards', [{}])[0].get('value', [{}]).get('amount', None)
                        dara_pending = json_data['awards'][0]['date']
                        datetime_obj_pending = datetime.fromisoformat(dara_pending)
                        """Дата и время победившей ставки"""
                        date_pending = datetime_obj_pending.strftime("%d.%m.%Y")
                        time_pending = datetime_obj_pending.strftime("%H:%M")
                        """Победитель ЕДРПО"""
                        edrpo_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get(
                            'identifier').get('id',
                                              None)
                        award_status = json_data.get('awards', [{}])[0].get('status', None)
                        if edrpo_customer in dict_comany_edrpo.values():
                            if award_status == 'pending':
                                award_status = 'Очікує рішення'
                            if award_status == 'active':
                                award_status = 'Переможець'
                        else:
                            award_status = None
                        cursor.execute("""
                                UPDATE tender
                                SET status_tender = ?, award_name_customer = ?, award_value_customer = ?, date_pending = ?, time_pending = ?, award_status = ?
                                WHERE tender_id = ?
                            """, (
                            new_status, award_name_customer, award_value_customer, date_pending, time_pending,
                            award_status,
                            tender_id_json))

                    """Завершена"""
                    if new_status == 'Завершена':
                        """Победитель """
                        award_name_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get('name',
                                                                                                             None)
                        """Ставка которая победила"""
                        award_value_customer = json_data.get('awards', [{}])[0].get('value', [{}]).get('amount', None)
                        dara_pending = json_data['awards'][0]['date']
                        datetime_obj_pending = datetime.fromisoformat(dara_pending)
                        """Дата и время победившей ставки"""
                        date_pending = datetime_obj_pending.strftime("%d.%m.%Y")
                        time_pending = datetime_obj_pending.strftime("%H:%M")
                        """Победитель ЕДРПО"""
                        edrpo_customer = json_data.get('awards', [{}])[0].get('suppliers', [{}])[0].get(
                            'identifier').get('id',
                                              None)
                        award_status = json_data.get('awards', [{}])[0].get('status', None)
                        if edrpo_customer in dict_comany_edrpo.values():
                            if award_status == 'pending':
                                award_status = 'Очікує рішення'
                            if award_status == 'active':
                                award_status = 'Переможець'
                        else:
                            award_status = None

                            """Розмір надання забезпечення пропозицій учасників"""
                        guarantee_amount = json_data['guarantee']['amount']
                        if len(json_data.get('criteria', [])) > 10:
                            criteria = json_data.get('criteria')[10]  # Теперь безопасно получаем элемент с индексом 10
                            requirementGroups = criteria.get('requirementGroups', [{}])[
                                0]  # Безопасно получаем первый элемент списка
                            requirements = requirementGroups.get('requirements', [{}])[
                                0]  # Снова безопасно получаем первый элемент
                            bank_garantiy = requirements.get('description', None)  # И, наконец, получаем 'description'
                            """забезпечення виконання договору """
                            if 'Відповідно до пункту 7 частини першої' in bank_garantiy:
                                bank_garantiy = 'Да'
                            else:
                                bank_garantiy = None
                        else:
                            bank_garantiy = None  # Если элементов в списке 'criteria' меньше 11, возвращаем None
                        cursor.execute("""UPDATE tender
                        SET status_tender = ?, award_name_customer = ?, award_value_customer = ?,
                        date_pending = ?, time_pending = ?, award_status = ?, guarantee_amount =?,bank_garantiy =?
                        WHERE tender_id = ? """, (
                            new_status, award_name_customer, award_value_customer, date_pending, time_pending,
                            award_status, guarantee_amount, bank_garantiy,
                            tender_id_json))

                    # # Обновление статуса в базе данных
                    # cursor.execute("UPDATE tender SET status_tender = ? WHERE tender_id = ?",
                    #                (new_status, tender_id_json))
                    # print(f"Статус тендера {tender_id_json} обновлен на '{new_status}'.")
                    break


"""Выгружает данные с БД"""


def get_all_tender_records_as_dicts():
    db_path = 'prozorro.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT tender_id, customer, status_tender FROM tender")
    records = c.fetchall()
    conn.close()
    return [dict(record) for record in records]


def export_to_csv():
    # Подключаемся к базе данных
    db_path = 'prozorro.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Выполняем SQL-запрос для выбора данных
    c.execute(
        '''SELECT tender_id, url_tender, customer, status_tender, date_auction, time_auction, date_enquiryPeriod, time_enquiryPeriod, date_auctionPeriod_auctionPeriod, time_auctionPeriod_auctionPeriod, award_name_customer, award_value_customer, date_pending, time_pending, award_status, guarantee_amount, bank_garantiy FROM tender''')

    # Получаем все строки
    rows = c.fetchall()

    # Открываем файл CSV для записи
    with open('export_to_csv.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        # Записываем заголовок
        writer.writerow([i[0] for i in c.description])

        # Записываем строки
        writer.writerows(rows)

    # Закрываем соединение с базой данных
    conn.close()


def write_to_sheet():
    client, spreadsheet_id = get_google()
    sheet = client.open_by_key(spreadsheet_id).worksheet('Тендера')
    # Подключаемся к базе данных
    db_path = 'prozorro.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Выполняем SQL-запрос для выбора данных
    c.execute(
        '''SELECT tender_id, url_tender, customer,
        status_tender, date_auction, time_auction,
         date_enquiryPeriod, time_enquiryPeriod,
         date_auctionPeriod_auctionPeriod,
         time_auctionPeriod_auctionPeriod,
         award_name_customer, award_value_customer,
         date_pending, time_pending, award_status,
         guarantee_amount, bank_garantiy FROM tender''')

    # Получаем все строки
    rows = c.fetchall()
    values = []
    for row in rows:
        # Создаем новую строку, начиная с двух пустых ячеек, и добавляем данные из базы данных
        new_row = ['', '', row[1], row[2], row[3], '', '', '', '', '',
                   '', '', '', '', '', '', row[6], row[7], row[8], row[9],
                   row[4], row[5], row[14], '', '', '', row[11]]
        values.append(new_row)

    # Обновляем данные в Google Sheets, начиная с ячейки A15
    range = 'A15'  # Укажите точный диапазон, если это необходимо
    sheet.update(values, range, value_input_option='USER_ENTERED')


if __name__ == '__main__':
    # creative_temp_folders()
    # get_all_tenders()
    # pars_all_tenders()
    # get_tender()
    # get_json_tender()
    pars_tender()
    # update_tenders_from_json()
    # write_to_sheet()
    # get_all_tender_records_as_dicts()

    # filename_tender = os.path.join(json_path, 'tender.json')
    # # Загрузка JSON из файла
    # with open(filename_tender, 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    #
    # print_key_value_pairs(data)
