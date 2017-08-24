import numpy as np


class Odometer:

    CLICK_GAIN = 0.1  # scale to convert the encoder counts (clicks) to cm
    RADIUS = 2  # radius of robot in cm

    def __init__(self, ardI2c, init_x=[0, 0, 90], init_readings=np.array([0, 0])):
        self.arduino = ardI2c
        self.x_previous = init_x
        self.previous_readings = init_readings


    def update(self):
        raw_readings = np.array(self.arduino.get_encoder_readings())
        readings = raw_readings*self.CLICK_GAIN
        delta = readings - self.previous_readings
        delta_l = delta[0]
        delta_r = delta[1]
        delta_ave = (delta_l+delta_r)/2
        delta_theta = (delta_r - delta_l)/2*self.RADIUS
        delta_x = delta_ave*np.cos(np.deg2rad(self.x_previous[2]) + delta_theta/2)
        delta_y = delta_ave * np.cos(np.deg2rad(self.x_previous[2]) + delta_theta/2)
        x = self.x_previous + [delta_x, delta_y, np.rad2deg(delta_theta)]
        x_prev = self.x_previous
        self.x_previous = x
        self.previous_readings = readings
        return x, x_prev

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname('..\pybot\I2c'))
    from I2c.ardI2C import Arduino
    ard = Arduino()
    odom = Odometer(ard)
    while True:
        print odom.update()

