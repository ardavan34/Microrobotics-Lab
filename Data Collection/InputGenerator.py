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
import numpy as np

def inputGenerator(x, y, z, current):

    currentIn = np.random.rand(8, 1) * (current[1] - current[0]) + current[0]
    xyIn = np.random.rand(4, 1) * (x[1] - x[0]) + x[0]
    zIn = np.random.rand(2, 1) * (z[1] - z[0]) + z[0]
    xyz1 = np.array([xyIn[0], xyIn[1], zIn[0]])
    xyz2 = np.array([xyIn[2], xyIn[3], zIn[1]])

    input = np.vstack((currentIn, xyz1))
    input = np.vstack((input, xyz2))

    return np.around(input, 3)

def jsonStacker(input):

    inputMap = {}
    for cur in range(8):
        inputMap["I" + str(cur+1)] = input[cur][0]
    for pos in range(2):
        inputMap["X" + str(pos+1)] = input[(3*pos) + 8][0]
        inputMap["Y" + str(pos+1)] = input[(3*pos) + 9][0]
        inputMap["Z" + str(pos+1)] = input[(3*pos) + 10][0]

    return inputMap

# Set the initials for our training data
totalSize = 3
xRange = [-100, 100]   # in mm
yRange = [-100, 100]   # in mm
zRange = [0, 100]   # in mm
currentRange = [-18, 18]   # in Ampere
inputs = []

for i in range(totalSize):
    inputArr = inputGenerator(xRange, yRange, zRange, currentRange)
    inputs.append(jsonStacker(inputArr))

print(inputs)

jsonInput = json.dumps(inputs, indent=4)

with open("./Data Collection/JSON Files/Input/Input.json", "w") as outfile:
    outfile.write(jsonInput)

