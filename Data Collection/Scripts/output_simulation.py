"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: output_simulation.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: A helper script to run simulations on COMSOL and save the results
-> Starting Date: May 24, 2023
"""

import json
# import mph

"""
Main function
"""
# Select and load the dataset
datasetNum = 23   # select the dataset to query
dataset = open("./Data Collection/Input/Input Datasets/Input" + str(datasetNum) + ".json")
data = json.load(dataset)

# Setup variables to us
axis = ['X', 'Y', 'Z']
start = 1   # index of input in 'data' to start simulation with (included)
end = 3   # index of input in 'data' to end simulation with (excluded)


"""
# Loading the COMSOL model
client = mph.start()
model = client.load('system_2.0.mph')   # the mph file must be located in Microrobotics-Lab directory

for input in data[start:end]:
    # Clearing the model
    model.clear()
    model.reset()

    # Next values to calculate
    for current in range(1, 9):
        var = 'I' + str(current)
        model.parameter(var, str(input[var]) + '[A]')
    for pos in range(1, 3):
        for direction in axis:
            var = direction + str(pos)
            model.parameter(var, str(input[var]) + '[mm]')

    # Start simulation
    model.build()
    model.mesh()
    model.solve('Study 1')

    # Export the point evalution result as a text file
    model.export('Data_Point_1')   # name and location of text file is set on COMSOL
    model.export('Data_Point_2')   # Append. name and location of text file is set on COMSOL
"""