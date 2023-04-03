import asyncio
from threading import Thread
from djitellopy import Tello
import cv2
import time
import image_proc

w, h = 1280, 720
centroid = None
area = None


def telloGetFrame(the_drone):
    global w, h
    my_frame = the_drone.get_frame_read()
    my_frame = my_frame.frame
    img = cv2.resize(my_frame, (w, h))
    return img


def run_robot(drone):
    while True:
        # Step 1
        global w, h, centroid, area
        img = telloGetFrame(drone)
        centroid, area = image_proc.contouring(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.streamoff()
            break


def flight_controller(drone: Tello):
    async def flight_main():  # this is a function declared inside another function
        try:
            drone.takeoff()
            await asyncio.sleep(0.5)
            print("taken off")
            global w, h, centroid, area
            deg_thresh_x = 5
            deg_thresh_y = 3
            area_thresh = w * h * 0.35
            while True:
                await asyncio.sleep(0.8)
                print(f"centroid: {centroid}")
                if centroid is not None:
                    px_error_x = centroid[0] - w / 2
                    px_error_y = centroid[1] - h / 2
                    print(f"error: {(px_error_x, px_error_y)}")

                    deg_error_x = px_error_x * 46 / w
                    deg_error_y = px_error_y * 22 / h
                    print(f"Degree error: {(deg_error_x, deg_error_y)}")

                    if abs(deg_error_x) > deg_thresh_x:
                        drone.rotate_clockwise(int(deg_error_x))
                        print("turning")
                        await asyncio.sleep(.5)
                    if deg_error_y > deg_thresh_y:
                        drone.move_down(20)
                        print("moving down")
                        await asyncio.sleep(.5)
                    elif deg_error_y < -deg_thresh_y:
                        drone.move_up(20)
                        print("moving up")
                        await asyncio.sleep(.5)
                    elif area is not None:
                        if area > area_thresh:
                            drone.land()
                            break
                        else:
                            print("Within bearing range")
                            print(f"area: {area} px, {round(area / (w * h) * 100)}%")
                            move_dist = int(2 / (area / (w * h)))
                            if move_dist > 150:
                                move_dist = 150
                            if move_dist < 20:
                                move_dist = 20
                            drone.move_forward(move_dist)
                else:
                    print("target not detected, rotating")
                    drone.rotate_clockwise(50)
        except Exception as e:
            print(repr(e))
        finally:
            print("arrived at target, stream off and land")
            drone.streamoff()
            drone.land()
            print(f"battery: {drone.get_battery()}%")
            drone.end()

    asyncio.run(flight_main())


def main():
    drone = Tello()
    drone.connect()
    print(f"battery: {drone.get_battery()}%")
    drone.streamon()
    time.sleep(2)
    # fly_thread = Thread(target=flight_controller, daemon=True, kwargs={"drone": drone})
    # fly_thread.start()
    # drone.takeoff()
    run_robot(drone)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
