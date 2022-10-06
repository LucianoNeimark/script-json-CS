from audioop import add
import csv
import json
import sys
import os.path
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials


def main():

    if len(sys.argv) <= 2 or len(sys.argv) > 4:
        print("Usage: ./main.py inFile.csv key.json [outFile.json]")
        return -1

    outFile = './out.json' if len(sys.argv) == 3 else sys.argv[3]
    inFile = sys.argv[1]
    key = sys.argv[2]

    if not os.path.isfile(inFile) or not inFile.endswith(".csv"):
        print("Invalid csv input file")
        return -1

    if not os.path.isfile(key) or not key.endswith(".json"):
        print("Invalid csv input file")
        return -1

    cred = credentials.Certificate(key)
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    data, ids = make_json(inFile, outFile)
    addToCollection(data, ids, db)


def make_json(csvFilePath, jsonFilePath):
    data = []
    ids = []
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            rowDict = {
                "name": rows['Nombre completo'],
                "title": rows['Departamento'],
                "social": [],
                "image": {
                    "src": "",
                    "alt": rows['Nombre completo']
                }
            }
            socialMediaSources = ["Instagram", "Linkedin", "Github"]
            for source in socialMediaSources:
                sourceVal = rows[source]
                if sourceVal != "":
                    rowDict["social"].append({
                        "logo": source.lower(),
                        "href": sourceVal,
                    })
            data.append(rowDict.copy())
            ids.append(rows["Legajo"])
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=2))

    return data, ids


def addToCollection(team, ids, db):
    for i, member in enumerate(team):
        db.collection(u'team').document(ids[i]).set(member)


if __name__ == "__main__":
    main()
