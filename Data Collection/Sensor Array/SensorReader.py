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
                 timeout: float = 10.0,
                 conversionFactor: float = 1e-3):
        self.ser = serial.Serial(comPort, baudRate, timeout=timeout)
        self.currentMeasurement = np.empty(shape=(1, 48), dtype=float).reshape((1, 48))
        self.calibrationOffsets = np.zeros(shape=(1, 48), dtype=float).reshape((1, 48))
        self.conversionFactor = conversionFactor
        self.listData = []
        self.csvData = {}
        self.directions = ['X', 'Y', 'Z']

    def measure(self):
        sensorValue = self.ser.readline().decode().split(',')
        if (sensorValue != ['']):
            sensorValue[-1] = sensorValue[-1][:-2]
            self.currentMeasurement = list(map(float, sensorValue))
            # print(self.currentMeasurement)
            return True
        else:
            return False
    
    def calibrate(self, calibrationSize):
        self.calibrateData = np.empty(shape=(calibrationSize, 48), dtype=float).reshape((calibrationSize, 48))
        for count in range(calibrationSize):
            while self.measure() == False:
                pass
            self.calibrateData[count] = self.currentMeasurement
        
        # print(self.calibrateData)
        self.calibrationOffsets = np.mean(self.calibrateData, axis=0, dtype=float)
        # print(self.calibrationOffsets)

    def dataCollection(self):
        while(1):
            try:
                self.measure()
                self.currentMeasurement = (self.currentMeasurement - self.calibrationOffsets) * self.conversionFactor
                self.listData.append(self.currentMeasurement)
                print(self.currentMeasurement)
            except:
                self.listData = np.array(self.listData).T.tolist()
                queryIndex = 0

                for mux in range(2):
                    for sensor in range(8):
                        for dir in self.directions:
                            columnName = f"mux{mux + 1}_sensor{sensor}_{dir} [mT]"
                            self.csvData[columnName] = self.listData[queryIndex]
                            queryIndex += 1
                
                dataframe = pd.DataFrame(self.csvData)
                print(dataframe)
                dataframe.to_csv("sensor_data_x.csv", index=False)

                break

if __name__ == '__main__':
    sensors = SensorArray()
    print("Starting Calibration ...")
    sensors.calibrate(calibrationSize=20)
    print("Calibration complete")
    sensors.dataCollection()