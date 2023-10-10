import logging

import aiohttp
import asyncio
import clipboard

import json

# Настройка логирования
logging.basicConfig(
    filename='my_log_file.log',  # Имя файла логов
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'
)


async def cf_challenge():

    cf_clearance_value = clipboard.paste()

    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', }
    cookies = {"cf_clearance": cf_clearance_value}
    # cookies = {"cf_clearance": '_.InF5VKG8AVmq0Xy4NNv7XaK35i9bfcbqaYRly34wY-1692872515-0-1-7eb265f4.a1a04b6b.64248b5-150.0.0'}
    return headers, cookies


async def async_process_urls():
    # headers, cookies = await cf_challenge()
    cookies = {
        'ai_user': 'QENdJP4zBYWRKRPDSHb7jQ|2023-08-01T08:52:50.526Z',
        'trackingPermissionConsentsValue': '%7B%22cookies_analytics%22%3Atrue%2C%22cookies_personalization%22%3Atrue%2C%22cookies_advertisement%22%3Atrue%7D',
        'lastViewedBannerKey': '2',
        'listing_view_type': 'tile',
        'recently_viewed': '[%221148249%22]',
        'cf_chl_2': 'd2beb2e5c858b98',
        'cf_clearance': 'PP8m5KA1WptdiMOaC998aDQ0oZNh9HRXHXuZEdLajd8-1695886629-0-1-d29a0353.e9be5546.2e36fbca-160.2.1695886629',
        '__cf_bm': 'SIjMD5BlXdrn4EhG25nIDppUt3bJ_fZS28KRUy328R0-1695888745-0-ASyrx/+94mvP/mgtsZup0LL7Lz1OY6euLFPX9YAixU9c04qovfQaAheG+LjPIJ0ptV/h83XwQZZRA+N0Djw3ArIkyticGNcSQVdbR/tkEOeQ',
        'ai_session': '2+j6F/19bveMhOE8XfLXpP|1695886630495|1695889399191',
        'breakpointName': 'sm',
        'startquestion-session': '%7B%22expirationDate%22%3A1695893669379%2C%22data%22%3A%7B%22pageTime%22%3A1610%2C%22numberOfVisitedPages%22%3A12%7D%7D',
    }

    headers = {
        'authority': 'mobileapi.x-kom.pl',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'dnt': '1',
        'origin': 'https://www.x-kom.pl',
        'referer': 'https://www.x-kom.pl/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'time-zone': 'UTC',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-api-key': 'jfsTOgOL23CN2G8Y',
    }


    # print(proxy_dict["http"], formatted_now)
    async with aiohttp.ClientSession() as session:
        for i in range(1, 58):
            params = {
                'displayProfile': 'Website',
                'criteria.useAutoFuzziness': 'false',
                'childCategorySort': 'priority desc',
                'criteria.groupIds': '2',
                'criteria.categoryIds': '159',
                'criteria.producerIds': '4,5,7,14,27,28,46,57,227,230,396,475,731',
                'criteria.availabilityStatus': 'Available',
                'criteria.expand': 'Features,Departments,ProductMarks,Seo',
                'pagination.currentPage': f'{i}',
                'pagination.pageSize': '30',
                'sort': 'Popularity desc',
            }
            try:
                url = 'https://mobileapi.x-kom.pl/api/v1/xkom/products'
                response = await session.get(url, cookies=cookies, headers=headers, params=params)

                logging.info(response.status)
                print(response.status)

                if response.status == 200:
                    json_data = await response.json()  # Изменение здесь
                    with open(f'test_{i}.json', 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=4)

                await response.release()  # Добавлено закрытие ответа

            except aiohttp.client_exceptions.ClientHttpProxyError:
                print('ClientHttpProxyError, skipping this URL')
                continue
            except Exception as e:  # Рекомендуется обрабатывать и другие исключения
                print(f"An error occurred: {e}")
                continue

            await asyncio.sleep(1)
            # print('Паузка 5сек')


if __name__ == "__main__":

    asyncio.run(async_process_urls())
