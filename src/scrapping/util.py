import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                  'Safari/537.36'
}


def goszakup_scrapping_all_suppliers(url: str, is_verify: bool):
    suppliers = []

    page = requests.get(url, headers=headers, verify=is_verify)

    soup = BeautifulSoup(page.text, 'html.parser')

    table_element = soup.find('table', {'class': 'table table-bordered table-hover'})

    for link in table_element.find_all('a'):
        suppliers.append(goszakup_scrapping_from_details_supplier(link['href'], False))

    return suppliers


def goszakup_scrapping_from_details_supplier(url: str, is_verify: bool):
    page = requests.get(url, headers=headers,
                        verify=is_verify)

    soup = BeautifulSoup(page.text, 'html.parser')

    th_elements = soup.find_all('th')
    td_elements = soup.find_all('td')

    keys = []
    values = []

    for th in th_elements:
        keys.append(th.text.strip())

    for td in td_elements:
        values.append(td.text.strip())

    data = {}

    desired_fields = ['БИН участника', 'ФИО', 'ИИН', 'Полный адрес(каз)']

    for i in range(len(keys)):
        if keys[i] in desired_fields:
            data[keys[i]] = values[i]

    return data
