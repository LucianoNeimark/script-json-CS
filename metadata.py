import sys
import os.path
from firebase_admin import storage, credentials, initialize_app


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
    initialize_app(cred, {
        'storageBucket': 'webpage-36e40.appspot.com'
    })
    
    file_names = []
    with open(inFile, encoding='utf-8') as csvf:
        csvf.readline() # Skip header
        for row in csvf:
            file_names.append("team/{}.jpg".format(row.split(',')[1]))

    metadata = {'Cache-Control': 'public, max-age=86400', 'Content-Type': 'image/jpeg'}

    bucket = storage.bucket()
    for file_name in file_names:
        blob = bucket.get_blob(file_name)
        if blob is None:
            print("File not found: " + file_name)
            continue

        blob.metadata = metadata
        blob.patch()

if __name__ == "__main__":
    main()
