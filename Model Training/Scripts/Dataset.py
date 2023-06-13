"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: Dataset.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Class for loading the dataset
-> Starting Date: Jun 5, 2023
"""

import torch
from torch.utils.data import Dataset, DataLoader


class ENSDataset(Dataset):
    """
    Class for loading our dataset
    """
    def __init__(self, inputMatrix, outputMatrix, inputTransform=None, outputTransform=None):
        """
        Constructor of our class
        """
        self.size = inputMatrix.shape[1]
        self.input = torch.tensor(inputMatrix)
        self.output = torch.tensor(outputMatrix)
        self.inputTransform = inputTransform
        self.outputTransform = outputTransform

    def __len__(self):
        """
        Returns the size of our dataset (number of the samples)
        """
        return self.size
    
    def __getitem__(self, index):
        """
        Returns a single sample
        """
        inputSample = self.input[:, index]
        outputSample = self.output[:, index]

        # Apply the transforms, if there are any
        if self.inputTransform:
            inputSample = self.inputTransform(inputSample)
        if self.outputTransform:
            outputSample = self.outputTransform(outputSample)

        return inputSample, outputSample
