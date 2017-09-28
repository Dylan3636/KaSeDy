
from __future__ import print_function
import os
import neat
from i2c.ardI2C import Arduino
from sensors.Line_Sensors import Line_Sensors
from time import time

arduino = Arduino()
ls = Line_Sensors()

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        #genome.fitness = 4.0
        'Evaluating Genome {}:, {}'.format(genome_id, genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        last_time = time()
        while ls.on_line:
            readings = ls.get_readings()
            output = net.activate(readings)
            output[0] = min(max(round(output[0]), -255), 255)
            output[1] = min(max(round(output[1]), -255), 255)
            arduino.drive(output[0], output[1])
        genome.fitness = time() - last_time()


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)