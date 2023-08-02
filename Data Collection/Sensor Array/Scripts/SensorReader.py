"""
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: SensorReader.py
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Script for reading the values from the Arduino and save the data
-> Starting Date: Jul 14, 2023
"""

import serial
import numpy as np
import pandas as pd


class SensorArray:
    def __init__(self, 
                 comPort: str = '/dev/ttyACM0',
                 baudRate: int = 57600,
                 timeout: float = 1.0,
                 conversionFactor: float = 1e-3):
        """
        Construct the class
        """
        self.ser = serial.Serial(comPort, baudRate, timeout=timeout)
        self.currentMeasurement = np.empty(shape=(1, 48), dtype=float).reshape((1, 48))
        self.calibrationOffsets = np.zeros(shape=(1, 48), dtype=float).reshape((1, 48))
        self.conversionFactor = conversionFactor
        self.listData = []
        self.csvData = {}
        self.directions = ['X', 'Y', 'Z']

    def measure(self):
        """
        read the data line from Serial
        """
        sensorValue = self.ser.readline().decode().split(',')   # Make a list from the reading data
        if len(sensorValue) == 48:   # Check if the reading is valid
            sensorValue[-1] = sensorValue[-1][:-2]
            self.currentMeasurement = list(map(float, sensorValue))
            if self.currentMeasurement[0] < 1000:
                return True
        
        return False
    
    def calibrate(self, calibrationSize):
        """
        Calibrate the all connected magnetometers
        """
        self.calibrateData = np.empty(shape=(calibrationSize, 48), dtype=float).reshape((calibrationSize, 48))
        for count in range(calibrationSize):
            while self.measure() == False:
                pass
            self.calibrateData[count] = self.currentMeasurement
        
        self.calibrationOffsets = np.mean(self.calibrateData, axis=0, dtype=float)   # Get average as the offset

    def dataCollection(self):
        """
        Collect data from reading the Serial
        """
        while(1):
            try:
                self.measure()
                self.currentMeasurement = (self.currentMeasurement - self.calibrationOffsets) * self.conversionFactor   # Subtract the offset, change to mT
                self.listData.append(self.currentMeasurement)
                print(self.currentMeasurement)
            except:    # The end of data collection process (unplugging the arduino)
                self.listData = np.array(self.listData).T.tolist()
                queryIndex = 0   # The list index to query

                for mux in range(2):
                    for sensor in range(8):
                        for dir in self.directions:
                            columnName = f"mux{mux + 1}_sensor{sensor}_{dir} [mT]"
                            self.csvData[columnName] = self.listData[queryIndex]
                            queryIndex += 1
                
                # Create dataframe and save the data into csv file
                dataframe = pd.DataFrame(self.csvData)
                print(dataframe)
                dataframe.to_csv("./Data Collection/Sensor Array/Validation Tests/magnitude_test.csv", index=False)

                break

if __name__ == '__main__':
    """
    Main function
    Key steps for using the code:
    1.  Upload SensorReader.ino to the Arduino, then unplug the Arduino
    2.  Make sure the port you are using the Arduino with matches the one mentioned in line 23.
        If not, change it to the desired one in line 23.
    3.  Plug in back the Arduino
    4.  Run the code in less than 10 seconds after the Arduino is plugged in
    5.  End the data collection only and only by unplugging the Arduino
    """
    sensors = SensorArray()
    print("Starting Calibration ...")
    sensors.calibrate(calibrationSize=20)
    print("Calibration complete")
    sensors.dataCollection()