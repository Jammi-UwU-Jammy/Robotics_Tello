from utils_image import *
from djitellopy import Tello
import cv2, numpy as np
import time
import matplotlib.pyplot as plt


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


    #cv2.imshow('mask', mask)
    cv2.imshow('result', result)
    cv2.waitKey()

def getGreen2(path):
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower bound and upper bound for Green color
    lower_bound = np.array([35,150,40])	 
    upper_bound = np.array([100,255,255])

    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    cv2.imshow('result', mask)
    cv2.waitKey()
    




def main():
    img_path = "./saved_img/an_img_obj0323_120942.png"
    image = cv2.imread(img_path)
    rgbimg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #plt has pixel coordinates in case need testing 
    plt.imshow(image)
    plt.waitforbuttonpress()
    plt.close('all')
    #Pixel coord is (y,x) ?*
    pixel = image[227,355]#[64,712]
    print(pixel)

    # cv2.imshow("img", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    getGreen(img_path)





    

    
            


if __name__ == '__main__':
    main()
    pass