from bs4 import BeautifulSoup
import lxml
with open('prom_ua.xml', 'r', encoding="utf8") as f:
	file = f.read()

# 'xml' is the parser used. For html files, which BeautifulSoup is typically used for, it would be 'html.parser'.
soup = BeautifulSoup(file, 'lxml')
item = soup.find_all('item')
price = soup.find_all('price')
guarantee_type = soup.find_all('guarantee type')
param_name = soup.find_all('param name')
for n, tag in enumerate(item):
    print(tag.text)
    print(price.text)
    print(price.text[n])
    print(guarantee_type.text[n])
    print(param_name.text[n])
