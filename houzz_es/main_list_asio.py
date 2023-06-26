import aiohttp
import asyncio
import aiofiles
from bs4 import BeautifulSoup
import json
import os
import random
from proxi import proxies


cookies = {
    'v': '1687721221_d9571992-11d5-4336-9dc0-d4f72c061fd2_fa6ef1b560887e44b80902671f711348',
    'vct': 'en-US-CR8FlZhk8B8FlZhkSBwFlZhk4R0FlZhk4h0FlZhk',
    '_csrf': '83yI-5DFw5ed6SJ-kU9zamj6',
    'jdv': '1%2BDQmxez6x%2FavGRR',
    'prf': 'prodirDistFil%7C%7D',
    'kcan': '0',
    'kucan': '0',
    '_gid': 'GA1.2.168314078.1687721224',
    '_gat': '1',
    '_gcl_au': '1.1.146263406.1687721224',
    '_sp_ses.c905': '*',
    '_sp_id.c905': 'cb0f8adb-3e1d-4d88-9d53-f6602ce9a2c8.1687721225.1.1687721225.1687721225.94705fb4-2dd9-49a6-8cdc-393fc21e883b',
    '_uetsid': '44567e90138e11ee9f8de1ce80c9178b',
    '_uetvid': '445673a0138e11ee84520b666ab2d805',
    'IR_gbd': 'houzz.com',
    'IR_5455': '1687721224911%7C0%7C1687721224911%7C%7C',
    'ln_or': 'eyIzODE1NzE2IjoiZCJ9',
    '_pin_unauth': 'dWlkPVlUWXdPRE0xWXprdE5qVTVPQzAwWkdVekxXSXdObVV0WlRFNFpUVTNNMlJpWmpVeQ',
    'crossdevicetracking': '6de4a030-78c1-4fe2-8ffb-fe00a36b9e0c',
    '_ga': 'GA1.2.1793262285.1687721224',
    '_dc_gtm_UA-3519678-1': '1',
    '_ga_PB0RC2CT7B': 'GS1.1.1687721224.1.0.1687721226.58.0.0',
    '_gali': 'hz-page-content-wrapper',
    'hzd': '041c894e-bfc6-4995-a700-de9af7373795%3A%3A%3Abrowse_service%3A%3AGetStarted',
    'documentWidth': '878',
}

