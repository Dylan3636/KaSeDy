import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
import time
plt.rcParams['figure.figsize'] = (10, 8)
plt.interactive(False)

class KalmanFilter(object):

    def __init__(self,N,h,A=None,B=None,H=None,Q=None,R=None):
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
        """Updating state belief using u (lx1 control vector) and z (hx1 observation vector)"""
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

