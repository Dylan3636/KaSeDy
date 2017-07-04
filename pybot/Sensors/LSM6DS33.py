#!/usr/bin/python

# Imports
import numpy as np
from smbus import SMBus
from time import sleep
from pandas import DataFrame
class LSM6DS33():
 # Constants
 LSM6DS33_ADDR= 0x6b
 LSM6DS33_CTRL1_XL = 0x10  # [+] Acceleration sensor control
 LSM6DS33_CTRL2_G= 0x11# Angular rate sensor (gyroscope) control

 # Gyroscope dps/LSB for 1000 dps full scale
 GYRO_GAIN= 0.035
 # Accelerometer g/LSB for +/- 2 g full scale
 ACCEL_GAIN =9.81*0.061/1000
 # LSM6DS33 Gyroscope and accelerometer output registers
 LSM6DS33_OUTX_L_G= 0x22# Gyroscope pitch axis (X) output, low byte
 LSM6DS33_OUTX_H_G= 0x23# Gyroscope pitch axis (X) output, high byte
 LSM6DS33_OUTY_L_G= 0x24 # Gyroscope roll axis (Y) output, low byte
 LSM6DS33_OUTY_H_G= 0x25 # Gyroscope roll axis (Y) output, high byte
 LSM6DS33_OUTZ_L_G= 0x26 # Gyroscope yaw axis (Z) output, low byte
 LSM6DS33_OUTZ_H_G= 0x27 # Gyroscope yaw axis (Z) output, high byte
 LSM6DS33_OUTX_L_XL= 0x28 # Accelerometer pitch axis (X) output, low byte
 LSM6DS33_OUTX_H_XL= 0x29 # Accelerometer pitch axis (X) output, high byte
 LSM6DS33_OUTY_L_XL= 0x2A # Accelerometer roll axis (Y) output, low byte
 LSM6DS33_OUTY_H_XL= 0x2B # Accelerometer roll axis (Y) output, high byte
 LSM6DS33_OUTZ_L_XL = 0x2C # Accelerometer yaw axis (Z) output, low byte
 LSM6DS33_OUTZ_H_XL = 0x2D # Accelerometer yaw axis (Z) output, high byte
 gyroRegisters = [
 LSM6DS33_OUTX_L_G,# low byte of X value
 LSM6DS33_OUTX_H_G,# high byte of X value
 LSM6DS33_OUTY_L_G,# low byte of Y value
 LSM6DS33_OUTY_H_G,# high byte of Y value
 LSM6DS33_OUTZ_L_G,# low byte of Z value
 LSM6DS33_OUTZ_H_G,# high byte of Z value
 ]
 accelRegisters = [
 LSM6DS33_OUTX_L_XL,# Accelerometer pitch axis (X) output, low byte
 LSM6DS33_OUTX_H_XL,# Accelerometer pitch axis (X) output, high byte
 LSM6DS33_OUTY_L_XL,# Accelerometer roll axis (Y) output, low byte
 LSM6DS33_OUTY_H_XL,# Accelerometer roll axis (Y) output, high byte
 LSM6DS33_OUTZ_L_XL,# Accelerometer yaw axis (Z) output, low byte
 LSM6DS33_OUTZ_H_XL,# Accelerometer yaw axis (Z) output, high byte
 ]
 i2c = SMBus(1)

 def setupGyro(self):
  # Disable accelerometer and gyroscope first
  #i2c.writeRegister(LSM6DS33_ADDR, LSM6DS33_CTRL2_G, 0x00)
  self.i2c.write_byte_data(self.LSM6DS33_ADDR, self.LSM6DS33_CTRL2_G, 0x58)
  self.calibrateGyro()

 def calibrateGyro(self):
     print('Calibrating Gyro...\n')
     b = True
     mat = []
     while (b):
         mat.extend([self.readRawGyro()])
         b = len(mat) == 1000
         sleep(0.05)
     m = DataFrame(mat)
     self.zeroGyro = m.mean.as_matrix()
     self.setupGyroSTD = m.std().as_matrix()

 def setupAccel(self):
  # Disable accelerometer and gyroscope first
  self.i2c.write_byte_data(self.LSM6DS33_ADDR, self.LSM6DS33_CTRL1_XL, 0x50)

 def combineLoHi(self,loByte, hiByte):
  """ Combine low and high bytes to an unsigned 16 bit value. """
  return (hiByte << 8) | loByte

 def combineSignedLoHi(self,loByte, hiByte):
  """ Combine low and high bytes to a signed 16 bit value. """
  combined = self.combineLoHi (loByte, hiByte)
  return combined if combined < 32768 else (combined - 65536)

 def readRawGyro(self):
  #Read register outputs and combine low and high byte values
  xl = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.gyroRegisters[0])
  xh = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.gyroRegisters[1])
  yl = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.gyroRegisters[2])
  yh = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.gyroRegisters[3])
  zl = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.gyroRegisters[4])
  zh = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.gyroRegisters[5])

  xVal = self.combineSignedLoHi(xl, xh)
  yVal = self.combineSignedLoHi(yl, yh)
  zVal = self.combineSignedLoHi(zl, zh)
  # Return the vector
  return [xVal, yVal, zVal]

 def readRawAccel(self):
  #Read register outputs and combine low and high byte values
  xl = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.accelRegisters[0])
  xh = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.accelRegisters[1])
  yl = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.accelRegisters[2])
  yh = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.accelRegisters[3])
  zl = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.accelRegisters[4])
  zh = self.i2c.read_byte_data(self.LSM6DS33_ADDR, self.accelRegisters[5])

  xVal = self.combineSignedLoHi(xl, xh)
  yVal = self.combineSignedLoHi(yl, yh)
  zVal = self.combineSignedLoHi(zl, zh)

  # Return the vector
  return [xVal, yVal, zVal]

 def readCalibAccel(self):
     rawAccel = self.readRawAccel()
     return np.array(rawAccel)*self.ACCEL_GAIN
 def readCalibGyro(self):
     rawGyro = self.readRawGyro()
     calGyro = np.array(rawGyro)-self.zeroGyro
     return np.array(rawGyro)*self.GYRO_GAIN
 def main(self):
  #self.setupAccel()
  self.setupGyro()
  while True:
   #rawAccel = self.readRawAccel()
   #print ('x: %f y: %f z: %f' %
   #(float (rawAccel[0]) * self.ACCEL_GAIN,
   #float(rawAccel[1]) * self.ACCEL_GAIN,
   #float(rawAccel[2]) * self.ACCEL_GAIN))

   rawGyro = self.readRawGyro()
   print ('x: %f y: %f z: %f' %
   (float (rawGyro[0]) * self.GYRO_GAIN,
   float(rawGyro[1]) * self.GYRO_GAIN,
   float(rawGyro[2]) * self.GYRO_GAIN))
   sleep(0.2)

