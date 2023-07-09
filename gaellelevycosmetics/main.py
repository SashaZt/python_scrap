from bs4 import BeautifulSoup
import csv
import glob
import re
import requests
import json
import cloudscraper
import os
import time
import undetected_chromedriver as webdriver
from selenium.common.exceptions import TimeoutException
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv

PROXY_HOST = '37.233.3.100'
PROXY_PORT = 9999
PROXY_USER = 'proxy_alex'
PROXY_PASS = 'DbrnjhbZ88'
# proxies = {
#     'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
#     'https': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'
# }
proxies = {"http": f"http://{PROXY_HOST}:{PROXY_PORT}", f"https": f"http://{PROXY_HOST}:{PROXY_PORT}"}
cookies = {
    'session-id': '142-4156051-2826849',
    'ubid-main': '135-0200416-6965265',
    'at-main': 'Atza|IwEBIHLENpvSo6IYU2heB7riylOu6be5vQagD_ucLEFt2UfXHgiQHVZ7xRfVcAYadFi8ib8mt-fhd1yegmao8hSuX5vcEWP8gg3vLHxTzmg5uzXvxGSyEUmjGKPMaxpfVxS7lmPJiL-CS44B4NsqT3lDkNv6PSHdresvfJ2HRvm-T13KHKaJx7EG7_tIDqQQSQF_zUIUzVgqprv7DJYz47K6FNZ-YNdpZMXNnl5PJXOmHXuXBSQDNOCBi8-KIab0HR2n0mEpcJcICzFoEJouFusIupwKR7CXC3KtMWfF78u8schavw',
    'sess-at-main': '"IdhMzuGhPU5e0XmtHASAFlgyp5zJI6ZHWIaM0QVTITM="',
    'sst-main': 'Sst1|PQGEmNiYL84BFT_awTvcUbA4CQR9fQwYZi3ZP9Zj2zJ9OuZEEcAWcba5pfE9rwjuJf8cPTsosQ1pJDbvcLNoNOc8e6FNYtKBjuzLH0rlVIxNYnTsBR40DzEDWTPe8aCEmgEBOKkg-q4dys-q8YuJVZMSSd8p1xMFDqpKz9GDYngmqPY4ahBksaFRFYToIt1Opvj6OgEoJVG8m_WzcCxiIezIFTm5TOYtpYdnvCuStLOWwhmDI-aiUU6JKLIDsyQTMnuLUL91ciNgFFve9HyJL_nuD9iip3LdNdvOa6ZcOcUnE-w',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'skin': 'noskin',
    'sp-cdn': '"L5Z9:UA"',
    'lc-main': 'en_US',
    'session-token': '"055TzHoT+uUJhMJxd/kR7PGDhkhW6CEFgHhJCQBFx5VubASmBtMoeKEE/HaJ/PaERrxeVX4fxw6sfyex1Z1kBPPY2PXJZAxdeVst+sQUU0tgk6wOb9+y72D0jR2xzO0NfBkqVjbcLnMwdJ+XhMhD8oG74qNhBQkH8H6jGk3xLquT+1+js/E6jCK166CFyrK+A6dBCSd0q2FA8XpByaXWOu6eLPGrZ4UEEbJrnNxOzy8="',
    'csm-hit': 'adb:adblk_no&t:1687247536508&tb:QCF6R5T7WFZ4R58FKXWX+sa-TZ7PKAZ4SSGZNHQ5QJ5X-7HB88RE8AF4W86G1Q5Y8|1687247536508',
}

headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'session-id=142-4156051-2826849; ubid-main=135-0200416-6965265; at-main=Atza|IwEBIHLENpvSo6IYU2heB7riylOu6be5vQagD_ucLEFt2UfXHgiQHVZ7xRfVcAYadFi8ib8mt-fhd1yegmao8hSuX5vcEWP8gg3vLHxTzmg5uzXvxGSyEUmjGKPMaxpfVxS7lmPJiL-CS44B4NsqT3lDkNv6PSHdresvfJ2HRvm-T13KHKaJx7EG7_tIDqQQSQF_zUIUzVgqprv7DJYz47K6FNZ-YNdpZMXNnl5PJXOmHXuXBSQDNOCBi8-KIab0HR2n0mEpcJcICzFoEJouFusIupwKR7CXC3KtMWfF78u8schavw; sess-at-main="IdhMzuGhPU5e0XmtHASAFlgyp5zJI6ZHWIaM0QVTITM="; sst-main=Sst1|PQGEmNiYL84BFT_awTvcUbA4CQR9fQwYZi3ZP9Zj2zJ9OuZEEcAWcba5pfE9rwjuJf8cPTsosQ1pJDbvcLNoNOc8e6FNYtKBjuzLH0rlVIxNYnTsBR40DzEDWTPe8aCEmgEBOKkg-q4dys-q8YuJVZMSSd8p1xMFDqpKz9GDYngmqPY4ahBksaFRFYToIt1Opvj6OgEoJVG8m_WzcCxiIezIFTm5TOYtpYdnvCuStLOWwhmDI-aiUU6JKLIDsyQTMnuLUL91ciNgFFve9HyJL_nuD9iip3LdNdvOa6ZcOcUnE-w; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; sp-cdn="L5Z9:UA"; lc-main=en_US; session-token="055TzHoT+uUJhMJxd/kR7PGDhkhW6CEFgHhJCQBFx5VubASmBtMoeKEE/HaJ/PaERrxeVX4fxw6sfyex1Z1kBPPY2PXJZAxdeVst+sQUU0tgk6wOb9+y72D0jR2xzO0NfBkqVjbcLnMwdJ+XhMhD8oG74qNhBQkH8H6jGk3xLquT+1+js/E6jCK166CFyrK+A6dBCSd0q2FA8XpByaXWOu6eLPGrZ4UEEbJrnNxOzy8="; csm-hit=adb:adblk_no&t:1687247536508&tb:QCF6R5T7WFZ4R58FKXWX+sa-TZ7PKAZ4SSGZNHQ5QJ5X-7HB88RE8AF4W86G1Q5Y8|1687247536508',
    'device-memory': '8',
    'dnt': '1',
    'downlink': '10',
    'dpr': '1',
    'ect': '4g',
    'referer': 'https://www.amazon.com/s?i=stripbooks&rh=n%3A283155&dc&fs=true&ds=v1%3AFW8FzwCBmo65EzoRsz1El3Z1rFWVVXAAYR6kFuYqSyk&qid=1687247019&ref=sr_ex_n_1',
    'rtt': '50',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '1100',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'viewport-width': '1100',
}

params = {
    'i': 'stripbooks',
    'rh': 'n%3A283155%2Cn%3A1',
    'dc': '',
    'fs': 'true',
    'page': 2,
    'qid': '1687247117',
    'rnid': '283155',
    'ref': 'sr_pg_2',
}


# url = 'https://www.g2g.com/categories/diablo-4-boosting-service?seller=AMELIBOOST'


def get_undetected_chromedriver():
    # Обход защиты
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--proxy-server=45.14.174.253:80")
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-setuid-sandbox')
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_requests():
    import requests

    cookies = {
        'data-timeout': 'false||false',
        'tk_or': '%22%22',
        'tk_r3d': '%22%22',
        'tk_lr': '%22%22',
        'wp-wpml_current_language': 'en',
    }

    headers = {
        'authority': 'gaellelevycosmetics.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru',
        'cache-control': 'no-cache',
        # 'cookie': 'data-timeout=false||false; tk_or=%22%22; tk_r3d=%22%22; tk_lr=%22%22; wp-wpml_current_language=en',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'https://gaellelevycosmetics.com/en/shop-3/page/2/?s=dermalosophy&post_type=product&per_page=24',
        # params=params,
        cookies=cookies,
        headers=headers, )
    src = response.text
    filename = f"02.html"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(src)


