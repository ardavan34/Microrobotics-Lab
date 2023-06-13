"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: ValidationSimulation.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: A script for simulating measured fields on COMSOL
-> Starting Date: Jun 9, 2023
"""

import pandas as pd
import mph
from os.path import exists
from ValidationHelpers import *
import json

"""
Main function
"""
dataframe = pd.read_csv("./Test Data/Old Test/2023-02-03_10-49-44-validation-100points-RobotLog.csv")
filteredDf = dataframe[['tableCmdPos_m_1', 'tableCmdPos_m_2', 'tableCmdPos_m_3', 
                        'cmdCoilCurrent_A_1', 'cmdCoilCurrent_A_2', 'cmdCoilCurrent_A_3', 'cmdCoilCurrent_A_4', 
                        'cmdCoilCurrent_A_5', 'cmdCoilCurrent_A_6', 'cmdCoilCurrent_A_7', 'cmdCoilCurrent_A_8']]
datasetSize = filteredDf.shape[0]
axis = ['X1', 'Y1', 'Z1']

# Paths of files used in the script
jsonFilePath = "./Test Data/Old Test/TheoreticalResult.json"
txtFilePath = "./Test Data/Old Test/SimulationResult.txt"

# Create the JSON file if not already created
if exists(jsonFilePath) == False:
    newFile = open(jsonFilePath, "x")
if exists(txtFilePath) == False:
    newFile = open(txtFilePath, "x")

# Loading the COMSOL model
client = mph.start()
model = client.load('system_2.0.mph')   # the mph file must be located in Microrobotics-Lab directory

for data in range(datasetSize):
    # Clearing the model
    model.clear()
    model.reset()

    # Next values to calculate
    for direction in range(3):
        model.parameter(axis[direction], str(filteredDf.loc[data][direction] * 1000.0) + '[mm]')
    for current in range(1, 9):
        var = 'I' + str(current)
        model.parameter(var, str(filteredDf.loc[data][current + 2]) + '[A]')
    
    # Start simulation
    model.build()
    model.mesh()
    model.solve('Study 1')   # name of solution is set on COMSOL

    # Export the point evalution result as a text file
    model.export('Data_Point_1')   # write. name and location of text file is set on COMSOL

    # Parse the exported data and save them in the json file
    result = txtParserVal(txtFilePath, data + 1)
    output = readFileVal(data, jsonFilePath, result)
    writeFileVal(jsonFilePath, output)
    
    print("Simulation #" + str(data + 1) + " is successfully completed")
