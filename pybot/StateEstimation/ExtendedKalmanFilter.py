import numpy as np

from StateEstimation.KalmanFilter import KalmanFilter


class EKF1():

    def __init__(self,odom,imu,alphas=[0.1,0.1,0.1,0.1],sample=False):
        self.odom = odom
        self.imu = imu
        self.x_hat = [0,0,0,0,0]
        self.P = np.eye(5)
        H= np.matrix([[1,0,0],[0,1,0],[0,0,1],[0,0,0],[0,0,0]])
        self.kf = KalmanFilter(5, 3, H)
        (self.alpha1,self.alpha2,self.alpha3,self.alpha4,self.alpha5) =alphas
        self.sample = sample

    def update(self):
        (z,R)=self.proccessOdomData()
        (A,B,u,Q)=self.proccessIMUData()
        (self.x_hat,self.P) = (self.x_hat_prime,self.P_prime)
        (self.x_hat_prime,self.P_prime)=self.kf.updateBeliefState(u,z,A,B,Q,R)

    def proccessIMUData(self):
        [u,deltaT]=self.imu.read()
        A=[[1,0,0,deltaT,0],[0,1,0,0,deltaT],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        B=[[0.5*deltaT**2,0,0],[0,0.5*deltaT**2,0],[0,0,deltaT],[deltaT,0,0],[0,deltaT,0]]
        M = np.Matrix([[0.5*deltaT**2],[0.5*deltaT**2],[deltaT],[deltaT],[deltaT]])
        Q = M*M.T*0.01

        return A, B, u, Q

    def proccessOdomData(self):
        (xbar, ybar, theta_bar, x_bar_prime, y_bar_prime, theta_bar_prime) = self.odom.update()
        (x, y, theta,) = self.x_hat

        xdiff = x_bar_prime - xbar
        ydiff = y_bar_prime - ybar

        deltaRot1 = np.sqrt(xdiff ** 2 + ydiff ** 2)
        deltaTrans = np.arctan2(ydiff, xdiff) -theta_bar
        deltaRot2 = theta_bar_prime-theta_bar-deltaRot1

        (err1,err2,err3) = (self.alpha1*deltaRot1 + self.alpha2*deltaTrans, self.alpha3*deltaTrans + self.alpha4*(deltaRot1 + deltaRot2) , self.alpha1*deltaRot1+self.alpha2*deltaTrans)
        if self.sample:
            deltaRot1 =deltaRot1- np.random.normal(0,err1,1)
            deltaTrans=deltaTrans- np.random.normal(0,err2,1)
            deltaRot2=deltaRot2- np.random.normal(0,err3,1)
        h1 = np.cos(theta + deltaRot1) - theta_bar
        h2 = np.sin(theta + deltaRot1) - theta_bar

        p = x + deltaTrans* h1
        q = y + deltaTrans* h2
        r = theta + deltaRot1 +deltaRot2

        f=np.array([p,q,r]).T
        R = np.diag([err1,err2,err3])
        return (f,R)

    def getF(self,u,x_hat):
        (xbar, ybar, theta_bar, x_bar_prime, y_bar_prime, theta_bar_prime) = u
        (x, y, theta,) = x_hat

        xdiff = x_bar_prime - xbar
        ydiff = y_bar_prime - ybar

        k = np.sqrt(xdiff ** 2 + ydiff ** 2)
        kxbar = (xdiff) / np.sqrt((xdiff) ** 2 + (ydiff) ** 2)
        kxbarprime = -kxbar
        kybar = (ydiff) / np.sqrt((xdiff) ** 2 + (ydiff) ** 2)
        kybarprime = -kybar
        kthetabar = 0
        kthetabarprime = 0

        g = np.arctan2(ydiff, xdiff) - theta_bar
        gxbar = -0.5 * np.power((xdiff), 3.5) / (xdiff ** 2 + ydiff)
        gxbarprime = -gxbar
        gybar = -0.5 * np.power((ydiff), 3.5) / (xdiff + ydiff ** 2)
        gybarprime = -gybar
        gthetabar = 0
        gthetabarprime = 0

        h1 = np.cos(theta + g) - theta_bar
        h1xbar = -np.sin(theta + g) * gxbar
        h1xbarprime = -np.sin(theta + g) * gxbarprime
        h1ybar = -np.sin(theta + g) * gybar
        h1ybarprime = -np.sin(theta + g) * gybarprime
        h1thetabar = -np.sin(theta + g) * gthetabar
        h1thetabarprime = -np.sin(theta + g) * gthetabarprime

        h2 = np.sin(theta + g) - theta_bar
        h2xbar = np.cos(theta + g) * gxbar
        h2xbarprime = np.cos(theta + g) * gxbarprime
        h2ybar = np.cos(theta + g) * gybar
        h2ybarprime = np.cos(theta + g) * gybarprime
        h2thetabar = np.cos(theta + g) * gthetabar
        h2thetabarprime = np.cos(theta + g) * gthetabarprime

        p = x + k * h1
        pxbar = h1 * kxbar + k * h1xbar
        pxbarprime = h1 * kxbarprime + k * h1xbarprime
        pybar = h1 * kybar + k * h1ybar
        pybarprime = h1 * kybarprime + k * h1ybarprime
        pthetabar = h1 * kthetabar + k * h1thetabar
        pthetabarprime = h1 * kthetabarprime + k * h1thetabarprime

        q = y + k * h2
        qxbar = h2 * kxbar + k * h2xbar
        qxbarprime = h2 * kxbarprime + k * h2xbarprime
        qybar = h2 * kybar + k * h2ybar
        qybarprime = h2 * kybarprime + k * h2ybarprime
        qthetabar = h2 * kthetabar + k * h2thetabar
        qthetabarprime = h2 * kthetabarprime + k * h2thetabarprime

        r = theta + theta_bar - theta_bar_prime
        rthetabar = 1
        rthetabarprime = -1
        (rxbar, rxbarprime, rybar, rybarprime) = (0, 0, 0, 0)

        F = np.matrix([[pxbar, pybar, pthetabar, pxbarprime, pybarprime, pthetabarprime],
                       [qxbar, qybar, qthetabar, qxbarprime, qybarprime, qthetabarprime],
                       [rxbar, rybar, rthetabar, rxbarprime, rybarprime, rthetabarprime], [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0]])