def parsing():
    cookies = {
        'data-timeout': 'false||false',
        'tk_or': '%22%22',
        'tk_r3d': '%22%22',
        'tk_lr': '%22%22',
        'wp-wpml_current_language': 'en',
    }

    headers = {
        'authority': 'gaellelevycosmetics.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru',
        'cache-control': 'no-cache',
        # 'cookie': 'data-timeout=false||false; tk_or=%22%22; tk_r3d=%22%22; tk_lr=%22%22; wp-wpml_current_language=en',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    # file = f"02.html"
    # with open(file, encoding="utf-8") as file:
    #     src = file.read()
    # soup = BeautifulSoup(src, 'lxml')
    # urls = soup.find_all('h3', attrs={'class': 'wd-entities-title'})
    urls_list = ['https://gaellelevycosmetics.com/en/product/24-moist-glow-serum-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/deep-moisturizer-and-protection-25spf-for-oily-to-normal-skin80-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/block-spf-50-demi-make-up-80-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/moisturizing-and-protection-spf-50-80-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/block-spf-50-soft-clear-80-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/b-white-cream-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/b-white-concentrated-gel-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/b-white-cleanser-foam-sls-free-225-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/white-intensive-liquigel-white-intensive-liquigel-30-ml-dermalosophy-copy/',
                 'https://gaellelevycosmetics.com/en/product/white-booster-liquigel-white-booster-liquigel-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/white-activator-liquigel-white-activator-liquigel-50-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/acn-e-bio-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/ultra-moisturizing-for-oily-skin-80-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/toner-for-treating-oily-skin-100-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/acn-e-super-liquid-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/mask-for-problematic-skin-80-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/acn-e-triple-gel-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/acn-e-repair-liquid-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/deep-cleanser-for-problematic-skin-sls-free-225-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/acn-e-super-liquid-forte-50-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/eye-zone-total-repair-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/glow-gel-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/ultimate-wrinkle-repair-serum-50-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/total-repair-forte-50-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/total-repair-rx-50-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/active-hydrator-moisturizer-for-very-dry-skin-50-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/active-hydrator-moisturizer-for-normal-to-dry-skin-50-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/deep-cleanser-foam-for-all-skin-types-sls-free-225-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/gala-cream-hyaluronic-acid-50-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/skin-protector-serum-multi-vitamin-c-anti-oxidant-complex-30-ml-dermalosophy-copy/',
                 'https://gaellelevycosmetics.com/en/product/hydrate-plus-serum-new-generation-hyaluronic-fragments-30-ml-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/micropeel-recovery-cream-dermalosophy/',
                 'https://gaellelevycosmetics.com/en/product/24-moist-glow-serum-dermalosophy/']
    response = requests.get(
        'https://gaellelevycosmetics.com/en/shop-3/page/2/?s=dermalosophy&post_type=product&per_page=24',
        # params=params,
        cookies=cookies,
        headers=headers, )
    src = response.text
    soup = BeautifulSoup(src, 'lxml')

    url_img = soup.find('div', attrs={'class': 'zoom woocommerce-product-gallery__image'}).find('img').get('src')
    new_url_img = re.sub(r'(.webp).*', r'\1', url_img)

    link_tag = soup.find("link", {"rel": "alternate", "type": "application/json"})
    # извлечение href из найденного тега
    href = link_tag['href'] if link_tag else None

    response = requests.get(
        href,
        cookies=cookies,
        headers=headers, )
    json_data = response.json()
    title = json_data['title']['rendered'].replace(' &#', ' ')
    desc = json_data['excerpt']['rendered']
    soup_desc = BeautifulSoup(desc, 'lxml')
    # Используем .get_text() для извлечения только текста, все теги будут удалены
    text_only_desc = soup_desc.get_text()

    content = json_data['content']['rendered']
    soup_content = BeautifulSoup(content, 'lxml')
    text_only_content = soup_content.get_text()
    trs = soup.find_all('tr', class_='woocommerce-product-attributes-item')
    size = ''
    for tr in trs:
        # Если в элементе <span> есть текст 'Size'
        if 'Size' in tr.find('span').text.strip():
            size = tr.find('p').text.strip()
            # Извлечь и распечатать текст из элемента <p>
    print(title)
    print(text_only_desc)
    print(text_only_content)
    print(size)
    print(new_url_img)

    # script_tag = soup.find('script', {'type': 'application/ld+json'})
    # json_data = json.loads(script_tag.string)
    # filename = f"data_0.json"
    # with open(filename, 'w') as f:
    #     json.dump(json_data, f)
    # print(json_data)
    # name_product = json_data['@graph'][1]['name']
    # sku_product = json_data['@graph'][1]['sku']
    # price_product = json_data['@graph'][1]['offers'][0]['price']
    # description_product = json_data['@graph'][1]['description']
    # image_product = json_data['@graph'][1]['image']
    # brand = json_data['@graph'][1]['brand']['name']
    #
    #
    #
    # print(name_product)
    # print(sku_product)
    # print(price_product)
    # print(description_product)
    # print(image_product)
    # print(brand)


def get_cloudscraper():
    cookies = {
        'test-session': '1',
        'PHPSESSID': '2162c74cc84c8ed8e95bacd138d01f7e',
        'BVBRANDID': '620af17a-81da-42a6-8734-2797d91a1470',
        'BVBRANDSID': '1b6b5d9a-4edc-4999-a37c-212eadce092d',
    }

    headers = {
        'authority': 'app.centraldispatch.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'cache-control': 'no-cache',
        # 'cookie': 'test-session=1; PHPSESSID=2162c74cc84c8ed8e95bacd138d01f7e; BVBRANDID=620af17a-81da-42a6-8734-2797d91a1470; BVBRANDSID=1b6b5d9a-4edc-4999-a37c-212eadce092d',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        's': 'a',
        'page': '1',
        'size': '100',
        'sort': 'relevance',
        'desc': 'true',
    }
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False

    })
    r = scraper.get(
        'https://app.centraldispatch.com/company-search', params=params, cookies=cookies,
        headers=headers
    )  # , proxies=proxies
    html = r.content
    filename = f"amazon.html"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(html.decode('utf-8'))


def get_selenium():
    url = 'https://app.centraldispatch.com/company-search?s=a&page=1&size=100&sort=relevance&desc=true'
    driver = get_undetected_chromedriver()
    driver.maximize_window()
    driver.get(url)
    time.sleep(30)

    file_name = f"amazon.html"
    with open(os.path.join('data', file_name), "w", encoding='utf-8') as fl:
        fl.write(driver.page_source)


if __name__ == '__main__':
    # get_requests()
    # get_cloudscraper()
    # get_selenium()
    parsing()
