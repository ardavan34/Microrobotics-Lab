"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: TrainHelpers.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: A helper script including all of the functions that are called in Train.py
-> Starting Date: Jun 6, 2023
"""

import json
import numpy as np


def inputOutputGenerator(datasetSize):
    inputUnits = 14
    outputUnits = 6
    inputDataMatrix = np.empty((inputUnits, datasetSize * 100), dtype=float)
    outputDataMatrix = np.empty((outputUnits, datasetSize * 100), dtype=float)

    inputPath = "./Data Collection/Input/Input Datasets/Input"
    outputPath = "./Data Collection/Output/Output"
    for dataset in range(datasetSize):
        inputFile = open(inputPath + str(dataset + 1) + ".json")
        inputData = json.load(inputFile)
        outputFile = open(outputPath + str(dataset + 1) + ".json")
        outputData = json.load(outputFile)
        
        for set in range(len(inputData)):
            inputItems = inputData[set].items()
            inputArray = np.array(list(inputItems))
            inputArray = np.array(np.delete(inputArray, 0, axis=1), dtype=float)
            
            inputDataMatrix[:, (100 * dataset)+set] = np.reshape(inputArray, (inputUnits,))

            outputItems = outputData[set].items()
            outputArray = np.array(list(outputItems))
            outputArray = np.array(np.delete(outputArray, 0, axis=1), dtype=float)
            outputArray = np.array(np.delete(outputArray, 0, axis=0), dtype=float)
            
            outputDataMatrix[:, (100 * dataset)+set] = np.reshape(outputArray, (outputUnits,))
    
    return inputDataMatrix, outputDataMatrix
