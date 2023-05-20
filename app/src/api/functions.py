import requests, json

def GovSpainProvincesAPI():
    urls = [
        requests.get("http://datos.gob.es/apidata/nti/territory/Province.json?_page=0"),
        requests.get("http://datos.gob.es/apidata/nti/territory/Province.json?_page=1"),
        requests.get("http://datos.gob.es/apidata/nti/territory/Province.json?_page=2"),
        requests.get("http://datos.gob.es/apidata/nti/territory/Province.json?_page=3"),
        requests.get("http://datos.gob.es/apidata/nti/territory/Province.json?_page=4"),
        requests.get("http://datos.gob.es/apidata/nti/territory/Province.json?_page=5"),
        ]
    data = []
    for url in urls:
        data.append(json.loads(url.text))

    provinces = []
    for d in data:
        for i in d["result"]["items"]:
            provinces.append(i["label"])

    return provinces