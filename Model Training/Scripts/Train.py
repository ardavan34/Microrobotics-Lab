"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: Train.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Script for training our model
-> Starting Date: Jun 6, 2023
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ModelHelpers import *
from Dataset import ENSDataset
from NeuralNetwork import *
import torch
from torch.utils.data import Dataset, DataLoader

"""
Main function
"""
# List of hyperparameters involved in model training
hyperparam = {'neuralNet': ArdavanNet_4(batchSize=512), 'modelName': "ArdavanNet_4", 'batchSize': 256,
              'learning rate': 1e-3, 'lossFunction': torch.nn.MSELoss(), 'epochsNum': 1500}

# Select our device
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

# Initialize our model
model = hyperparam['neuralNet'].to(device=device)
model.batchSize = hyperparam['batchSize']

# Set the and optimizer
hyperparam['optimizer'] = torch.optim.Adam(model.parameters(), lr=hyperparam['learning rate'], weight_decay=1e-3)

# Generate the train-dev dataset
fileNum = 50
trainDevInArray, trainDevOutArray = datasetGenerator(fileNum, fileNum + 1)
trainDevInput = torch.tensor(trainDevInArray.T)
trainDevActualOutput = torch.tensor(trainDevOutArray.T)
trainDevInput = trainDevInput.reshape(trainDevInput.shape[0], 1, trainDevInput.shape[1])
trainDevActualOutput = trainDevActualOutput.reshape(trainDevActualOutput.shape[0], 1, trainDevActualOutput.shape[1])
print(trainDevInput)
print(trainDevInput.shape)
# Generate the test dataset
testInput, testActualOutput = testDataCollector()
print(testInput)
print(testInput.shape)

# Generate the input data and number of samples
fromFile = 1
toFile = 49
inputMatrix, outputMatrix = datasetGenerator(fromFile, toFile + 1)

# Load the dataset for our model
trainSet = ENSDataset(inputMatrix, outputMatrix)
trainDataLoader = DataLoader(trainSet, batch_size=hyperparam['batchSize'], shuffle=True)

# Generate the mini batches
trainInput, trainOutput = next(iter(trainDataLoader))
print(f"Input batch shape: {trainInput.size()}")
print(f"Output batch shape: {trainOutput.size()}")

# Train the model with 5 times of iteration
trainLossList = []
trainDevLossList = []
testLossList = []
for t in range(hyperparam['epochsNum']):
    print(f"Epoch {t+1}\n-------------------------------")
    epochLoss = train(trainDataLoader, model, hyperparam['lossFunction'], hyperparam['optimizer'], device)
    print(f'epoch loss: {epochLoss}')
    trainLossList.append(epochLoss)
    trainDevEpochLoss = test(trainDevInput, trainDevActualOutput, model, hyperparam['lossFunction'], device)
    trainDevLossList.append(trainDevEpochLoss)
    testEpochLoss = test(testInput, testActualOutput, model, hyperparam['lossFunction'], device)
    testLossList.append(testEpochLoss)

# Save the trained model and the visual graph
torch.save(model.state_dict(), "./Model Training/Models/" + hyperparam['modelName'] + ".pth")
graph(trainLossList, trainDevLossList, testLossList, hyperparam['modelName'])
print("Done!")
print(model)
