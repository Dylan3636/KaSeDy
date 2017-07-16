import numpy as np
from scipy.stats import multivariate_normal

class GridLocalization:
    'Basic GridLocalization Algorithm'
    def __init__(self, states, motion_model, sensor_model, initial_probs=None):
        self.states = states
        self.motion_model = motion_model
        self.sensor_model = sensor_model
        if initial_probs is None:
            self.posterior = np.ones([len(states),1])/len(states)
        else:
            self.posterior = initial_probs

    def update(self,u,reading):
        trans_matrix = np.zeros(len(self.gl.states))

        for i, state in enumerate(self.gl.states):
            trans_matrix[i] = self.motion_model(self.states,u,state)

        bel_bar = np.dot(trans_matrix, self.posterior)

        sensor_prob = self.sensor_model(reading)

        unnormalized_post = np.multiply(bel_bar, sensor_prob)
        eta = np.sum(unnormalized_post)
        self.posterior = unnormalized_post / eta


class OCGridLocalization:
    'Grid Localization using Odometry as the motion model and the colour sensor as the sensor model'
    def __init__(self, states, alphas, odom, color_sensor, map, initial_probs=None):
        self.odom = odom
        self.color_sensor = color_sensor
        self.map = map

        self.alphas = alphas
        self.one_dim = len(states[0]) == 1
        self.colour_model = {}
        self.init_color_sensor_model()
        self.prob_model = lambda y: multivariate_normal(0, y)

        self.gl = GridLocalization(states,self.odom_motion_model,self.colour_sensor_model,initial_probs)

    def odom_motion_model(self,x_new,odom_reading,x_prev):
        if (not self.one_dim):
            (x_bar, y_bar, theta_bar, x_bar_prime, y_bar_prime, theta_bar_prime) = odom_reading

            (x_prime, y_prime, theta_prime) = x_new
            (x, y, theta) = x_prev

            delta_y = y_bar_prime - y_bar
            delta_x = x_bar_prime - x_bar

            rot1 = np.arctan2(delta_y,delta_x)-theta_bar
            trans = np.sqrt(delta_x**2+delta_y**2)
            rot2 = theta_bar_prime-theta_bar-rot1

            delta_y = y_prime - y
            delta_x = x_prime - x

            rot1_hat = np.arctan2(delta_y,delta_x)-theta
            trans_hat = np.sqrt(delta_x**2 + delta_y**2)
            rot2_hat = theta_prime-theta-rot1_hat

            p1 = self.prob_model(self.alphas[1]*rot1_hat+self.alphas[2]*trans_hat).logpdf(rot1-rot1_hat)
            p2 = self.prob_model(self.alphas[3] * trans_hat + self.alphas[4] * (rot1_hat+rot2_hat)).logpdf(trans - trans_hat)
            p3 = self.prob_model(self.alphas[1] * rot2_hat + self.alphas[2] * trans_hat).logpdf(rot2 - rot2_hat)
            prob = np.log(p1+p2+p3)
        else:
            (x_bar, _, _, x_bar_prime) = odom_reading
            (x_prime,) = x_new
            (x,) = x_prev
            delta_x = x_bar_prime - x_bar
            trans = delta_x
            delta_x = x_prime - x
            trans_hat = delta_x
            prob = self.prob_model(self.alphas[0] * trans_hat).pdf(trans - trans_hat)
        return prob

    def init_color_sensor_model(self):
        pos = map.pos
        colour_map = map.colour_map

        for reading in map.get_colours:
            i = 0
            prob = np.zeros(len(colour_map.keys), len(self.gl.states))
            for node, colour in colour_map.iter_values:
                if colour == reading:
                    if self.one_dim:
                        mn= multivariate_normal(pos[node][0],1)
                    else:
                        mn= multivariate_normal(pos[node][0],[[1,0],[0,1]])
                    prob[i]=mn.pdf(self.gl.states)
                else:
                    prob[i] = np.zeros([len(self.gl.states),1])
                i = i+1
            temp = np.sum(prob * 1 / np.size(prob, 0))
            self.colour_model[reading] = temp / np.sum(temp)

    def colour_sensor_model(self,reading):
        return self.colour_model[reading]

    def update(self):
        odom_reading = self.odom.update()
        colour_reading = self.color_sensor.read()

        return self.gl.update(odom_reading,colour_reading)

    def get_posterior(self):
        return self.gl.posterior