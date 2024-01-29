# import csv
# import json
# from pathlib import Path
# import concurrent.futures
# from bs4 import BeautifulSoup
#
#
# def parsing_product():
#     path = Path('c:/Data_olekmotocykle/').glob('*.html')
#     # files_html = glob.glob(targetPattern)
#     data = []
#     with open('output.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['id_product', 'name', 'brandName', 'gtin', 'brutto_price', 'netto_price'])
#         for item in path:
#
#             with open(item, encoding="utf-8") as file:
#                 src = file.read()
#             soup = BeautifulSoup(src, 'lxml')
#             script_tag = soup.find('script', {'id': 'datablock1'})
#             try:
#                 json_content = script_tag.contents[0].strip().replace('},\n}\n}', '}\n}\n}')
#             except:
#                 print(item)
#                 continue
#             try:
#                 data = json.loads(json_content)
#                 id_product = soup.find('div', {'class': 'product-code-ui product-code-lq'}).text
#                 name = data['itemOffered']['productName'][0]['@value']
#                 brandName = data['itemOffered']['brand']['brandName'][0]['@value']
#                 gtin = data['itemOffered']['gtin']
#                 brutto_price = soup.find('div', {'class': 'brutto-price-ui'}).text.strip().replace(" PLN", "").replace(
#                     "\nbrutto", "")
#                 netto_price = soup.find('div', {'class': 'netto-price-ui'}).text.strip().replace(" PLN", "").replace(
#                     "\nnetto", "")
#                 writer.writerow([id_product, name, brandName, gtin, brutto_price, netto_price])
#             except:
#                 print(item)
#                 continue
# if __name__ == '__main__':
#     parsing_product()
    # for item in Path('c:/Data_olekmotocykle/').glob('*.html'):
    #     item.unlink()
    # div = soup.find_all("div", {"class": "lazyslider-container-lq"})[0]
    # imgs = div.find_all("img", {"class": "open-gallery-lq"})
    #
    # urls_photo = []
    # for img in imgs:
    #     urls_photo.append('https://' + img["data-src"].replace("//", ""))
    #
    # coun = 0
    # file_path_1 = f'c:\\Data_olekmotocykle\\img\\{id_product.replace("/", "_")}.jpg'
    # file_path_2 = f'c:\\Data_olekmotocykle\\img\\{id_product.replace("/", "_")}_{coun}.jpg'
    # for u in urls_photo:
    #     """Настройка прокси серверов случайных"""
    #     proxy = random.choice(proxies)
    #     proxy_host = proxy[0]
    #     proxy_port = proxy[1]
    #     proxy_user = proxy[2]
    #     proxy_pass = proxy[3]
    #
    #     proxi = {
    #         'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
    #         'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
    #     }
    #     coun += 1
    #     if len(urls_photo) == 1:
    #         if not os.path.exists(file_path_1):
    #             try:
    #                 img_data = requests.get(u, headers=header, proxies=proxi)
    #                 with open(file_path_1, 'wb') as file_img:
    #                     file_img.write(img_data.content)
    #             except:
    #                 print(f"Ошибка при выполнении запроса для URL: {u}")
    #                 continue
    #     elif len(urls_photo) > 1:
    #         if not os.path.exists(file_path_2):
    #             img_data = requests.get(u, headers=header, proxies=proxi)
    #             with open(file_path_2, 'wb') as file_img:
    #                 file_img.write(img_data.content)


import csv
import json
from pathlib import Path
from bs4 import BeautifulSoup
import concurrent.futures
import pandas as pd


def process_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    script_tag = soup.find('script', {'id': 'datablock1'})
    try:
        json_content = script_tag.contents[0].strip().replace('},\n}\n}', '}\n}\n}').replace('\\', '\\\\')
        data = json.loads(json_content)
        id_product = soup.find('div', {'class': 'product-code-ui product-code-lq'}).text
        name = data['itemOffered']['productName'][0]['@value']
        brandName = data['itemOffered']['brand']['brandName'][0]['@value']
        gtin = data['itemOffered']['gtin']
        brutto_price = soup.find('div', {'class': 'brutto-price-ui'}).text.strip().replace(" PLN", "").replace(
            "\nbrutto", "")
        netto_price = soup.find('div', {'class': 'netto-price-ui'}).text.strip().replace(" PLN", "").replace("\nnetto",
                                                                                                             "")
        return [id_product, name, brandName, gtin, brutto_price, netto_price]
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None


def parsing_product():
    path = list(Path('c:/Data_olekmotocykle/').glob('*.html'))
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(process_file, path)

    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id_product', 'name', 'brandName', 'gtin', 'brutto_price', 'netto_price'])
        for result in results:
            if result is not None:
                writer.writerow(result)


def csv_excell():
    # Загрузка данных из файла CSV
    data = pd.read_csv(f'output.csv', encoding='utf-8')

    # Сохранение данных в файл XLSX
    data.to_excel(f'output.xlsx', index=False, engine='openpyxl')

if __name__ == '__main__':
    # parsing_product()
    csv_excell()
