# import requests
# from bs4 import BeautifulSoup
#
# # Ваш список слов, разделенных запятыми
# l = 'Грант, кредит, беззалоговый займ, мсб, банки второго уровня, Фонд Даму, Атамекен, Самрук Казына, Байтерек, акимат гранты, поддержка бизнеса, поддержка молодёжи, женщины и бизнес, безработные поддержка'
#
# # Преобразование списка слов в список Python
# words = [word.strip() for word in l.split(',')]
#
# # URL страницы, которую нужно проверить
# url = 'https://adilet.zan.kz/rus/docs/G23ZF00021M'
#
# # Получение HTML-кода страницы
# response = requests.get(url)
# html = response.text
#
# # Парсинг HTML
# soup = BeautifulSoup(html, 'html.parser')
# text = soup.get_text()
#
# # Проверка, есть ли одно из слов в тексте на странице
# for word in words:
#     if word.lower() in text.lower():
#         print(f"На странице найдено слово: {word}")
#         # Вы можете перейти на страницу, сделать скриншот, сохранить данные и т.д.
#         break
# else:
#     print("На странице не найдено ни одного из заданных слов.")


import requests
import re
from urllib.parse import urljoin
import csv
from urllib.parse import urlparse
import random

def parsing():
    visited_urls = set()
    file = "amazon.html"
    with open(file, encoding="utf-8") as file:
        src = file.read()
    found_emails = set()
    url = 'miningmx.com'
    url = url.strip()
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, src)

    # Проверка на валидность (простая)
    valid_emails = [email for email in emails if '.' in email.split('@')[1]]
    found_emails.update(valid_emails)  # Добавляем уникальные email-адреса во множество

    # Находим все ссылки для обхода (простой пример, без учета относительных путей и т.д.)
    link_pattern = r'href=[\'"]?([^\'" >]+)'
    links = re.findall(link_pattern, src)
    for link in links:
        full_link = urljoin(url, link)
        if any(full_link.endswith(ext) for ext in ['.png', '.ico', '.jpg', '.jpeg']):
            continue
        if url in full_link:
            visited_urls.add(url)
    print(visited_urls)
        # Проверка, содержит ли link url

if __name__ == '__main__':
    parsing()