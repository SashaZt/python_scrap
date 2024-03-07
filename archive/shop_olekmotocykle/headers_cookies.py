cookies = {
    'isMobileDevice': '0',
    '.cdneshopsid': 'H0jAXO6+lNEoUuyNBLPcZTO7HtUl+d5Es9IEUhFiUKHu+gHHy4VTE9RDpcGaZDdQ5QUDeITOADmCpMFYFQ|004',
    'LastSeenProducts': '68398',
    'lastCartId': '-1',
    '_gid': 'GA1.2.896583286.1702022356',
    '_gat_UA-232962489-1': '1',
    '_clck': 'ad7fhz%7C2%7Cfhd%7C0%7C1437',
    '_clsk': '1bu0812%7C1702022357450%7C1%7C1%7Cw.clarity.ms%2Fcollect',
    '_gat_gtag_UA_232962489_1': '1',
    '_ga_YBF7Q20GFD': 'GS1.1.1702022356.1.0.1702022356.0.0.0',
    '_ga': 'GA1.1.401714990.1702022356',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'isMobileDevice=0; .cdneshopsid=H0jAXO6+lNEoUuyNBLPcZTO7HtUl+d5Es9IEUhFiUKHu+gHHy4VTE9RDpcGaZDdQ5QUDeITOADmCpMFYFQ|004; LastSeenProducts=68398; lastCartId=-1; _gid=GA1.2.896583286.1702022356; _gat_UA-232962489-1=1; _clck=ad7fhz%7C2%7Cfhd%7C0%7C1437; _clsk=1bu0812%7C1702022357450%7C1%7C1%7Cw.clarity.ms%2Fcollect; _gat_gtag_UA_232962489_1=1; _ga_YBF7Q20GFD=GS1.1.1702022356.1.0.1702022356.0.0.0; _ga=GA1.1.401714990.1702022356',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in cookies.items()])