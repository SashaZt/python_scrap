# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.common.exceptions import TimeoutException
# # from selenium import webdriver
# import undetected_chromedriver as webdriver
# import time
# import requests
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from concurrent.futures import ThreadPoolExecutor
# # def get_chromedriver():
# #     options = webdriver.ChromeOptions()
# #
# #     options.add_argument('--disable-blink-features=AutomationControlled')
# #     options.add_argument("--disable-gpu")
# #     # options.add_experimental_option("excludeSwitches", ['enable-automation'])
# #     # chrome_options.add_argument('--disable-infobars')
# #     options.add_argument("--start-maximized")
# #     options.add_argument('--ignore-certificate-errors')
# #     options.add_argument('--ignore-ssl-errors')
# #     # options.add_argument('--disable-extensions') # Отключает использование расширений
# #     # options.add_argument('--disable-dev-shm-usage')
# #     # options.add_argument('--no-sandbox')
# #     # options.add_argument('--disable-setuid-sandbox')
# #     options.add_argument(
# #             '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
# #     service = ChromeService(executable_path='C:\\scrap_tutorial-master\\chromedriver.exe')
# #     driver = webdriver.Chrome(service=service, options=options)
# #     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
# #         'source': '''
# #             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
# #             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
# #             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
# #       '''
# #     })
# #     return driver
#
# def un():
#     import undetected_chromedriver as uc
#     driver = uc.Chrome(headless=True, use_subprocess=False)
#     driver.get('https://www.vaurioajoneuvo.fi/')
#     time.sleep(30)
#
# # def get_url():
# #     url = 'https://www.vaurioajoneuvo.fi/'
# #     driver = un()
# #     driver.maximize_window()
# #     driver.get(url)
# #     time.sleep(30)
# #     cookies = driver.get_cookies()
# #     driver.quit()
# #     s = requests.Session()
# #
# #     # Добавляем каждую куку в сессию
# #     for cookie in cookies:
# #         s.cookies.set(cookie['name'], cookie['value'])
# #
# #     # Теперь мы можем отправить запрос с этой сессией, и куки будут включены
# #     response = s.get("https://www.vaurioajoneuvo.fi/")
# #     print(response.status_code)
#
#
#
#
#
#
# if __name__ == '__main__':
#     un()
import undetected_chromedriver as uc
driver = uc.Chrome(headless=True,use_subprocess=False)
driver.get('https://www.vaurioajoneuvo.fi/')
# driver.save_screenshot('nowsecure.png')