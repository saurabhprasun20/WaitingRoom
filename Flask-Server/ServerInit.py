import json

with open("data.json", "r+") as jsonFile:
    data = json.load(jsonFile)
    data['cycleChange'] = 1
    jsonFile.seek(0)  # rewind
    json.dump(data, jsonFile)
    jsonFile.truncate()
