"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 
 
-> Filename: input-helpers.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: A helper script including all of the functions that are called in input_generator.py
-> Starting Date: May 25, 2023
"""

import plotly.express as px
from scipy import stats
import pandas as pd
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


def jsonStacker(inputVec):
    """
    Helper function to convet the input vector into a dictionary
    Format: 8 currents, 6 coordinate positions used for 2 points
    """
    inputMap = {}

    # Set the current values
    for cur in range(8):
        inputMap["I" + str(cur+1)] = inputVec[cur][0]

    # Set the position values
    for pos in range(2):
        inputMap["X" + str(pos+1)] = inputVec[(3*pos) + 8][0]
        inputMap["Y" + str(pos+1)] = inputVec[(3*pos) + 9][0]
        inputMap["Z" + str(pos+1)] = inputVec[(3*pos) + 10][0]

    return inputMap


def posDatasetPlot(inputData, fileNumber, type):
    """
    Helper function to plot the randomly generated positions on a 3D map
    Used to analyze the data distribution
    """
    dataframe, dataframeRounded = dataframeAssembler(inputData)

    # Plot distribution map for all datasets
    if type == "all data":
        # Set up the map
        mapTitle = "Distribution map for all datasets"
        fig = px.scatter_3d(dataframeRounded, x='x', y='y', z='z', title=mapTitle, 
                            color=dataframeRounded['size'] ** 2, size='size', color_continuous_scale='RdBu_r',
                            labels={'x': 'x axis [mm]', 'y': 'y axis [mm]', 'z': 'z axis [mm]', 'color': 'size^2'})
        fig.update_layout(title={'text': mapTitle, 'y':0.9, 'x':0.5,'xanchor': 'center', 'yanchor': 'top'})
        # Save the html file of the map
        fig.write_html("./Data Collection/Input/Distribution Files/AllInput_Distribution.html")

        # Save the information about the datasets into a text file
        with open("./Data Collection/Input/Distribution Files/AllInput_Data.txt", 'w') as outfile:
            df_string = dataframeRounded.to_string(header=True, index=True)
            outfile.write(df_string)
    
    # Plot density map for single json file
    elif type == "json data":
        # Calculate the density
        kernel = stats.gaussian_kde([dataframe.x, dataframe.y, dataframe.z])
        dataframe['density'] = kernel([dataframe.x, dataframe.y, dataframe.z])
        
        # Set up the map
        mapTitle = "Density map for dataset #" + str(fileNumber)
        fig = px.scatter_3d(dataframe, x='x', y='y', z='z', color='density', color_continuous_scale='RdBu_r', opacity=0.9, title=mapTitle,
                            labels={'x': 'x axis [mm]', 'y': 'y axis [mm]', 'z': 'z axis [mm]'}) 
        fig.update_layout(title={'text': mapTitle, 'y':0.9, 'x':0.5,'xanchor': 'center', 'yanchor': 'top'})
        # Save the html file of the map
        fig.write_html("./Data Collection/Input/Distribution Files/Input" + str(fileNumber) + "_Distribution.html")


def dataframeAssembler(inputData):
    """
    Helper function to create the dataframe based on the given data
    """
    # Set up the dictionary
    struct = {'x': [], 'y': [], 'z': []}
    for data in inputData:
        struct['x'].append(data['X1'])
        struct['y'].append(data['Y1'])
        struct['z'].append(data['Z1'])
        struct['x'].append(data['X2'])
        struct['y'].append(data['Y2'])
        struct['z'].append(data['Z2'])

    df = pd.DataFrame(data=struct)   # raw dataframe
    dfRounded = (df // 20) * 20 + 10
    dfRounded = dfRounded.groupby(df.columns.tolist(), as_index=False).size()
    dfRounded = dfRounded.sort_values(by=['size'])   # dataframe for the defined subsections
    
    return df, dfRounded