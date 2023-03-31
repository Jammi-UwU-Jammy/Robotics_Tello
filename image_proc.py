from utils_image import *
from djitellopy import Tello
import cv2, numpy as np
import time
# import matplotlib.pyplot as plt

centroid = None


def getGreen(path):
    oimage = cv2.imread(path)
    #h, w, d = image.shape
    image = cv2.cvtColor(oimage, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    # worked
    lower = np.array([35,150,60])
    upper = np.array([70,255,255])

    mask = cv2.inRange(image, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    # cv2.imshow('result', result)
    # cv2.waitKey()

def getGreen2(path):
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower bound and upper bound for Green color
    lower_bound = np.array([35,150,40])	 
    upper_bound = np.array([100,255,255])

    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    # cv2.imshow('result', mask)
    # cv2.waitKey()


def getGreenFromVid(img):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    # worked
    lower = np.array([35,150,60])
    upper = np.array([70,255,255])

    mask = cv2.inRange(image, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result


def contouring(img):
    # img = cv2.imread('saved_img/an_img_obj0323_120942.png')
    green = getGreenFromVid(img)
    gray = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)

    # Apply threshold to create binary image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = None
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            largest_contour = contour
            max_area = area

    ####
    M = cv2.moments(largest_contour)

# calculate x and y coordinates of centroid
    try:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

    # create a tuple of (x, y) coordinates for the centroid
        centroid = (cx, cy)

        # Draw the largest contour on the original image
        cv2.drawContours(img, [largest_contour], -1, (0, 0, 255), 2)
        cv2.circle(img, centroid, 5, (0, 0, 255), -1)

        # Show the result
        cv2.imshow('Result', img)
        return centroid
    except ZeroDivisionError:
        # print("Obj not in sight")
        cv2.imshow('Result', img)


def main():
    pass


if __name__ == '__main__':
    main()
    pass