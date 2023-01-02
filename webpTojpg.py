from PIL import Image

im = Image.open("C:\\scrap_tutorial-master\\webp\\b29f1333ca6c022a45cf49059d3eced4.webp").convert("RGB")
im.save("test.jpg", "jpeg")

PROXY_HOST = '141.145.205.4'
PROXY_PORT = 31281
PROXY_USER = 'proxy_alex'
PROXY_PASS = 'DbrnjhbZ88'
proxies = {'https': f'https://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'}
