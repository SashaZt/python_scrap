import csv
import random

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

useragent = UserAgent()


def main():
    url = 'https://www.enfsolar.com/directory/installer'
    usersagent = {'User-Agent': useragent.random}
    proxy_list = []
    # Перед запуском запускаем scrap_proxy.py для обновления списка проки-серверов
    with open('proxylist.csv', 'r') as files:
        reader = csv.reader(files)
        for row in reader:
            proxy_list.append(row[0])

    for i in proxy_list:

        session = requests.Session()
        session.proxies = {
            'http': f'http://{i}',
            'https': f'http://{i}'
        }
        try:
            resp = session.get(url, headers=usersagent, timeout=8, )
            if resp.status_code == 200:
                print('Рабочий прокси')
                soup = BeautifulSoup(resp.text, 'lxml')
                table = soup.find('div', class_='mk-body')
                table_continent = table.find_all('div', class_='clearfix mk-section')
                for item in table_continent:
                    country_list = item.find_all('li', class_='pull-left')
                    for j in country_list:
                        href = 'https://www.enfsolar.com' + j.find_next('a').get("href")
                        print(href)
        except:
            print('Не рабочий прокси')


if __name__ == '__main__':
    main()
