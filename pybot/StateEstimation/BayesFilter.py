import os
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath('..//..//..//Machine_Learning//ReinforcementLearning//environments')))
from environments.random_maze.Map import Map
'''Basic filter for estimating discrete states.'''


class DiscreteBayesFilter:
    def __init__(self,transition_model,sensor_model,initial_probabilities):
        self.transition_model = transition_model #Function that takes an action and returns the transition probabilities.
        self.sensor_model = sensor_model # Function that takes sensor readings and returns probabilities of seeing that readings given the states.
        self.posterior = np.reshape(initial_probabilities,len(initial_probabilities))  # Nx1 matrix describing the probability of being in each of the N states.

    def update(self,action,sensor_reading):
        transition_probabilities = np.matrix(self.transition_model(action)).transpose()  # NxN numpy matrix describing the probabilities of trasnsitioning from one state to the next.
        bel_bar = np.dot(transition_probabilities, self.posterior)
        sensor_prob = np.array(self.sensor_model(sensor_reading)) # Probabilities of seeing the sensor reading in the given states P(z|X)
        sensor_prob=sensor_prob.reshape(len(sensor_prob))
        temp = np.multiply(bel_bar,sensor_prob).tolist()
        self.posterior = (np.array(temp)/np.sum(temp))[0]
        return self.posterior
    def predict(self, action, sensor_reading):
        transition_probabilities = np.matrix(self.transition_model(action)).transpose()  # NxN numpy matrix describing the probabilities of trasnsitioning from one state to the next.
        bel_bar = np.dot(transition_probabilities, self.posterior)
        sensor_prob = np.array(
            self.sensor_model(sensor_reading))  # Probabilities of seeing the sensor reading in the given states P(z|X)
        sensor_prob = sensor_prob.reshape(len(sensor_prob))
        temp = np.multiply(bel_bar, sensor_prob).tolist() # P(z,s'|a,b)
        return np.array(temp)


def test():
    map = Map.random_grid_map(3, 5)
    transition_model = map.get_transition_model()
    sensor_model = map.get_sensor_model()
    initial_belief = np.asarray(np.ones(map.num_states),dtype=float)/map.num_states
    bf = DiscreteBayesFilter(transition_model, sensor_model, initial_belief)
    print('Starting Bayes Filter map test... (Press q to quit.)')
    print('List of actions: N,S,W,E')
    print('List of sensor readings: {}'.format(np.unique(map.colour_map)))
    prev_state = np.random.choice(range(map.num_states))
    ax = plt.subplot(111)
    map.show(initial_belief, prev_state, ax=ax, show=True, delay=0.4)
    while True:
        action = input('Enter action: ')
        if action == 'q':
            break

        tmp = transition_model(action)
        state = np.random.choice(range(map.num_states),p=tmp[prev_state])
        sensor_reading = map.colour_map[state]
        if sensor_reading == 'q':
            break
        belief = bf.update(action.strip().capitalize(), sensor_reading)
        print(tmp[prev_state])
        print(sensor_model(sensor_reading))
        print(belief)
        map.show(belief, state, ax=ax, show=False)
        prev_state = state

def basic_transition_model(action):
    '''Basic example: 3 states labelled 1,2 and 3 on a 1 D plane. Agent can only move left (L) or right (R) with some noise.
    Sensor model detects color of the nodes with some noise.
    '''
    transition_model = {
        'L': [[0.6, 0.4, 0],[0.4,0.2,0.4],[0,0.6,0.4]],
        'R': [[0.4, 0.6, 0], [0.4, 0.2, 0.4],[0, 0.4, 0.6] ]
    }
    return transition_model[action]

def basic_sensor_model(sensor_reading):

    colour_map={
        'R':'red',
        'B':'blue',
        'Y':'yellow'
    }

    sensor_model = {
        'red' : [0.7,0.1,0.3],
        'blue': [0.2,0.7,0.1],
        'yellow':[0.1,0.2,0.6]
    }

    return sensor_model[colour_map[sensor_reading]]

if __name__ == '__main__':
    test()