"""
*** DILLER MICROROBOTICS LAB ***

-> Filename: simulation.py
-> Project: Electromagnetic Navigation System Calibratio
-> Author: Ardavan Alaei Fard
-> Description: A helper script to run simulations on COMSOL and save the results
-> Starting Date: May 16, 2023
"""

import mph
import time

# Loading the COMSOL model
client = mph.start()
model = client.load('system_2.0.mph')

# Print the details about the system
print(model.parameters())
print(model.materials())
print(model.physics())
print(model.studies())
print(model.datasets())
print(model.exports())

# Start simulation
model.build()
model.mesh()
model.solve('Study 1')

# Export the point evalution result as a text file
model.export('Data_Point_1')
model.export('Data_Point_2')

start = time.time()

# Clearing the model
model.clear()
model.reset()

# Next values to calculate
model.parameter('I1', '-12.5[A]')
model.parameter('Y2', '123[mm]')
model.parameter('I8', '5[A]')
print(model.parameters())

# Start simulation
model.build()
model.mesh()
model.solve('Study 1')

# Export the point evalution result as a text file
model.export('Data_Point_1')
model.export('Data_Point_2')

end = time.time()
print(end - start)
start = time.time()

# Clearing the model
model.clear()
model.reset()

# Next values to calculate
model.parameter('X1', '1[mm]')
model.parameter('Y1', '1[mm]')
model.parameter('Z1', '1[mm]')
print(model.parameters())

# Start simulation
model.build()
model.mesh()
model.solve('Study 1')

# Export the point evalution result as a text file
model.export('Data_Point_1')
model.export('Data_Point_2')

end = time.time()
print(end - start)

# Clearing the model
model.clear()
model.reset()