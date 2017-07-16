import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal


class MCL:
    def __init__(self,state_space,num_particles,sample_motion_model,sensor_model,initial_particles):
        self.state_space = state_space
        self.num_particles = num_particles
        self.sample_motion_model = sample_motion_model
        self.sensor_model = sensor_model
        self.particles = pd.DataFrame()

        if initial_particles is None:
            for i, dim in enumerate(state_space):
                self.particles.iloc[:,i] = np.random.uniform(state_space[i][0],state_space[i][1],num_particles)
            self.particles = self.particles.as_matrix()
        else:
            self.particles= initial_particles

    def update(self,u,z):
        new_particles = self.sample_motion_model(u,self.particles)  # Sample new particles based on control command.
        weights = self.sensor_model(z,new_particles)  # Weight each sample based on measurement reading.
        self.particles = np.random.choice(new_particles,np.size(self.particles),p=weights)  # Resample particles based on weight given by sensor_model.
        return self.particles

class OCMCL:
    def __init__(self,state_space,num_particles,alphas,odom,map,colour_sensor,initial_particles=None):
        self.alphas = alphas
        self.odom = odom
        self.map = map
        self.colour_sensor = colour_sensor
        self.one_dim = len(state_space)==1
        self.mcl = MCL(state_space,num_particles,self.odom_sample_motion_model,self.color_sensor_model,initial_particles)

    def odom_sample_motion_model(self,u):
        if not self.one_dim:
            (xbar, ybar, theta_bar, x_bar_prime, y_bar_prime, theta_bar_prime) = u

            (x, y, theta,) = self.mcl.particles

            xdiff = x_bar_prime - xbar
            ydiff = y_bar_prime - ybar

            deltaRot1 = np.sqrt(xdiff ** 2 + ydiff ** 2)
            deltaTrans = np.arctan2(ydiff, xdiff) - theta_bar
            deltaRot2 = theta_bar_prime - theta_bar - deltaRot1

            (err1, err2, err3) = (self.alphas[0] * deltaRot1 + self.alphas[1] * deltaTrans,
                                  self.alphas[2] * deltaTrans + self.alphas[3] * (deltaRot1 + deltaRot2),
                                  self.alphas[0] * deltaRot1 + self.alphas[1] * deltaTrans)

            deltaRot1 = deltaRot1 - np.random.normal(0, err1, 1)
            deltaTrans = deltaTrans - np.random.normal(0, err2, 1)
            deltaRot2 = deltaRot2 - np.random.normal(0, err3, 1)
            h1 = np.cos(theta + deltaRot1) - theta_bar
            h2 = np.sin(theta + deltaRot1) - theta_bar

            p = x + deltaTrans * h1
            q = y + deltaTrans * h2
            r = theta + deltaRot1 + deltaRot2
            return [p,q,r]
        else:
            (xbar, _, _, x_bar_prime,) = u
            (x, y, theta,) = self.mcl.particles

            xdiff = x_bar_prime - xbar

            deltaTrans = xdiff

            err = self.alphas[0] * deltaTrans

            deltaTrans = deltaTrans - np.random.normal(0, err, 1)


            p = x + deltaTrans
            return p

    def colour_sensor_model(self,reading):
        pos = map.pos
        colour_map = map.colour_map
        i = 0
        prob = np.zeros(len(colour_map.keys), len(self.gl.states))
        for node, colour in colour_map.iter_values:
            if colour == reading:
                if self.one_dim:
                    mn = multivariate_normal(pos[node][0], 1)
                else:
                    mn = multivariate_normal(pos[node][0], [[1, 0], [0, 1]])
                prob[i] = mn.pdf(self.gl.states)
            else:
                prob[i] = np.zeros([len(self.gl.states), 1])
            i = i + 1
        temp = np.sum(prob * 1 / np.size(prob, 0))
        return temp/np.sum(temp)
