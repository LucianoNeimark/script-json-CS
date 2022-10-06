import csv
import json
import sys
import os.path
from firebase_admin import firestore, credentials, initialize_app


def main():
    if len(sys.argv) <= 2 or len(sys.argv) > 4:
        print("Usage: ./main.py inFile.csv key.json")
        return -1

    inFile = sys.argv[1]
    key = sys.argv[2]

    if not os.path.isfile(inFile) or not inFile.endswith(".csv"):
        print("Invalid csv input file")
        return -1

    if not os.path.isfile(key) or not key.endswith(".json"):
        print("Invalid key file")
        return -1

    cred = credentials.Certificate(key)
    initialize_app(cred)
    
    data, ids = make_json(inFile)
    addTeam(ids, data)


def make_json(csvFilePath):
    data = []
    ids = []
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            if invalidRow(row):
                print('Invalid row, skipping')
                print(row)
                continue
            
            rowDict = {
                "name": row['Nombre completo'],
                "title": row['Departamento'],
                "social": [],
                "image": {
                    "src": row['Foto'],
                    "alt": row['Nombre completo']
                }
            }

            socialMediaSources = ["Instagram", "Linkedin", "Github", "WebPersonal"]
            for source in socialMediaSources:
                sourceVal = row[source]
                if sourceVal != "":
                    rowDict["social"].append({
                        "logo": source.lower(),
                        "href": sourceVal,
                    })
            data.append(rowDict.copy())
            ids.append(row['Legajo'])

    return data, ids


def addTeam(ids, team):
    db = firestore.client()
    for idx, member in enumerate(team):
        db.collection(u'team').document(ids[idx]).set(member)

def invalidRow(row):
    return row['Legajo'] == '' or row['Foto'] == '' or row['Nombre completo'] == '' or row['Departamento'] == ''


if __name__ == "__main__":
    main()
