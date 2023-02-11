import csv
import re
import json
import random
import datetime
import aiohttp
import asyncio
import concurrent.futures
from math import floor
from bs4 import BeautifulSoup

datas = []


async def get_page(session, url):
    bad_url = []
    with open('proxies.csv', newline='', encoding='utf-8') as files:
        csv_reader = list(csv.reader(files, delimiter=' ', quotechar='|'))
        # print(random.choice(csv_reader))

        proxy = f'http://{random.choice(csv_reader)[0]}'
        proxy_auth = aiohttp.BasicAuth('USQ5Q5FG3', 'pN5hqMms')

        # # start_time = datetime.datetime.now()
        # proxy = 'http://141.145.205.4:31281'
        # proxy_auth = aiohttp.BasicAuth('proxy_alex', 'DbrnjhbZ88')
        header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

        }
        async with session.get(url, headers=header, proxy=proxy, proxy_auth=proxy_auth) as r:
            if r.status == 200:
                # print(proxy)
                # print(url)
                return await r.text()
            else:
                print(proxy)
                bad_url.append(url)
                with open(f"bad_url.csv", "a", newline='', errors='ignore') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        bad_url
                    )


async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    await parse(results)


async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data


async def parse(results):
    counter = 0
    for i in results:
        if i != None:
            counter += 1
            with open(f"C:\\scrap_tutorial-master\\webstaurantstore\\data\\{counter}.html", "w",
                      encoding='utf-8') as file:
                file.write(i)
        else:
            continue


if __name__ == '__main__':
    urls = [

    ]
    with open('url.csv', newline='', encoding='utf-8') as files:
        csv_reader = list(csv.reader(files, delimiter=' ', quotechar='|'))
        for row in csv_reader[:100]:
            urls.append(row[0])

    results = asyncio.run(main(urls))
    # parse(results)
