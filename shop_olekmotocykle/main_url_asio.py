import asyncio
import csv
import requests
from bs4 import BeautifulSoup

async def fetch_url(url, header):
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url, header)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_links = []
    for img in soup.find_all('img', alt=lambda x: x and '9' in x):
        a = img.find_previous('a')
        if a and 'href' in a.attrs:
            img_links.append('https://shop.olekmotocykle.com/' + a['href'])
    return img_links

async def process_category(url, header, writer):
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url, header)
    soup = BeautifulSoup(response.text, 'html.parser')
    span_tag = soup.find('span', {'class': 'page-amount-ui'})
    data_max_int = int(span_tag.text.split()[1]) if span_tag is not None else 1
    group = url.split('produkty/')[1].split(',')[0]
    # print(f'Текущая категория {group}')
    tasks = []
    for i in range(1, data_max_int + 1):
        # print(f'В категории {group} {i} из {data_max_int}')
        if i == 1:
            img_links = await fetch_url(url, header)
            writer.writerows([[img_link] for img_link in img_links])
        else:
            tasks.append(fetch_url(f'{url}?pageId={i}', header))
    if tasks:
        img_links_list = await asyncio.gather(*tasks)
        for img_links in img_links_list:
            writer.writerows([[img_link] for img_link in img_links])

async def main():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    with open(f'category_product.csv', newline='', encoding='utf-8') as files, open('url.csv', 'a', newline='', encoding='utf-8') as f:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        writer = csv.writer(f)
        tasks = []
        for row in urls: #Убрать срез
            url = row[0]
            tasks.append(process_category(url, header, writer))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())