import asyncio
import json
import os
from datetime import datetime
import aiofiles
from playwright.async_api import async_playwright
import asyncio
import time
import aiofiles.os
import os

current_directory = os.getcwd()
temp_path = os.path.join(current_directory, "temp")
all_hotels = os.path.join(temp_path, "all_hotels")
hotel_path = os.path.join(temp_path, "hotel")

# Создание директории, если она не существует
os.makedirs(temp_path, exist_ok=True)
os.makedirs(all_hotels, exist_ok=True)
os.makedirs(hotel_path, exist_ok=True)


async def save_response_json(json_response, url_name):
    """Асинхронно сохраняет JSON-данные в файл."""
    filename = os.path.join(hotel_path, f"{url_name}.json")
    async with aiofiles.open(filename, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(json_response, ensure_ascii=False, indent=4))


async def main(url):
    timeout_selector = 10000
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Устанавливаем обработчик для сбора и сохранения данных ответов
        def create_log_response_with_counter(url_name):
            async def log_response(response):
                api_url = "https://r.pl/api/wyszukiwarka/wyszukaj-kalkulator"
                request = response.request
                if (
                    request.method == "POST" and api_url in request.url
                ):  # Подставьте актуальное условие URL
                    try:
                        json_response = await response.json()
                        await save_response_json(json_response, url_name)

                    except Exception as e:
                        print(
                            f"Ошибка при получении JSON из ответа {response.url}: {e}"
                        )

            return log_response

        
        url_name = url.split("/")[-1]
        await page.goto(url)  # Замените URL на актуальный
        # Здесь нажимаем кнопку cookies
        button_cookies = '//button[@class="r-button r-button--accent r-button--hover r-button--contained r-button--only-text r-button--svg-margin-left r-consent-buttons__button cmpboxbtnyes"]'
        await page.wait_for_selector(button_cookies, timeout=timeout_selector)
        cookies_button = await page.query_selector(button_cookies)
        if cookies_button:
            # Кликаем по кнопке "Следующая", если она найдена
            await cookies_button.click()

        # Дождитесь загрузки страницы и элементов
        await page.wait_for_selector(
            '//button[@class="r-select-button r-select-button-termin"]',
            timeout=timeout_selector,
        )
        termin_element = '//button[@class="r-select-button r-select-button-termin"]'
        # Найдите все элементы по селектору
        await page.wait_for_selector(termin_element, timeout=timeout_selector)
        element_termin = await page.query_selector(termin_element)
        # Проверка наличия элементов перед извлечением текста
        # await asyncio.sleep(5)
        if element_termin:
            await element_termin.click()
        else:
            print("Элементы не найдены")
        list_element = '//button[@class="r-tab"]'
        # Найдите все элементы по селектору
        await page.wait_for_selector(list_element, timeout=timeout_selector)
        element_list = await page.query_selector(list_element)
        # Проверка наличия элементов перед извлечением текста
        # await asyncio.sleep(5)
        if element_list:
            await element_list.click()
        else:
            print("Элементы не найдены")
        try:
            list_item = '//div[@class="kh-terminy-list__item kh-terminy-list__item--active"]'
        except:
            list_item = '//div[@class="kh-terminy-list__item"]'
        await page.wait_for_selector(list_item, timeout=timeout_selector)
        item_list = await page.query_selector_all(list_item)
        # Проверка наличия элементов перед извлечением текста
        # await asyncio.sleep(5)
        if item_list:
            await item_list[0].click()
        else:
            print("Элементы не найдены")

        # Итерация по страницам
        handler = create_log_response_with_counter(url_name)
        page.on("response", handler)
        await asyncio.sleep(1)
        await browser.close()

print("Вставьте ссылку")
url = input()
asyncio.run(main(url))
