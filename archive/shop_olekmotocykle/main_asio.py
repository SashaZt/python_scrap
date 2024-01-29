import asyncio
import csv
import os
import random
from pathlib import Path

import aiohttp
from aiohttp.client_exceptions import ServerDisconnectedError

from headers_cookies import headers
from proxi import proxies

coun = 0


async def fetch(session, url, coun):
    try:
        proxy = random.choice(proxies)
        proxy_host = proxy[0]
        proxy_port = proxy[1]
        proxy_user = proxy[2]
        proxy_pass = proxy[3]
        proxi = f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
        async with session.get(url, headers=headers, proxy=proxi) as response:
            name_files = Path('c:/Data_olekmotocykle/') / f'data_{coun}.html'
            if not os.path.exists(name_files):
                with open(name_files, "w", encoding='utf-8') as file:
                    file.write(await response.text())
    except ServerDisconnectedError:
        print(f"Server disconnected when fetching {url}, retrying...")
        await fetch(session, url, coun)


async def main():
    current_directory = os.getcwd()
    name_files = Path(current_directory) / 'url_product.csv'

    global coun

    async with aiohttp.ClientSession() as session:
        with open(name_files, newline='', encoding='utf-8') as files:
            urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
            for i in range(0, len(urls), 50):
                tasks = []
                for row in urls[i:i + 50]:
                    coun += 1
                    url = row[0]
                    data_file_path = Path('c:/Data_olekmotocykle/') / f'data_{coun}.html'
                    if not os.path.exists(data_file_path):
                        tasks.append(fetch(session, url, coun))
                if tasks:
                    await asyncio.gather(*tasks)
                    print(f'Completed {coun} requests')
                    await asyncio.sleep(1)


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
