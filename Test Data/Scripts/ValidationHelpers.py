"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: ValidationHelpers.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: A helper script including all of the functions that are called in ValidationSimulation.py
-> Starting Date: Jun 9, 2023
"""

import json


def txtParserVal(txtFilePath, inputNum):
    """
    Helper function to parse the text file exported from the simulation
    """
    # Set up variables
    magneticField = ['Bx', 'By', 'Bz']
    result = {}

    with open(txtFilePath, "r") as txtFile:
        for line in txtFile:
            dataList = [float(val) for val in line.split()]   # list of numbers in each line. first 3 are for position, last 3 are the magnetic field densities
            result["input set"] = inputNum
            for i in range(1, 4):
                result[magneticField[i-1]] = dataList[i+2]   # save the magnetic fields
    
    return result


def readFileVal(inputNum, filePath, newResult):
    """
    Helper function to read (load) the already-existing json file
    """
    output = []

    # Load the previously saved data if the file is not empty
    if inputNum != 0:
        with open(filePath, "r") as jsonFile:
            output = json.load(jsonFile)
    output.append(newResult)

    return output


def writeFileVal(filePath, newOutput):
    """
    Helper function to update the json file with our new results
    """
    # Write the dataset into a json file
    with open(filePath, "w") as jsonFile:
        jsonInput = json.dumps(newOutput, indent=4)
        jsonFile.write(jsonInput)