import KalmanFilter
import LSM6DS33
from time import sleep

def main():
 LSM6DS33.setupAccel()
 while True:
  rawAccel = LSM6DS33.readRawAccel()

  sleep(0.2)

if __name__ == "__main__":
  main()