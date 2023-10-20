import os
import csv
import time
from bardapi import Bard
from dotenv import load_dotenv

start_time = time.time()  # Записываем начальное время
load_dotenv()
token = 'cQgh7ceQrpXs_q42wcwlxiXiIn8LCBslluJ8ayFm6TXyUixBm9Clp_hLQgOIi6H3k3ubiA.'
bard = Bard(token=token)
name_files = 'questions.csv'
with open(name_files, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for q in csvfile:
        response = bard.get_answer(q)['content']
        print(response)
        end_time = time.time()  # Записываем конечное время
        elapsed_time = end_time - start_time  # Вычисляем разницу
        print(f"Время выполнения кода: {elapsed_time:.2f} секунд.")