import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
import time
plt.rcParams['figure.figsize'] = (10, 8)
plt.interactive(False)

class KalmanFilter(object):

    def __init__(self, N, h, A=None, B=None, H=None, Q=None, R=None):
        self.N = N
        if A != None:

            self.A = np.array(A) #NxN matrix prediction matrix
            self.B = np.array(B) #Nxl control matrix
            self.Q = Q  # process covariance
            self.R = R  # sensor covariance
        if H != None:
            self.H = np.array(H) #hxN sensor matrix

        self.h = np.size(h, 0)
        self.K = np.zeros([self.N,self.h])  #Kalman Gain Nxh matrix
        self.x_hat = np.zeros([self.N,1]) # a posteriori estimate of current state
        self.P = np.zeros(self.N) #a posteriori error estimate (covariance matrix)

    def updateStateBelief(self,u,z,A=None,B=None,H=None,Q=None,R=None):
        """Updating state belief using u (lx1 control vector) and z (hx1 previous_observation vector)"""
        #Time Update "Predict"
        if A==None:
            (A,B,H,Q,R) = (self.A,self.B,self.H,self.Q,self.R)
        x_hat_minus = A*self.x_hat + B*u # a priori estimate of current state
        P_minus = A*self.P*A.T + Q # a priori error estimate (covariance matrix)

        #Measurement Update "Correct"
        val = H * P_minus * H.T + R
        if len(val.shape)>1:
         tmp=np.linalg.inv(val)
        else:
         tmp = 1/val

        self.K = P_minus*H.T*tmp
        self.x_hat = x_hat_minus + self.K*(z-H*x_hat_minus)
        self.P = (np.eye(self.N)-self.K)*H*P_minus
        return self.x_hat

    def stateProb(self):
        return multivariate_normal.pdf(self.x_hat,self.x_hat,self.P)

    class AGOKalmanFilter:

        def __init__(self, odom, imu, alphas=[0.1, 0.1, 0.1, 0.1], sample=False):
            self.odom = odom
            self.imu = imu
            self.x_hat = [0, 0, 0, 0, 0]
            self.P = np.eye(5)
            H = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]])
            self.kf = KalmanFilter(5, 3, H)
            (self.alpha1, self.alpha2, self.alpha3, self.alpha4, self.alpha5) = alphas
            self.sample = sample

        def update(self):
            (z, R) = self.proccessOdomData()
            (A, B, u, Q) = self.proccessIMUData()
            (self.x_hat, self.P) = (self.x_hat_prime, self.P_prime)
            (self.x_hat_prime, self.P_prime) = self.kf.updateBeliefState(u, z, A, B, Q, R)

        def proccessIMUData(self):
            [u, deltaT] = self.imu.read()
            A = [[1, 0, 0, deltaT, 0], [0, 1, 0, 0, deltaT], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
            B = [[0.5 * deltaT ** 2, 0, 0], [0, 0.5 * deltaT ** 2, 0], [0, 0, deltaT], [deltaT, 0, 0], [0, deltaT, 0]]
            M = np.Matrix([[0.5 * deltaT ** 2], [0.5 * deltaT ** 2], [deltaT], [deltaT], [deltaT]])
            Q = M * M.T * 0.01

            return (A, B, u, Q)

        def proccessOdomData(self):
            (xbar, ybar, theta_bar, x_bar_prime, y_bar_prime, theta_bar_prime) = self.odom.update()
            (x, y, theta,) = self.x_hat

            xdiff = x_bar_prime - xbar
            ydiff = y_bar_prime - ybar

            deltaRot1 = np.sqrt(xdiff ** 2 + ydiff ** 2)
            deltaTrans = np.arctan2(ydiff, xdiff) - theta_bar
            deltaRot2 = theta_bar_prime - theta_bar - deltaRot1

            (err1, err2, err3) = (self.alpha1 * deltaRot1 + self.alpha2 * deltaTrans,
                                  self.alpha3 * deltaTrans + self.alpha4 * (deltaRot1 + deltaRot2),
                                  self.alpha1 * deltaRot1 + self.alpha2 * deltaTrans)
            if self.sample:
                deltaRot1 = deltaRot1 - np.random.normal(0, err1, 1)
                deltaTrans = deltaTrans - np.random.normal(0, err2, 1)
                deltaRot2 = deltaRot2 - np.random.normal(0, err3, 1)
            h1 = np.cos(theta + deltaRot1) - theta_bar
            h2 = np.sin(theta + deltaRot1) - theta_bar

            p = x + deltaTrans * h1
            q = y + deltaTrans * h2
            r = theta + deltaRot1 + deltaRot2

            f = np.array([p, q, r]).T
            R = np.diag([err1, err2, err3])
            return (f, R)


def main():
    A = [1]
    B = A
    H = [1]
    Q = 1e-5
    R = 0.1**2
    kf = KalmanFilter(A,B,H,Q,R)
    x = -0.3
    x_hat = np.zeros([100,1])
    z = np.zeros([100,1])
    for i in range(0,100):
        z[i] = np.random.normal(i**2, 100)
        x_hat[i]=kf.updateStateBelief(0,z[i])
    plt.figure()
    plt.plot(z, 'k+', label='noisy measurements')
    plt.plot(x_hat, 'b-', label='a posteri estimate')
    plt.plot(np.square(range(0,100)), 'g-', label='truth value')
    #plt.axhline(x, color='g', label='truth value')
    plt.legend()
    plt.title('Estimate vs. iteration step', fontweight='bold')
    plt.xlabel('Iteration')
    plt.ylabel('Voltage')
    plt.show()
    return kf



if __name__ == "__main__":
  main()

