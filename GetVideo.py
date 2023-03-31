import asyncio
from threading import Thread
from djitellopy import Tello
import cv2
import time
from image_proc import *

w, h = 1280, 720
centroid = None


def telloGetFrame(the_drone, w=360, h=240):
    my_frame = the_drone.get_frame_read()
    my_frame = my_frame.frame
    img = cv2.resize(my_frame, (w, h))
    return img


def run_robot(drone):
    count = 0
    while True:
        # Step 1
        global w,h
        img = telloGetFrame(drone, w, h)
        # cv2.imshow('Image', getGreenFromVid(img=img))
        global centroid 
        centroid = contouring(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.streamoff()
            break


def flight_controller(drone: Tello):
    async def flight_main():  # this is a function declared inside of another function
        #try:
            # drone.takeoff()
            print(f"battery: {drone.get_battery()}%")
            await asyncio.sleep(0.5)
            print("taken off")
            pixel_error = (0, 0)
            global centroid,w,h
            x_thresh = 20
            while True:
                await asyncio.sleep(0.8)
                #print("turning")
                print(f"centroid: {centroid}")
                if centroid is not None:
                    error_x = centroid[0] - w/2
                    error_y = centroid[1] - h/2
                    pixel_error = (error_x, error_y)
                    print(f"error: {pixel_error}")

                    if pixel_error[0] < -x_thresh:
                        drone.rotate_counter_clockwise(2)
                    if pixel_error[0] > x_thresh:
                        drone.rotate_clockwise(2)
                    else:
                        print("Within range")  # move forward

                # if centroid is not None:
                #     print(f"found! {centroid}")
                #     drone.land()
                #     time.sleep(2)
                #     break
        #finally:
            #print("stream off")
            #drone.streamoff()
            #drone.end()

    asyncio.run(flight_main())


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
    fly_thread = Thread(target=flight_controller, daemon=True, kwargs={"drone": drone})
    fly_thread.start()
    # drone.takeoff()
    run_robot(drone)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
