# -*- coding: utf-8 -*-
# from bs4 import BeautifulSoup
# import csv
# import glob
# from selenium.webdriver.common.keys import Keys
# import re
# import requests
import json

import requests


# import cloudscraper
# import os
# import time
# import undetected_chromedriver as webdriver
# from selenium.common.exceptions import TimeoutException
# # from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from concurrent.futures import ThreadPoolExecutor
# import csv
#
# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from concurrent.futures import ThreadPoolExecutor
def get_json():
    cookies = {
        "RABTests": "eyJ0ZXN0cyI6W3sibmFtZSI6Imlsb3NjQmxvY3prb3ciLCJkZXZpY2VzIjpbIkQiLCJNIiwiVCJdLCJwYWdlc1R5cGVzIjpbInN6dWthaiJdLCJwYXRoUGF0dGVybiI6bnVsbCwidmFsdWUiOiIxQmxvY3playJ9LHsibmFtZSI6Imxwc20iLCJkZXZpY2VzIjpbIkQiLCJNIiwiVCJdLCJwYWdlc1R5cGVzIjpbImxwLWJsb2N6a2kiXSwicGF0aFBhdHRlcm4iOm51bGwsInZhbHVlIjoibHBCIn1dfQ==",
        "_cq_duid": "1.1708771687.WETX2LlQMRgC6Xfw",
        "_cq_suid": "1.1708771687.PFslkA1899a9Cmnl",
        "liczbaPokoi": "1",
        "dowolnaLiczbaPokoi": "false",
        "KlientIdSchowek": "5516194b-a642-485d-b6cb-138703b41c8e",
        "cto_h2h": "A",
        "_gcl_au": "1.1.1477052105.1708772126",
        "_ga": "GA1.1.579902053.1708771691",
        "__cmpcpc": "__52_54_51_53__",
        "__rtbh.lid": "%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22k7LygS1KVySpkdMr8xkt%22%7D",
        "smuuid": "18ddac16dae-1352194280d3-27fe2ce4-2c748fea-aa34f895-8e0937dfbd41",
        "_fbp": "fb.1.1708772126153.1019136533",
        "smPopupFormShowOnVisitCnt": "30",
        "FPAU": "1.1.1477052105.1708772126",
        "BHTGuid": "4795220b-21c6-4816-93b7-a5c0582bb89c",
        "wiek": "%5B%221994-01-01T12%3A00%3A00.000Z%22%2C%221994-01-01T12%3A00%3A00.000Z%22%5D",
        "smvr": "eyJ2aXNpdHMiOjIsInZpZXdzIjozLCJ0cyI6MTcwODg5MTE3ODkzNywiaXNOZXdTZXNzaW9uIjpmYWxzZX0=",
        "_hjSessionUser_1823437": "eyJpZCI6IjVlMWMyMDlkLWYxMWItNWVkYi1hMGNjLWY1OWJjZmM1ZmZlMCIsImNyZWF0ZWQiOjE3MDg3NzI0NzQ0ODAsImV4aXN0aW5nIjp0cnVlfQ==",
        "smOViewsPopCap": "views:3|",
        "smPopupFormVisitCnt": "3",
        "_smvs": "DIRECT",
        "cto_bundle": "Vse0gV82ZFZRU2x3WGhlV01tSk1ncWh2JTJGeGlqdHoyQ21TZ3ZVUkMlMkZycGZ4UzkzR09SMSUyQlVDRnEwOXBnZFl1Vm44TGd6YUV1WUtPN1FLY1YlMkI1eUViNXc3ZWdjZXl6RWlaNXFBU01ZWGF0NHBhUTdrTnZka2VpRXBKR0IlMkJzbm1lTCUyRiUyRlp6YW0lMkJISHhqa0E1V09RJTJCZmE2Q0FjJTJGQSUzRCUzRA",
        "_clck": "iz523t%7C2%7Cfjl%7C0%7C1515",
        "_hjSession_1823437": "eyJpZCI6IjlmYzUxZWU0LTY0YjItNDc1ZS1hY2MzLWU3YWRjMDgwMTkxYSIsImMiOjE3MDg5MzM4NDUwODQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==",
        "_uetsid": "6823eb20d41811ee895441fcf2bab905",
        "_uetvid": "374bc430d30311eeaa244b50bf403da7",
        "_clsk": "b3urr6%7C1708934447236%7C7%7C0%7Cw.clarity.ms%2Fcollect",
        "_ga_HQWQ6ZSR4S": "GS1.1.1708933844.3.1.1708934486.0.0.0",
    }

    headers = {
        "authority": "r.pl",
        "accept": "application/json",
        "accept-language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6",
        "content-type": "application/json",
        # 'cookie': 'RABTests=eyJ0ZXN0cyI6W3sibmFtZSI6Imlsb3NjQmxvY3prb3ciLCJkZXZpY2VzIjpbIkQiLCJNIiwiVCJdLCJwYWdlc1R5cGVzIjpbInN6dWthaiJdLCJwYXRoUGF0dGVybiI6bnVsbCwidmFsdWUiOiIxQmxvY3playJ9LHsibmFtZSI6Imxwc20iLCJkZXZpY2VzIjpbIkQiLCJNIiwiVCJdLCJwYWdlc1R5cGVzIjpbImxwLWJsb2N6a2kiXSwicGF0aFBhdHRlcm4iOm51bGwsInZhbHVlIjoibHBCIn1dfQ==; _cq_duid=1.1708771687.WETX2LlQMRgC6Xfw; _cq_suid=1.1708771687.PFslkA1899a9Cmnl; liczbaPokoi=1; dowolnaLiczbaPokoi=false; KlientIdSchowek=5516194b-a642-485d-b6cb-138703b41c8e; cto_h2h=A; _gcl_au=1.1.1477052105.1708772126; _ga=GA1.1.579902053.1708771691; __cmpcpc=__52_54_51_53__; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22k7LygS1KVySpkdMr8xkt%22%7D; smuuid=18ddac16dae-1352194280d3-27fe2ce4-2c748fea-aa34f895-8e0937dfbd41; _fbp=fb.1.1708772126153.1019136533; smPopupFormShowOnVisitCnt=30; FPAU=1.1.1477052105.1708772126; BHTGuid=4795220b-21c6-4816-93b7-a5c0582bb89c; wiek=%5B%221994-01-01T12%3A00%3A00.000Z%22%2C%221994-01-01T12%3A00%3A00.000Z%22%5D; smvr=eyJ2aXNpdHMiOjIsInZpZXdzIjozLCJ0cyI6MTcwODg5MTE3ODkzNywiaXNOZXdTZXNzaW9uIjpmYWxzZX0=; _hjSessionUser_1823437=eyJpZCI6IjVlMWMyMDlkLWYxMWItNWVkYi1hMGNjLWY1OWJjZmM1ZmZlMCIsImNyZWF0ZWQiOjE3MDg3NzI0NzQ0ODAsImV4aXN0aW5nIjp0cnVlfQ==; smOViewsPopCap=views:3|; smPopupFormVisitCnt=3; _smvs=DIRECT; cto_bundle=Vse0gV82ZFZRU2x3WGhlV01tSk1ncWh2JTJGeGlqdHoyQ21TZ3ZVUkMlMkZycGZ4UzkzR09SMSUyQlVDRnEwOXBnZFl1Vm44TGd6YUV1WUtPN1FLY1YlMkI1eUViNXc3ZWdjZXl6RWlaNXFBU01ZWGF0NHBhUTdrTnZka2VpRXBKR0IlMkJzbm1lTCUyRiUyRlp6YW0lMkJISHhqa0E1V09RJTJCZmE2Q0FjJTJGQSUzRCUzRA; _clck=iz523t%7C2%7Cfjl%7C0%7C1515; _hjSession_1823437=eyJpZCI6IjlmYzUxZWU0LTY0YjItNDc1ZS1hY2MzLWU3YWRjMDgwMTkxYSIsImMiOjE3MDg5MzM4NDUwODQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==; _uetsid=6823eb20d41811ee895441fcf2bab905; _uetvid=374bc430d30311eeaa244b50bf403da7; _clsk=b3urr6%7C1708934447236%7C7%7C0%7Cw.clarity.ms%2Fcollect; _ga_HQWQ6ZSR4S=GS1.1.1708933844.3.1.1708934486.0.0.0',
        "dnt": "1",
        "origin": "https://r.pl",
        "referer": "https://r.pl/marsa-alam-wypoczynek/marina-resort-port-ghalib?data=2024-07-27&dlugoscPobytu=8&iataWyjazdu=POZ&liczbaPokoi=1&wiek=1994-01-01&wiek=1994-01-01&wiek=2020-02-25&wybranePokoje={%221%22:1}&wyzywienie=all-inclusive",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "x-source": "r.pl",
    }

    json_data = {
        "HotelUrl": "marina-resort-port-ghalib",
        "ProduktUrl": "marsa-alam-wypoczynek",
        "LiczbaPokoi": 1,
        "Dlugosc": 8,
        "TerminWyjazdu": "2024-07-27",
        "Iata": "POZ",
        "DatyUrodzenia": [
            "1994-01-01",
            "1994-01-01",
            "1994-01-01",
        ],
        "Wyzywienie": "all-inclusive",
        "CzyV2": True,
    }

    response = requests.post(
        "https://r.pl/api/wyszukiwarka/wyszukaj-kalkulator",
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    hotelurl = json_data["HotelUrl"]
    json_data_r = response.json()
    with open("r.json", "w", encoding="utf-8") as f:
        json.dump(json_data_r, f, ensure_ascii=False, indent=4)  # Записываем в файл

    return hotelurl


def pars_json():
    hotelurl = get_json()  # Получаем URL отеля

    with open("r.json", "r", encoding="utf-8") as f:
        data_json = json.load(f)

    terminy = data_json["Terminy"]

    # Создаем словарь с hotelurl как ключом, и пустым словарем в качестве значения
    result = {hotelurl: {}}

    for t in terminy:
        term = t["Dlugosc"]
        terminy_data = t["Terminy"]

        # Для каждого term создаем список для хранения его данных
        term_data_list = []

        for tt in terminy_data:
            date_from = tt["Termin"]
            date_until = tt["DataKoniec"]
            price = tt["Cena"]
            price_per_person = tt["CenaZaOsobe"]

            data_dict = {
                "date_from": date_from,
                "date_until": date_until,
                "price": price,
                "price_per_person": price_per_person,
            }

            # Добавляем словарь с данными в список для текущего term
            term_data_list.append(data_dict)

        # Добавляем список с данными по текущему term в словарь result под ключом hotelurl
        result[hotelurl][term] = term_data_list
    with open("rr.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)  # Записываем в файл


if __name__ == "__main__":
    get_json()
    # pars_json()
