import time
import re
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from browsermobproxy import Server
server = Server(r"c:\Program Files (x86)\browsermob-proxy\bin\browsermob-proxy")
server.start()
proxy = server.create_proxy()

def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
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
    proxy.new_har("synevo", options={'captureHeaders': True, 'captureContent': True})

    url = "https://www.synevo.ua/ua/tests"
    driver = get_chromedriver()
    driver.get(url)
    time.sleep(5)
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
    time.sleep(5)
    # получить все запросы из Network panel
    requests = driver.execute_script('''
        var performanceEntries = performance.getEntriesByType("resource");
        var fetchRequests = [];
        for (var i = 0; i < performanceEntries.length; i++) {
            var entry = performanceEntries[i];
            fetchRequests.push(entry);
        }
        return fetchRequests;
    ''')

    """Рабочий для JSON файлов"""
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

    response_list = []
    # for request in requests:
    #     print(request)
        # response = requests.get(request.name)
        # response_json = response.json()
        # response_list.append(response_json)
        # print(response_json)
    curl_command = "curl "
    entries = proxy.har['log']['entries']
    for entry in entries:
        if entry['request']['url'] == 'https://www.synevo.ua/api/test/tests-by-loc':
            # Method (GET, POST, etc.)
            curl_command += "-X {} ".format(entry['request']['method'])

            # URL
            curl_command += "'{}' \\\n".format(entry['request']['url'])

            # Headers
            for header in entry['request']['headers']:
                header_name = header['name']
                header_value = header['value']
                curl_command += "  -H '{}: {}' \\\n".format(header_name, header_value)

            if entry['request']['method'] == 'POST' and 'postData' in entry['request']:
                if 'text' in entry['request']['postData']:
                    curl_command += "  --data '{}'".format(entry['request']['postData']['text'])

            break
    # Extracting cookies
    cookies_match = re.search(r"Cookie:\s(.*?)'", curl_command)
    if cookies_match:
        cookies_str = cookies_match.group(1)
        cookies_list = cookies_str.split('; ')
        cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies_list}

    # Extracting headers
    headers_match = re.findall(r"-H '(.*?)'", curl_command)
    headers = {header.split(': ')[0]: header.split(': ')[1] for header in headers_match}
    print(curl_command)
    server.stop()
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

    # """Рабочий"""
    # driver.execute_script('window.open("devtools://devtools/bundled/inspector.html");')
    # driver.switch_to.window(driver.window_handles[-1])
    # driver.execute_script('window.network = performance.getEntriesByType("resource").map((resource) => resource.name);')
    # requests = driver.execute_script('return window.network;')
    # print(requests)


if __name__ == '__main__':
    main()
