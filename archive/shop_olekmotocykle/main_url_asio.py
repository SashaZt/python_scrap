import asyncio
import csv
import os
import random
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, ConnectTimeout

from proxi import proxies


def get_random_proxy():
    proxy = random.choice(proxies)
    proxy_host = proxy[0]
    proxy_port = proxy[1]
    proxy_user = proxy[2]
    proxy_pass = proxy[3]
    return {
        'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
        'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
    }


def get_with_proxies(url, headers):
    max_retries = 5  # Максимальное количество попыток
    for attempt in range(max_retries):
        try:
            proxy = get_random_proxy()
            response = requests.get(url, headers=headers, proxies=proxy, timeout=5)  # Установка таймаута
            return response
        except ConnectTimeout:
            print(f"Проблема с временем ожидания соединения для прокси {proxy}. Попытка {attempt + 1}")
        except RequestException as e:
            print(f"Проблема с прокси {proxy}: {e}")
            return None
    return None  # Возвращаем None, если все попытки неудачны


async def fetch_and_save(url, header):
    max_retries = 5

    path = Path(
        'c:/Data_olekmotocykle/') / f"{url.replace('https://shop.olekmotocykle.com/', '').replace('/', '_').replace('?', '_').replace('=', '_').replace(',', '_')}.html"

    if not path.exists():
        for attempt in range(max_retries):
            response = await asyncio.get_event_loop().run_in_executor(None, get_with_proxies, url, header)
            if response and response.status_code == 200:
                with open(path, "w", encoding='utf-8') as file:
                    file.write(response.text)
                break
            else:
                print(f"Ошибка при загрузке {url}, попытка {attempt + 1}")
                await asyncio.sleep(1)


async def process_category(url, header):
    try:
        response = await asyncio.get_event_loop().run_in_executor(None, get_with_proxies, url, header)
        if not response or response.status_code != 200:
            print(f"Ошибка при загрузке страницы категории {url}")
            return

        soup = BeautifulSoup(response.text, 'lxml')
        span_tag = soup.find('span', {'class': 'page-amount-ui'})
        data_max_int = int(span_tag.text.split()[1]) if span_tag else 1

        tasks = []
        for i in range(1, data_max_int + 1):
            page_url = f'{url}?pageId={i}' if i > 1 else url
            # print(page_url)
            tasks.append(fetch_and_save(page_url, header))

        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Ошибка при обработке категории {url}: {e}")


async def main():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    current_directory = os.getcwd()
    name_files = Path(current_directory) / 'category_product.csv'
    with open(name_files, newline='', encoding='utf-8') as files:
        urls = [row[0] for row in csv.reader(files, delimiter=' ', quotechar='|')]

    tasks = [process_category(url, headers) for url in urls]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
