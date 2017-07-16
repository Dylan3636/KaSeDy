import numpy as np

'''Basic filter for estimating discrete states.'''


class DiscreteBayesFilter:
    def __init__(self,transition_model,sensor_model,initial_probabilities):
        self.transition_model = transition_model #Function that takes an action and returns the transition probabilities.
        self.sensor_model = sensor_model # Function that takes sensor readings and returns probabilities of seeing that readings given the states.
        self.posterior = np.reshape(initial_probabilities,[len(initial_probabilities),1])  # Nx1 matrix describing the probability of being in each of the N states.

    def update(self,action,sensor_reading):
        transition_probabilities = np.matrix(self.transition_model(action))  # NxN numpy matrix describing the probabilities of trasnsitioning from one state to the next.
        bel_bar = np.dot(transition_probabilities,self.posterior)
        z = np.array(self.sensor_model(sensor_reading)) # Probabilities of seeing the sensor reading in the given states P(z|X)
        z=z.reshape([len(z),1])
        temp = np.multiply(bel_bar,z)
        self.posterior = temp/np.sum(temp)
        return self.posterior

def test():
    bf = DiscreteBayesFilter(basic_transition_model,basic_sensor_model,np.asarray([1,1,1],dtype=float)/3)
    print('Starting Bayes Filter test... (Press q to quit.)')
    print('List of actions: L & R')
    print('List of sensor readings: R, B & Y')
    while True:
        action = raw_input('Enter action: ')
        if action == 'q':
            break
        senor_reading = raw_input('Enter senor reading: ')
        if senor_reading == 'q':
            break
        print bf.update(action.strip().capitalize(),senor_reading.strip().capitalize())

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