import json
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium import webdriver
import random
from fake_useragent import UserAgent

# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

proxies = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--proxy-server=37.233.3.100:9999')
    chrome_options.add_argument('--disable-gpu')
    s = Service(
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    return driver

def main():
    # url = "https://www.meetmable.com/2go-organic-snacks"
    url = "https://api.meetmable.com/v1/search?include=variants%2CproductsForVariants%2Cfilters%2Csellers&page=1&pageSize=100&sellerSlug=2go-organic-snacks&respectCustomSellerFilters=true&useNewSearch=false"
    # # Определение параметров для драйвера
    # driver = get_chromedriver()
    # # Загрузка страницы
    # driver.get(url)
    #
    # # Получение заголовков запросов
    # headers = driver.execute_script(
    #     "return JSON.stringify(window.performance.getEntriesByType('resource'), undefined, 4)")
    # headers_json = json.loads(headers)
    # # Сохранение заголовков в файл в формате JSON
    # with open('headers.json', 'w') as f:
    #     json.dump(headers_json, f)
    # driver.quit()

    with open('headers.json', 'r') as f:
        headers = json.load(f)

    headers_dict = {}
    for item in headers:
        if 'requestHeaders' in item:
            for header in item['requestHeaders']:
                headers_dict[header['name']] = header['value']

    response = requests.post(url, proxies=proxies)
    if response.status_code == 200:
        print("Получилось")
        data = response.json()
        with open(f"_.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        print(response.status_code)


if __name__ == '__main__':
    main()
