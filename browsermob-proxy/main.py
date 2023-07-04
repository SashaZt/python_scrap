
def main():
    from browsermobproxy import Server
    import requests
    server = Server(r"c:\Program Files (x86)\browsermob-proxy\bin\browsermob-proxy")


    # Укажите путь к директории browsermob-proxy

    server.start()
    proxy = server.create_proxy()

    # Настройка параметров прокси для requests
    proxies = {
        "http": f'http://{proxy.proxy}',
        "https": f'http://{proxy.proxy}'
    }

    # Включение захвата HAR
    proxy.new_har("instagram")

    # Совершение запроса через прокси
    response = requests.get("https://www.instagram.com/stories/jlo/3139144661487166563/", proxies=proxies)

    # Просмотр данных HAR
    print(proxy.har)

    # Остановка прокси-сервера
    server.stop()

if __name__ == '__main__':
    main()
