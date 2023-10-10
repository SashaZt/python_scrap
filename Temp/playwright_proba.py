import asyncio
import os
import csv
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://ua.e-cat.intercars.eu/ru/")
        await page.type('xpath=//input[@id="loginForm:username"]', 'logisticamotoprox@gmail.com')
        await page.type('xpath=//input[@id="loginForm:password"]', 'GEkz54x!')
        # Отправка формы (нажатие Enter)
        await page.press('xpath=//input[@id="loginForm:password"]', 'Enter')
        await asyncio.sleep(1)
        await page.goto("https://ua.e-cat.intercars.eu/ru/vehicle/full-offer")
        await asyncio.sleep(10)
        if os.path.exists('data.csv'):
            os.remove('data.csv')
        with open(f'C:\\scrap_tutorial-master\\intercars_eu\\price.csv', newline='', encoding='utf-8') as files:
            csv_reader = list(csv.reader(files, delimiter=';', quotechar='|'))

        for start in csv_reader[0:5]:
            value = start[0]  # Значение из второго столбца

            # Ожидание элемента и очистка поля
            await page.wait_for_selector('xpath=//input[@name="query"]')
            await page.focus('xpath=//input[@name="query"]')
            await page.keyboard.press('Control+a')
            await page.keyboard.press('Delete')

            # Ввод данных
            await page.type('xpath=//input[@name="query"]', value)
            await page.press('xpath=//input[@name="query"]', 'Enter')

            # Возможно, выполнение дополнительных действий

            await asyncio.sleep(1)  # заменяет time.sleep(1)
            try:
                all_products = await page.query_selector_all('.listingcollapsed__activenumbercontainer')
            except:
                print("Продукты не найдены")
                return

                # Выбор первого продукта из списка
            try:
                first_product = all_products[0]
                find_product_anchor = await first_product.query_selector('a')
                find_product = await find_product_anchor.get_attribute('data-id')
                print(f'{find_product} то что найдено')
            except IndexError:
                print("Нет продуктов в списке")


        await browser.close()





if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())