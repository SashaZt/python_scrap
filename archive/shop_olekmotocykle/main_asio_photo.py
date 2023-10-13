import random
import aiohttp
import asyncio
import json
import os
from proxi import proxies

async def download_image(session, url, filename, headers, proxy_dict):
    try:
        async with session.get(url, proxy=proxy_dict['http']) as response:
            with open(filename, "wb") as f:
                f.write(await response.read())
    except Exception as e:
        print(f'Error downloading {url}: {e}')

async def main():
    with open("result.json", "r") as json_file:
        result_dict = json.loads(json_file.read())

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    tasks = []
    count = 0
    async with aiohttp.ClientSession(headers=header) as session:
        for item, item_dict in result_dict.items():
            url_count = sum(key.startswith("url_") for key in item_dict.keys())
            for i in range(1, url_count + 1):
                proxy = random.choice(proxies)
                proxy_host = proxy[0]
                proxy_port = proxy[1]
                proxy_user = proxy[2]
                proxy_pass = proxy[3]
                proxy_dict = {
                    'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
                    'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
                }

                url = item_dict[f"url_{i}"]
                id_product = item_dict[f"id_{i}"].replace("/", "-")
                filename = f'c:\\Data_olekmotocykle\\img\\{id_product}.jpg'
                previous_filename = f'c:\\Data_olekmotocykle\\img\\{id_product}_{i - 1}.jpg'

                if os.path.exists(filename) or (i > 1 and os.path.exists(previous_filename)):
                    continue
                if i > 1:
                    filename = previous_filename
                tasks.append(download_image(session, url, filename, header, proxy_dict))
                count += 1

                if count % 1000 == 0:
                    print(f'Saved {count} files, waiting 10 seconds...')
                    await asyncio.sleep(1)
        if count % 1000 != 0:
            print(f'Saved {count} files, waiting 10 seconds...')
            await asyncio.sleep(1)
        await asyncio.gather(*tasks)

asyncio.run(main())