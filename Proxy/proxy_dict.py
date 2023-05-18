import csv

proxies = []

with open('C:\\scrap_tutorial-master\\Proxy\\proxylist.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        proxies.append(f"{row[0]}")
print(proxies)