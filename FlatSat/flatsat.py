"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

# AUTHOR:
# DATE:

# import libraries
import time
import board
import sys
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL

from git import Repo
from picamera2 import Picamera2

# VARIABLES
THRESHOLD = 15  # Any desired value from the accelerometer
REPO_PATH = "/home/pi/Desktop/CubesatChallenge"  # Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = (
    "/FlatSat/Images"  # Your image folder path in your GitHub repo: ex. /Images
)

auto_push = len(sys.argv) > 1 and sys.argv[1] == "y"

# IMG_LIMIT = 10
# img_taken = 0

# imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()


def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = f"{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg"
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
    This function is NOT complete. Takes a photo when the FlatSat is shaken.
    Replace psuedocode with your own code.
    """

    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        total = (accelx**2 + accely**2 + accelz**2) ** 0.5
        # print(f"{total=:.3f} | {accelx=:.3f} {accely=:.3f} {accelz=:.3f}")

        # CHECKS IF READINGS ARE ABOVE THRESHOLD -> done
        if total > THRESHOLD:
            print(f"Total reached {total:.3f}")
            picam2.start()

            # PAUSE
            time.sleep(2)

            # TAKE PHOTO
            NAME = "FlatSat"
            picam2.capture_file(img_gen(NAME))

            # PUSH PHOTO TO GITHUB
            if auto_push:
                git_push()

            # PAUSE
            time.sleep(0.5)


def main():
    take_photo()


if __name__ == "__main__":
    main()
