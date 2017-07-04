import smbus
import time

#I2C bus
bus = smbus.SMBus(1)

# Constants
TSL2591_ADDR = 0x29
TSL2591_CTRL1_XL = 0x10  # [+] Acceleration sensor control
TSL2591_CTRL2_G = 0x11  # Angular rate sensor (gyroscope) control
