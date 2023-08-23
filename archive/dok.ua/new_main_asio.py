import aiohttp
import asyncio
from pathlib import Path
import csv
import os
import ssl

import random
from proxi import proxies
from headers_cookies_aiso import headers
# from headers_cookies_aiso_rus import headers
coun = 0
delta = '''
avtoshampuni
bity
bokorezy
boltorezy
buksirovochnyy_tros
distillirovannaya_voda
domkraty
dozhd
fm_modulyatory
germetik
gruzovye_boksy
gubki_mochalki
homuty
kamery_zadnego_vida
kanistra
klei
klemmi_akkumuliatora
kleshchi
kompressory_avtomobilnye
kreplenie_dlya_velosipeda_na_avto
krepleniya_dlya_lyzh_i_snoubordov
kruglogubcy
leyki
manometry
maslo_motornoe
molotki
motornoe_maslo_dlya_mototekhniki
multituly
nabor_avtomobilista
nabor_instrumentov
napilniki
nasosy
nozhi_montazhnye
nozhnicy_po_metallu
ochistiteli_dvigatelya_naruzhnye
ochistiteli_karbiuratora
ochistiteli_kondicionera
ochistiteli_ruk
ochistiteli_salona
ochistiteli_tormoznoy_sistemy
ochki_zashchitnye
ognetushitel
omyvatel
otvertki
parktroniki
passatizhi
'''
# folders = 'passatizhi'
delta_list = delta.strip().split("\n")
async def fetch(session, url, coun, folders):
    proxy = random.choice(proxies)
    proxy_host = proxy[0]
    proxy_port = proxy[1]
    proxy_user = proxy[2]
    proxy_pass = proxy[3]
    proxi = f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
    name_files = Path(f'c:/DATA/dok_ua/products/{folders}/ua/') / f'data_{coun}.html'
    # name_files = Path(f'c:/DATA/dok_ua/products/{folders}/rus/') / f'data_{coun}.html'
    if not os.path.exists(name_files):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)  # Используйте подходящую версию протокола
        ssl_context.verify_mode = ssl.CERT_NONE  # Отключите проверку сертификата
        try:
            async with session.get(url, headers=headers, proxy=proxi, ssl=ssl_context) as response:
                with open(name_files, "w", encoding='utf-8') as file:
                    file.write(await response.text())
        except Exception as e:
            print(f"An error occurred: {e}. Skipping this iteration.")

async def main():
    global coun
    for folders in delta_list:
        coun = 0  # Сброс счётчика для нового значения folders
        name_files = Path(f'c:/scrap_tutorial-master/archive/dok.ua/link/') / f'{folders}.csv'
        async with aiohttp.ClientSession() as session:
            with open(name_files, newline='', encoding='utf-8') as files:
                urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
            for i in range(0, len(urls), 10):
                tasks = []
                for row in urls[i:i + 10]:
                    coun += 1
                    url = row[0]
                    tasks.append(fetch(session, url, coun, folders))  # передаем folders как аргумент
                await asyncio.gather(*tasks)
                print(f'Completed {coun} requests for {folders}')
                await asyncio.sleep(1)

asyncio.run(main())