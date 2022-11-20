import requests
import csv
from bs4 import BeautifulSoup

url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
    'accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'

}
req = requests.get(url, headers=headers)
src = req.text
# print(src)
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(src)

# with open('index2.html', encoding='utf-8') as file:
#     src = file.read()
# soup = BeautifulSoup(src, 'lxml')
#
# # Собираем заголовки таблиц
# table_head = soup.find(class_="GeneratedTable").find('thead').find('tr').find_all('th')
# product = table_head[0].text
# protein = table_head[1].text
# fats = table_head[2].text
# carbohydrates = table_head[3].text
# calories = table_head[4].text
# with open('test_q.csv', 'w') as file: # дописываем если необходимо encoding='utf-8'
#     writer = csv.writer(file)
#     writer.writerow(
#         (
#             product,
#             protein,
#             fats,
#             carbohydrates,
#             calories
#         )
#     )
#
# product_data = soup.find(class_="GeneratedTable").find('tbody').find_all('tr')
# for item in product_data:
#     product_ls = []
#     product_tds = item.find('td')
#
#
#     print(product_tds)