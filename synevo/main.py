import requests
import json
import csv
from bs4 import BeautifulSoup


def get_synevo():

    cookies = {
        'cookiesession1': '678A3EE4486EB95915E1BB52DB06333A',
        'XSRF-TOKEN': 'eyJpdiI6IlYyZlVDWHZ0a01BcVlyOHRcL2ZDbThnPT0iLCJ2YWx1ZSI6InFVdnVRbTFtT1FQZW9WSUJCRUdYT3R4NEhVMGRMekd0UmVPUUdrTTVmQlJmVEZ5SmllbnNPaTdjSFJpVXV1ME4iLCJtYWMiOiJmZjZlYTdmNzk1ZjA4NDhmOWRlZDEwY2FkODVlNTY2NTg4ODA0OWY4YTIyZTVhYzAwOWE1ZjMyODlmZTU3MzY5In0%3D',
        'laravel_session': 'eyJpdiI6InZMekZCc3psS3VwSzFWV3FGT2FjaVE9PSIsInZhbHVlIjoidkRtY3V5SEY5NTBVdGdBR1c3ekhjMWdjZTREWElkUklYNjJna2FcL1dVVVFqOEtjN1ZmU2YybXYrU091Q05heXoiLCJtYWMiOiI5ZDgwMzk3MzZkYmQ2ZTYxNzhmNzllYmNhNDUwYjI0ZTUxNGY1NTU4Mzc1ZTUyYTNiZjIxZTJiNmUwYjA1NzJlIn0%3D',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'cookiesession1=678A3EE4486EB95915E1BB52DB06333A; XSRF-TOKEN=eyJpdiI6IlYyZlVDWHZ0a01BcVlyOHRcL2ZDbThnPT0iLCJ2YWx1ZSI6InFVdnVRbTFtT1FQZW9WSUJCRUdYT3R4NEhVMGRMekd0UmVPUUdrTTVmQlJmVEZ5SmllbnNPaTdjSFJpVXV1ME4iLCJtYWMiOiJmZjZlYTdmNzk1ZjA4NDhmOWRlZDEwY2FkODVlNTY2NTg4ODA0OWY4YTIyZTVhYzAwOWE1ZjMyODlmZTU3MzY5In0%3D; laravel_session=eyJpdiI6InZMekZCc3psS3VwSzFWV3FGT2FjaVE9PSIsInZhbHVlIjoidkRtY3V5SEY5NTBVdGdBR1c3ekhjMWdjZTREWElkUklYNjJna2FcL1dVVVFqOEtjN1ZmU2YybXYrU091Q05heXoiLCJtYWMiOiI5ZDgwMzk3MzZkYmQ2ZTYxNzhmNzllYmNhNDUwYjI0ZTUxNGY1NTU4Mzc1ZTUyYTNiZjIxZTJiNmUwYjA1NzJlIn0%3D',
        'DNT': '1',
        'Origin': 'https://www.synevo.ua',
        'Pragma': 'no-cache',
        'Referer': 'https://www.synevo.ua/ua/tests',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'hujVsTTW3EcLYy5FoQnmAQUPO81gYvvBduyBc0ZW',
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
    with open('synevo_data.csv', 'w', newline='', encoding='utf-8') as file:
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
    with open('esculab_data.csv', 'w', newline='', encoding='utf-8') as file:
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
    with open('data_onelab.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=",")
        headers = ["Id", "Description", "Time", "Cost"]  # Замените на свои заголовки
        writer.writerow(headers)
        writer.writerows(data)
    # for item in data[:1]:
    #     print(item)


if __name__ == '__main__':
    # get_synevo()
    # parsing_synevo()
    # get_esculab()
    # parsing_esculab()
    # get_onelab()
    parsing_onelab()