if __name__ == "__main__":
  ls=LSM6DS33()
  ls.main()

 #All the outpust are taken when the gyro is no moving (steady set on the table)



"""
Outputs when combining to signed 16 bit:
r: 73 p: -76 y: -77
r: 71 p: -74 y: -78
r: 73 p: -71 y: -76
r: 75 p: -72 y: -78
r: 75 p: -70 y: -78
r: 74 p: -74 y: -77
r: 74 p: -71 y: -80
r: 71 p: -69 y: -78
r: 72 p: -73 y: -75
r: 75 p: -74 y: -79
r: 74 p: -69 y: -79
r: 74 p: -72 y: -78
r: 74 p: -70 y: -78
r: 73 p: -70 y: -76
r: 74 p: -76 y: -81
r: 73 p: -72 y: -79
r: 67 p: -69 y: -77
r: 74 p: -73 y: -73
r: 72 p: -73 y: -77
r: 72 p: -75 y: -76
r: 70 p: -73 y: -76
r: 74 p: -67 y: -78
r: 74 p: -72 y: -79
r: 69 p: -66 y: -78
r: 74 p: -73 y: -77
r: 70 p: -69 y: -80
r: 72 p: -70 y: -78
"""

"""
Outputs when combining to unsigned 16 bit:
r: 74 p: 65467 y: 65460
r: 73 p: 65466 y: 65459
r: 76 p: 65462 y: 65459
r: 76 p: 65465 y: 65461
r: 73 p: 65467 y: 65461
r: 69 p: 65465 y: 65457
r: 76 p: 65465 y: 65458
r: 73 p: 65470 y: 65458
r: 74 p: 65465 y: 65460
r: 76 p: 65467 y: 65462
r: 73 p: 65464 y: 65460
r: 77 p: 65465 y: 65457
r: 73 p: 65465 y: 65457
r: 76 p: 65463 y: 65459
r: 72 p: 65465 y: 65461
r: 69 p: 65466 y: 65456
r: 74 p: 65465 y: 65457
r: 74 p: 65463 y: 65459
r: 77 p: 65469 y: 65458
r: 76 p: 65465 y: 65458
r: 73 p: 65464 y: 65458
r: 76 p: 65466 y: 65459
r: 77 p: 65462 y: 65456
"""

"""
Output when combining to signed 16bit value and multipling with the gyro gain.
r: 2.555000 p: -2.625000 y: -2.695000
r: 2.625000 p: -2.590000 y: -2.695000
r: 2.555000 p: -2.380000 y: -2.660000
r: 2.660000 p: -2.520000 y: -2.765000
r: 2.555000 p: -2.625000 y: -2.765000
r: 2.765000 p: -2.415000 y: -2.695000
r: 2.485000 p: -2.380000 y: -2.695000
r: 2.590000 p: -2.450000 y: -2.730000
r: 2.625000 p: -2.555000 y: -2.730000
r: 2.520000 p: -2.520000 y: -2.625000
r: 2.555000 p: -2.450000 y: -2.660000
r: 2.590000 p: -2.695000 y: -2.660000
r: 2.555000 p: -2.555000 y: -2.765000
r: 2.695000 p: -2.520000 y: -2.660000
r: 2.555000 p: -2.380000 y: -2.730000
r: 2.590000 p: -2.520000 y: -2.660000
r: 2.520000 p: -2.485000 y: -2.765000
r: 2.625000 p: -2.380000 y: -2.660000
r: 2.625000 p: -2.555000 y: -2.730000
r: 2.415000 p: -2.555000 y: -2.695000
r: 2.485000 p: -2.380000 y: -2.765000
r: 2.555000 p: -2.415000 y: -2.660000
r: 2.625000 p: -2.450000 y: -2.695000
r: 2.590000 p: -2.590000 y: -2.730000
r: 2.520000 p: -2.450000 y: -2.695000
r: 2.555000 p: -2.555000 y: -2.800000
r: 2.625000 p: -2.485000 y: -2.590000
"""