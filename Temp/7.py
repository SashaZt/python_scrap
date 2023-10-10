import requests

API_KEY = '238fd9f22f6e6a63a058e98770994d0f'

proxies = {
"http": f"http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001"
}
r = requests.get('http://httpbin.org/ip', proxies=proxies, verify=False)
print(r.text)
