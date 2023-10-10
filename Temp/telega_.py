import re
import csv

# Открываем файл для чтения
with open('new_4.txt', 'r', encoding='utf-8') as file:
    content = file.read()

text = content
# Убираем лишние пробелы
text = re.sub(r'\s*,\s*', ',', text)
text = re.sub(r'\s{2,}', ' ', text)

pattern = (r'(\d+,\d{1,4}) га,(.*?),(.*?),(.*?),(.*? область)'
          r' Вартість ₴([\d\s]+) \(₴([\d\s]+)\/га\) ,дохідність (\d,\d{1})%'
          r' (\d{10}:\d{2}:\d{2}:\d{4})'
          r' Орендар:(.*?),Оренда:(\d+ років)')

matches = re.findall(pattern, text)
for match in matches:
    print(match)



# # Если есть соответствия
# if matches:
#     # Открываем CSV файл для записи
#     with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile, delimiter='/')
#
#         # Записываем заголовок
#         writer.writerow(['Площадь', 'Населенный пункт', 'Район', 'Область', 'Цена',
#                          'Цена за га', 'Доходность', 'ID', 'Орендар', 'Период аренды'])
#
#         # Записываем каждое соответствие
#         for match in matches:
#             writer.writerow(match)
# else:
#     print("Нет соответствий в файле.")
