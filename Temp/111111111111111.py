import requests
import random
import json
import csv
import concurrent.futures

#opens a csv file of proxies and prints out the ones that work with the url in the extract function

proxylist = []

with open('proxylist_all.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # print(row[0])
        proxylist.append(row[0])

def extract(proxy):
    proxy = random.choice(proxylist)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=2)
        with open(f"proxylist.json", 'a') as file:
            json.dump(r.json()['origin'], file, indent=4, ensure_ascii=False)
    except:
        pass
    return proxy

with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(extract, proxylist)