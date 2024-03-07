import requests
import xml.etree.ElementTree as ET

# URL XML файла
url = 'https://breezy.ua/storage/app/public/feed/mytechnika/ua/ua.xml'

# Скачиваем файл
response = requests.get(url)
# Проверяем, успешно ли был выполнен запрос
if response.status_code == 200:
    root = ET.fromstring(response.content)

    # Перебираем все товары
    for offer in root.findall('.//offer')[:1]:
        print('--- Товар ---')
        print(f'Код: {offer.attrib.get("code")}')
        print(f'Уникальный ID: {offer.attrib.get("unique")}')
        print(f'ID Категории: {offer.find("categoryId").text}')
        print(f'Название: {offer.find("name").text}')
        print(f'Код Производителя: {offer.find("vendorCode").text}')
        print(f'Производитель: {offer.find("vendor").text}')
        print(f'Модель: {offer.find("model").text}')
        print(f'Цена (UAH): {offer.find("priceUAH").text}')
        print(f'Старая Цена: {offer.find("oldprice").text if offer.find("oldprice") is not None else "N/A"}')
        print(f'Описание: {ET.tostring(offer.find("description"), encoding="unicode", method="text").strip()}')

        # Извлекаем и печатаем ключевые слова, если они есть
        if offer.find("keywords") is not None:
            print(f'Ключевые слова: {offer.find("keywords").text}')

        # Перебираем все цены, если они есть
        for price in offer.findall(".//prices/price"):
            print(f'Цена: {price.find("value").text}, Количество: {price.find("quantity").text}')

        # Перебираем все изображения
        images = offer.findall(".//image") + offer.findall(".//picture")
        for img in images:
            print(f'Ссылка на изображение: {img.text}')

        # Перебираем все параметры товара
        for param in offer.findall(".//param"):
            print(f'{param.attrib.get("name")}: {param.text}')

        print('\n')  # Добавляем пустую строку между товарами для удобства чтения
else:
    print(f'Ошибка загрузки файла: HTTP {response.status_code}')

