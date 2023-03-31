import asyncio
from threading import Thread
from djitellopy import Tello
import cv2
import time
from image_proc import *

w, h = 1280, 720
centroid = None


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
        # cv2.imshow('Image', getGreenFromVid(img=img))
        global centroid 
        centroid = contouring(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.streamoff()
            break


def flight_controller(drone:Tello):
    async def main(): #this is a function declared inside of another function
        try:
            drone.takeoff()
            await asyncio.sleep(0.5)
            print("taken off")
            while True:
                drone.rotate_clockwise(20)
                asyncio.sleep(0.8)
                print("turning")
                if centroid is not None:
                    print(f"found! {centroid}")
                    drone.land()
                    time.sleep(2)
                    break
        finally:
            print("stream off")
            drone.streamoff()
            drone.end()

    asyncio.run(main())


def main():
    # # Instantiating the Tello module
    # drone = Tello()
    # # Connecting the drone to the python script after connecting to the Drone's WiFi
    # drone.connect()
    # print(f" batt: {drone.get_battery()}")
    # drone.streamon()
    # time.sleep(2)
    # run_robot(drone)
    # Instantiating the Tello module

    drone = Tello()
    # Connecting the drone to the python script after connecting to the Drone's WiFi
    drone.connect()
    drone.streamon()
    time.sleep(2)
    fly_thread = Thread(target=flight_controller, daemon=True, kwargs={"drone":drone})
    fly_thread.start()
    # drone.takeoff()
    run_robot(drone)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()