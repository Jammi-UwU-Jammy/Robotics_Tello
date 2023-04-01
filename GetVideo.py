import asyncio
from threading import Thread
from djitellopy import Tello
import cv2
import time
import image_proc

w, h = 1280, 720
centroid = None


def telloGetFrame(the_drone):
    my_frame = the_drone.get_frame_read()
    my_frame = my_frame.frame
    img = cv2.resize(my_frame, (w, h))
    return img


def run_robot(drone):
    while True:
        # Step 1
        global w, h
        img = telloGetFrame(drone)
        # cv2.imshow('Image', getGreenFromVid(img=img))
        global centroid
        centroid = image_proc.contouring(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.streamoff()
            break


def flight_controller(drone: Tello):
    async def flight_main():  # this is a function declared inside another function
        try:
            # drone.takeoff()
            await asyncio.sleep(0.5)
            print("taken off")
            global centroid, w, h
            x_thresh = 80
            while True:
                await asyncio.sleep(0.8)
                print(f"centroid: {centroid}")
                if centroid is not None:
                    # noinspection PyUnresolvedReferences
                    px_error_x = centroid[0] - w / 2
                    # noinspection PyUnresolvedReferences
                    px_error_y = centroid[1] - h / 2
                    pixel_error = (px_error_x, px_error_y)
                    print(f"error: {pixel_error}")

                    if px_error_x < -x_thresh:
                        # drone.rotate_counter_clockwise(2)
                        print("turning counter-clockwise")
                        await asyncio.sleep(3)
                    elif px_error_x > x_thresh:
                        # drone.rotate_clockwise(2)
                        print("turning clockwise")
                        await asyncio.sleep(3)
                    else:
                        print("Within range")  # move forward
        except Exception as e:
            print(repr(e))
        finally:
            print("stream off")
            drone.streamoff()
            drone.land()
            drone.end()

    asyncio.run(flight_main())


def main():

    drone = Tello()
    drone.connect()
    print(f"battery: {drone.get_battery()}%")
    drone.streamon()
    time.sleep(2)
    fly_thread = Thread(target=flight_controller, daemon=True, kwargs={"drone": drone})
    fly_thread.start()
    # drone.takeoff()
    run_robot(drone)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
