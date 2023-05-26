"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 
 
-> Filename: input-generator.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Script for generating the input arrays, saving them into JSON files, and analyzing the data distribution
-> Starting Date: May 18, 2023
"""

import json
from input_helpers import *

"""
Main function
"""
# Set the initials for our training data
numOfData = 100   # number of datasets in each json file
numOfFiles = 50   # number of json files
xRange = [-100, 100]   # in mm
yRange = [-100, 100]   # in mm
zRange = [0, 100]   # in mm
currentRange = [-18, 18]   # in Ampere
fileInputs = []
allInputs = []

for file in range(numOfFiles):

    # Generate a list of inputs for one of the files and save them in our lists
    for data in range(numOfData):
        inputArr = inputGenerator(xRange, yRange, zRange, currentRange)
        inputDict = jsonStacker(inputArr)
        fileInputs.append(inputDict)
        allInputs.append(inputDict)

    # Write the dataset into a json file
    jsonInput = json.dumps(fileInputs, indent=4)

    with open("./Data Collection/Input/Input Datasets/Input" + str(file + 1) + ".json", "w") as outfile:
        outfile.write(jsonInput)

    # Clear the list for other files
    fileInputs.clear()

# Plot the data distribution for all points
dataAnalysis(allInputs, 0)