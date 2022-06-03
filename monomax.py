import requests
import json
import re

data = []
url = "http://monomax.by/map"
r = requests.get(url)
stores = re.findall(r'Placemark\([\w\W]+?\}', r.text)

for store in stores:
    latlon = re.search(r'\d{2}\.\d{6,30}\,\s+\d{2}\.\d{6,30}', store).group(0).split(',')
    phone = re.search(r'\+\d{3}\s*\(*\d{2}\)*\s*\d{3}\s*\d{2}\s*\d{2}', store).group(0)
    address = re.search(r'\w+[А-ЯЁа-яё].*\s*\w+[А-ЯЁа-яё]\,*\s*\w+\S', store).group(0)

    data.append({
        'address': address,
        'latlon': [float(latlon[0]), float(latlon[1])],
        'name': 'Мономах',
        'phones': phone
    })

with open('monomax.json', 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, indent=2, ensure_ascii=False)

