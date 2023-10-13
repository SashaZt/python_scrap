import csv
import aiohttp
import asyncio

datas = []
category = "meskie"

async def get_page(session, url, category):
    bad_url = []
    good_url = []
    proxy = 'http://141.145.205.4:31281'
    proxy_auth = aiohttp.BasicAuth('proxy_alex', 'DbrnjhbZ88')
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    async with session.get(url, headers=header) as r: #, proxy=proxy, proxy_auth=proxy_auth
        if r.status == 200:
            good_url.append(url)
            return await r.text()
        else:
            bad_url.append(url)
            with open(f'c:\\nbsklep_pl\\csv_url\\{category}\\bad_url.csv', "a",
                      newline='', errors='ignore') as file:
                writer = csv.writer(file)
                writer.writerow(bad_url)


async def get_all(session, urls, category):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url, category))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def parse(results, counter, category):
    for i in results:
        if i != None:
            counter += 1
            with open(
                    f"c:\\nbsklep_pl\\html_product\\{category}\\0_{counter}.html",
                    "w", encoding='utf-8') as file:
                file.write(i)
        else:
            continue
    return counter


async def main(category):
    async with aiohttp.ClientSession() as session:
        with open(f'c:\\nbsklep_pl\\csv_url\\{category}\\url.csv', newline='',
                  encoding='utf-8') as files:
            csv_reader = list(csv.reader(files, delimiter=' ', quotechar='|'))
            counter = 0
            while len(csv_reader) > 0:
                url_batch = csv_reader[:100]
                urls = [row[0] for row in url_batch]
                results = await asyncio.gather(get_all(session, urls, category))
                counter = await parse(results[0], counter, category)
                csv_reader = csv_reader[100:]
                """Таймер перерыва в секундах"""
                await asyncio.sleep(30)

    # Остановить петлю событий и закрыть все async context managers
    await asyncio.sleep(0)
    await asyncio.get_running_loop().shutdown_asyncgens()


if __name__ == '__main__':
    categories = ['damskie', 'dzieciece', 'meskie']
    for category in categories:
        asyncio.run(main(category))


