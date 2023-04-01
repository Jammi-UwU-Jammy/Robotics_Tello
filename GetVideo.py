import asyncio
import math
from threading import Thread
from djitellopy import Tello
import cv2
import time
from image_proc import *

w, h = 1280, 720
camera_center = (w/2, h/2)
centroid = None


def telloGetFrame(theDrone, w=w, h=h):
    myFrame = theDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img

def approach():

    distance = math.sqrt(math.pow(centroid[0]-camera_center[0], 2) + math.pow(centroid[1]-camera_center[1], 2))
    print("approaching")
    # camera center == obj centroid => do smth
    if distance == 0 or centroid[1] == camera_center[1]:
        return None
    
    # else correct the angle
    alpha = math.acos((centroid[1]-camera_center[1])/distance)
    print(f'alpha = {alpha*57.3}')

    turn_right = centroid[0] > camera_center[0]
    alpha = alpha if alpha < 90 else 180 - alpha

    return turn_right, int(alpha*57.3)
                           



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
        # try:
            drone.takeoff()
            await asyncio.sleep(0.5)
            print("taken off")
            while True: # finding centroid
                drone.rotate_clockwise(20)
                await asyncio.sleep(0.5)
                print("turning")

                if centroid is not None:
                    print(f"found! {centroid}")
                    while True:
                        cw, forward = approach()
                        print(f"centroid = {centroid}")


                        if forward == None: #when close enough or something
                            drone.move_forward(50)
                        elif cw == True:
                            drone.rotate_clockwise(forward)
                        else:
                            drone.rotate_counter_clockwise(forward)
                        drone.move_forward(50)
        # # finally:
        #     print("stream off")
        #     drone.streamoff()
        #     drone.end()

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
    print(drone.get_battery())
    drone.streamon()
    time.sleep(2)
    fly_thread = Thread(target=flight_controller, daemon=True, kwargs={"drone":drone})
    fly_thread.start()
    # drone.takeoff()
    run_robot(drone)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()