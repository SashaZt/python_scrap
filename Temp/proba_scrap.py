import cloudscraper
from bs4 import BeautifulSoup


def main():
    import cloudscraper
    from bs4 import BeautifulSoup
    # # Данные для прокси
    # PROXY_HOST = '193.124.190.63'
    # PROXY_PORT = 9317
    # PROXY_USER = 'rdZvZY'
    # PROXY_PASS = '4hB2v9'
    #
    # # Настройка для requests чтобы использовать прокси
    # proxies = {
    #     'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
    #     'https': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'
    # }
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })
    html = scraper.get("https://combomed.ru/antigrippin-ruzam").content
    # # print(scraper.get("https://combomed.ru/antigrippin-ruzam", proxies=proxies).text)
    soup = BeautifulSoup(html, 'html.parser')

    print(soup)

    # import requests
    # import urllib.parse
    # from bs4 import BeautifulSoup
    #
    # sa_key = '5762b6b89e9e4462baf572e921fade22'  # paste here
    # sa_api = 'https://api.scrapingant.com/v2/general'
    # qParams = {'url': 'https://combomed.ru/antigrippin-simziya', 'x-api-key': sa_key}
    # reqUrl = f'{sa_api}?{urllib.parse.urlencode(qParams)}'
    #
    # r = requests.get(reqUrl)
    # # print(r.text) # --> html
    # soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup)




if __name__ == '__main__':
    main()
