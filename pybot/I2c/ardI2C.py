import smbus
from time import sleep


class Arduino():
    def __init__(self, address=0x04,i2c_bus = 1):
        self.address = address
        self.bus = smbus.SMBus(i2c_bus)

    def talk(self,message,internal_addr=0x00):
        self.bus.write_i2c_block_data(self.address,internal_addr,message )

    def listen(self):
        return self.bus.read_byte(self.address)

    def get_encoder_readings(self):
        self.talk([0x05])
        #sleep(0.01)
	readings = []
	#readings.append(self.bus.read_byte_data(self.address,0x05))
        #readings.append(self.bus.read_byte_data(self.address, 0x05))
	#readings.append(self.listen())
	readings = self.bus.read_i2c_block_data(self.address,0)
	
        return readings


def test():
    ard = Arduino()
    while True:
        print ard.get_encoder_readings()
        sleep(0.5)
if __name__ == '__main__':
    test()
