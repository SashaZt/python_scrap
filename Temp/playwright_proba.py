import asyncio
import aiohttp
import json
from playwright.async_api import async_playwright

headers = {
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.anofm.ro/lmvw.html?agentie=&categ=3&subcateg=1&id_lmv=2413790',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.anofm.ro/lmvw.html?agentie=&categ=3&subcateg=1")

        async with aiohttp.ClientSession() as session:  # Создание aiohttp сессии
            for i in range(1, 9):
                selector_tr = f"//tbody[@id='tableRepeat2']//tr[{i}]"
                await page.wait_for_selector(selector_tr)
                await page.click(selector_tr)
                await asyncio.sleep(1)

                selector_id = '//h5[@class="modal-title text-dark"]'
                await page.wait_for_selector(selector_id)
                text_tr = await page.locator(selector_id).inner_text()
                id_company = int(text_tr.replace('ID oferta: ', ''))

                params = {'id_lmv': str(id_company)}

                # Выполнение асинхронного GET запроса
                async with session.get('https://www.anofm.ro/dmxConnect/api/oferte_bos/detalii_lmv_test.php',
                                       params=params, headers=headers) as response:
                    json_data = await response.json()

                    with open(f'{id_company}.json', 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл

                button_close = '//*[@id="modal1"]/div/div/div[4]/button[2]'
                await page.wait_for_selector(button_close)
                await page.click(button_close)

        await browser.close()

        # await asyncio.sleep(1)
        # await page.type('xpath=//input[@id="loginForm:password"]', 'GEkz54x!')
        # # Отправка формы (нажатие Enter)
        # await page.press('xpath=//input[@id="loginForm:password"]', 'Enter')
        # await asyncio.sleep(1)
        # await page.goto("https://ua.e-cat.intercars.eu/ru/vehicle/full-offer")
        # await asyncio.sleep(10)
        # if os.path.exists('data.csv'):
        #     os.remove('data.csv')
        # with open(f'C:\\scrap_tutorial-master\\intercars_eu\\price.csv', newline='', encoding='utf-8') as files:
        #     csv_reader = list(csv.reader(files, delimiter=';', quotechar='|'))
        #
        # for start in csv_reader[0:5]:
        #     value = start[0]  # Значение из второго столбца
        #
        #     # Ожидание элемента и очистка поля
        #     await page.wait_for_selector('xpath=//input[@name="query"]')
        #     await page.focus('xpath=//input[@name="query"]')
        #     await page.keyboard.press('Control+a')
        #     await page.keyboard.press('Delete')
        #
        #     # Ввод данных
        #     await page.type('xpath=//input[@name="query"]', value)
        #     await page.press('xpath=//input[@name="query"]', 'Enter')
        #
        #     # Возможно, выполнение дополнительных действий
        #
        #     await asyncio.sleep(1)  # заменяет time.sleep(1)
        #     try:
        #         all_products = await page.query_selector_all('.listingcollapsed__activenumbercontainer')
        #     except:
        #         print("Продукты не найдены")
        #         return
        #
        #         # Выбор первого продукта из списка
        #     try:
        #         first_product = all_products[0]
        #         find_product_anchor = await first_product.query_selector('a')
        #         find_product = await find_product_anchor.get_attribute('data-id')
        #         print(f'{find_product} то что найдено')
        #     except IndexError:
        #         print("Нет продуктов в списке")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
