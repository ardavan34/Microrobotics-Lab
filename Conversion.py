import json

filePath = "./Test Data/Old Test/TheoreticalResult.json"
newFilePath = "./Test Data/Old Test/TheoreticalResultmT.json"

file = open(filePath)
data = json.load(file)

for set in data:
    set['Bx'] *= 1000.0
    set['By'] *= 1000.0
    set['Bz'] *= 1000.0

with open(newFilePath, "w") as jsonFile:
    jsonInput = json.dumps(data, indent=4)
    jsonFile.write(jsonInput)



