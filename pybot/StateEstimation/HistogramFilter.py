import numpy as np
from scipy.stats import multivariate_normal
from BayesFilter import DiscreteBayesFilter


class HistogramFilter:
    def __init__(self,states,odom,color_sensor,map, alphas, initial_probs=None):
        self.states = states
        self.odom = odom
        self.color_sensor = color_sensor
        self.map = map
        self.alphas = alphas
        self.one_dim = len(self.states[0]) == 1
        if initial_probs is None:
            self.posterior = np.ones([len(states),1])/len(states)
        else:
            self.posterior = initial_probs
        self.colour_model = {}
        self.init_color_sensor_model()
        self.prob_model = lambda y: multivariate_normal(0, y)

    def odom_transition_model(self,x_new,x_prev,odom_reading):
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
            prob = np.zeros(len(colour_map.keys), len(self.states))
            for node, colour in colour_map.iter_values:
                if colour == reading:
                    if self.one_dim:
                        mn= multivariate_normal(pos[node][0],1)
                    else:
                        mn= multivariate_normal(pos[node][0],[[1,0],[0,1]])
                    prob[i]=mn.pdf(self.states)
                else:
                    prob[i] = np.zeros([len(self.states),1])
                i = i+1
            self.colour_model[reading]= np.sum(prob*1/np.size(prob,0))

    def colour_sensor_model(self,reading):
        return self.colour_model[reading]

    def update(self):
        odom_reading = self.odom.update()
        colour_reading = self.color_sensor.read()
        trans_matrix = np.zeros(len(self.states))
        
        for i,state in enumerate(self.states):
            trans_matrix[i] = self.odom_transition_model(self.states,state,odom_reading)
        bel_bar = np.dot(trans_matrix,self.posterior)
        z = self.colour_sensor_model(colour_reading)
        unnormalized_post = np.multiply(bel_bar,z)
        eta = np.sum(unnormalized_post)
        self.posterior = unnormalized_post/eta
