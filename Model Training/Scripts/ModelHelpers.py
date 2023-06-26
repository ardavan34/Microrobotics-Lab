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
    """
    Generate the dataset in numpy array format
    Loads the json files
    """
    inputUnits = 11   # number of input units
    outputUnits = 3   # number of output units
    # Generate the empty arrays
    inputDataMatrix = np.empty((inputUnits, (toFile - fromFile) * 100), dtype=float)
    outputDataMatrix = np.empty((outputUnits, (toFile - fromFile) * 100), dtype=float)

    inputPath = "./Data Collection/Input/Input Datasets/Input"
    outputPath = "./Data Collection/Output/Output"
    for dataset in range(fromFile, toFile):

        # Load the json files
        inputFile = open(inputPath + str(dataset) + ".json")
        inputData = json.load(inputFile)
        outputFile = open(outputPath + str(dataset) + ".json")
        outputData = json.load(outputFile)
        
        for set in range(len(inputData)):

            # Set the input items into seperate column vectors
            inputItems = inputData[set].items()
            inputArray = np.array(list(inputItems)[:inputUnits])
            inputArray = np.array(np.delete(inputArray, 0, axis=1), dtype=float)
            # Rewrite the column of the matrix with the new sample
            inputDataMatrix[:, (100 * (dataset - fromFile))+set] = np.reshape(inputArray, (inputUnits,))

            # Set the output items into seperate column vectors
            outputItems = outputData[set].items()
            outputArray = np.array(list(outputItems)[:outputUnits + 1])
            outputArray = np.array(np.delete(outputArray, 0, axis=1), dtype=float)
            outputArray = np.array(np.delete(outputArray, 0, axis=0), dtype=float)
            # Rewrite the column of the matrix with the new sample
            outputDataMatrix[:, (100 * (dataset - fromFile))+set] = np.reshape(outputArray, (outputUnits,))
    
    print(inputDataMatrix)
    print(inputDataMatrix.shape)
    print(outputDataMatrix)
    print(outputDataMatrix.shape)
    return inputDataMatrix, outputDataMatrix


def train(dataloader, model, lossFunc, optimizer, device):
    """
    Train the DL model
    """
    model.double()   # change the format to float64
    model.train()
    lossList = []

    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = lossFunc(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        lossList.append(loss.item())
        print(f"loss: {loss:>7f}")

    return lossList