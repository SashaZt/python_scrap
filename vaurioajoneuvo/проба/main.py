from datetime import datetime
import asyncio
from bs4 import BeautifulSoup
import re
from config import bot_token, chat_id, list_urls
import csv
import requests
import random
import aiohttp
from playwright.async_api import async_playwright
from cf_clearance import async_cf_retry, async_stealth

file_path = "proxy.txt"
def load_proxies(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if '@' in line and ':' in line]


async def send_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    async with aiohttp.ClientSession() as session:
        await session.post(url, data=data)
def get_random_proxy(proxies):
    return random.choice(proxies)

async def cf_challenge():
    url_pl = 'https://www.vaurioajoneuvo.fi'
    # not use cf_clearance, cf challenge is fail
    proxies = load_proxies(file_path)
    proxy = get_random_proxy(proxies)
    login_password, ip_port = proxy.split('@')
    login, password = login_password.split(':')
    ip, port = ip_port.split(':')
    proxy_dict = {
        "http": f"http://{login}:{password}@{ip}:{port}",
        "https": f"https://{login}:{password}@{ip}:{port}"
    }
    res = requests.get(url_pl)
    assert "<title>Just a moment...</title>" in res.text
    async with async_playwright() as p:
        browser = await p.chromium.launch(proxy={
                                        "server": f"http://{ip}:{port}",
                                        "username": login,
                                        "password": password
                                    },
            headless=False,
            devtools=True,
        )
        context = await browser.new_context()
        page = await context.new_page()
        await async_stealth(page, pure=True)
        await page.goto(url_pl)
        success, cf = await async_cf_retry(page)
        if cf:
            if success:
                cookies = await page.context.cookies()
                for cookie in cookies:
                    if cookie.get("name") == "cf_clearance":
                        cf_clearance_value = cookie.get("value")
                # print(cf_clearance_value)
                ua = await page.evaluate("() => {return navigator.userAgent}")
                assert cf_clearance_value
            else:
                raise
        else:
            print("No cloudflare challenges encountered")

        await browser.close()
    # use cf_clearance, must be same IP and UA
    headers = {"user-agent": ua}
    cookies = {"cf_clearance": cf_clearance_value}
    return headers, cookies, proxy_dict
async def async_process_urls(bot_token, chat_id, list_urls):
    headers, cookies, proxy_dict = await cf_challenge()

    now = datetime.now()
    formatted_now = now.strftime("%H:%M_%d.%m.%Y")
    print(proxy_dict["http"], formatted_now)
    async with aiohttp.ClientSession() as session:
        while True:
            for url in list_urls:
                try:
                    response = await session.get(url, cookies=cookies, headers=headers, proxy=proxy_dict["http"])
                except:
                    headers, cookies, proxy_dict = await cf_challenge()
                    print(f'Смена прокси при ошибке {proxy_dict}')
                    response = await session.get(url, cookies=cookies, headers=headers, proxy=proxy_dict["http"])
                if response.status != 200:
                    headers, cookies, proxy_dict = await cf_challenge()
                    print(f'Смена прокси при статусе != 200 {proxy_dict}')
                    response = await session.get(url, cookies=cookies, headers=headers, proxy=proxy_dict["http"])
                src = await response.text()
                soup = BeautifulSoup(src, 'lxml')
                table_row = soup.find('div', attrs={'class': 'cars-list'})
                regex_containr = re.compile('.*(?=item-lift-container)')
                try:
                    item_lift_container = table_row.find_all('div', attrs={'class': 'col-12 col-lg-3 item-lift-container'})
                except:
                    continue
                if item_lift_container:  # Проверка, что список не пуст
                    file_name = 'id_ad.csv'
                    try:
                        with open(file_name, 'r', encoding='utf-8') as csvfile:
                            reader = csv.reader(csvfile)
                            id_list = [row[0] for row in reader]
                    except:
                        with open(file_name, 'a', encoding='utf-8') as csvfile:
                            reader = csv.reader(csvfile)
                    i = item_lift_container[0]
                    id_avto = i.find('div', {'class': 'item-lift'}).get('data-auction-id')
                    # print(id_avto, url)
                    if id_avto in id_list:
                        print(id_avto, id_list)
                        continue
                    else:
                        now = datetime.now()
                        formatted_now = now.strftime("%H:%M_%d.%m.%Y")
                        print(f"Новый id {id_avto}_____________{formatted_now}_____________________________")
                        # print(url)
                        with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([id_avto])
                        link = 'https://www.vaurioajoneuvo.fi' + i.find('a').get('href')
                        # Извлечь текст из блока с названием
                        title = i.find('strong').text
                        # Извлечь текст из блока с информацией о цене
                        regex_price = re.compile('item-lift-price-now auction-price-now.*')
                        try:
                            price = i.find('strong', {'class': regex_price}).text
                        except:
                            price = None
                        details_all = [span.text for span in i.find_all('span')]
                        details = f"{details_all[0]} {details_all[1]} {details_all[2]}"
                        message = f"\nURL Title: {title}\nLink: {link}\nPrice: {price}\nDetails: {details}"
                        # print(message)  # print to console

                        await send_message(bot_token, chat_id, message)
                await asyncio.sleep(60)
            # print('Паузка 5сек')

if __name__ == "__main__":

    asyncio.run(async_process_urls(bot_token, chat_id, list_urls))

# if __name__ == "__main__":
#     import asyncio
#
#     asyncio.run(cf_challenge("https://www.vaurioajoneuvo.fi/"))