from bs4 import BeautifulSoup
import csv
import os
import glob
import requests
import time
import json
"""Рабочи скрипт"""
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

def parsing():
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
    with open('data.csv', "w", errors='ignore', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\r")
        writer.writerow(("Название компании", "Телефон компании", "Сайт компании", "Оборот компании", "Адресс компании",
                         "Facebook", "Twitter", "LinkedIn", "Blog", "Услуги", "Категория"))
        for url in urls:
            group = url.split('/')[-2]
            folders_html = [fr"c:\data_houzz_es\product\{group}\*.html"]
            for file_html in folders_html:
                files_html = glob.glob(file_html)
                for item in files_html:
                    datas = []
                    with open(item, encoding="utf-8") as html_file:
                        src = html_file.read()
                    facebook_company = ""
                    twitter_company = ""
                    linkedin_company = ""
                    blog_company = ""
                    soup = BeautifulSoup(src, 'lxml')
                    script_tag = soup.find('script', {'type': 'application/json'})
                    try:
                        json_data = json.loads(script_tag.string)
                    except:
                        # print(item)
                        continue

                    try:
                        name_company = json_data['data']['stores']['data']['ProProfileStore']['data']['user']['displayName'].replace('- ', '').replace('* ', '').replace('· ', '')
                    except:
                        name_company = None
                    try:
                        telephone_company = \
                        json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional'][
                            'formattedPhone']
                    except:
                        telephone_company = None
                    try:
                        www_company = \
                        json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['rawDomain']
                    except:
                        www_company = None
                    try:
                        costEstimate_company = \
                        json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional'][
                            'costEstimate']
                    except:
                        costEstimate_company = None

                    try:
                        address_company = \
                            json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional'][
                            'formattedAddress']
                    except:
                        continue
                    address = ''
                    try:
                        category_companys = json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['seoProType']
                        soup_category = BeautifulSoup(category_companys, 'html.parser')
                        category_company = soup_category.find('span').text.strip()

                    except:
                        category_company = None
                    try:
                        soup_add = BeautifulSoup(address_company, 'html.parser')

                        address_elements = soup_add.find_all('span', itemprop='streetAddress')
                        for element in address_elements:
                            address += element.text.strip() + ' '
                    except:
                        pass

                    try:
                        service_company = json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['servicesProvided'].replace('-', '').replace('* ', '').replace('· ', '').replace('\n', '')
                    except:
                        service_company = None
                    try:
                        postal_code_element = soup_add.find('span', itemprop='postalCode')
                        if postal_code_element:
                            address += postal_code_element.text.strip() + ' '
                    except:
                        pass

                    try:
                        locality_element = soup_add.find('span', itemprop='addressLocality')
                        if locality_element:
                            address += locality_element.text.strip() + ' '
                    except:
                        pass

                    try:
                        country_element = soup_add.find('span', itemprop='addressCountry')
                        if country_element:
                            address += country_element.text.strip()
                    except:
                        pass


                    try:
                        socialLinks_company = json_data['data']['stores']['data']['ProProfileStore']['data']['user'][
                            'socialLinks']

                        for item in socialLinks_company:
                            if item['type'] == 'LINK_TYPE_FB':
                                facebook_company = item['trackedUrl']
                            elif item['type'] == 'LINK_TYPE_TWITTER':
                                twitter_company = item['trackedUrl']
                            elif item['type'] == 'LINK_TYPE_LINKEDIN':
                                linkedin_company = item['trackedUrl']
                            elif item['type'] == 'LINK_TYPE_BLOG':
                                blog_company = item['trackedUrl']
                    except:
                        continue
                    # print(name_company, telephone_company, www_company, costEstimate_company, address,
                    #               facebook_company, twitter_company, linkedin_company, blog_company, service_company, category_company)
                    datas.append([name_company, telephone_company, www_company, costEstimate_company, address,
                                  facebook_company, twitter_company, linkedin_company, blog_company, service_company, category_company])
                    writer.writerows(datas)


if __name__ == '__main__':
    parsing()