from djitellopy import Tello


def main():
    drone = Tello()
    drone.connect()
    drone.streamoff()
    drone.land()
    print(f"battery: {drone.get_battery()}%")
    drone.end()


if __name__ == '__main__':
    main()
