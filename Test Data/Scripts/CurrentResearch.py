import json

filePath = "./Data Collection/Output/Output1.json"
file = open(filePath)
data = json.load(file)
limited = True
count = 0

compareList = [101, 50, 50, 50, 50, 50, 50]
for set in range(len(data)):
    for outElem, refElem in zip(list(data[set].values()), compareList):
        if (abs(outElem) > refElem):
            limited = False
            break
    
    if limited == True:
        count += 1
    else:
        limited = True

print(count)
        