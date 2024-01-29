import re
from pathlib import Path

from bs4 import BeautifulSoup


def main():
    path = Path('c:/Data_olekmotocykle/').glob('*.html')

    with open('url_product.csv', 'w', newline='') as csvfile:
        for item in path:
            with open(item, encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            regex_cart = re.compile('product-item-ui.*')
            table_products = soup.find_all('div', attrs={'class': regex_cart})
            for img in table_products:
                a = img.find('a').get('href')
                url = f'https://shop.olekmotocykle.com/{a}'
                csvfile.write(url + '\n')

    # После обработки файлов, удаляем их
    for item in Path('c:/Data_olekmotocykle/').glob('*.html'):
        item.unlink()
    print('Собрали все ссылки')


if __name__ == '__main__':
    main()
