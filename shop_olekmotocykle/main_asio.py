# import csv
# import os
# import re
# import requests
#
# bad_url = []
# def get_page(url):
#     proxy = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
#     header = {
#         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
#     }
#     """Get page by url"""
#     try:
#         response = requests.get(url, headers=header)
#         if response.status_code == 200:
#             return response.text
#         else:
#             bad_url.append(url)
#             with open(f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\bad_url.csv', "a",
#                       newline='', errors='ignore') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(bad_url)
#             return None
#     except requests.exceptions.RequestException as e:
#         print(e)
#         return None
#
#
# def save_html(html, counter):
#     """Save the html page with the given counter and category"""
#     filename = f"c:\\Data_olekmotocykle\\0_{counter}.html"
#     with open(filename, "w", encoding='utf-8') as f:
#         f.write(html)
#
#
# def process_url(url, counter):
#     """Process url to get page and save as html"""
#     if re.match(r'^https?://', url):
#         html = get_page(url)
#         if html is not None:
#             save_html(html, counter)
# # def check_bad_url_file():
# #     retry_count = 0
# #     while retry_count < 3:
# #         """Check if bad_url.csv exists, rename it to url.csv and remove it if it exists"""
# #         if os.path.isfile(f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\bad_url.csv'):
# #             # если файл bad_url.csv существует
# #             if os.path.isfile(f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\url.csv'):
# #                 # если файл url.csv существует, удаляем его
# #                 os.remove(f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\url.csv')
# #             # переименовываем bad_url.csv в url.csv
# #             os.rename(f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\bad_url.csv', f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\url.csv')
# #             if os.path.isfile(f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\bad_url.csv'):
# #                 # если bad_url.csv все еще существует (например, если произошла ошибка при переименовании)
# #                 # удаляем его
# #                 os.remove(f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\bad_url.csv')
# #                 retry_count += 1
# #             else:
# #                 break
#
# def main_asio():
#     counter = 0
#     with open(f'C:\\scrap_tutorial-master\\shop_olekmotocykle\\url.csv', newline='', encoding='utf-8') as files:
#         urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
#         for url in urls:
#             counter += 1
#             # print(url[0])
#             process_url(url[0], counter)
#             # print(f"ссылка {counter} из {len(urls)}")
#
#
# if __name__ == '__main__':
#     main_asio()
import csv
import os
import re
import requests

def get_page(url):
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=header)
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