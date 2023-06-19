"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: ValidationAnalysis.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Analyze how close the real-life measurements are to the simulation values
-> Starting Date: Jun 14, 2023
"""

import pandas as pd
import numpy as np
import json

"""
Main function
"""
dataNumber = 100
dirList = ['X', 'Y', 'Z']
dfByCoordinates = {}

# Set the dataframe for measured values
fullDataframe = pd.read_csv("./Test Data/Old Test/2023-02-03_10-49-44-validation-100points-RobotLog.csv")
dataframe = fullDataframe[['msdFieldvalue_mT_1', 'msdFieldvalue_mT_2', 'msdFieldvalue_mT_3']]
dataframe = dataframe.rename({'msdFieldvalue_mT_1': 'measuredValue_X', 'msdFieldvalue_mT_2': 'measuredValue_Y', 'msdFieldvalue_mT_3': 'measuredValue_Z'}, axis='columns')

# Load the json file for theoretical values
dataset = open("./Test Data/Old Test/TheoreticalResult.json")
realData = json.load(dataset)

# Set the numpy array for simulated magnetic field density values in x, y, and z direction
realValMatrix = np.empty([dataNumber, 3])
for set in range(dataNumber):
    realValMatrix[set] = [realData[set]['Bx'], realData[set]['By'], realData[set]['Bz']]

dataframe[['simulatedValue_X', 'simulatedValue_Y', 'simulatedValue_Z']] = realValMatrix

# Calculate the difference between measured and simulated values and an error percentage (measured value is assumed to be the real value)
for dir in dirList:
    dataframe['diff_' + dir] = dataframe['simulatedValue_' + dir] - dataframe['measuredValue_' + dir]
    dataframe['error%_' + dir] = 100.0 * (dataframe['diff_' + dir] / abs(dataframe['measuredValue_' + dir]))
    dfByCoordinates[dir] = dataframe[['simulatedValue_' + dir, 'measuredValue_' + dir, 'diff_' + dir, 'error%_' + dir]]
    # Print the result of the analysis
    print(f"----- Analyze {dir} coordinate -----")
    print(dfByCoordinates[dir].sort_values(by='diff_'+dir))




