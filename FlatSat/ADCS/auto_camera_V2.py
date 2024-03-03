"""
The code below is a template for the auto_camera.py file. You will need to
finish the capture() function to take a picture at a given RPY angle. Make
sure you have completed the sensor_calc.py file before you begin this one.
"""

#import libraries
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
import time
import os
import board
import busio
from picamera2 import Picamera2
import numpy as np
import sys
from sensor_calc_V2 import *

#imu and camera initialization
i2c = busio.I2C(board.SCL, board.SDA)
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

#Code to take a picture at a given offset angle
def capture(dir ='roll', target_angle = 30):
    #Calibration lines should remain commented out until you implement calibration
    offset_mag = calibrate_mag()
    offset_gyro =calibrate_gyro()
    initial_angle = set_initial(offset_mag)
    prev_angle = initial_angle
    print("Begin moving camera.")
    while True:
        accelX, accelY, accelZ = accel_gyro.acceleration #m/s^2
        magX, magY, magZ = mag.magnetic #gauss
	    #Calibrate magnetometer readings
        magX = magX - offset_mag[0]
        magY = magY - offset_mag[1]
        magZ = magZ - offset_mag[2]
        gyroX, gyroY, gyroZ = accel_gyro.gyro #rad/s
        #Convert to degrees and calibrate
        gyroX = gyroX *180/np.pi - offset_gyro[0]
        gyroY = gyroY *180/np.pi - offset_gyro[1]
        gyroZ = gyroZ *180/np.pi - offset_gyro[2]
        
        #TODO: Everything else! Be sure to not take a picture on exactly a
        #certain angle: give yourself some margin for error. 

if __name__ == '__main__':
    capture(*sys.argv[1:])
