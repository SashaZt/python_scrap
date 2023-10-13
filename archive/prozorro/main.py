import csv
import json
import os


# def get_token():
#     with open('token.txt', 'r') as file:
#         first_value = file.readline().strip()
#         return first_value

# def main():
#     # Определите текущую директорию, где находится скрипт
#     current_directory = os.getcwd()
#
#     # Задайте имя папки data_json
#     data_json_directory = 'data_json'
#
#     # Создайте полный путь к папке data_json
#     data_json_path = os.path.join(current_directory, data_json_directory)
#
#     # Проверьте, существует ли папка data_json, и если нет, создайте ее
#     if not os.path.exists(data_json_path):
#         os.makedirs(data_json_path)
#     filename = f'test.json'
#     file_path = os.path.join(data_json_path, filename)
#     # token = get_token()
#     cookies = {
#         'XSRF-TOKEN': 'eyJpdiI6IlFjYnpIbU9VbTAxcXcwc0JGRkZ0T0E9PSIsInZhbHVlIjoibTV2TFdmQ2xvTFNKYW13QlhUa3hsOE40cjA3MFBCRmIxcnN4aVJmdEJRYjhOc3kwWFdSMkNJVFprZHovdHUzU1VVc083R3lZbXBDYVVBUVkrcHVMRXVwaGo3d21OSEVXck1sbEpiZkRRcnpMRm94NkNTTnZFZGxoeVdBRmJQRVQiLCJtYWMiOiJhMDA0MjJjNWE0MDFhOTdkNTE5ODkzOWY5MmJhODNhMjc4YjRmNjY3ZDg1M2VlY2I5MjYxMWFiMWQyMGJlMjFhIiwidGFnIjoiIn0%3D',
#         'exam_session': 'eyJpdiI6InQrdW5JL3cvSGxCNFdSOTkxQnFnZ2c9PSIsInZhbHVlIjoid1ZISFZ1VVJIVlVBOTBLR01qVVptbzBYSnlwZmJUbldQZG13QlhUdXYzUno1bTVsRSt5NERxdVo1OW1wdGNKYTBrdVlVU0ZITGpBVTBUcngzUDdLdXNHa0l5eWo1RUhpelFpa1pib0tzKzdNL21SNnZ2YzVGdysxVVh5Zy82d2giLCJtYWMiOiI3OTk4NTA3Njc0OGQ4ZGQ0NTUyN2ZjZmQ0ZjhkNTA4ZWMxNDgwNjUwYjc3YTI5YTM3YjAwZGIyMzM2NDI4NDI4IiwidGFnIjoiIn0%3D',
#         '_ga': 'GA1.3.94094941.1694512235',
#         '_gat': '1',
#         'XSRF-TOKEN': 'eyJpdiI6IlNPOWc1KzRQVW1aTTdnYTVxa1NjcWc9PSIsInZhbHVlIjoiWDQxQ0trUnFBODU2djNkWXZnWEE3Mjl5ZlJ0bGxrSTRuR3AxOVgwVENuY0lzaEdnQWxOQnVobHE1L25jUkFHUjJkdGxSRzVFSWluc3gvbW1SeUdNN3BWRkswdXY0bnA1Z3NNY2F3bHUxc1VTRnZVYkgzOUFaZTJ2M245dnQ2RUciLCJtYWMiOiIxM2NiMTM2Y2Q2Yjg5MzUwMmFhMzk4MTQ2MzU1ZTNlNDMxODdkNDBiNDc1ZTliMDUxYzg0N2U1MmEyNDQ3MmNiIiwidGFnIjoiIn0%3D',
#         'portal_session': 'eyJpdiI6InBvYVFjd3RHUHVoWlZDRTlUSHc1SXc9PSIsInZhbHVlIjoib2RWREhQUG51dW5BWXhIN3V4MFgyMlJCdG44ZGNSVHBvZFpPRlVFNU02WXZtWEwzMm9ETVk5aDV4N2xGZFpmbHJZMFRvNVdOdWY4Q1FDSHIxcXJMOGRkdVpXRGZVR2RPNzVjUS9TcFA4L1B4Ukc3cGtsNXVQYjUrNWFMWVAyWGMiLCJtYWMiOiJlZDllMWUyODE3ZTZmNWQ4MWVhMGM5Mzk2ZDZhMDUxN2FlYzYzNDgwMjk4ZmZhMDhhZWQ5ZmY2YzQxNWQ2OTcxIiwidGFnIjoiIn0%3D',
#     }
#
#     headers = {
#         'authority': 'prozorro.gov.ua',
#         'accept': 'application/json, text/plain, */*',
#         'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
#         # 'content-length': '0',
#         'content-type': 'application/x-www-form-urlencoded',
#         # 'cookie': '_ga=GA1.3.94094941.1694512235; XSRF-TOKEN=eyJpdiI6IjFBVWVGUVY3cU1qb2xMOWdGK2ovWFE9PSIsInZhbHVlIjoiZjRNbGNDZWMvRnZMaFRmZzg5c1g4UHhidTdZeVExQ2YzNlFMVVFGa1ppUi9lckw3R3RWU0hobUttZDM4cG95U1lrK3NsY2EvaXY1VXEyWE9KdGhUMmNleHFLZE9uek4xaUg0cklObFhYTFZUVXpzRURyNW5HSDdIbnB5RkdXeW4iLCJtYWMiOiI5NjRlY2M5MTlhNzYwMWE3ZDQ2MzZkMmJjOGE4YTdjYTI2NzM5OTkzZTQ3Mzg0MGRlMWZkNWRlODdiNDMxNjJiIiwidGFnIjoiIn0%3D; portal_session=eyJpdiI6IjNFck53cDI1amN4eXpTRk1CSGtkVlE9PSIsInZhbHVlIjoiemIyKzArL2pDWHhPVVdoNzEvOXVDcTQ4Z1VNQlB1MlFYeGdXYzdWU0JkQjVYMWFVZWEwSmZmMEJPb2dBSmVDT043VmhKbXNkMTJQYXdkMitUTXBuZVZjdkx3ZkNIbkVDZFovN0UySjNuZmRlMCtkVi9wQkIzRldQTDRiUEw4WW0iLCJtYWMiOiI3MDdkZjIzMjczYWQxZTljOTgxZWU0MDkwMTEwNWRiNGRiMWVlNjFlNjNjZTc2YTg3ZTAwNWM2M2YyMDA5OGYzIiwidGFnIjoiIn0%3D',
#         'dnt': '1',
#         'origin': 'https://prozorro.gov.ua',
#         'referer': 'https://prozorro.gov.ua/search/tender?text=%D0%90%D0%BF%D1%82%D0%B5%D1%87%D0%BA%D0%B0&status=active.enquiries&status=active.tendering',
#         'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-origin',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
#         'x-xsrf-token': 'eyJpdiI6IjFBVWVGUVY3cU1qb2xMOWdGK2ovWFE9PSIsInZhbHVlIjoiZjRNbGNDZWMvRnZMaFRmZzg5c1g4UHhidTdZeVExQ2YzNlFMVVFGa1ppUi9lckw3R3RWU0hobUttZDM4cG95U1lrK3NsY2EvaXY1VXEyWE9KdGhUMmNleHFLZE9uek4xaUg0cklObFhYTFZUVXpzRURyNW5HSDdIbnB5RkdXeW4iLCJtYWMiOiI5NjRlY2M5MTlhNzYwMWE3ZDQ2MzZkMmJjOGE4YTdjYTI2NzM5OTkzZTQ3Mzg0MGRlMWZkNWRlODdiNDMxNjJiIiwidGFnIjoiIn0=',
#     }
#
#     params = {
#         'filterType': 'tenders',
#         'text': 'Аптечка',
#         'status[0]': 'active.enquiries',
#         'status[1]': 'active.tendering',
#     }
#
#     response = requests.post('https://prozorro.gov.ua/api/search/tenders', params=params, cookies=cookies,
#                              headers=headers)
#     json_data = response.json()
#     # Определите текущую директорию, где находится скрипт
#
#     with open(file_path, 'w',
#               encoding='utf-8') as f:
#         json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл

