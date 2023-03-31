#original was https://neptune.ai/blog/building-a-facemask-surveillance-system-with-drone-technology
#and
#https://gr33nonline.wordpress.com/2021/07/14/course-notes-drone-face-tracking/
#which I then mixed together with
# https://tellopilots.com/threads/the-secret-of-showing-video-with-opencv-is.5987/

# Importing the Tello Drone Library
from djitellopy import Tello
# Importing OpenCV library
import cv2
# Importing time package
import time
# Importing OS module
import asyncio
from threading import Thread
from image_proc import getGreenFromVid





#w, h = 360, 480
w, h = 1280, 720


def telloGetFrame(theDrone, w=360, h=240):
    myFrame = theDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img


def flight_controller(drone:Tello):
    async def main(): #this is a function declared inside of another function
        try:
            await drone.takeoff()
            await drone.turn_clockwise(360)
            # await drone.move_left(20)
            await drone.land()
        finally:
            await drone.streamoff()
            await drone.disconnect()

    asyncio.run(main())


def run_robot(drone):
    count = 0
    while True:
        # Step 1
        img = telloGetFrame(drone, w, h)
        cv2.imshow('Image', getGreenFromVid(img))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.streamoff()
            drone.land()
            break


def main():
    # Instantiating the Tello module
    drone = Tello()
    # Connecting the drone to the python script after connecting to the Drone's WiFi
    drone.connect()
    drone.streamon()
    time.sleep(2)
    fly_thread = Thread(target=flight_controller, daemon=True, kwargs={"drone":drone})
    fly_thread.start()
    drone.takeoff()
    run_robot(drone)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()