"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: ModelHelpers.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: A helper script including all of the functions that are called in Train.py and Test.py
-> Starting Date: Jun 6, 2023
"""

import json
import numpy as np
import torch
from torch.utils.data import DataLoader


def datasetGenerator(fromFile, toFile):
    inputUnits = 14
    outputUnits = 6
    inputDataMatrix = np.empty((inputUnits, (toFile - fromFile) * 100), dtype=float)
    outputDataMatrix = np.empty((outputUnits, (toFile - fromFile) * 100), dtype=float)

    inputPath = "./Data Collection/Input/Input Datasets/Input"
    outputPath = "./Data Collection/Output/Output"
    for dataset in range(fromFile, toFile):
        inputFile = open(inputPath + str(dataset) + ".json")
        inputData = json.load(inputFile)
        outputFile = open(outputPath + str(dataset) + ".json")
        outputData = json.load(outputFile)
        
        for set in range(len(inputData)):
            inputItems = inputData[set].items()
            inputArray = np.array(list(inputItems))
            inputArray = np.array(np.delete(inputArray, 0, axis=1), dtype=float)
            
            inputDataMatrix[:, (100 * (dataset - fromFile))+set] = np.reshape(inputArray, (inputUnits,))

            outputItems = outputData[set].items()
            outputArray = np.array(list(outputItems))
            outputArray = np.array(np.delete(outputArray, 0, axis=1), dtype=float)
            outputArray = np.array(np.delete(outputArray, 0, axis=0), dtype=float)
            
            outputDataMatrix[:, (100 * (dataset - fromFile))+set] = np.reshape(outputArray, (outputUnits,))
    
    return inputDataMatrix, outputDataMatrix


def train(dataloader, model, lossFunc, optimizer, device):
    model.double()
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = lossFunc(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        print(f"loss: {loss:>7f}")