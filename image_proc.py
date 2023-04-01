import cv2
import numpy as np
from GetVideo import w, h


def getGreenFromVid(img):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blurred = cv2.GaussianBlur(image, (19, 19), 3)
    lower = np.array([35, 183, 170])
    upper = np.array([70, 255, 255])

    mask = cv2.inRange(blurred, lower, upper)
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
    m = cv2.moments(largest_contour)

    # calculate x and y coordinates of centroid
    try:
        cx = int(m["m10"] / m["m00"])
        cy = int(m["m01"] / m["m00"])

        # create a tuple of (x, y) coordinates for the centroid
        centroid = (cx, cy)

        # Draw the largest contour on the original image
        cv2.drawContours(img, [largest_contour], -1, (0, 0, 255), 2)
        cv2.circle(img, centroid, 5, (0, 0, 255), -1)

        # draw crosshair to easier see center of camera
        cv2.line(img, (0, int(h / 2)), (w, int(h / 2)), (194, 194, 194), 1)  # horizontal
        cv2.line(img, (int(w / 2), 0), (int(w / 2), h), (194, 194, 194), 1)  # vertical

        # Show the result
        cv2.imshow('Result', img)
        return centroid, max_area
    except ZeroDivisionError:
        # print("Obj not in sight")
        cv2.imshow('Result', img)
        return None, None


def main():
    pass


if __name__ == '__main__':
    main()
