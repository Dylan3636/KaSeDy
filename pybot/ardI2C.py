import smbus
import time
class Arduino():
    def __init__(self,address=0x04,i2c_bus = 1):
        self.address = address
        self.bus = smbus.SMBus(1)
    def talk(self,message):
        self.bus.write_byte(self.address,message )

    def listen(self):
        return self.bus.read_byte(self.address)
def main():
    ard = Arduino()
    while True:
        ard.talk(1)
        time.sleep(0.5)
if __name__ == '__main__':
    main()
