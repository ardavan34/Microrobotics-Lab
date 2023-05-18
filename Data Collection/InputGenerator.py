"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 
 
-> Filename: InputGenerator.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: A helper script to generate the input arrays and save them into JSON file
-> Starting Date: May 18, 2023
"""

import json
from itertools import permutations
import matplotlib

def orderedInputGenerator(size):
    
    inputs = []
    positions = [[-5, -5, 0], [5, -5, 0], [5, 5, 0], [-5, 5, 0], [0, 0, 0]]
    currents = [0, 0, 0, 0, 0, 0, 0, 0]
    pointOne = [0, 0, 0]
    pointTwo = [0, 0, 0]
    currentInput = {'I1': 0, 
                    'I2': 0,
                    'I3': 0,
                    'I4': 0,
                    'I5': 0,
                    'I6': 0,
                    'I7': 0,
                    'I8': 0,
                    'X1': 0,
                    'Y1': 0,
                    'Z1': 0,
                    'X2': 0,
                    'Y2': 0,
                    'Z2': 0}

    return inputs


# Set the initials for our training data
totalSize = 3000
orderedSize = 1280
randomSize = totalSize - orderedSize
xRange = [-100, 100]   # in mm
yRange = [-100, 100]   # in mm
zRange = [0, 100]   # in mm
currentRange = [-18, 18]   # in Ampere
inputs = []

orderedInputs = orderedInputGenerator(orderedSize)
randomInputs = []

jsonInput = json.dumps(inputs, indent=4)

with open("./Data Collection/JSON Files/Input/Input.json", "w") as outfile:
    outfile.write(jsonInput)

