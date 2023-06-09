"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: Test.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Script for testing the accuracy of our model
-> Starting Date: Jun 6, 2023
"""

import numpy as np
import torch
from NeuralNetwork import SimpleNeuralNetwork

"""
Main function
"""
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
error = torch.tensor(np.empty(3))

testingModel = SimpleNeuralNetwork().to(device)
testingModel.load_state_dict(torch.load("./Model Training/Models/SimpleModel.pth"))

# upload testing dataset
# predict using the model
pred = torch.tensor(np.array([1.0, 3.0, 5.0]))
y = torch.tensor(np.array([3.0, 3.0, 3.0]))

testLoss = torch.nn.MSELoss()
for params in range(len(y)):
    loss = testLoss(pred[params], y[params])
    error[params] = -loss if pred[params] < y[params] else loss

print(error)