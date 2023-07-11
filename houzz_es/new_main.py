# Import required modules
from bs4 import BeautifulSoup
import csv
import os
import random
import requests
import time
import json
import requests
import re
from urllib.parse import urlparse

#keywords to search on the site
keywords = ["Commercial", "Residential", "LEED", "Greengaurd", "Phthalates", "Polyvinyl", "PVC"]

#Cookies and headers for response
cookies = {
    'v': '1689076489_844d796b-afae-45d9-a402-afb22b6b6c71_e13e5a67651e3f4ad72d3580494e2d8b',
    'vct': 'en-US-CR8JQ61k8B8JQ61kSBwJQ61k4R0JQ61k4h0JQ61k',
    '_csrf': 'CVz3_VMX-r7Z0DsjFW8sdO5m',
    'jdv': 't7WOzUb2vHLZtWVVHSk8XJEYN7ua9jR7X0XubdRfWUW1hRdAn%2B%2F6c7HkuMqiSwXuBLJ6I8unFQioHhomdG2xiY6t5dBH',
    'prf': 'prodirDistFil%7C%7D',
    'documentWidth': '1920',
    '_gid': 'GA1.2.2097402768.1689076492',
    '_gcl_au': '1.1.90367831.1689076492',
    '_gat': '1',
    '_pin_unauth': 'dWlkPU5qbGpaR0UzTmpJdFpqUTNNQzAwTXpaaUxUbGlPR010WkdaaE9UVTROMlkyWldNeg',
    'hzd': 'acfa5231-c483-421e-b7c9-8586c303569b%3A%3A%3A%3A%3AGetStarted',
    '_ga_PB0RC2CT7B': 'GS1.1.1689076492.1.1.1689076494.58.0.0',
    '_ga': 'GA1.1.263616427.1689076492',
    '_uetsid': 'bec9eae01fe111eebcaed1af8211f75e',
    '_uetvid': 'beca1c901fe111ee975175ae1159fa27',
}

