import csv
import os
import re
import requests
import random
def get_page(url):

    proxies = [
        ('185.112.12.122', 2831, '36675', 'g6Qply4q'),
        ('185.112.14.126', 2831, '36675', 'g6Qply4q'),
        ('185.112.15.239', 2831, '36675', 'g6Qply4q'),
        ('195.123.189.137', 2831, '36675', 'g6Qply4q'),
        ('195.123.190.104', 2831, '36675', 'g6Qply4q'),
        ('195.123.193.81', 2831, '36675', 'g6Qply4q'),
        ('195.123.194.134', 2831, '36675', 'g6Qply4q'),
        ('195.123.197.233', 2831, '36675', 'g6Qply4q'),
        ('195.123.252.157', 2831, '36675', 'g6Qply4q'),
        ('212.86.111.68', 2831, '36675', 'g6Qply4q')
    ]
    """Настройка прокси серверов случайных"""
    proxy = random.choice(proxies)
    proxy_host = proxy[0]
    proxy_port = proxy[1]
    proxy_user = proxy[2]
    proxy_pass = proxy[3]

    proxi = {
        'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
        'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
    }
    header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'isMobileDevice=0; .cdneshopsid=qyf3ftsWHDkCCEMAWo84B5PBRfA37UPj1r5BqLgIC0HwtT9qXGLaGvPtNx7JyG10P4JEPs3+gjg1PpYHoQ|004; lastCartId=-1; config-message-052fd829-3229-4b96-a597-13e6f2ebee5f=hidden; undefined=hidden; LastSeenProducts=107614,136492,180377,130232,107630,174306',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
    try:
        response = requests.get(url, headers=header, proxies=proxi)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def save_html(html, counter):
    filename = f"c:\\Data_olekmotocykle\\0_{counter}.html"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(html)

def process_url(url, counter):
    filename = f"c:\\Data_olekmotocykle\\0_{counter}.html"
    if not os.path.exists(filename):
        if re.match(r'^https?://', url):
            html = get_page(url)
            if html is not None:
                save_html(html, counter)

def main_asio():
    counter = 0
    with open(f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\url.csv', newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        for url in urls:
            counter += 1
            process_url(url[0], counter)
            print(f"ссылка {counter} из {len(urls)}")

if __name__ == '__main__':
    main_asio()