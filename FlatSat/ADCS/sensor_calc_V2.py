"""
The code you will write for this module should calculate
roll, pitch, and yaw (RPY) and calibrate your measurements
for better accuracy. Your functions are split into two activities.
The first is basic RPY from the accelerometer and magnetometer. The
second is RPY using the gyroscope. Finally, write the calibration functions.
Run plot.py to test your functions, this is important because auto_camera.py 
relies on your sensor functions here.
"""

#import libraries
import time
import math
import board
import busio
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL

#imu initialization
i2c = busio.I2C(board.SCL, board.SDA)
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

#Activity 1: RPY based on accelerometer and magnetometer
def roll_am(accelX,accelY,accelZ):
    roll = math.atan(accelY / (accelX**2+accelZ**2) ** .5)
    return roll

def pitch_am(accelX,accelY,accelZ):
    pitch = math.atan(accelX / (accelY**2+accelZ**2) ** .5)
    return pitch

def yaw_am(accelX,accelY,accelZ,magX,magY,magZ):
    mag_x = magX*math.cos(pitch_am(accelX,accelY,accelZ))
    mag_x += magY*math.sin(roll_am(accelX,accelY,accelZ))*math.sin(pitch_am(accelX,accelY,accelZ))
    mag_x += magZ*math.cos(roll_am(accelX,accelY,accelZ))*math.sin(pitch_am(accelX,accelY,accelZ))
    mag_y = magY*math.cos(roll_am(accelX, accelY, accelZ)) - magZ*math.sin(roll_am(accelX, accelY, accelZ))
    yaw = -mag_y/mag_x
    return math.atan(accelZ / (accelY**2+accelX**2) ** .5)

#Activity 2: RPY based on gyroscope
# only going to utilize magnetometer & accelerometer measurements, doesn't need this functionality
def roll_gy(prev_angle, delT, gyro):
    #TODO NOT DONE
    return
def pitch_gy(prev_angle, delT, gyro):
    #TODO NOT DONE
    return
def yaw_gy(prev_angle, delT, gyro):
    #TODO NOT DONE
    return

#Activity 3: Sensor calibration
def calibrate_mag():
    #TODO: Set up lists, time, etc
    magX, magY, magZ = mag.magnetic #gauss
    
    startT = time.time()

    print("Preparing to calibrate magnetometer. Please wave around.")
    maxX = minX = magX
    maxY = minY = magY
    maxZ = minZ = magZ

    while(time.time() - startT < 3):
        maxX = max(maxX, magX)
        minX = min(minX, magX)
        maxY = max(maxY, magY)
        minY = min(minY, magY)
        maxZ = max(maxZ, magZ)
        minZ = min(minZ, magZ)

    print("Calibrating...")
    offsetX = (maxX+minY)/2
    offsetY = (maxY+minY)/2
    offsetZ = (maxZ+minZ)/2
    
    #TODO: Calculate calibration constants
    print("Calibration complete.")
    return [offsetX,offsetY,offsetZ]

def calibrate_gyro():
    #TODO
    #print("Preparing to calibrate gyroscope. Put down the board and do not touch it.")
    #time.sleep(3)
    #print("Calibrating...")
    #TODO
    #print("Calibration complete.")
    return [0, 0, 0]

def get_rpy(mag_offset = [0,0,0]):
    """
    This function is complete. Finds RPY values.

    Parameters:
        mag_offset (list): magnetometer calibration offsets
    """
    #Sets the initial position for plotting and gyro calculations.
    print("Preparing to set initial angle. Please hold the IMU still.")
    time.sleep(3)
    print("Setting angle...")

    accelX, accelY, accelZ = accel_gyro.acceleration #m/s^2
    magX, magY, magZ = mag.magnetic #gauss

    #Calibrate magnetometer readings. Defaults to zero until you
    #write the code
    magX = magX - mag_offset[0]
    magY = magY - mag_offset[1]
    magZ = magZ - mag_offset[2]

    roll = roll_am(accelX, accelY,accelZ)
    pitch = pitch_am(accelX,accelY,accelZ)
    yaw = yaw_am(accelX,accelY,accelZ,magX,magY,magZ)

    print("Initial angle set.")

    return [roll,pitch,yaw]