def main():


def pars():
    # Определите текущую директорию, где находится скрипт
    current_directory = os.getcwd()

    # Задайте имя папки data_json
    data_json_directory = 'data_json'

    # Создайте полный путь к папке data_json
    data_json_path = os.path.join(current_directory, data_json_directory)

    # Проверьте, существует ли папка data_json, и если нет, создайте ее
    if not os.path.exists(data_json_path):
        os.makedirs(data_json_path)
    filename = f'test.json'
    file_path = os.path.join(data_json_path, filename)
    with open("wallet_transactions.csv", "w", errors='ignore', newline='', encoding="utf-8") as result_csv:
        result_writer = csv.writer(result_csv, delimiter=",")
        result_writer.writerow(
            (
                'contactPoint_name', 'contactPoint_telephone', 'contactPoint_email',
                'procuringEntity_contactPoint_name', 'procuringEntity_contactPoint_title',
                'procuringEntity_contactPoint_tenderID', 'value_amount', 'status'
            ))
        with open(file_path, 'r', encoding="utf-8") as f:
            data_json = json.load(f)
        for j in data_json['data']:
            contactPoint_name = j['procuringEntity']['contactPoint']['name']
            contactPoint_telephone = j['procuringEntity']['contactPoint']['telephone']
            contactPoint_email = j['procuringEntity']['contactPoint']['email']
            procuringEntity_contactPoint_name = j['procuringEntity']['name']
            procuringEntity_contactPoint_title = j['title'].replace('\n', '')
            procuringEntity_contactPoint_tenderID = j['tenderID']
            value_amount = j['value']['amount']
            status = j['status']
            datas = [contactPoint_name, contactPoint_telephone, contactPoint_email, procuringEntity_contactPoint_name,
                     procuringEntity_contactPoint_title, procuringEntity_contactPoint_tenderID, value_amount, status]
            result_writer.writerow(datas)


if __name__ == '__main__':
    # main()
    pars()
