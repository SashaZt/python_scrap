from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import glob
import requests
import time
import json

"""Рабочи скрипт"""
cookies = {
    'v': '1685342053_398c990a-5e3a-4fc6-9a54-2e1738a2b82c_1fcb553b0f2c8f94c21109cd9040f041',
    '_csrf': 'tQX_Zde7kKPolFIfWRE8pxIL',
    'jdv': 't7WOzUb2vHLZtWVVHSk%2BXJMaN7ua9zR%2FUkXpY9RZDRS20RNAnLz7eLbg7JysQQXvVbYtdZ6jEQ%2FwTRwkfzK7it%2BquIxC',
    'prf': 'prodirDistFil%7C%7D',
    'cced': '1',
    'xauth': '1685342062',
    'v2': '1685342062_e996f727-364e-4c7d-be7a-10a74a80ac59_cb26317f415693fb03b109d615ea09e4',
    'g_state': '{"i_p":1685349277940,"i_l":1}',
    'ppclk': 'organicUId%3D30338175%2Cpage%3D2',
    'vct': 'es-ES-Bh4oS3RkOR8oS3RkTBwoS3Rk6R0oS3Rk6h0oS3Rk',
    'documentWidth': '1122',
    'kcan': '0',
    'hzd': '17ce7623-0051-4b44-aa1b-b6ca149842b5%3A%3A%3A%3A%3AArquitectosPonteencontactoconp',
}

headers = {
    'authority': 'www.houzz.es',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
    'cache-control': 'no-cache',
    # 'cookie': 'v=1685342053_398c990a-5e3a-4fc6-9a54-2e1738a2b82c_1fcb553b0f2c8f94c21109cd9040f041; _csrf=tQX_Zde7kKPolFIfWRE8pxIL; jdv=t7WOzUb2vHLZtWVVHSk%2BXJMaN7ua9zR%2FUkXpY9RZDRS20RNAnLz7eLbg7JysQQXvVbYtdZ6jEQ%2FwTRwkfzK7it%2BquIxC; prf=prodirDistFil%7C%7D; cced=1; xauth=1685342062; v2=1685342062_e996f727-364e-4c7d-be7a-10a74a80ac59_cb26317f415693fb03b109d615ea09e4; g_state={"i_p":1685349277940,"i_l":1}; ppclk=organicUId%3D30338175%2Cpage%3D2; vct=es-ES-Bh4oS3RkOR8oS3RkTBwoS3Rk6R0oS3Rk6h0oS3Rk; documentWidth=1122; kcan=0; hzd=17ce7623-0051-4b44-aa1b-b6ca149842b5%3A%3A%3A%3A%3AArquitectosPonteencontactoconp',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.houzz.es/professionals/arquitectos/probr0-bo~t_17749',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}
proxies = {'http': 'http://37.233.3.100:9999', 'https': 'http://37.233.3.100:9999'}
def get_category():
    response = requests.get('https://www.houzz.es/professionals/manitas/probr0-bo~t_27214', cookies=cookies, headers=headers)  # Используйте индекс 0, чтобы получить URL из списка
    src = response.text
    soup = BeautifulSoup(src, 'lxml')
    script_json = soup.find('script', type="application/json")
    data_json = json.loads(script_json.string)
    urls_all = data_json['data']['stores']['data']['NavigationStore']['data']['filters'][2]['options']
    urls = []

    for item in urls_all:
        options = item['options']
        for option in options:
            url = option['url']
            urls.append(url)

    print(urls)

def get_requests(url):
    data_url = []

    group = url.split('/')[-2]
    print(f'Собираем категорию {group}')
    response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies)
    src = response.text
    soup = BeautifulSoup(src, 'lxml')
    script_json = soup.find('script', type="application/json")
    data_json = json.loads(script_json.string)
    pagination_total = int(
        data_json['data']['stores']['data']['ViewProfessionalsStore']['data']['paginationSummary']['total'].replace('.',
                                                                                                                    ''))
    amount_page = pagination_total // 15
    print(f"Всего {pagination_total} а файлов будет {amount_page + 2}")
    coun = 0
    for i in range(1, amount_page + 2):
        if i == 1:
            filename = f"c:\\data_houzz_es\\list\\{group}\\data_{coun}.html"
            if not os.path.exists(filename):
                url_first = 'https://www.houzz.es/professionals/arquitectos/probr0-bo~t_17749'
                response = requests.get(url_first, cookies=cookies, headers=headers)
                with open(filename, "w", encoding='utf-8') as file:
                    file.write(response.text)
            else:
                continue
        elif i > 1:
            coun += 15
            filename = f"c:\\data_houzz_es\\list\\{group}\\data_{coun}.html"
            if not os.path.exists(filename):
                urls = f'{url}?fi={coun}'
                response = requests.get(urls, cookies=cookies, headers=headers)
                with open(filename, "w", encoding='utf-8') as file:
                    file.write(response.text)
            else:
                continue
        print(f'Сейчас {coun} из {pagination_total}')
        time.sleep(5)
    print('Собрали все html')


