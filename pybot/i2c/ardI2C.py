import smbus
from time import sleep


class Arduino():
    def __init__(self, address=0x04,i2c_bus = 1):
        self.address = address
        self.bus = smbus.SMBus(i2c_bus)

    def talk(self,message,internal_addr=0x00):
        self.bus.write_i2c_block_data(self.address,internal_addr,message )

    def listen(self, num = 1, shift = 0):
        return self.bus.read_i2c_block_data(self.address, shift, num)

    def drive(self, leftAccel, rightAccel):
        self.talk([0x07, leftAccel, rightAccel])




def test():
    ard = Arduino()
    while True:
        print ard.get_encoder_readings()
        sleep(0.5)
if __name__ == '__main__':
    test()
