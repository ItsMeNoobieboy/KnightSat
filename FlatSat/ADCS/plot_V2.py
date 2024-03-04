"""
All functions here are complete, please you this to test your 
sensor_calc.py functions.
"""

#import libraries
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
import time
import os
import board
import busio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import sys
from sensor_calc_V2 import *

#imu initialization
i2c = busio.I2C(board.SCL, board.SDA)
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xs = []
y1 = []
y2 = []
y3 = []
rpy = [0,0,0]

def convert_to_degrees(radians):
    return radians * (180/np.pi)

def animate(i, xs, type,y1,y2,y3, mag_offset, gyro_offset, initial_angle):
    if len(y1) ==0:
        prev_ang = initial_angle
    else:
        a = y1[-1]
        b = y2[-1]
        c = y3[-1]
        prev_ang = [a,b,c]

    accelX, accelY, accelZ = accel_gyro.acceleration #m/s^2
    magX, magY, magZ = mag.magnetic #gauss
    #Calibrate magnetometer readings
    magX = magX - mag_offset[0]
    magY = magY - mag_offset[1]
    magZ = magZ - mag_offset[2]

    gyroX, gyroY, gyroZ = accel_gyro.gyro #rad/s

    gyroX = convert_to_degrees(gyroX) - gyro_offset[0]
    gyroY = convert_to_degrees(gyroY) - gyro_offset[1]
    gyroZ = convert_to_degrees(gyroZ) - gyro_offset[2]

    xs.append(time.time())

    if type == 'am':
       y1.append(convert_to_degrees(roll_am(accelX,accelY,accelZ)))
       y2.append(convert_to_degrees(pitch_am(accelX,accelY,accelZ)))
       y3.append(convert_to_degrees(yaw_am(accelX,accelY,accelZ,magX,magY,magZ)))

       ax.clear()
       ax.plot(xs,y1,label = "Roll")
       ax.plot(xs,y2,label = "Pitch")
       ax.plot(xs,y3,label = "Yaw")
       plt.title('Roll Pitch Yaw, Using Accelerometer and Magnetometer')
       plt.ylabel('deg')

    elif type =='gyro':
       if len(xs) == 1:
           y1.append(prev_ang[0])
           y2.append(prev_ang[1])
           y3.append(prev_ang[2])
       else:
           delT = xs[-1] - xs[-2]
           y1.append(roll_gy(prev_ang[0],delT,gyroY))
           y2.append(pitch_gy(prev_ang[1],delT,gyroX))
           y3.append(yaw_gy(prev_ang[2],delT,gyroZ))

       ax.clear()
       ax.plot(xs,y1,label = "Roll")
       ax.plot(xs,y2,label = "Pitch")
       ax.plot(xs,y3,label = "Yaw")
       plt.title('Roll Pitch Yaw, Using Gyro')
       plt.ylabel('deg')

    else:
       print("Not a valid argument.")
       return
    #Keep the plot from being too long
    xs = xs[-20:]
    y1 = y1[-20:]
    y2 = y2[-20:]
    y3 = y3[-20:]
    plt.grid()
    plt.legend()
    plt.xlabel('Time')

def plot_data(type = 'am'):
    mag_offset = calibrate_mag()
    initial_angle = get_rpy(mag_offset)
    gyro_offset = calibrate_gyro()
    ani = animation.FuncAnimation(fig, animate, fargs =(xs,type,y1,y2,y3,mag_offset,gyro_offset,initial_angle), interval = 250)
    plt.show()


if __name__ == '__main__':
    plot_data(*sys.argv[1:])
