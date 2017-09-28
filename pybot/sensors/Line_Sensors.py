from i2c.ardI2C import Arduino

class Line_Sensors:
    def __init__(self):
        self.on_line = True
        self.arduino = Arduino()

    def get_readings(self):

        self.arduino.talk([0x06])
        raw_readings = self.arduino.listen(9)
        self.on_line = raw_readings.pop(0) not in [1, 4]
        readings = []

        reading = raw_readings[0]
        reading |= raw_readings[1] << 8
        readings.append(reading)

        reading = raw_readings[2]
        reading |= raw_readings[3] << 8
        readings.append(reading)

        reading = raw_readings[4]
        reading |= raw_readings[5] << 8
        readings.append(reading)

        reading = raw_readings[6]
        reading |= raw_readings[7] << 8
        readings.append(reading)

        return readings

    def is_on_line(self):
        self.arduino.talk([0x06])
        raw_readings = self.arduino.listen(1)
        self.on_line = raw_readings.pop(0) not in [1, 4]
        return self.on_line