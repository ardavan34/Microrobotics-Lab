import torch
import numpy as np
from NeuralNetwork import SimpleNeuralNetwork
import ModelHelpers


model = SimpleNeuralNetwork()
model.load_state_dict(torch.load("./Model Training/Models/ArdavanNet_3.pth"))

testInput = torch.tensor([-0.057, 3.386, 7.098, 6.472, 14.358, 3.652, 2.649, 16.934, -41.025, 14.131, 69.848])
testActualOutput = torch.tensor([22.611485916439555, 0.9199387151462516, 15.34238691214148])
testPredictedOutput = model(testInput)
testPredictedOutputNorm = model(ModelHelpers.normalize(testInput))

print(testActualOutput)
print(testPredictedOutput)
print(testPredictedOutputNorm)