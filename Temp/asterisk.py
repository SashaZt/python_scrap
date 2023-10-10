import csv
"""Внутринние номера"""
data = {}

with open('file.csv', newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)  # пропускаем первую строку
    for row in reader:
        vn = row[0]
        p_i_p = row[1]
        data[vn] = f'(aut)\ncallerid="{p_i_p}" <{vn}>\ncontext=outcoling_ice'

for vn, value in data.items():
    print(f'[{vn}]{value}')
