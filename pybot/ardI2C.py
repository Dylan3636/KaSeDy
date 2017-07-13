import smbus
import time
class Arduino():
    def __init__(self,address=0x04,i2c_bus = 1):
        self.address = address
        self.bus = smbus.SMBus(i2c_bus)

    def talk(self,message,internal_addr=0x00):
        self.bus.write_block_data(self.address,internal_addr,message )

    def listen(self):
        return self.bus.read_byte(self.address)

def test():
    ard = Arduino()
    while True:
        ard.talk([1,2])
        time.sleep(0.5)
if __name__ == '__main__':
    test()
