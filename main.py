import csv
import json
import sys
import os.path


def main():
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print("Usage: ./main.py inFile.csv [outFile.json]")
        return -1

    outFile = './out.json' if len(sys.argv) == 2 else sys.argv[2]
    inFile = sys.argv[1]
    if not os.path.isfile(inFile) or not inFile.endswith(".csv"):
        print("Invalid csv input file")
        return -1
    make_json(inFile, outFile)


def make_json(csvFilePath, jsonFilePath):
    data = []

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

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
