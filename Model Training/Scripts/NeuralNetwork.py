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
from ModelHelpers import normalize

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
        """
        self.linearRelu = nn.Sequential( 
            nn.Linear(in_features=11, out_features=40),
            nn.ReLU(),
            nn.Linear(in_features=40, out_features=40),
            nn.Dropout(p=0.2),
            nn.ReLU(),
            nn.Linear(in_features=40, out_features=40),
            nn.ReLU(),
            nn.Linear(in_features=40, out_features=40),
            nn.Dropout(p=0.2),
            nn.ReLU(),
            nn.Linear(in_features=40, out_features=20),
            nn.ReLU(),
            nn.Linear(in_features=20, out_features=3),
        )
        """
        self.threeIn = nn.Sequential(
            nn.Linear(in_features=3, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=32),
            nn.Dropout(p=0.2),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=8),
            nn.ReLU(),
            nn.Linear(in_features=8, out_features=3)
        )
        self.fiveIn = nn.Sequential(
            nn.Linear(in_features=5, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=32),
            nn.Dropout(p=0.2),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=8),
            nn.ReLU(),
            nn.Linear(in_features=8, out_features=3)
        )
        self.eightIn = nn.Sequential(
            nn.Linear(in_features=8, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=32),
            nn.Dropout(p=0.2),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=8),
            nn.ReLU(),
            nn.Linear(in_features=8, out_features=3)
        )
        self.allIn = nn.Sequential(
            nn.Linear(in_features=11, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=32),
            nn.Dropout(p=0.2),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=8),
            nn.ReLU(),
            nn.Linear(in_features=8, out_features=3)
        )
        self.finalLayer = nn.Sequential(
            nn.Linear(in_features=12, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=32),
            nn.Dropout(p=0.2),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=8),
            nn.ReLU(),
            nn.Linear(in_features=8, out_features=3)
        )

    def forward(self, input):
        """
        Apply the forward propagation
        """
        """
        logits = self.linearRelu(input)
        return logits
        """
        if input.ndim is 2:
            subset1 = input[:,:3]
            subset2 = input[:,:5]
            subset3 = input[:,:8]
        else:
            subset1 = input[:3]
            subset2 = input[:5]
            subset3 = input[:8]

        x1 = self.threeIn(subset1)
        x2 = self.fiveIn(subset2)
        x3 = self.eightIn(subset3)
        x4 = self.allIn(input)

        if input.ndim is 2:
            result = torch.cat((x1, x2, x3, x4), dim=1)
        else:
            result = torch.cat((x1, x2, x3, x4))

        result = torch.from_numpy(normalize(result.detach().numpy()))
        logits = self.finalLayer(result)

        return logits
    