from image_registration import image_registration
from find_outages import find_difference

import time
import board
import sys
import os

from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL

from git import Repo
from picamera2 import Picamera2, Preview

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
LED_PIN = 26
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, False)


# VARIABLES
THRESHOLD = 15  # Any desired value from the accelerometer
REPO_PATH = "/home/pi/Desktop/CubesatChallenge"  # Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "image_analysis/cubesat_output"  # Your image folder path in your GitHub repo: ex. /Images

# imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()


def img_gen(name, image_time):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    imgname = f"{REPO_PATH}/{FOLDER_PATH}/{name}_{image_time}.jpg"
    return imgname


def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote("origin")
        print("added remote")
        origin.pull()
        print("pulled changes")
        repo.git.add(REPO_PATH + "/" + FOLDER_PATH)
        repo.index.commit("New Photo")
        print("made the commit")
        origin.push()
        print("pushed changes")

    except Exception as e:
        print(e)
        # Print important information about the exception
        print(f"Exception occurred: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        print("Couldn't upload to git")


def take_photo():
    """
    Takes a photo when the FlatSat is shaken.
    """

    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        total = (accelx**2 + accely**2 + accelz**2) ** 0.5

        # CHECKS IF READINGS ARE ABOVE THRESHOLD -> done
        if total > THRESHOLD:
            print(f"Total reached {total:.3f}")
            break

    shake_time = time.strftime("%m-%d-%Y_%H:%M")

    picam2.start()

    for _ in range(3):
        GPIO.output(LED_PIN, True)
        time.sleep(.1)
        GPIO.output(LED_PIN, False)
        time.sleep(.1)

    time.sleep(1)

    # TAKE PHOTO

    GPIO.output(LED_PIN, True)
    time.sleep(.5)
    
    picam2.capture_file(img_gen("no_outages", shake_time))

    GPIO.output(LED_PIN, False)

    time.sleep(2)


    GPIO.output(LED_PIN, True)
    time.sleep(.5)
    
    picam2.capture_file(img_gen("with_outages", shake_time))

    GPIO.output(LED_PIN, False)

    return shake_time


def main():
    while True:
        shake_time = take_photo()

        os.makedirs(f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}", exist_ok=True)

        no_outages_path = f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}/no_outages.jpg"
        with_outages_path = f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}/with_outages.jpg"
        aligned_image_path = f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}/aligned_image"

        print(no_outages_path)
        print(with_outages_path)
        print(aligned_image_path)

        image_registration(
            f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}/no_outages.jpg",
            f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}/with_outages.jpg",
            f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}/aligned_image",
        )
        find_difference(
            f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}/no_outages.jpg",
            f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}/aligned_image.png",
            f"{REPO_PATH}/{FOLDER_PATH}/{shake_time}/outage_map",
        )
        git_push()


if __name__ == "__main__":
    main()
