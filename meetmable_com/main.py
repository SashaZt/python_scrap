from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver

def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--proxy-server=37.233.3.100:9999')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--auto-open-devtools-for-tabs=devtools://devtools/bundled/inspector.html')

    s = Service(
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    return driver

def main():
    url = "https://www.meetmable.com/product/801442/18-chestnuts/beetroot-apple?variant=236574"

    driver = get_chromedriver()
    # Загрузка страницы
    driver.get(url)
    # Ожидание загрузки страницы
    time.sleep(5)
    # Переключение на вкладку Network
    driver.execute_script('''
        var elements = document.querySelectorAll('[aria-label="Network panel"]');
        for (var i = 0; i < elements.length; i++) {
            var element = elements[i];
            if (element.offsetWidth > 0 && element.offsetHeight > 0) {
                element.click();
                break;
            }
        }
    ''')

    # Ожидание загрузки списка запросов
    time.sleep(5)

    # Получение списка запросов
    requests = driver.execute_script('''
        var performanceEntries = performance.getEntriesByType("resource");
        var fetchRequests = [];
        for (var i=0; i < performanceEntries.length; i++) {
            var entry = performanceEntries[i];
            if (entry.initiatorType === 'fetch' || entry.initiatorType === 'xmlhttprequest') {
                fetchRequests.push(entry);
            }
        }
        return fetchRequests;
    ''')
    urls_product = []
    # Вывод списка запросов
    for request in requests:
        if "https://api.meetmable.com/v1/products/" in request['name']:
            urls_product.append(request['name'])
    print('*'*100)
    print(urls_product)













    """Рабочий"""
    # driver.execute_script('window.open("devtools://devtools/bundled/inspector.html");')
    # driver.switch_to.window(driver.window_handles[-1])
    # driver.execute_script('window.network = performance.getEntriesByType("resource").map((resource) => resource.name);')
    # requests = driver.execute_script('return window.network;')
    # print(requests)


if __name__ == '__main__':
    main()