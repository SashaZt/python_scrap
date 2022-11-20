from selenium import webdriver
import time
from fake_user_agent import user_agent

# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
user_agents = user_agent()
url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent/"
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")

driver_service = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
driver = webdriver.Chrome(
    service=driver_service,
    options=options
)

try:
    driver.get(url=url)
    time.sleep(5)
    # with open("dila.html", 'w', encoding='utf-8') as file:
    #     file.write(driver.page_source)

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()
