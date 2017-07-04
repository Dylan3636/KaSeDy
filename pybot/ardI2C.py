import smbus


class Arduino():
    def __init__(self,address=0x04,i2c_bus = 1):
        self.adress = address
        self.bus = smbus.SMBus(1)
    def talk(self,message):

        self.bus.write.data()

