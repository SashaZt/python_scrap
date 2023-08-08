import requests
import json
import csv
from bs4 import BeautifulSoup

def get_synevo():

    cookies = {
        'cookiesession1': '678A3ED620B6DA870B8CFCCFEC898BD3',
        '_gid': 'GA1.2.23311358.1691222848',
        '_clck': '1d3dezd|2|fdw|0|1312',
        '_fbp': 'fb.1.1691222848224.1595282608',
        '_ga_2B071QW08K': 'GS1.1.1691222847.1.1.1691222885.0.0.0',
        '_ga': 'GA1.1.594218207.1691222848',
        '_clsk': 'go9nqt|1691222886248|4|1|o.clarity.ms/collect',
        'XSRF-TOKEN': 'eyJpdiI6Imt6Sk9KOGpab01wdWJcL3oya3ByNFBnPT0iLCJ2YWx1ZSI6IlA0aVpkV1dXakZ6b1gzenV0SjV3WVM3VllcL1YwYlU3SlgrRjZOZ0hMR2JQN08xQ1pQZzVCM2VEQnpDeGhwZStmIiwibWFjIjoiM2ZjMTA3M2VjMjkxY2FiYzFiMDcwYWRiOGFlZGMyMmRlZWE3N2JkODY3Yzc4YTI3YWI2ZWY4ODNjM2YzOTg2YiJ9',
        'laravel_session': 'eyJpdiI6Inh1QVBwUmR2NitCOG1kbjFaUitzYmc9PSIsInZhbHVlIjoiM1FiMTFWU05NT3VKb3BnYWZ4MWlHUTVFNW9aY1ZjRHZpQm1UeVJzNkNPR2tINXA2bkFxSjBab0xESWlKY0IzXC8iLCJtYWMiOiIxMzk1MmYyZTJiN2MzNTRmYzVmMjU2NjEyMTA2OGU0MGQ4NjNkYjM1OThiNjAzYzEzMGM1MDkxMTgyMTEwZTM3In0%3D',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'cookiesession1=678A3ED620B6DA870B8CFCCFEC898BD3; _gid=GA1.2.23311358.1691222848; _clck=1d3dezd|2|fdw|0|1312; _fbp=fb.1.1691222848224.1595282608; _ga_2B071QW08K=GS1.1.1691222847.1.1.1691222885.0.0.0; _ga=GA1.1.594218207.1691222848; _clsk=go9nqt|1691222886248|4|1|o.clarity.ms/collect; XSRF-TOKEN=eyJpdiI6Imt6Sk9KOGpab01wdWJcL3oya3ByNFBnPT0iLCJ2YWx1ZSI6IlA0aVpkV1dXakZ6b1gzenV0SjV3WVM3VllcL1YwYlU3SlgrRjZOZ0hMR2JQN08xQ1pQZzVCM2VEQnpDeGhwZStmIiwibWFjIjoiM2ZjMTA3M2VjMjkxY2FiYzFiMDcwYWRiOGFlZGMyMmRlZWE3N2JkODY3Yzc4YTI3YWI2ZWY4ODNjM2YzOTg2YiJ9; laravel_session=eyJpdiI6Inh1QVBwUmR2NitCOG1kbjFaUitzYmc9PSIsInZhbHVlIjoiM1FiMTFWU05NT3VKb3BnYWZ4MWlHUTVFNW9aY1ZjRHZpQm1UeVJzNkNPR2tINXA2bkFxSjBab0xESWlKY0IzXC8iLCJtYWMiOiIxMzk1MmYyZTJiN2MzNTRmYzVmMjU2NjEyMTA2OGU0MGQ4NjNkYjM1OThiNjAzYzEzMGM1MDkxMTgyMTEwZTM3In0%3D',
        'DNT': '1',
        'Origin': 'https://www.synevo.ua',
        'Referer': 'https://www.synevo.ua/ua/tests',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'DRfRsH3OT4QPJzgun6XM6BXItvuFfyFYvTb4BOh4',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'location_id': '26',
    }

    response = requests.post('https://www.synevo.ua/api/test/tests-by-loc', cookies=cookies, headers=headers, data=data)
    json_data = response.json()
    with open(f'synevo_data.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл


def parsing_synevo():
    file_name = 'synevo_data.json'
    with open(file_name, encoding='utf-8') as f:
        data = json.load(f)
    heandler = ['code', 'name_ru', 'name_ua', 'term', 'location_id', 'price']
    with open('synevo.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(heandler)  # Записываем заголовки только один раз
        for key in data['json']:
            for item in data['json'][key]:
                code = item['code']
                name_ru = item['name_ru']
                name_ua = item['name_ua']
                term = item['term']
                location_id = item['location_id']
                price = item['price']
                values = [code, name_ru, name_ua, term, location_id, price]
                writer.writerow(values)


def get_esculab():
    headers = {
        'authority': 'esculab.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://esculab.com',
        'pragma': 'no-cache',
        'referer': 'https://esculab.com/analysis',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    json_data = {
        'idreg': '3201',
    }

    response = requests.post('https://esculab.com/api/customers/getPriceByRegionLocal/ua', headers=headers,
                             json=json_data)
    json_data = response.json()
    with open(f'esculab_data.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл

def parsing_esculab():
    file_name = 'esculab_data.json'
    with open(file_name, encoding='utf-8') as f:
        data = json.load(f)
    heandler = ['code', 'name', 'nameRu', 'duration_day', 'price']
    with open('esculab.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(heandler)  # Записываем заголовки только один раз
        for item in data:
            for child in item['childAnalyzes']:
                code = child['code']
                name = child['name']
                nameRu = child['nameRu']
                price = child['price']
                duration_day = child['duration_day']
                values = [code, name, nameRu, duration_day, price]
                writer.writerow(values)



def get_onelab():
    cookies = {
        'we.ss.re': 's%3ASkum0FSlLW3gRvC1gzC9okwXYUmV4PMF.5GG85WbgiTRgyE1Fe2BOzoIc142Iq21q2Y97jKKmJdE',
        '_ga_GRSQWWV2KT': 'GS1.1.1690807485.1.0.1690807485.0.0.0',
        '_ga': 'GA1.1.1078542883.1690807486',
    }

    headers = {
        'authority': 'onelab.com.ua',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru',
        'cache-control': 'no-cache',
        # 'cookie': 'we.ss.re=s%3ASkum0FSlLW3gRvC1gzC9okwXYUmV4PMF.5GG85WbgiTRgyE1Fe2BOzoIc142Iq21q2Y97jKKmJdE; _ga_GRSQWWV2KT=GS1.1.1690807485.1.0.1690807485.0.0.0; _ga=GA1.1.1078542883.1690807486',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    response = requests.get('https://onelab.com.ua/ua/analyses', cookies=cookies, headers=headers)
    with open(f"data_onelab.html", "w", encoding='utf-8') as file:
        file.write(response.text)

def parsing_onelab():
    file = f"data_onelab.html"
    with open(file, encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    rows = soup.find_all('tr', class_='a-an')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.replace('\n', '').strip() for ele in cols]
        cols[1] = cols[1].replace("[", "").replace("]", "")  # Удаляем скобки только из первого элемента
        data.append([ele for ele in cols if ele])
    with open('onelab.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=",")
        headers = ["Id", "Description", "Time", "Cost"]  # Замените на свои заголовки
        writer.writerow(headers)
        writer.writerows(data)
    # for item in data[:1]:
    #     print(item)



if __name__ == '__main__':
    get_synevo()
    get_esculab()
    get_onelab()
    parsing_synevo()
    parsing_esculab()
    parsing_onelab()
