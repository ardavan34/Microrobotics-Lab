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
import matplotlib.pyplot as plt
import numpy as np

def inputGenerator(x, y, z, current):
    """
    Helper function to generate a random vector of inputs
    8 currents, 6 coordinate positions used for 2 points
    """
    # Generate random currents and positions based on the boundaries
    currentIn = np.random.rand(8, 1) * (current[1] - current[0]) + current[0]
    xIn = np.random.rand(2, 1) * (x[1] - x[0]) + x[0]
    yIn = np.random.rand(2, 1) * (y[1] - y[0]) + y[0]
    zIn = np.random.rand(2, 1) * (z[1] - z[0]) + z[0]

    # Create the arrays for the positions and stack the arrays into one input
    xyz1 = np.array([xIn[0], yIn[0], zIn[0]])
    xyz2 = np.array([xIn[1], yIn[1], zIn[1]])

    input = np.vstack((currentIn, xyz1))
    input = np.vstack((input, xyz2))

    # Return the array after rounding it to 3 decimal place
    return np.around(input, 3)

def jsonStacker(input):
    """
    Helper function to convet the input vector into a dictionary
    Format: 8 currents, 6 coordinate positions used for 2 points
    """
    inputMap = {}

    # Set the current values
    for cur in range(8):
        inputMap["I" + str(cur+1)] = input[cur][0]

    # Set the position values
    for pos in range(2):
        inputMap["X" + str(pos+1)] = input[(3*pos) + 8][0]
        inputMap["Y" + str(pos+1)] = input[(3*pos) + 9][0]
        inputMap["Z" + str(pos+1)] = input[(3*pos) + 10][0]

    return inputMap

def inputPlot(input):
    """
    Helper function to plot data about the randomly generated dataset
    Used to analyze the distribution of the data
    """
    fig = plt.figure()
    dataPlot = fig.add_subplot(projection='3d')

    for dataset in input:
        for point in range(2):
            x = dataset["X" + str(point + 1)]
            y = dataset["Y" + str(point + 1)]
            z = dataset["Z" + str(point + 1)]
            dataPlot.scatter(x, y, z, 'o')

    dataPlot.set_xlabel('x axis')
    dataPlot.set_ylabel('y axis')
    dataPlot.set_zlabel('z axis')

    plt.savefig("./Data Collection/JSON Files/Input/input_distribution.pdf", bbox_inches='tight')
    plt.show()

"""
Main function
"""
# Set the initials for our training data
numOfData = 5   # number of datasets in each json file
numOfFiles = 3   # number of json files
xRange = [-100, 100]   # in mm
yRange = [-100, 100]   # in mm
zRange = [0, 100]   # in mm
currentRange = [-18, 18]   # in Ampere
fileInputs = []
allInputs = []

for file in range(numOfFiles):

    # Generate a list of inputs for one of the files and save them in our lists
    for data in range(numOfData):
        inputArr = inputGenerator(xRange, yRange, zRange, currentRange)
        inputDict = jsonStacker(inputArr)
        fileInputs.append(inputDict)
        allInputs.append(inputDict)

    # Write the dataset into a json file
    jsonInput = json.dumps(fileInputs, indent=4)

    with open("./Data Collection/JSON Files/Input/Input" + str(file + 1) + ".json", "w") as outfile:
        outfile.write(jsonInput)

    # Clear the list for other files
    fileInputs.clear()

print(allInputs)
inputPlot(allInputs)

