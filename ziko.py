from bs4 import BeautifulSoup
import requests
import json

url = "https://www.ziko.pl/lokalizator/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
pharmacies = soup.find_all('tr', class_='mp-pharmacy-element')
data = []

for el in pharmacies:
    hours = el.find('td', class_='mp-table-hours').find_all('span')
    link = el.find('div', class_='morepharmacy').find('a', href=True)
    r1 = requests.get("https://www.ziko.pl" + link['href'])
    soup1 = BeautifulSoup(r1.text, 'lxml')
    span_list = soup1.find_all('span', attrs={'style': "margin-left: 5px;"})
    name = span_list[0].text
    address = f"{span_list[1].text}, {span_list[2].text}"
    phone = span_list[4].text
    coords = soup1.find('div', class_='coordinates').find_all('span')
    lat = ''.join(i for i in coords[0].text if not i.isalpha())
    lon = ''.join(i for i in coords[1].text if not i.isalpha())
    latlon = [float(lat[3:]), float(lon[3:])]
    data.append({
        'address': address,
        'latlon': latlon,
        'name': name,
        'phones': phone,
        'working_hours': [i.text for i in hours]
    })

with open('ziko.json', 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, indent=2, ensure_ascii=False)
