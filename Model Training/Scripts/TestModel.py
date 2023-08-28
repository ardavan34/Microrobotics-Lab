import torch
import numpy as np
from NeuralNetwork import *
from ModelHelpers import *


device = 'cpu'
model = ArdavanNet_3().to(device=device)
model.load_state_dict(torch.load("./Model Training/Models/ArdavanNet_3.pth"))
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

newList = [x ** 0.5 for x in lossList]
print(sum(newList) / len(newList))
print(np.std(newList))