headers = {
    'authority': 'www.houzz.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru',
    'cache-control': 'no-cache',
    # 'cookie': 'v=1689076489_844d796b-afae-45d9-a402-afb22b6b6c71_e13e5a67651e3f4ad72d3580494e2d8b; vct=en-US-CR8JQ61k8B8JQ61kSBwJQ61k4R0JQ61k4h0JQ61k; _csrf=CVz3_VMX-r7Z0DsjFW8sdO5m; jdv=t7WOzUb2vHLZtWVVHSk8XJEYN7ua9jR7X0XubdRfWUW1hRdAn%2B%2F6c7HkuMqiSwXuBLJ6I8unFQioHhomdG2xiY6t5dBH; prf=prodirDistFil%7C%7D; documentWidth=1920; _gid=GA1.2.2097402768.1689076492; _gcl_au=1.1.90367831.1689076492; _gat=1; _pin_unauth=dWlkPU5qbGpaR0UzTmpJdFpqUTNNQzAwTXpaaUxUbGlPR010WkdaaE9UVTROMlkyWldNeg; hzd=acfa5231-c483-421e-b7c9-8586c303569b%3A%3A%3A%3A%3AGetStarted; _ga_PB0RC2CT7B=GS1.1.1689076492.1.1.1689076494.58.0.0; _ga=GA1.1.263616427.1689076492; _uetsid=bec9eae01fe111eebcaed1af8211f75e; _uetvid=beca1c901fe111ee975175ae1159fa27',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.houzz.com/professionals/hznb/probr2-bo~t_11785~b_1v3-1v4',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


# Define the function `get_url_company`
def get_url_company():
    # Open 'houzz_input.txt' file in read mode
    with open('houzz_input.txt', 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Remove any leading/trailing white spaces from the line and assign it to variable `url`
            url = line.strip()
            # Send a GET request to the url and retrieve the server's response
            response = requests.get(url, cookies=cookies, headers=headers, )
            # Get the text of the response and assign it to `src`
            src = response.text

            # Create a BeautifulSoup object and parse the `src` using lxml parser
            soup = BeautifulSoup(src, 'lxml')
            # Find a 'script' tag with 'application/json' type in the parsed HTML
            script_json = soup.find('script', type="application/json")
            # Load the content of the script tag as a JSON
            data_json = json.loads(script_json.string)
            try:
                # Try to retrieve the total number of pages from the JSON data and convert it to integer
                pagination_total = int(
                    data_json['data']['stores']['data']['ViewProfessionalsStore']['data']['paginationSummary'][
                        'total'].replace(
                        ',', ''))
            except:
                # If not possible, skip to the next iteration
                continue
            # Calculate the amount of pages by dividing the total by 15
            amount_page = pagination_total // 15
            # Initialize a counter
            coun = 0
            # If 'url_products.csv' file exists, remove it
            if os.path.exists('url_products.csv'):
                os.remove('url_products.csv')
            # Open 'url_products.csv' file in append mode
            with open('url_products.csv', 'a', newline='', encoding='utf-8') as csvfile:
                # Create a csv writer object
                writer = csv.writer(csvfile)
                # Iterate over the range of amount of pages plus 2
                for i in range(1, amount_page + 2):
                    # Generate a random pause time between 1 and 5
                    pause_time = random.randint(1, 5)
                    # If it's the first iteration
                    if i == 1:
                        # Assign the original url to `url_first`
                        url_first = url
                        try:
                            # Try to send a GET request to the url and retrieve the server's response
                            response = requests.get(url_first, cookies=cookies, headers=headers, )
                            # Get the text of the response and assign it to `src_1`
                            src_1 = response.text
                            # Create a BeautifulSoup object and parse the `src_1` using lxml parser
                            soup = BeautifulSoup(src_1, 'lxml')
                            try:
                                # Try to find all the urls of the products in the parsed HTML
                                products_urls = soup.find('ul', attrs={'class': 'hz-pro-search-results mb0'}).find_all(
                                    'a')
                            except:
                                # If not possible, skip to the next iteration
                                continue
                            # For each product url found
                            for u in products_urls:
                                # Get the 'href' attribute (the url) of the product and write it into the CSV file
                                url = u.get("href")
                                writer.writerow([url])
                        except:
                            # If not possible, skip to the next iteration
                            continue

                    # If it's not the first iteration
                    elif i > 1:
                        # Increase the counter by 15
                        coun += 15
                        # Generate the new url by adding the counter to the original url
                        urls = f'{url}?fi={coun}'
                        try:
                            # Try to send a GET request to the url and retrieve the server's response
                            response = requests.get(urls, cookies=cookies, headers=headers, )
                            # Get the text of the response and assign it to `src_2`
                            src_2 = response.text
                            # Create a BeautifulSoup object and parse the `src_2` using lxml parser
                            soup = BeautifulSoup(src_2, 'lxml')
                            try:
                                # Try to find all the urls of the products in the parsed HTML
                                products_urls = soup.find('ul', attrs={'class': 'hz-pro-search-results mb0'}).find_all(
                                    'a')
                            except:
                                # If not possible, skip to the next iteration
                                continue
                            # For each product url found
                            for u in products_urls:
                                # Get the 'href' attribute (the url) of the product and write it into the CSV file
                                url = u.get("href")
                                writer.writerow([url])
                        except:
                            # If not possible, skip to the next iteration
                            continue
                    # Sleep for the pause time before the next iteration
                    time.sleep(pause_time)


def get_company():
    # Open a CSV file for writing company data
    with open('data_test.csv', "w", errors='ignore', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",", lineterminator="\r", quoting=csv.QUOTE_ALL)

        # Define headers for the CSV file
        headers_csv = ('url', 'name_company', 'www_company', 'telephone_company', 'address', 'street_address',
                       'addressLocality', 'addressRegion', 'postalCode', 'addressCountry', 'emails',
                       "Commercial", "Residential", "LEED", "Greengaurd", "Phthalates", "Polyvinyl", "PVC")
        # Write the headers to CSV file
        writer.writerow(headers_csv)

        # Open another CSV file for reading company URLs
        with open('url_products.csv', newline='', encoding='utf-8') as files:
            # Use csv reader to read the URLs
            csv_reader = list(csv.reader(files, delimiter=' ', quotechar='|'))

            # Iterate through each URL
            for url in csv_reader:
                # Initialize a set for emails
                emails = set()

                # Send a GET request to the URL
                response = requests.get(url[0], cookies=cookies, headers=headers, )
                # Parse the response using BeautifulSoup
                src = response.text
                soup = BeautifulSoup(src, 'lxml')

                # Find the JSON script tag in the parsed HTML
                script_tag = soup.find('script', {'type': 'application/json'})

                # Initialize JSON data
                try:
                    # Load the JSON data from the script tag
                    json_data = json.loads(script_tag.string)
                except:
                    # If JSON data is not found, continue to the next URL
                    continue

                # The following blocks try to extract different information
                # from the JSON data. If a piece of data is not found, it
                # assigns a default value to the corresponding variable.
                # This pattern is repeated for each piece of information.

                # Extract the 'sfru' value from the JSON data
                try:
                    sfru = json_data['sfru']
                except:
                    sfru = None

                # Extract the company name from the JSON data
                try:
                    name_company = \
                    json_data['data']['stores']['data']['MetaDataStore']['data']['htmlMetaTags'][2]['attributes'][
                        'content']
                except:
                    name_company = None

                # Extract the company phone number from the JSON data
                try:
                    telephone_company = \
                    json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional'][
                        'formattedPhone']
                except:
                    telephone_company = None

                # Extract the company website from the JSON data
                try:
                    www_company = \
                    json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['rawDomain']
                except:
                    www_company = None

                # Send a GET request to the company website
                try:
                    main_site = requests.get(www_company)
                except requests.exceptions.RequestException:
                    main_site = None

                # The following code block searches for keywords on the company's main website
                # and follows all links on the website to extract further information, including emails.
                # If a keyword is found in the text of the website, the corresponding variable is set to 'yes',
                # otherwise it remains 'no'.

                # Initialize the keywords
                Commercial = ''
                Residential = ''
                LEED = ''
                Greengaurd = ''
                Phthalates = ''
                Polyvinyl = ''
                PVC = ''

                # If the company's main website is reachable
                if main_site is not None:
                    main_soup = BeautifulSoup(main_site.text, 'html.parser')

                    # Add all emails from the main site text to the emails set
                    emails |= set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', main_site.text))
                    main_text = main_soup.get_text().lower()

                    # Check for keywords in the main site text
                    Commercial = 'yes' if 'commercial' in main_text else 'no'
                    Residential = 'yes' if 'residential' in main_text else 'no'
                    LEED = 'yes' if 'leed' in main_text else 'no'
                    Greengaurd = 'yes' if 'greengaurd' in main_text else 'no'
                    Phthalates = 'yes' if 'phthalates' in main_text else 'no'
                    Polyvinyl = 'yes' if 'polyvinyl' in main_text else 'no'
                    PVC = 'yes' if 'pvc' in main_text else 'no'

                    # Get all links from the main site
                    main_links = set([a['href'] for a in main_soup.find_all('a', href=True)])

                    # Iterate through each link on the main site
                    for link in main_links:
                        if not link.startswith('http'):
                            if www_company.endswith('/') and link.startswith('/'):
                                link = www_company + link[1:]
                            else:
                                link = www_company + link

                        # Send a GET request to the link
                        try:
                            site = requests.get(link)
                        except requests.exceptions.RequestException:
                            continue

                        # Parse the response from the link
                        soup = BeautifulSoup(site.text, 'html.parser')
                        domain = urlparse(www_company).netloc

                        # Find all emails in the link's text and add them to the emails set
                        matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', site.text)
                        emails |= set([email for email in matches if
                                       not (email.endswith('.png') or email.endswith('.jpg')) and email.endswith(
                                           domain)])

                        # Get the text of the link's content
                        text = soup.get_text().lower()

                        # Check for keywords in the link's text
                        Commercial = 'yes' if 'commercial' in text else Commercial
                        Residential = 'yes' if 'residential' in text else Residential
                        LEED = 'yes' if 'leed' in text else LEED
                        Greengaurd = 'yes' if 'greengaurd' in text else Greengaurd
                        Phthalates = 'yes' if 'phthalates' in text else Phthalates
                        Polyvinyl = 'yes' if 'polyvinyl' in text else Polyvinyl
                        PVC = 'yes' if 'pvc' in text else PVC

                # Extract the address information from the JSON data
                try:
                    address = \
                    json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['address'][
                        'fullAddress']
                    street_address = \
                    json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['address'][
                        'streetAddress']
                    addressLocality = \
                    json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['address'][
                        'addressLocality']
                    addressRegion = \
                    json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['address'][
                        'addressRegion']
                    postalCode = \
                    json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['address'][
                        'postalCode']
                    addressCountry = \
                    json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['address'][
                        'addressCountry']
                except:
                    address = None
                    street_address = None
                    addressLocality = None
                    addressRegion = None
                    postalCode = None
                    addressCountry = None

                # Prepare a row to be written to the CSV file
                row = (url, name_company, www_company, telephone_company, address, street_address, addressLocality,
                       addressRegion,
                       postalCode, addressCountry, emails, Commercial, Residential, LEED, Greengaurd, Phthalates,
                       Polyvinyl, PVC)

                # Write the row to the CSV file
                writer.writerow(row)


if __name__ == '__main__':
    get_url_company()
    get_company()
