from time import sleep
import git
import os

from image_analysis.image_registration import image_registration
from image_analysis.find_outages import find_difference

REPO_PATH = os.path.abspath(__file__)
FOLDER_PATH = "image_analysis/cubesat_output"

repo = git.Repo("")

last_commit = repo.head.commit

path_to_output = "image_analysis/cubesat_output"

while True:

    sleep(1)

    repo.pull('origin','main')

    new_commit = repo.head.commit

    if (last_commit != new_commit):

        folders = os.listdir(path_to_output)

        shake_time = max(folders)

        path_to_folder = f"{FOLDER_PATH}/{shake_time}"

        no_outages_path = f"{path_to_folder}/no_outages.jpg"
        with_outages_path = f"{path_to_folder}/with_outages.jpg"

        aligned_image_path = f"{path_to_folder}/aligned_image"
        outage_map_path = f"{path_to_folder}/outage_map"

        image_registration(
            no_outages_path,
            with_outages_path,
            aligned_image_path
        )
        
        find_difference(
            no_outages_path,
            aligned_image_path + ".png",
            outage_map_path
        )




