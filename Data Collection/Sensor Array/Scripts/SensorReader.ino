/*
  _____  _ _ _             __  __ _                          _           _   _            _           _     
 |  __ \(_) | |           |  \/  (_)                        | |         | | (_)          | |         | |    
 | |  | |_| | | ___ _ __  | \  / |_  ___ _ __ ___  _ __ ___ | |__   ___ | |_ _  ___ ___  | |     __ _| |__  
 | |  | | | | |/ _ \ '__| | |\/| | |/ __| '__/ _ \| '__/ _ \| '_ \ / _ \| __| |/ __/ __| | |    / _` | '_ \ 
 | |__| | | | |  __/ |    | |  | | | (__| | | (_) | | | (_) | |_) | (_) | |_| | (__\__ \ | |___| (_| | |_) |
 |_____/|_|_|_|\___|_|    |_|  |_|_|\___|_|  \___/|_|  \___/|_.__/ \___/ \__|_|\___|___/ |______\__,_|_.__/ 

-> Filename: SensorDetector.ino
-> Project: Electromagnetic Navigation System Calibration
-> Author: Ardavan Alaei Fard
-> Description: Arduino script for detecting the magnetometers on multiplexers, attached to the Arduino
-> Starting Date: Jul 5, 2023
*/

#include <Wire.h>
#include <SparkFun_I2C_Mux_Arduino_Library.h>
#include <MLX90393.h>

QWIICMUX myMux[2];                   // The two multiplexers
int muxAddress[2] = { 0X70, 0X71 };  // The addresses of the multiplexers
int sensorAddress = 0X0C;
MLX90393 mlx[2][8];
MLX90393::txyz data;  //Create a structure, called data, of four floats (t, x, y, and z)

void setup() {
  Serial.begin(57600);

  Wire.begin();

  // Check if both multiplexers are attached
  if (myMux[0].begin(muxAddress[0]) == false || myMux[1].begin(muxAddress[1]) == false) {
    Serial.println("Muxes not detected. Freezing...");
    while (myMux[0].begin(muxAddress[0]) == false || myMux[1].begin(muxAddress[1]) == false)
      ;
  }

  // Disable all ports
  for (int mux = 0; mux < 2; mux++) {
    for (int port = 0; port < 8; port++) {
      myMux[mux].enablePort(port);
      myMux[mux].setPort(port);
      Wire.beginTransmission(sensorAddress);
      byte error = Wire.endTransmission();

      if (error == 0) {
        byte sensorStatus = mlx[mux][port].begin(0, 0);
        mlx[mux][port].setGainSel(7);
        mlx[mux][port].setResolution(0, 0, 0);
      }
      myMux[mux].disablePort(port);
    }
  }
  
  delay(10000);
}

void loop() {
  delay(100);

  for (int number = 0; number < 2; number++) {
    Wire.beginTransmission(muxAddress[number]);
    byte error = Wire.endTransmission();

    // Check if the mux is attached
    if (error == 0) {
      for (int sensor = 0; sensor < 8; sensor++) {
        myMux[number].enablePort(sensor);  // Enable the port
        myMux[number].setPort(sensor);     // Set the mux port to check

        Wire.beginTransmission(sensorAddress);
        byte error = Wire.endTransmission();

        // Print the address if a device (a magnetometer in this case) other than the other mux is detected
        if (error == 0) {
          mlx[number][sensor].readData(data);
          Serial.print(data.x);
          Serial.print(",");
          Serial.print(data.y);
          Serial.print(",");
          Serial.print(data.z);
          if (sensor == 7 && number == 1)
            Serial.println();
          else
            Serial.print(",");
        } else {
          Serial.print("0,0,0");
          if (sensor == 7 && number == 1)
            Serial.println();
          else
            Serial.print(",");
        }

        myMux[number].disablePort(sensor);  // Disable the port
      }
    }
  }
}
