from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
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
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument('--auto-open-devtools-for-tabs=devtools://devtools/bundled/inspector.html')

    s = Service(
        executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    return driver

def main():
    url_product_post = []
    url = "https://www.meetmable.com/the-empowered-cookie"
    driver = get_chromedriver()
    driver.get(url)
    time.sleep(5)
    # сохраняем куки в файл cookies.pkl
    # cookies = driver.get_cookies()
    # if cookies:
    #     with open("C:\\scrap_tutorial-master\\meetmable_com\\cookies.pkl", "wb") as f:
    #         pickle.dump(cookies, f)
    # else:
    #     print("No cookies found!")
    with open('cookies.pkl', 'rb') as file:
        cookies = pickle.load(file)

    # добавляем куки в WebDriver
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)
    driver.close()
    driver.quit()
    # with open('cookies.pkl', 'rb') as file:
    #     cookies = pickle.load(file)

    # driver.execute_script('''
    #                    var elements = document.querySelectorAll('[aria-label="Network panel"]');
    #                    for (var i = 0; i < elements.length; i++) {
    #                        var element = elements[i];
    #                        if (element.offsetWidth > 0 && element.offsetHeight > 0) {
    #                            element.click();
    #                            break;
    #                        }
    #                    }
    #                ''')
    # time.sleep(5)
    # # получить все запросы с типом 'fetch' и 'xmlhttprequest' из Network panel
    # requests = driver.execute_script('''
    #     var performanceEntries = performance.getEntriesByType("resource");
    #     var fetchRequests = [];
    #     for (var i = 0; i < performanceEntries.length; i++) {
    #         var entry = performanceEntries[i];
    #         if (entry.initiatorType === 'fetch' || entry.initiatorType === 'xmlhttprequest') {
    #             fetchRequests.push(entry);
    #         }
    #     }
    #     return fetchRequests;
    # ''')
    #
    # response_list = []
    # for request in requests:
    #     print(request)
    #     # response = requests.get(request.name)
    #     # response_json = response.json()
    #     # response_list.append(response_json)
    #     # print(response_json)


    #
    # url_product_post.append(response_list)
    # # выполнить каждый запрос и сохранить response в список
    # response_list = []
    # for request in requests:
    #     print(request)
    # #     response = requests.get(request['name'])
    # #     response_list.append(response)
    # #
    # # # вывести список response
    # # print(response_list)
    #












    """Рабочий"""
    # driver.execute_script('window.open("devtools://devtools/bundled/inspector.html");')
    # driver.switch_to.window(driver.window_handles[-1])
    # driver.execute_script('window.network = performance.getEntriesByType("resource").map((resource) => resource.name);')
    # requests = driver.execute_script('return window.network;')
    # print(requests)


if __name__ == '__main__':
    main()