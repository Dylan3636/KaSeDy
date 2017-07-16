class Odometer():

    def __init__(self,encoders,x=0,y=0,theta=90):
        self.encL = encoders[0]
        self.encR = encoders[1]
        self.x_previous = x
        self.y_previous = y
        self.theta_previous=theta


