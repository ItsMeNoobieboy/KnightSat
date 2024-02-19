from image_registration import image_registration
from find_outages import find_difference

import time
import board
import sys
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL

from git import Repo
from picamera2 import Picamera2, Preview

# VARIABLES
THRESHOLD = 15  # Any desired value from the accelerometer
REPO_PATH = "/home/pi/Desktop/CubesatChallenge"  # Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = (
    "image_analysis/cubesat_output"  # Your image folder path in your GitHub repo: ex. /Images
)

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
    imgname = f"cubesat_output/{image_time}.jpg" #f"{REPO_PATH}/{FOLDER_PATH}/{name}_{image_time}.jpg"
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
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit("New Photo")
        print("made the commit")
        origin.push()
        print("pushed changes")
    except:
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

    shake_time = time.strftime("%m/%d/%Y-%H:%M")

    picam2.start()
    time.sleep(2)

    # TAKE PHOTO

    picam2.capture_file(img_gen("no_outage", shake_time))

    time.sleep(2)

    picam2.capture_file(img_gen("with_outage", shake_time))

    return shake_time


def main():
    while True:
        shake_time = take_photo()
        image_registration(f"{REPO_PATH}/{FOLDER_PATH}/no_outages_{shake_time}.jpg",f"{REPO_PATH}/{FOLDER_PATH}/with_outages_{shake_time}.jpg", f"{REPO_PATH}/{FOLDER_PATH}/aligned_image_{shake_time}")
        find_difference(f"{REPO_PATH}/{FOLDER_PATH}/no_outages_{shake_time}.jpg", f"{REPO_PATH}/{FOLDER_PATH}/aligned_image_{shake_time}", f"{REPO_PATH}/{FOLDER_PATH}/outage_map_{shake_time}")
        git_push()


if __name__ == "__main__":
    main()
