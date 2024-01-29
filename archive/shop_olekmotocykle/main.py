import asyncio
import glob
import json
import os

import requests
from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'isMobileDevice=0; .cdneshopsid=AxgBlrk23osNW8YA7wOKY5TBd97quwsCXbiyd6FgsXEkmIDZteN8nxi6JcIPqYz6YICeW7hGJu9wiGP9yA|004; LastSeenProducts=; lastCartId=-1',
    'DNT': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def parsing_url_category_in_html():
    folder_path = "C:/Data_olekmotocykle/"

    files = glob.glob(folder_path + "*.html")

    for file in files:
        os.remove(file)
    url = "https://shop.olekmotocykle.com/"
    response = requests.get(url, headers=headers)  # , proxies=proxies
    with open('category_product.csv', 'w', newline='') as csvfile:
        if response.content:
            soup = BeautifulSoup(response.content, 'lxml')
            table_category = soup.find('div', attrs={'class': 'category-content-ui'}).find_all('a', attrs={
                'class': 'category-label-ui inline-flex-ui vertically-centered-ui'})
            for link in table_category:
                href = f"https://shop.olekmotocykle.com/{link.get('href')}"
                csvfile.write(href + '\n')  # Прямая запись строки в файл без использования csv.writer
                col_category = int(
                    link.find('small', attrs={'class': 'category-amount-ui'}).get_text(strip=True).replace('(',
                                                                                                           '').replace(
                        ')', ''))
                # Проверка количества товаров
                # print(col_category, href)


        else:
            print("No content received")


def urls_photo():
    targetPattern = f"c:\\Data_olekmotocykle\\*.html"
    files_html = glob.glob(targetPattern)

    result_dict = {}
    for item in files_html:
        with open(item, encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, 'html.parser')
        div = soup.find_all("div", {"class": "lazyslider-container-lq"})[0]
        id_product = soup.find('div', {'class': 'product-code-ui product-code-lq'}).text.strip()
        imgs = div.find_all("img", {"class": "open-gallery-lq"})

        item_dict = {}
        for i, img in enumerate(imgs):
            url_photo = 'https://' + img["data-src"].replace("//", "")
            item_dict[f"url_{i + 1}"] = url_photo
            item_dict[f"id_{i + 1}"] = id_product

        result_dict[item.replace("c:\\Data_olekmotocykle\\", "")] = item_dict

    # записываем результат в файл JSON
    with open("result.json", "w") as json_file:
        json.dump(result_dict, json_file)


# def run_main_asio_photo():
#     import main_asio_photo
#     asyncio.run(main_asio_photo.main())


def main_download_url():
    import main_url_asio
    asyncio.run(main_url_asio.main())


def main_asio_html():
    import main_asio
    asyncio.run(main_asio.main_asio())


def parsing_url():
    import parisng_html
    parisng_html.main()


if __name__ == '__main__':
    print("Собираем категории товаров")
    parsing_url_category_in_html()
    print("Скачиваем все ссылки")
    main_download_url()
    parsing_url()
    print("Скачиваем все HTML страницы")
    main_asio_html()
    # print("Получаем все url на фото")
    # urls_photo()
    # print("Скачиваем все фото")
    # run_main_asio_photo()
    # print("Получаем все данные")
    # parsing_product()
    # print("Все получилось")
