import requests
import json

data = []
url = "https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true"
response = requests.get(url)
apidata = response.text
restaurants = json.loads(apidata)
for el in restaurants['searchResults']:
    address = \
        el['storePublic']['contacts']['streetAddress']['ru'] if 'ru' in el['storePublic']['contacts'][
            'streetAddress'] \
            else el['storePublic']['contacts']['streetAddress']

    latlon = el['storePublic']['contacts']['coordinates']['geometry']['coordinates']
    name = el['storePublic']['title']['ru']
    phones = el['storePublic']['contacts']['phoneNumber']
    wh = el['storePublic']['openingHours']['regular']
    working_hours = \
        ["closed"] if el['storePublic'][
                          'status'] == "Closed" else ([f"пн-пт {wh['startTimeLocal']} до {wh['endTimeLocal']},"
                                                       f" сб-вс {wh['startTimeLocal']}-{wh['endTimeLocal']}"])

    data.append({
        "address": address,
        "lanton": latlon,
        "name": name,
        "phones": phones,
        "working_hours": working_hours
    })

with open('kfc.json', 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, indent=2, ensure_ascii=False)