headers = {
    'authority': 'www.houzz.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru',
    'cache-control': 'no-cache',
    # 'cookie': 'v=1687721221_d9571992-11d5-4336-9dc0-d4f72c061fd2_fa6ef1b560887e44b80902671f711348; vct=en-US-CR8FlZhk8B8FlZhkSBwFlZhk4R0FlZhk4h0FlZhk; _csrf=83yI-5DFw5ed6SJ-kU9zamj6; jdv=1%2BDQmxez6x%2FavGRR; prf=prodirDistFil%7C%7D; kcan=0; kucan=0; _gid=GA1.2.168314078.1687721224; _gat=1; _gcl_au=1.1.146263406.1687721224; _sp_ses.c905=*; _sp_id.c905=cb0f8adb-3e1d-4d88-9d53-f6602ce9a2c8.1687721225.1.1687721225.1687721225.94705fb4-2dd9-49a6-8cdc-393fc21e883b; _uetsid=44567e90138e11ee9f8de1ce80c9178b; _uetvid=445673a0138e11ee84520b666ab2d805; IR_gbd=houzz.com; IR_5455=1687721224911%7C0%7C1687721224911%7C%7C; ln_or=eyIzODE1NzE2IjoiZCJ9; _pin_unauth=dWlkPVlUWXdPRE0xWXprdE5qVTVPQzAwWkdVekxXSXdObVV0WlRFNFpUVTNNMlJpWmpVeQ; crossdevicetracking=6de4a030-78c1-4fe2-8ffb-fe00a36b9e0c; _ga=GA1.2.1793262285.1687721224; _dc_gtm_UA-3519678-1=1; _ga_PB0RC2CT7B=GS1.1.1687721224.1.0.1687721226.58.0.0; _gali=hz-page-content-wrapper; hzd=041c894e-bfc6-4995-a700-de9af7373795%3A%3A%3Abrowse_service%3A%3AGetStarted; documentWidth=878',
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


async def get_requests(session, url):
    data_url = []

    group = url.split('/')[-2]
    print(f'Собираем категорию {group}')

    proxy = random.choice(proxies)
    ip, port, user, password = proxy
    proxy_auth_str = f'http://{user}:{password}@{ip}:{port}'

    async with session.get(url, headers=headers, cookies=cookies, proxy=proxy_auth_str) as response:
        src = await response.text()

    soup = BeautifulSoup(src, 'lxml')
    script_json = soup.find('script', type="application/json")
    data_json = json.loads(script_json.string)
    try:
        pagination_total = int(
            data_json['data']['stores']['data']['ViewProfessionalsStore']['data']['paginationSummary']['total'].replace(
                ',', ''))
    except:
        print(f'Нет данных в категории {group}')
        return

    amount_page = pagination_total // 15
    print(f"{pagination_total} а файлов будет {amount_page + 2}")
    coun = 0
    for i in range(1, amount_page + 2):
        if i == 1:
            filename = f"c:\\DATA\\houzz_com\\list\\{group}\\data_{coun}.html"
            if not os.path.exists(filename):
                url_first = url
                async with session.get(url_first, headers=headers, cookies=cookies, proxy=proxy_auth_str) as response:
                    response_text = await response.text()
                async with aiofiles.open(filename, mode='w', encoding='utf-8') as f:
                    await f.write(response_text)
                async with aiofiles.open('log.txt', 'a') as f:
                    await f.write(f'{url_first}\n')
        elif i > 1:
            coun += 15
            filename = f"c:\\DATA\\houzz_com\\list\\{group}\\data_{coun}.html"
            if not os.path.exists(filename):
                urls = f'{url}?fi={coun}'
                async with session.get(urls, headers=headers, cookies=cookies, proxy=proxy_auth_str) as response:
                    response_text = await response.text()
                async with aiofiles.open(filename, mode='w', encoding='utf-8') as f:
                    await f.write(response_text)
                async with aiofiles.open('log.txt', 'a') as f:
                    await f.write(f'{urls}\n')
        print(f'Группа {group} осталось {pagination_total - coun} ')

    print('Собрали все html')


async def main():
    urls = [
        'https://www.houzz.com/professionals/home-remodeling/probr0-bo~t_34257',
        'https://www.houzz.com/professionals/home-additions-and-extensions/probr0-bo~t_34259',
        'https://www.houzz.com/professionals/stone-pavers-and-concrete/probr0-bo~t_11824',
        'https://www.houzz.com/professionals/specialty-contractors/probr0-bo~t_11811',
        # 'https://www.houzz.com/professionals/staircases/probr0-bo~t_11839',
        # 'https://www.houzz.com/professionals/wine-cellars/probr0-bo~t_11841',
        # 'https://www.houzz.com/professionals/custom-countertops/probr0-bo~t_33909',
        # 'https://www.houzz.com/professionals/tile-and-stone-contractors/probr0-bo~t_33910',
        # 'https://www.houzz.com/professionals/basement-remodelers/probr0-bo~t_34261',
        # 'https://www.houzz.com/professionals/bedding-and-bath/probr0-bo~t_11806',
        # 'https://www.houzz.com/professionals/cabinets/probr0-bo~t_11829',
        # 'https://www.houzz.com/professionals/carpenter/probr0-bo~t_11831',
        # 'https://www.houzz.com/professionals/carpet-and-flooring/probr0-bo~t_11799',
        # 'https://www.houzz.com/professionals/doors/probr0-bo~t_11827',
        # 'https://www.houzz.com/professionals/environmental-services-and-restoration/probr0-bo~t_11813',
        # 'https://www.houzz.com/professionals/hardwood-flooring-dealers/probr0-bo~t_28349',
        # 'https://www.houzz.com/professionals/furniture-and-accessories/probr0-bo~t_11802',
        # 'https://www.houzz.com/professionals/furniture-refinishing-and-upholstery/probr0-bo~t_11840',
        # 'https://www.houzz.com/professionals/glass-and-shower-door-dealers/probr0-bo~t_27203',
        # 'https://www.houzz.com/professionals/ironwork/probr0-bo~t_11834',
        # 'https://www.houzz.com/professionals/kitchen-and-bath-fixtures/probr0-bo~t_11804',
        # 'https://www.houzz.com/professionals/lighting/probr0-bo~t_11794',
        # 'https://www.houzz.com/professionals/windows/probr0-bo~t_11797',
        # 'https://www.houzz.com/professionals/universal-design/probr0-bo~t_34260',
        # 'https://www.houzz.com/professionals/backyard-courts/probr0-bo~t_11838',
        # 'https://www.houzz.com/professionals/decks-and-patios/probr0-bo~t_11830',
        # 'https://www.houzz.com/professionals/driveways-and-paving/probr0-bo~t_11832',
        # 'https://www.houzz.com/professionals/fencing-and-gates/probr0-bo~t_11833',
        # 'https://www.houzz.com/professionals/garden-and-landscape-supplies/probr0-bo~t_11809',
        # 'https://www.houzz.com/professionals/lawn-and-sprinklers/probr0-bo~t_11835',
        # 'https://www.houzz.com/professionals/hot-tub-and-spa-dealers/probr0-bo~t_28350',
        # 'https://www.houzz.com/professionals/outdoor-lighting-and-audio-visual-systems/probr0-bo~t_11836',
        # 'https://www.houzz.com/professionals/outdoor-play/probr0-bo~t_11837',
        # 'https://www.houzz.com/professionals/spa-and-pool-maintenance/probr0-bo~t_28351',
        # 'https://www.houzz.com/professionals/pools-and-spas/probr0-bo~t_11795',
        # 'https://www.houzz.com/professionals/tree-service/probr0-bo~t_11821',
        # 'https://www.houzz.com/professionals/custom-closet-designers/probr0-bo~t_33907',
        # 'https://www.houzz.com/professionals/professional-organizers/probr0-bo~t_33908',
        # 'https://www.houzz.com/professionals/artist-and-artisan/probr0-bo~t_11801',
        # 'https://www.houzz.com/professionals/handyman/probr0-bo~t_27204',
        # 'https://www.houzz.com/professionals/home-staging/probr0-bo~t_11789',
        # 'https://www.houzz.com/professionals/movers/probr0-bo~t_27206',
        # 'https://www.houzz.com/professionals/paint-and-wall-coverings/probr0-bo~t_11807',
        # 'https://www.houzz.com/professionals/painters/probr0-bo~t_27105',
        # 'https://www.houzz.com/professionals/photographer/probr0-bo~t_11792',
        # 'https://www.houzz.com/professionals/agents-and-brokers/probr0-bo~t_11822',
        # 'https://www.houzz.com/professionals/roofing-and-gutter/probr0-bo~t_11819',
        # 'https://www.houzz.com/professionals/window-coverings/probr0-bo~t_11798',
        # 'https://www.houzz.com/professionals/appliances/probr0-bo~t_11810',
        # 'https://www.houzz.com/professionals/electrical-contractors/probr0-bo~t_11818',
        # 'https://www.houzz.com/professionals/home-media/probr0-bo~t_11787',
        # 'https://www.houzz.com/professionals/hvac-contractors/probr0-bo~t_11814',
        # 'https://www.houzz.com/professionals/plumbing-contractors/probr0-bo~t_11817',
        # 'https://www.houzz.com/professionals/septic-tanks-and-systems/probr0-bo~t_11815',
        # 'https://www.houzz.com/professionals/solar-energy-contractors/probr0-bo~t_11816',
        # 'https://www.houzz.com/professionals/carpet-cleaners/probr0-bo~t_27201',
        # 'https://www.houzz.com/professionals/chimney-cleaners/probr0-bo~t_27200',
        # 'https://www.houzz.com/professionals/exterior-cleaners/probr0-bo~t_27202',
        # 'https://www.houzz.com/professionals/house-cleaners/probr0-bo~t_27205',
        # 'https://www.houzz.com/professionals/rubbish-removal/probr0-bo~t_11820',
        # 'https://www.houzz.com/professionals/pest-control/probr0-bo~t_27207',
        # 'https://www.houzz.com/professionals/window-cleaners/probr0-bo~t_27209'
    ]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(get_requests(session, url)))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
