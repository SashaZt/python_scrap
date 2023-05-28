import asyncio
import aiohttp
from aiohttp import ClientProxyConnectionError
from bs4 import BeautifulSoup
import json
import csv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import bot_token, chat_id, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

previous_low_prices = {}
previous_high_prices = {}


async def fetch_data():
    async def read_csv():
        with open(f'id.csv', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=' ', quotechar='|')
            urls = list(reader)
        return urls

    urls = await read_csv()

    async with aiohttp.ClientSession(connector=aiohttp.connector.TCPConnector(ssl=False, limit=None, force_close=True)) as session:
        for url in urls:
            futures = url[0]
            url = f'https://www.binance.com/fapi/v1/ticker/24hr?symbol={futures}'
            try:
                async with session.get(url,
                                       proxy=f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}') as response:
                    src = await response.text()
            except ClientProxyConnectionError as e:
                print(f'Failed to connect to the proxy: {PROXY_HOST}:{PROXY_PORT}')
                return

            soup = BeautifulSoup(src, 'html.parser')
            json_data = soup.string
            data = json.loads(json_data)
            symbol = data['symbol']
            high_price = float(data['highPrice'])
            low_price = float(data['lowPrice'])
            quote_volume = data['quoteVolume']

            # Сравнение значений с предыдущими значениями
            if futures in previous_low_prices and low_price < previous_low_prices[futures]:
                print(f'{symbol} минимальная: {low_price}')
                message = f'{symbol} минимальная: {low_price}'
                await send_message_to_group(message)

            if futures in previous_high_prices and high_price > previous_high_prices[futures]:
                print(f'{symbol} максимальная: {high_price}')
                message = f'{symbol} максимальная: {high_price}'
                await send_message_to_group(message)

            # Обновление предыдущих значений
            previous_low_prices[futures] = low_price
            previous_high_prices[futures] = high_price

    # Закрытие сессии и коннектора
    await session.close()


async def send_message_to_group(message):
    await bot.send_message(chat_id=chat_id, text=message)


async def main():
    while True:
        await fetch_data()
        await asyncio.sleep(3)


if __name__ == '__main__':
    asyncio.run(main())