def parsing(group):
    data_url = []
    folders_html = [fr"c:\data_houzz_es\list\{group}\*.html"]
    for file in folders_html:
        files_json = glob.glob(file)
        for item in files_json:
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            try:
                products_urls = soup.find('ul', attrs={'class': 'hz-pro-search-results mb0'}).find_all('a')
            except:
                print(item)
                continue
            for u in products_urls:
                url = u.get("href")
                data_url.append([url])  # Оборачиваем URL-адрес в список

    with open(f'url/{group}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data_url)  # Записываем данные построчно

    print(f"Данные успешно записаны в файл {group}.csv.")


def drop_duplicates(group):
    all_csv = [
        f'url/{group}.csv'
    ]
    for f in all_csv:
        df = pd.read_csv(f)

        # удалить дубликаты строк и сохранить уникальные строки в новом DataFrame
        df_unique = df.drop_duplicates()

        # сохранить уникальные строки в CSV-файл
        df_unique.to_csv(f'url/{group}.csv', index=False)
    print("Дубликты удалили, переходим к обработке main_asio")


if __name__ == '__main__':
    # get_category()
    urls = ['https://www.houzz.es/professionals/arquitectos/probr0-bo~t_17749',
            'https://www.houzz.es/professionals/arquitectos-tecnicos-y-aparejadores/probr0-bo~t_23817',
            'https://www.houzz.es/professionals/contratistas/probr0-bo~t_17804',
            'https://www.houzz.es/professionals/albaniles/probr0-bo~t_17805',
            'https://www.houzz.es/professionals/empresas-de-reformas/probr0-bo~t_17794',
            'https://www.houzz.es/professionals/interioristas-y-decoradores/probr0-bo~t_17750',
            'https://www.houzz.es/professionals/instalacion-y-reformas-de-cocinas-y-banos/probr0-bo~t_17760',
            'https://www.houzz.es/professionals/paisajistas-y-diseno-de-jardines/probr0-bo~t_17757',
            'https://www.houzz.es/professionals/accesos-y-pavimentacion/probr0-bo~t_17796',
            'https://www.houzz.es/professionals/azulejos-y-encimeras/probr0-bo~t_17774',
            'https://www.houzz.es/professionals/chimeneas/probr0-bo~t_17800',
            'https://www.houzz.es/professionals/cocina-y-bano/probr0-bo~t_17776',
            'https://www.houzz.es/professionals/cortinas-persianas-y-estores/probr0-bo~t_17772',
            'https://www.houzz.es/professionals/electrodomesticos/probr0-bo~t_17784',
            'https://www.houzz.es/professionals/escaleras-y-barandillas/probr0-bo~t_17752',
            'https://www.houzz.es/professionals/iluminacion/probr0-bo~t_17766',
            'https://www.houzz.es/professionals/iluminacion-exterior-y-sistemas-audiovisuales/probr0-bo~t_17781',
            'https://www.houzz.es/professionals/materiales-de-construccion/probr0-bo~t_17788',
            'https://www.houzz.es/professionals/mobiliario-y-decoracion/probr0-bo~t_17801',
            'https://www.houzz.es/professionals/mobiliario-y-decoracion-infantiles/probr0-bo~t_17780',
            'https://www.houzz.es/professionals/patios-cubiertas-y-cercados/probr0-bo~t_17793',
            'https://www.houzz.es/professionals/pavimentos-y-muros/probr0-bo~t_17771',
            'https://www.houzz.es/professionals/piscinas-y-spas/probr0-bo~t_17768',
            'https://www.houzz.es/professionals/puertas/probr0-bo~t_17795',
            'https://www.houzz.es/professionals/ropa-de-cama-y-bano/probr0-bo~t_17787',
            'https://www.houzz.es/professionals/suelos-y-moquetas/probr0-bo~t_17791',
            'https://www.houzz.es/professionals/suministros-de-jardineria/probr0-bo~t_17803',
            'https://www.houzz.es/professionals/tapiceria/probr0-bo~t_17754',
            'https://www.houzz.es/professionals/tejados-y-canalones/probr0-bo~t_17763',
            'https://www.houzz.es/professionals/ventanas/probr0-bo~t_17770',
            'https://www.houzz.es/professionals/disenadores-y-fabricantes-de-bodegas/probr0-bo~t_17756',
            'https://www.houzz.es/professionals/artistas-y-artesanos/probr0-bo~t_17785',
            'https://www.houzz.es/professionals/carpinteros/probr0-bo~t_17790',
            'https://www.houzz.es/professionals/domotica-e-instalaciones-multimedia/probr0-bo~t_17806',
            'https://www.houzz.es/professionals/electricistas-y-antenistas/probr0-bo~t_17797',
            'https://www.houzz.es/professionals/servicios-de-limpieza/probr0-bo~t_27217',
            'https://www.houzz.es/professionals/fontaneros/probr0-bo~t_17761',
            'https://www.houzz.es/professionals/forjadores/probr0-bo~t_17777',
            'https://www.houzz.es/professionals/impermeabilizacion-y-restauracion-de-danos/probr0-bo~t_17798',
            'https://www.houzz.es/professionals/instaladores-de-energia-solar/probr0-bo~t_17758',
            'https://www.houzz.es/professionals/jardineros/probr0-bo~t_17751',
            'https://www.houzz.es/professionals/manitas/probr0-bo~t_27214',
            'https://www.houzz.es/professionals/pintores-y-empresas-de-decoracion-de-paredes/probr0-bo~t_17778',
            'https://www.houzz.es/professionals/poda-de-arboles/probr0-bo~t_17767',
            'https://www.houzz.es/professionals/rehabilitacion-de-edificios/probr0-bo~t_28484',
            'https://www.houzz.es/professionals/restauradores-de-muebles/probr0-bo~t_24619',
            'https://www.houzz.es/professionals/servicios-de-climatizacion/probr0-bo~t_17753',
            'https://www.houzz.es/professionals/servicios-de-revestimientos-y-reformas-de-exteriores/probr0-bo~t_17775',
            'https://www.houzz.es/professionals/soluciones-de-almacenamiento-y-organizadores-profesionales/probr0-bo~t_17792',
            'https://www.houzz.es/professionals/otros-servicios-especializados/probr0-bo~t_17782',
            'https://www.houzz.es/professionals/agentes-inmobiliarios/probr0-bo~t_17769',
            'https://www.houzz.es/professionals/delineantes-y-expertos-en-cad/probr0-bo~t_24581',
            'https://www.houzz.es/professionals/disenadores-industriales/probr0-bo~t_24456',
            'https://www.houzz.es/professionals/fotografos/probr0-bo~t_17764',
            'https://www.houzz.es/professionals/home-stagers/probr0-bo~t_17807',
            'https://www.houzz.es/professionals/ingenieros-de-estructuras/probr0-bo~t_28485',
            'https://www.houzz.es/professionals/escuelas-y-organizaciones/probr0-bo~t_17759',
            'https://www.houzz.es/professionals/ferias-medios-prensa-y-bloggers/probr0-bo~t_17762']
    for url in urls[:1]:
        group = url.split('/')[-2]
        # folder_path = f"c:\\data_houzz_es\\list\\{group}"
        # if os.path.exists(folder_path):
        #     continue  # Пропустить итерацию, если папка уже существует
        # os.mkdir(folder_path)
        get_requests(url)
        # parsing(group)
        # drop_duplicates(group)
        # print(f'Категория {group} готова')
        # time.sleep(10)