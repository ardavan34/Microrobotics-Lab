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
import pandas as pd
import torch
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt


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

    inputPath = "./Data Collection/Simulation/Input/Input Datasets/Input"
    outputPath = "./Data Collection/Simulation/Output/Output"
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
            inputArray = normalize(inputArray)
            # Rewrite the column of the matrix with the new sample
            inputDataMatrix[:, (100 * (dataset - fromFile))+set] = np.reshape(inputArray, (inputUnits,))

            # Set the output items into seperate column vectors
            outputItems = outputData[set].items()
            outputArray = np.array(list(outputItems)[:outputUnits + 1])
            outputArray = np.array(np.delete(outputArray, 0, axis=1), dtype=float)
            outputArray = np.array(np.delete(outputArray, 0, axis=0), dtype=float)
            # Rewrite the column of the matrix with the new sample
            outputDataMatrix[:, (100 * (dataset - fromFile))+set] = np.reshape(outputArray, (outputUnits,))
    
    return inputDataMatrix, outputDataMatrix


def testDataCollector():
    df = pd.read_csv("Test Data/Old Test/2023-02-03_10-49-44-validation-100points-RobotLog.csv")
    selectedCols = {'cmdCoilCurrent_A_1': 1.0, 'cmdCoilCurrent_A_2': 1.0, 'cmdCoilCurrent_A_3': 1.0, 
                'cmdCoilCurrent_A_4': 1.0, 'cmdCoilCurrent_A_5': 1.0, 'cmdCoilCurrent_A_6': 1.0,
                'cmdCoilCurrent_A_7': 1.0, 'cmdCoilCurrent_A_8': 1.0, 'tableCmdPos_m_1': 1000.0,
                'tableCmdPos_m_2': 1000.0, 'tableCmdPos_m_3': 1000.0}
    inputDf = df[list(selectedCols.keys())]
    inputDf = inputDf.multiply(selectedCols)
    outputDf = df[['msdFieldvalue_mT_1', 'msdFieldvalue_mT_2', 'msdFieldvalue_mT_3']]

    testInArray = np.empty((100, 1, 11), dtype=float)
    testOutArray = np.empty((100, 1, 3), dtype=float)
    for row in range(len(df.index)):
        normalizedInput = normalize(inputDf.loc[pd.Index([row])].to_numpy().T)
        testInArray[row][0] = normalizedInput.T
        testOutArray[row][0] = outputDf.loc[pd.Index([row])].to_numpy()
    
    return torch.tensor(testInArray), torch.tensor(testOutArray)


def normalize(dataVector):
        
    mean = sum(dataVector) / len(dataVector)
    differences = (dataVector - mean) ** 2
    sumOfDiff = sum(differences)
    stdDev = (sumOfDiff / len(dataVector)) ** 0.5
    zscores = (dataVector - mean) / stdDev

    return zscores


def train(dataloader, model, lossFunc, optimizer, device):
    """
    Train the DL model
    """
    model.double()   # change the format to float64
    model.train()
    lossTot = 0
    batchCount = 0

    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        
        # Compute prediction error
        model.batchSize = X.shape[0]
        pred = model(X)
        loss = lossFunc(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        lossTot += loss.item()
        batchCount += 1
        # print(f"loss: {loss:>7f}")

    return (lossTot / batchCount)


def test(testInput, testActualOutput, model, lossFunc, device):
    """
    Test the DL model
    """
    model.double()   # change the format to float64
    model.eval()
    lossTot = 0

    for (setInput, setActualOutput) in zip(testInput, testActualOutput):
        X, y = setInput.to(device), setActualOutput.to(device)
        model.batchSize = X.shape[0]
        pred = model(X)
        loss = lossFunc(pred, y)
        lossTot += loss.item()
    
    return lossTot / len(testInput)

def graph(trainLossList, trainDevLossList, testLossList, modelName):

    # Graph the error plot for the train, train-dev, and test databases
    x = np.linspace(1, len(trainLossList), len(trainLossList))
    trainLoss = np.array(trainLossList)
    trainDevLoss = np.array(trainDevLossList)
    testLoss = np.array(testLossList)
    plt.rcParams.update({'font.size': 22})
    plt.figure(figsize=(25, 15))
    plt.plot(x, trainLoss, label='train')
    plt.plot(x, trainDevLoss, label='train-dev')
    plt.plot(x, testLoss, label='test')
    plt.legend(loc="upper left")
    plt.xlabel('Epoch')
    plt.ylabel('Mean-Squared-Error [mT^2]')
    plt.savefig("./Model Training/Models/" + modelName + ".png")
    plt.show()