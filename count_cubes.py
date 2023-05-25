'''
MATTHEW BEDARD
COMP4500 - Mobile Robotics 1
Lab 1
University of Massachusetts Lowell
'''

import cv2
import numpy as np


#TODO: Modify these values for yellow color range.
#      Add separate thresholds for detecting green.

yellow_lower = np.array([10, 170, 120])
yellow_upper = np.array([20, 230, 255])

green_lower = np.array([20, 0, 0])
green_upper = np.array([100, 150, 255])

#TODO: Change this function so that it filters the image based
#      on color using the hsv range for each color.

def filter_image(img, hsv_lower, hsv_upper):
    # Modify mask
    mask = cv2.inRange(img, hsv_lower, hsv_upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    mask = cv2.dilate(mask, kernel)
    return mask

    
#TODO: Change the parameters to make blob detection more accurate.
#      Hint: You might need to set some parameters to specify features
#      such as color, size, and shape.
#      The features have to be selected based on the application. 

def detect_blob(mask):

   # Set up the SimpleBlobdetector with default parameters with specific values.

    params = cv2.SimpleBlobDetector_Params()
    params.filterByCircularity = 0
    params.filterByInertia = 0
    params.filterByConvexity = 0
    params.filterByColor = 1
    params.filterByArea = 1
    
    params.minArea = 500
    params.maxArea = 7000
    params.blobColor = 255
    
    
  # builds a blob detector with the given parameters 
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(mask)
    blobs = cv2.drawKeypoints(mask, keypoints, (0,255,255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)
    #cv2.imshow("blobs", blobs)
    #cv2.waitKey(0)
    return len(keypoints)
    
def count_cubes(img):
    img = cv2.GaussianBlur(img, (11,11), cv2.BORDER_DEFAULT)
    hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_yellow = filter_image(hsvimg, yellow_lower, yellow_upper)
    mask_green = filter_image(hsvimg, green_lower, green_upper)
    
    mask_yellow = cv2.medianBlur(mask_yellow, 5)
    mask_green = cv2.medianBlur(mask_green, 5)
    
    #cv2.imshow("yellow", mask_yellow)
    #cv2.imshow("green", mask_green)
    #cv2.imshow("img", img)
    #cv2.waitKey(0)

    num_yellow = detect_blob(mask_yellow)
    num_green = detect_blob(mask_green)
    
    #TODO: Modify to return number of detected cubes for both yellow and green (instead of 0)
    return num_yellow, num_green

