# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import requests
import json
import re
import csv
import requests
import os
import glob
import random
from proxi import proxies
from bs4 import BeautifulSoup

current_directory = os.getcwd()
temp_directory = "temp"
# Создайте полный путь к папке temp
temp_path = os.path.join(current_directory, temp_directory)
summary_path = os.path.join(temp_directory, "summary")
contact_path = os.path.join(temp_directory, "contact")


def proba():

    cookies = {
        "ARRAffinity": "9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6",
        "ARRAffinitySameSite": "9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6",
    }

    headers = {
        "authority": "obd.hcraontario.ca",
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6",
        "cache-control": "no-cache",
        # 'cookie': 'ARRAffinity=9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6; ARRAffinitySameSite=9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6',
        "dnt": "1",
        "pragma": "no-cache",
        "referer": "https://obd.hcraontario.ca/buildersearchresults?&page=1",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    response = requests.get(
        "https://obd.hcraontario.ca/api/builders?&page=1",
        cookies=cookies,
        headers=headers,
    )
    json_data = response.json()
    with open(f"test.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


def delete_old_data():
    # Убедитесь, что папки существуют или создайте их
    for folder in [temp_path, contact_path, summary_path]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def proxy_random():
    """
    Функция для случайного прокси
    """
    proxy = random.choice(proxies)
    proxy_host = proxy[0]
    proxy_port = proxy[1]
    proxy_user = proxy[2]
    proxy_pass = proxy[3]
    formatted_proxy = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    # Возвращаем словарь с прокси
    return {"http": formatted_proxy, "https": formatted_proxy}


def parsing():
    with open(f"test.json", "r") as f:
        data_json = json.load(f)
    all_accountnumber = []
    for d in data_json[:1]:
        accountnumber = d["ACCOUNTNUMBER"]
        all_accountnumber.append(accountnumber)
    return all_accountnumber


def get_summary():
    a = get_all_id()
    cookies = {
        "ARRAffinity": "9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6",
        "ARRAffinitySameSite": "9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6",
    }

    headers = {
        "authority": "obd.hcraontario.ca",
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6",
        "cache-control": "no-cache",
        # 'cookie': 'ARRAffinity=9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6; ARRAffinitySameSite=9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6',
        "dnt": "1",
        "pragma": "no-cache",
        "referer": "https://obd.hcraontario.ca/profile/B48156",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    params = {
        "id": a,
    }
    filename_summary = os.path.join(summary_path, f"{params['id']}.json")
    if not os.path.exists(filename_summary):
        proxi = proxy_random()
        response_summary = requests.get(
            "https://obd.hcraontario.ca/api/buildersummary",
            params=params,
            cookies=cookies,
            headers=headers,
            proxies=proxi,
        )

        if response_summary.status_code == 200:
            json_data = response_summary.json()
        with open(filename_summary, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)


def get_contact():
    a = get_all_id()
    cookies = {
        "ARRAffinity": "9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6",
        "ARRAffinitySameSite": "9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6",
    }

    headers = {
        "authority": "obd.hcraontario.ca",
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6",
        "cache-control": "no-cache",
        # 'cookie': 'ARRAffinity=9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6; ARRAffinitySameSite=9dbd9775f7b40d4bcba2cb924d9b50a65fe5685a62f1bd21d92e4be6e85df8c6',
        "dnt": "1",
        "pragma": "no-cache",
        "referer": "https://obd.hcraontario.ca/profile/B48156",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    params = {
        "id": a,
    }
    filename_contact = os.path.join(contact_path, f"{params['id']}.json")
    if not os.path.exists(filename_contact):
        proxi = proxy_random()
        response_contact = requests.get(
            "https://obd.hcraontario.ca/api/builderPDOs",
            params=params,
            cookies=cookies,
            headers=headers,
            proxies=proxi,
        )

        if response_contact.status_code == 200:
            json_data = response_contact.json()
        with open(filename_contact, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)


def get_all_id():
    all_data = parsing()
    for a in all_data:
        return a


def parse_contact_info(contact_info):
    if not contact_info:
        return None, None, None, None

    # Удаление указанных фраз
    phrases_to_remove = [
        "Public Contact Number",
        "Public Fax Number",
        "Public Alternate Phone Number",
    ]
    for phrase in phrases_to_remove:
        contact_info = contact_info.replace(phrase, "")

    # Ищем электронную почту
    email_match = re.search(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", contact_info
    )
    email = email_match.group(0) if email_match else None

    # Извлекаем и удаляем электронную почту из строки
    if email:
        contact_info = contact_info.replace(email, "")
    # Ищем веб-сайт
    website_match = re.search(
        r"(?:http[s]?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", contact_info
    )
    website = website_match.group(0) if website_match else None

    # Извлекаем и удаляем веб-сайт из строки
    if website:
        contact_info = contact_info.replace(website, "")

    # Ищем телефоны
    # Ищем телефоны в формате (123) 456-7890 или 123-456-7890
    phones = re.findall(
        r"\(\d{3}\)\s?\d{3}[- ]?\d{4}|\d{3}-\d{3}-\d{4}|\d{3} \d{3}-\d{4}", contact_info
    )

    # Удаляем телефоны из строки, чтобы оставить только адрес
    for phone in phones:
        contact_info = contact_info.replace(phone, "")

    address = contact_info.strip()

    # Возвращаем адрес, строку с телефонами, веб-сайт и электронную почту
    return address, ", ".join(phones), website, email


def pars():
    a = get_all_id()
    filename_contact = os.path.join(contact_path, f"{a}.json")
    filename_summary = os.path.join(summary_path, f"{a}.json")
    with open(filename_contact, "r") as f:
        data_json = json.load(f)
    with open(filename_summary, "r") as f:
        data_json = json.load(f)



    folder = os.path.join(temp_path, "*.html")

    files_html = glob.glob(folder)
    # Задаем имя выходного файла
    # Задаем имя выходного файла
    # Задаем имя выходного файла
    output_filename = "company_info.csv"

    # Проверяем, существует ли файл, и определяем, нужно ли записывать заголовки
    file_exists = os.path.isfile(output_filename)

    with open(output_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Если файл не существует, мы пишем заголовки
        writer.writerow(
            [
                "Company Name",
                "Incorporation #",
                "Licence #",
                "Licence Type",
                "Status",
                "Expiry Date",
                "Closed Date",
                "Person responsible for the company",
                "Contact Information",
            ]
        )

        for item in files_html:
            with open(item, encoding="utf-8") as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")

            # Функция для извлечения текста или возврата None, если элемент не найден
            def get_text_or_none(search_query):
                found = soup.find(string=search_query)
                return (
                    found.find_next().get_text(strip=True)
                    if found and found.find_next()
                    else None
                )

            contact_info_raw = get_text_or_none("Contact Information:")
            address, phones, website, email = parse_contact_info(contact_info_raw)

            company_info = {
                "Company Name": soup.strong.text.strip() if soup.strong else None,
                "Incorporation #": get_text_or_none("Incorporation #:"),
                "Licence #": get_text_or_none("Licence #:"),
                "Licence Type": get_text_or_none("Licence Type:"),
                "Status": get_text_or_none("Status:"),
                "Expiry Date": get_text_or_none("Expiry Date:"),
                "Closed Date": get_text_or_none("Closed Date:"),
                "Person responsible for the company": get_text_or_none(
                    "Person responsible for the company:"
                ),
                "Address": address,
                "Phone Numbers": phones,
                "Website": website,
                "Email": email,
            }

            # Записываем данные компании
            writer.writerow(company_info.values())


if __name__ == "__main__":
    # delete_old_data()
    # proba()
    # parsing()
    # pars()
    get_contact()
    get_summary()
