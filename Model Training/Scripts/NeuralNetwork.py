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

class ArdavanNet_1(nn.Module):
    """
    Class for a simply neural network as a DL model
    """
    def __init__(self):
        """
        Constructor of the model
        """
        super().__init__()
        # Set the model with two hidden layers, each 20 units, with ReLU activatoin function
        self.mlpLayer = nn.Sequential(
            nn.Linear(in_features=11, out_features=256, bias=True),
            nn.ReLU(),
            nn.Dropout(p=0.5, inplace=False),
            nn.Linear(in_features=256, out_features=256, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=256, out_features=256, bias=True),
            nn.ReLU(),
            nn.Dropout(p=0.5, inplace=False),
            nn.Linear(in_features=256, out_features=32, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=3, bias=True)
        )

    def forward(self, input):
        """
        Apply the forward propagation
        """
        logits = self.mlpLayer(input)

        return logits
    
class ArdavanNet_2(nn.Module):
    """
    Class for a simply neural network as a DL model
    """
    def __init__(self):
        """
        Constructor of the model
        """
        super().__init__()
        # Set the model with two hidden layers, each 20 units, with ReLU activatoin function
        self.recurrentLayer = nn.Sequential(
            nn.Linear(in_features=11, out_features=128, bias=True),
            nn.ReLU(),
            nn.Dropout(p=0.4, inplace=False),
            nn.Linear(in_features=128, out_features=128, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=11, bias=True)
        )
        self.finalLayer = nn.Sequential(
            nn.Linear(in_features=11, out_features=128, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=32, bias=True),
            nn.ReLU(),
            nn.Dropout(p=0.3, inplace=False),
            nn.Linear(in_features=32, out_features=8, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=8, out_features=3, bias=True)
        )

    def block(self, input):
        x1 = self.recurrentLayer(input)
        x2 = self.recurrentLayer(x1)

        return x2 + input

    def forward(self, input):
        """
        Apply the forward propagation
        """
        logits = input
        for i in range(3):
            logits = ArdavanNet_2.block(self, logits)

        logits = self.finalLayer(logits)

        return logits
    
class ArdavanNet_3(nn.Module):
    """
    Class for a simply neural network as a DL model
    """
    def __init__(self):
        """
        Constructor of the model
        """
        super().__init__()
        # Set the model with two hidden layers, each 20 units, with ReLU activatoin function
        self.layerBlock = nn.Sequential(
            nn.Linear(in_features=11, out_features=128, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=64, bias=True),
            nn.Dropout(p=0.2, inplace=False),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=32, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=11, bias=True),
            nn.Dropout(p=0.2, inplace=False),
            nn.ReLU()
        )
        self.endingBlock = nn.Sequential(
            nn.Linear(in_features=11, out_features=32, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=16, bias=True),
            nn.Dropout(p=0.2, inplace=False),
            nn.ReLU(),
            nn.Linear(in_features=16, out_features=3, bias=True)
        )

    def forward(self, input):
        x1 = self.layerBlock(input)
        x2 = self.layerBlock(x1) + x1
        x3 = self.layerBlock(x2) + x1 + x2
        x4 = self.layerBlock(x3) + x1 + x2 + x3
        logits = self.endingBlock(x4)
        return logits
    