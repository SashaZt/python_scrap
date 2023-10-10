import requests
from bs4 import BeautifulSoup

def main():
    sitemap_url = 'https://shop.olekmotocykle.com/sitemap.xml'
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for loc in soup.select('loc'):
        url = loc.text
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        for a in soup.find_all('a', href=True):
            link = a['href']
            if link.startswith('https://shop.olekmotocykle.com'):
                links.append(link)
    print(links)


if __name__ == '__main__':
    main()
