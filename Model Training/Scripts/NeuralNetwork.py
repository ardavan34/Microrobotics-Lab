"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: NeuralNetwork.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Class(es) for the neural network model(s) used for training
-> Starting Date: Jun 6, 2023
"""

import torch
from torch import nn

class SimpleNeuralNetwork(nn.Module):
    """
    Class for a simply neural network as a DL model
    """
    def __init__(self):
        """
        Constructor of the model
        """
        super().__init__()
        # Set the model with two hidden layers, each 20 units, with ReLU activatoin function
        self.linearRelu = nn.Sequential( 
            nn.Linear(in_features=14, out_features=20),
            nn.ReLU(),
            nn.Linear(in_features=20, out_features=20),
            nn.ReLU(),
            nn.Linear(in_features=20, out_features=6)
        )

    def forward(self, input):
        """
        Apply the forward propagation
        """
        logits = self.linearRelu(input)
        return logits
    