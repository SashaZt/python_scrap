import requests

base_url = "https://api.openchain.xyz"  # Замените на фактический URL API

endpoint = "/signature-database/v1/export"

url = f"{base_url}{endpoint}"

response = requests.get(url)

if response.status_code == 200:
    content_type = response.headers["content-type"]
    if "text/plain" in content_type:
        filename = "export.csv"  # Имя файла, под которым сохранится экспорт
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"База данных успешно скачана и сохранена как {filename}")
    else:
        print("Неверный тип контента")
else:
    print(f"Ошибка: {response.status_code} - {response.text}")
