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
from NeuralNetwork import SimpleNeuralNetwork
import torch
from torch.utils.data import Dataset, DataLoader

"""
Main function
"""
# Generate the train-dev dataset
fileNum = 50
trainDevInArray, trainDevOutArray = datasetGenerator(fileNum, fileNum + 1)
trainDevInput = torch.tensor(trainDevInArray.T)
trainDevActualOutput = torch.tensor(trainDevOutArray.T)
print(trainDevInput)
print(trainDevInput.shape)
# Generate the test dataset
testInput, testActualOutput = testDataCollector()

# Generate the input data and number of samples
fromFile = 1
toFile = 49
inputMatrix, outputMatrix = datasetGenerator(fromFile, toFile + 1)

# Load the dataset for our model
trainSet = ENSDataset(inputMatrix, outputMatrix)
trainDataLoader = DataLoader(trainSet, batch_size=64, shuffle=False)

# Generate the mini batches
trainInput, trainOutput = next(iter(trainDataLoader))
print(f"Input batch shape: {trainInput.size()}")
print(f"Output batch shape: {trainOutput.size()}")

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
model = SimpleNeuralNetwork().to(device=device)
print(model)

# List of hyperparameters involved in model training
hyperparam = {'learning rate': 1e-3}

# Set our loss function and optimizer
lossFunction = torch.nn.MSELoss()
trainLossList = []
trainDevLossList = []
testLossList = []
optimizer = torch.optim.SGD(model.parameters(), lr=hyperparam['learning rate'])

# Train the model with 5 times of iteration
epochs = 1000
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    epochLoss = train(trainDataLoader, model, lossFunction, optimizer, device)
    trainLossList.append(epochLoss)
    trainDevEpochLoss = test(trainDevInput, trainDevActualOutput, model, lossFunction, device)
    trainDevLossList.append(trainDevEpochLoss)
    testEpochLoss = test(testInput, testActualOutput, model, lossFunction, device)
    testLossList.append(testEpochLoss)

# Save the trained model
torch.save(model.state_dict(), "./Model Training/Models/SimpleModel.pth")
print("Done!")

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
plt.savefig("figure.png")
plt.show()

