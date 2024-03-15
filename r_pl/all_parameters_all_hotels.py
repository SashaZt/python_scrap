import asyncio
import json
import os
from datetime import datetime
import aiofiles
from playwright.async_api import async_playwright


current_directory = os.getcwd()
temp_directory = "temp"
temp_path = os.path.join(current_directory, temp_directory)
all_hotels = os.path.join(temp_path, "all_hotels")

# Создание директории, если она не существует
os.makedirs(all_hotels, exist_ok=True)


async def save_response_json(json_response, i):
    """Асинхронно сохраняет JSON-данные в файл."""
    filename = os.path.join(all_hotels, f"response_page_{i}.json")
    async with aiofiles.open(filename, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(json_response, ensure_ascii=False, indent=4))
    print(f"Сохранён файл: {filename}")


async def log_response(response, i):
    """Логирует и сохраняет JSON-ответы от определённого URL."""
    api_url = "https://r.pl/api/bloczki/pobierz-bloczki"
    request = response.request
    if request.method == "POST" and api_url in request.url:
        try:
            json_response = await response.json()
            print(f"Получен JSON-ответ на {response.url}: {json_response}")
            # Передача данных для сохранения в файл
            # Счетчик итерации `p` будет передан из внешнего контекста
            await save_response_json(json_response, i)
        except Exception as e:
            print(f"Ошибка при получении JSON из ответа {response.url}: {e}")


async def main(url):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Устанавливаем обработчик для сбора и сохранения данных ответов
        def create_log_response_with_counter(i):
            async def log_response(response):
                api_url = "https://r.pl/api/bloczki/pobierz-bloczki"
                request = response.request
                if (
                    request.method == "POST" and api_url in request.url
                ):  # Подставьте актуальное условие URL
                    try:
                        json_response = await response.json()
                        await save_response_json(json_response, i)
                    except Exception as e:
                        print(
                            f"Ошибка при получении JSON из ответа {response.url}: {e}"
                        )

            return log_response

        # Переход на страницу, которая инициирует интересующие запросы
        response_handlers = {}  # Словарь для хранения ссылок на обработчики
        await page.goto(url)  # Замените URL на актуальный
        # Здесь нажимаем кнопку cookies
        button_cookies = '//button[@class="r-button r-button--accent r-button--hover r-button--contained r-button--only-text r-button--svg-margin-left r-consent-buttons__button cmpboxbtnyes"]'
        cookies_button = await page.query_selector(button_cookies)
        if cookies_button:
            # Кликаем по кнопке "Следующая", если она найдена
            await cookies_button.click()

        # Дождитесь загрузки страницы и элементов
        await page.wait_for_selector(
            '//a[@class="r-button r-button--primary r-button--hover r-button--text r-button--only-text r-button--svg-margin-left r-pagination__page-btn"]',
            timeout=5000,
        )

        # Найдите все элементы по селектору
        elements = await page.query_selector_all(
            '//a[@class="r-button r-button--primary r-button--hover r-button--text r-button--only-text r-button--svg-margin-left r-pagination__page-btn"]'
        )
        last_page = None
        # Проверка наличия элементов перед извлечением текста
        if elements:
            # Получите текст из последнего элемента
            last_page = int(await elements[-1].text_content()) + 1
            print(last_page)
        else:
            print("Элементы не найдены")
        # Итерация по страницам

        for i in range(1, last_page):
            print(i)
            # Создаем обработчик и сохраняем его в словарь
            handler = create_log_response_with_counter(i)
            response_handlers[i] = handler
            page.on("response", handler)
            # Для каждой итерации устанавливаем свой обработчик с уникальным счетчиком

            next_button_selector = '//a[@class="r-button r-button--accent r-button--hover r-button--contained r-button--icon r-button--svg-margin-left r-button-circle r-button-circle--small r-pagination__btn r-pagination__btn--next"]'

            # Проверяем, доступна ли кнопка "Следующая"
            next_button = await page.query_selector(next_button_selector)
            if i == 1:
                buttons = await page.query_selector_all(
                    '//a[@class="r-button r-button--primary r-button--hover r-button--text r-button--only-text r-button--svg-margin-left r-pagination__page-btn r-pagination__page-btn--active"]'
                )

                # Проверяем, что список элементов не пустой
                if buttons:
                    # Нажимаем на первый элемент в списке
                    await buttons[0].click()

            elif i > 1:
                if next_button:
                    # Кликаем по кнопке "Следующая", если она найдена
                    await next_button.click()
                    # Ожидаем загрузку следующей страницы или определенный элемент на следующей странице
                    await page.wait_for_load_state("networkidle")
                    page.remove_listener("response", response_handlers[i - 1])
            await asyncio.sleep(5)
            if last_page in response_handlers:
                page.remove_listener("response", response_handlers[last_page])

        await browser.close()

print("Вставьте ссылку")
url = input()
asyncio.run(main(url))
