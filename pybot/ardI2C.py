import smbus
import time
class Arduino():
    def __init__(self,address=0x04,i2c_bus = 1):
        self.address = address
        self.bus = smbus.SMBus(1)
<<<<<<< HEAD
    def talk(self,message,internal_addr=0x00):
        self.bus.write_byte_data(self.address,internal_addr,message )
=======
    def talk(self,message):
        self.bus.write_block_data(self.address,0x00,message )
>>>>>>> df9150e476e373e2d9f3555491a908de7a4372e4

    def listen(self):
        return self.bus.read_byte(self.address)
def test():
    ard = Arduino()
    while True:
        ard.talk([1,2])
        time.sleep(0.5)
if __name__ == '__main__':
    test()
