from djitellopy import Tello
import cv2
import time
from datetime import datetime
import os
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
        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.streamoff()
            cv2.destroyAllWindows() #de-allocate GUI
            break


def get_and_save_image(drone):
    img = telloGetFrame(drone, w, h)
    cv2.imshow('Image', img)
    os.chdir("./saved_img")
    date = datetime.today().strftime("%m%d_%H%M%S")
    filename = "an_img_obj" + date + ".png"
    cv2.imwrite(filename, img)
    drone.streamoff()
    cv2.destroyAllWindows() #de-allocate GUI



def main():
    # Instantiating the Tello module
    drone = Tello()
    # Connecting the drone to the python script after connecting to the Drone's WiFi
    drone.connect()
    print(f" batt: {drone.get_battery()}")
    drone.streamon()
    time.sleep(2)
    # run_robot(drone)
    get_and_save_image(drone)

if __name__ == '__main__':
    main()
    pass