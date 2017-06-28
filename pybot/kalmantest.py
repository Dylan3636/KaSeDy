import KalmanFilter
import LSM6DS33
from time import sleep


def main():
    LSM6DS33.setupAccel()
    while True:
        accel = LSM6DS33.readCalibAccel()
        accel = accel[0:1]

        sleep(0.2)


if __name__ == "__main__":
    main()