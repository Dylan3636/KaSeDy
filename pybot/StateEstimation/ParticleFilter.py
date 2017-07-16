import numpy as np
import pandas as pd


class ParticleFilter:
    def __init__(self,state_space,num_particles,sample_state_model,sensor_model,initial_particles):
        self.state_space = state_space
        self.num_particles = num_particles
        self.sample_state_model = sample_state_model
        self.sensor_model = sensor_model
        self.particles = pd.DataFrame()
        if initial_particles is None:
            for i, dim in enumerate(state_space):
                self.particles.iloc[:,i] = np.random.uniform(state_space[i][0],state_space[i][1],num_particles)
            self.particles = self.particles.as_matrix()
        else:
            self.particles= initial_particles

    def update(self,u,z):
        new_particles = self.sample_state_model(u,self.particles)  # Sample new particles based on control command/ action u.
        weights = self.sensor_model(z,new_particles)  # Weight each sample based on measurement reading.
        self.particles = np.random.choice(new_particles,np.size(self.particles),p=weights)  # Resample particles based on weight given by sensor_model.
        return self.particles

