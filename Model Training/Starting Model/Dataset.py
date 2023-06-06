"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: Dataset.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Class for loading the dataset
-> Starting Date: Jun 5, 2023
"""

import json
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader


class ENSDataset(Dataset):
    def __init__(self, datasetSize, inputTransform=None, outputTransform=None):
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
        
        self.size = inputDataMatrix.shape[1]
        self.input = torch.tensor(inputDataMatrix)
        self.output = torch.tensor(outputDataMatrix)
        self.inputTransform = inputTransform
        self.outputTransform = outputTransform

    def __len__(self):
        return self.size
    
    def __getitem__(self, index):
        inputSample = self.input[:, index]
        outputSample = self.output[:, index]

        if self.inputTransform:
            inputSample = self.inputTransform(inputSample)
        if self.outputTransform:
            outputSample = self.outputTransform(outputSample)

        return inputSample, outputSample


trainData = ENSDataset(1)
trainDataLoader = DataLoader(trainData, batch_size=32, shuffle=False)

trainInput, trainOutput = next(iter(trainDataLoader))
print(f"Feature batch shape: {trainInput.size()}")
print(f"Labels batch shape: {trainOutput.size()}")
print(trainInput)
print(trainOutput)
