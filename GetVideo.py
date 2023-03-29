from djitellopy import Tello
import cv2; from matplotlib import pyplot as plt
import time
from image_proc import getGreenFromVid

w, h = 1280, 720



def telloGetFrame(theDrone, w=360, h=240):
    myFrame = theDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img

def run_robot(drone):
    count = 0
    while True:
        # Step 1
        img = telloGetFrame(drone, w, h)

        cv2.imshow('Image', getGreenFromVid(img=img))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.streamoff()
            break


def main():
    # Instantiating the Tello module
    drone = Tello()
    # Connecting the drone to the python script after connecting to the Drone's WiFi
    drone.connect()
    print(f" batt: {drone.get_battery()}")
    drone.streamon()
    time.sleep(2)
    run_robot(drone)

if __name__ == '__main__':
    main()