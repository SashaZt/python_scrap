import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By





chrome_options = Options()

# Без аутификации
ip_not = '37.233.3.100'
port_not = 30808

#С аутификацией
username = 'proxy_alex'
password = 'DbrnjhbZ88'
ip = '141.145.205.4'
port = 31281



proxy_aut = f'{username}:{password}@{ip}:{port}'
proxy_not_aut = f'{ip_not}:{port_not}'

options = {

    'proxy': {
        'https': f'https://{proxy_aut}',
    }
}

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),)
driver = webdriver.Chrome(ChromeDriverManager().install(),seleniumwire_options=options, options=chrome_options)
driver.get('https://2ip.ua/ru/')
ip_country = driver.find_element(By.XPATH, '//div[@class="ipblockgradient"]//div[@class="ip"]//text()').get_attribute('outerText')
time.sleep(5)
print(ip_country)
driver.close()
driver.quit()
