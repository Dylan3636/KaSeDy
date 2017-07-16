class Odometer():

    def __init__(self,encoders,x=[0,0,90]):
        self.encL = encoders[0]
        self.encR = encoders[1]
        self.x_previous = x


