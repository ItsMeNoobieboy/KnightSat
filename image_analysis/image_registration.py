# adapted from https://www.geeksforgeeks.org/image-registration-using-opencv-python/

import cv2 
import numpy as np

def image_registration(no_outages_path, with_outages_path, output_path):

    # Open the image files. 
    with_outages_color = cv2.imread(with_outages_path) # Image to be aligned. 
    no_outages_color = cv2.imread(no_outages_path) # Reference image. 

    # Convert to grayscale. 
    with_outages = cv2.cvtColor(with_outages_color, cv2.COLOR_BGR2GRAY) 
    no_outages = cv2.cvtColor(no_outages_color, cv2.COLOR_BGR2GRAY) 
    height, width = no_outages.shape 

    # Create ORB detector with 5000 features. 
    orb_detector = cv2.ORB_create(5000) 

    # Find keypoints and descriptors. 
    # The first arg is the image, second arg is the mask 
    # (which is not required in this case). 
    kp1, d1 = orb_detector.detectAndCompute(with_outages, None) 
    kp2, d2 = orb_detector.detectAndCompute(no_outages, None) 

    # Match features between the two images. 
    # We create a Brute Force matcher with 
    # Hamming distance as measurement mode. 
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 

    # Match the two sets of descriptors. 
    matches = list(matcher.match(d1, d2))
    print(type(matches))

    # Sort matches on the basis of their Hamming distance. 
    matches.sort(key = lambda x: x.distance) 

    # Take the top 90 % matches forward. 
    matches = matches[:int(len(matches)*0.9)] 
    no_of_matches = len(matches) 

    # Define empty matrices of shape no_of_matches * 2. 
    p1 = np.zeros((no_of_matches, 2)) 
    p2 = np.zeros((no_of_matches, 2)) 

    for i in range(len(matches)): 
        p1[i, :] = kp1[matches[i].queryIdx].pt 
        p2[i, :] = kp2[matches[i].trainIdx].pt 

    # Find the homography matrix. 
    homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC) 

    # Use this matrix to transform the 
    # colored image wrt the reference image. 
    transformed_img = cv2.warpPerspective(with_outages_color, 
                        homography, (width, height)) 

    # Save the output. 
    cv2.imwrite(f'{output_path}.png', transformed_img) 

image_registration("image_analysis/satelite_images/city.png", "image_analysis/misaligned_input/with_outages6.jpeg", "image_analysis/aligned_output/test1")