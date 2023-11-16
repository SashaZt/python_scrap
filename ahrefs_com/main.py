import requests
import json




def get_requests():

    cookies = {
        '__cflb': '02DiuFMJyRDQ1SqAwiXnXeziU6ebmGZn9jdP5qUKiJuoJ',
        'BSSESSID': '3inAHX4gWDTQOn3ELYzYmEfOIzlZGHWOxa6tpyvY',
        'kd-b1b6369c00f15bbb': 'MS%2FanAtPRDlT7e7onG5opee1qceShjVaoa6Sm5%2FHZzgd5ehd4lD%2BA0S4J7oUU9Q1lAKH%2FsR5H8fK32KEcrQ',
        '__cf_bm': 'IYQkUtQ4JUAR59KhOhHZwrONiGN135339JW8eyDFvNk-1700128201-0-AcHAi1h08KpgyIq84FSs+6/2joFAjpiGh4szEovq/WFVRjyCwcFwIWtch0kX4T6YhNvMeoTG7hqnqvc/JhVu/0o=',
        'cf_clearance': 'urUqJFphiqw.c6BboAVVN5prvkYsV_jkHgZg1OXFxYc-1700128203-0-1-f6f46a16.ef2c8e30.9c04a62f-0.2.1700128203',
        'io': 'TqXx4kgPksN_0lWvCo6w',
        'intercom-device-id-dic5omcp': '7c6db7aa-d9e5-451a-993d-66b9e886d803',
        'x-consistency': '1700128349.497%2CseSetOverviewSettings',
        'intercom-session-dic5omcp': 'OFc1akxVUXExWjVBUWZraTg2dlJnd3EyWVd3YW1kZHJqUmtEdFArOS94OGt3blVEa2lzdDVJd21ITUhpOFh6eS0tRUpDYWNOVHQ2UDFFdG9kb250SHlqdz09--f6c5fefd357cf639e845d85d8de7d880e090c4cc',
    }
    headers = {
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Referer': 'https://app.ahrefs.com/v2-site-explorer/overview?backlinksChartMode=metrics&backlinksChartPerformanceSources=domainRating%7C%7CurlRating&backlinksCompetitorsSource=%22UrlRating%22&chartGranularity=daily&chartInterval=all&competitors=&countries=ru&country=all&generalChartMode=metrics&generalChartPerformanceSources=organicTraffic%7C%7CpaidTraffic%7C%7CrefDomains&generalChartTopPosition=top11_20%7C%7Ctop21_50%7C%7Ctop3%7C%7Ctop4_10%7C%7Ctop51&generalCompetitorsSource=%22OrganicTraffic%22&generalCountriesSource=organic-traffic&highlightChanges=30d&keywordsSource=all&mode=subdomains&organicChartMode=metrics&organicChartPerformanceSources=organicTraffic%7C%7CorganicTrafficValue&organicChartTopPosition=top11_20%7C%7Ctop21_50%7C%7Ctop3%7C%7Ctop4_10%7C%7Ctop51&organicCompetitorsSource=%22OrganicTraffic%22&organicCountriesSource=organic-traffic&overview_tab=general&target=wiki.merionet.ru&topOrganicKeywordsMode=normal&topOrganicPagesMode=normal&trafficType=organic&volume_type=monthly',
        'DNT': '1',
        'X-Client-Version': 'release-20231116-bk157790-20f3a35189c',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }
    params = {
        'input': f'{{"args":{{"competitors":[],"compareDate":["Date","2023-10-17"],"multiTarget":["Single",{{"protocol":"both","mode":"subdomains","target":"{site} /"}}],"url":"{site} /","protocol":"both","mode":"subdomains"}}}}',
    }

    response = requests.get('https://app.ahrefs.com/v4/seGetMetricsByCountry', params=params, headers=headers, cookies=cookies)
    response.encoding = 'utf-8'
    # print(response)
    data_json = response.json()

    with open(f'{site.replace('.', '_')}.json', 'w', encoding='utf-8') as f:
        json.dump(data_json, f, ensure_ascii=False, indent=4)  # Записываем в файл