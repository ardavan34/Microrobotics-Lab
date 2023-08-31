"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: TestModel.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Testing performance of the deep learning models
-> Starting Date: Aug 7, 2023
"""

import torch
import numpy as np
from NeuralNetwork import *
from ModelHelpers import *


# Load the model to test
device = 'cpu'
model = ArdavanNet_4().to(device=device)
model.load_state_dict(torch.load("./Model Training/Models/ArdavanNet_4.pth", map_location=torch.device(device)))
model.double()
model.eval()
lossFunc = torch.nn.MSELoss()

# Generate the test dataset
testInput, testActualOutput = testDataCollector()
lossList = []
for (inputSet, outputSet) in zip(testInput, testActualOutput):
    testPredictedOutput = model(inputSet.to(device=device))
    loss = lossFunc(testPredictedOutput.to(device=device), outputSet.to(device=device))
    lossList.append(loss.item())

newList = [x ** 0.5 for x in lossList]   # Take the root of all of the squared errors
print(np.mean(newList))   # Calculate the average
print(np.std(newList))   # Calculate the standard deviation