from time import sleep

from sensors import LSM6DS33


def main():
 LSM6DS33.setupAccel()
 while True:
  rawAccel = LSM6DS33.readRawAccel()

  sleep(0.2)

if __name__ == "__main__":
  main()