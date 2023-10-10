import requests
import re
from urllib.parse import urljoin
import csv
from urllib.parse import urlparse
import random


file_path = "proxies.txt"
def is_valid_url(url):
    # проверка, является ли ссылка абсолютной и не содержит ли она нежелательных элементов
    parsed = urlparse(url)
    if bool(parsed.netloc) and bool(parsed.scheme):
        if "javascript:void(0)" not in url and "tel:" not in url and "#" not in url:
            return True
    return False


def load_proxies(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if '@' in line and ':' in line]


def get_random_proxy(proxies):
    return random.choice(proxies)
proxies = load_proxies(file_path)

def find_emails(url, depth=1):
    if depth > 2:
        return []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'cookielawinfo-checkbox-necessary=yes; cookielawinfo-checkbox-functional=no; cookielawinfo-checkbox-performance=no; cookielawinfo-checkbox-analytics=no; cookielawinfo-checkbox-advertisement=no; cookielawinfo-checkbox-others=no; _ga_6YLZ4K60MS=GS1.1.1694695462.1.0.1694695462.0.0.0; _ga=GA1.2.1378876797.1694695462; _gid=GA1.2.1461157657.1694695462; _gat_gtag_UA_15926027_1=1',
        'dnt': '1',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }
    found_emails = set()  # Используем множество для хранения уникальных email-адресов

    try:
        if not url.startswith('http'):
            url = 'https://' + url  # Добавляем схему 'https://' если она отсутствует

        # Очищаем URL от некорректных символов
        url = clean_url(url)
        url = url.strip()
        url = url.replace('/\\', '')


        proxy = get_random_proxy(proxies)
        login_password, ip_port = proxy.split('@')
        login, password = login_password.split(':')
        ip, port = ip_port.split(':')
        proxy_dict = {
            "http": f"http://{login}:{password}@{ip}:{port}",
            "https": f"http://{login}:{password}@{ip}:{port}"
        }
        response = requests.get(url, headers=headers, proxies=proxy_dict)
        print(url)
        # Если запрос успешен, продолжаем
        print(response.status_code)
        if response.status_code == 200:
            content = response.text
            # filename = f"amazon.html"
            # with open(filename, "w", encoding='utf-8') as file:
            #     file.write(content)
            # exit()
            # Ищем email-адреса
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, content)

            # Проверка на валидность (простая)
            valid_emails = [email for email in emails if '.' in email.split('@')[1]]
            found_emails.update(valid_emails)  # Добавляем уникальные email-адреса во множество

            # Находим все ссылки для обхода (простой пример, без учета относительных путей и т.д.)
            link_pattern = r'href=[\'"]?([^\'" >]+)'
            links = re.findall(link_pattern, content)
            print()
            for link in links:
                full_link = urljoin(url, link)

                # Проверка на наличие специфических расширений файлов
                if any(full_link.endswith(ext) for ext in ['.png', '.ico', '.jpg', '.jpeg']):
                    continue

                # Проверка, содержит ли link url
                if url in full_link:
                    found_emails.update(find_emails(full_link, depth + 1))
        else:
            print(url)

    except Exception as e:
        print(f"An error occurred: {e}")

    return found_emails

def get_urls():
    # Открываем текстовый файл для чтения и возвращаем список URL-ов
    with open('c84f86a4225c2327.txt', 'r', encoding='utf-8') as file:
        return file.read().splitlines()

def clean_url(url):
    return re.sub(r'[^\x00-\x7F]+', '', url)

if __name__ == '__main__':
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(['URL', 'Unique Emails'])  # Записываем заголовок

        urls = get_urls()
        for url in urls:
            print(f'Переходим на сайт {url}')
            emails = find_emails(url)
            if emails:  # Проверяем, есть ли email-адреса
                writer.writerow([url, ', '.join(emails)])  # Записываем URL и уникальные email-адреса через запятую
            else:
                writer.writerow([url, 'No emails'])  # Если email-адресов нет, записываем "No emails"
