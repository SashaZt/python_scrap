from bs4 import BeautifulSoup
import csv
import glob
import re
import requests
import json
import cloudscraper
import os
import time
import undetected_chromedriver as webdriver
from selenium.common.exceptions import TimeoutException
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor


def main():

    headers = {
        'authority': 'api.debank.com',
        'accept': '*/*',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
        'account': '{"random_at":1694007925,"random_id":"1596a8c1301e4bd1a80cb55c1cd8ceeb","user_addr":null}',
        'dnt': '1',
        'origin': 'https://debank.com',
        'referer': 'https://debank.com/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'source': 'web',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-api-nonce': 'n_D0KmyU4yFqu2Oam15Fp8HIOQ9b5O4LBk7v1RpT7T',
        'x-api-sign': '53226108110118de07fc4e18adf10fc797706b53e8c0105d808ef59b6e9b9c50',
        'x-api-ts': '1694028070',
        'x-api-ver': 'v2',
    }

    params = {
        'user_addr': '0x5396a70112bbaceacc2fe660b8d5855299e47d1f',
        'chain': '',
        'start_time': '0',
        'page_count': '20',
    }

    response = requests.get('https://api.debank.com/history/list', params=params, headers=headers)
    json_data = response.json()
    with open(f'test.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл
#
#
# import datetime
#
# timestamp = 1691404356
# dt_object = datetime.datetime.fromtimestamp(timestamp)
#
# print(dt_object)
#
# import datetime
#
# # Создать объект datetime для даты 2023-08-13 00:00:00
# dt_object = datetime.datetime(year=2023, month=9, day=6, hour=0, minute=0, second=0)
#
# # Перевести объект datetime в Unix-время
# timestamp = int(dt_object.timestamp())
#
# print(timestamp)

def par_json():
    with open('test.json', 'r', encoding="utf-8") as f:
        data_json = json.load(f)
    coun = 0
    with open(f"++.csv", "w",
              errors='ignore', encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv, delimiter=",")
        writer.writerow(
            (
                'cate_id', 'cex_id', 'chain', 'id', 'is_scam', 'other_addr', 'project_id', 'cate_id', 'receives_amount',
                'receives_from_addr', 'receives_token_id', 'sends_amount', 'sends_price', 'sends_to_addr',
                'sends_token_id', 'time_at', 'token_approve', 'tx_from_addr', 'tx_message', 'tx_name', 'tx_selector',
                'tx_status', 'tx_to_addr', 'tx_value'
            )
        )
        for j in data_json['data']['history_list']:
            cate_id = j['cate_id']
            cex_id = j['cex_id']
            chain = j['chain']
            j_id = j['id']
            is_scam = j['is_scam']
            other_addr = j['other_addr']
            project_id = j['project_id']
            try:
                receives_amount = j['receives'][0]['amount']
                receives_from_addr = j['receives'][0]['from_addr']
                receives_token_id = j['receives'][0]['token_id']
            except:
                receives_amount = None
                receives_from_addr = None
                receives_token_id = None
            try:
                sends_amount = j['sends'][0]['amount']
                sends_price = j['sends'][0]['price']
                sends_to_addr = j['sends'][0]['to_addr']
                sends_token_id = j['sends'][0]['token_id']

            except:
                sends_amount = None
                sends_price = None
                sends_to_addr = None
                sends_token_id = None
            time_at = None
            token_approve = None
            try:
                tx_from_addr = j['tx']['from_addr']
                tx_message = j['tx']['message']
                tx_name = j['tx']['name']
                tx_selector = j['tx']['selector']
                tx_status = j['tx']['status']
                tx_to_addr = j['tx']['to_addr']
                tx_value = j['tx']['value']
            except:
                tx_from_addr = None
                tx_message = None
                tx_name = None
                tx_selector = None
                tx_status = None
                tx_to_addr = None
                tx_value = None
            datas = [cate_id, cex_id, chain, j_id, is_scam, other_addr, project_id, cate_id, receives_amount,
                    receives_from_addr, receives_token_id, sends_amount, sends_price, sends_to_addr,
                    sends_token_id, time_at, token_approve, tx_from_addr, tx_message, tx_name, tx_selector,
                    tx_status, tx_to_addr, tx_value]
            writer.writerow((datas))


if __name__ == '__main__':
    main()
    par_json()
