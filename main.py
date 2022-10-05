
import csv
import json


def make_json(csvFilePath, jsonFilePath):
    data = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in csvReader:
            rowDict = {
                "name": rows['Nombre completo'],
                "title": rows['Departamento'],
                "social": [
                    {
                        "logo": "instagram",
                        "href": rows['Instagram'],
                    },
                    {
                        "logo": "linkedin",
                        "href": rows['Linkedin'],
                    },
                    {
                        "logo": "github",
                        "href": rows['Github'],
                    },

                ],
                "image": {
                    "src": "",
                    "alt": rows['Nombre completo']
                }
            }
            data.append(rowDict.copy())

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


csvFilePath = r'/Users/lucho/Desktop/Equipo.csv'
make_json(csvFilePath, r'./out.json')
