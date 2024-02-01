import time
import json
import random
from playwright.sync_api import sync_playwright
from proxi import proxies


def save_cookies(page):
    return page.context.cookies()


def proxy_random():
    proxy = random.choice(proxies)
    proxy_host = proxy[0]
    proxy_port = proxy[1]
    proxy_user = proxy[2]
    proxy_pass = proxy[3]
    formatted_proxy = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    return {
        "server": formatted_proxy,
        # Заметьте, что для Playwright не нужно разделять на http и https
    }


def run(playwright):
    proxy = proxy_random()
    # """Так передаем один прокси для playwright"""
    # browser = playwright.chromium.launch(headless=False, proxy={
    #     'server': 'http://85.237.196.5:51523',  # Замените на ваш прокси-сервер
    #     'username': 'locomgmt',  # Имя пользователя прокси
    #     'password': 'ogzj4wAZnz'  # Пароль прокси
    # })
    """Так передаем случайные прокси для playwright"""
    browser = playwright.chromium.launch(headless=False, proxy=proxy)

    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.manyvids.com/Login/')
    # Находим элемент ввода логина и вводим значение
    page.fill('input#triggerUsername', 'calllili_one@outlook.com')
    #
    # # Находим элемент ввода пароля и вводим значение
    page.fill('input#triggerPassword', '@oK4/7o=P5usF')

    # Нажимаем Enter после ввода пароля
    page.press('input#triggerPassword', 'Enter')
    # Здесь добавьте действия для входа на сайт: ввод логина, пароля и нажатие на кнопку входа.

    time.sleep(60)
    # page.goto('https://www.manyvids.com/View-my-earnings/')
    # Сохранение куки после входа
    cookies = save_cookies(page)
    # Сохранение кук в файл
    cookies = context.cookies()
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)

    browser.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
