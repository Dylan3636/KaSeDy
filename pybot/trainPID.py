#from ardI2C import Arduino
#ard = Arduino()
import numpy as np
import click
exit = 0

while(exit == 0):
    #value = raw_input('Enter PID gains (q to quit): ')
    click.echo()
    if value == 'q':
        exit = 1
    else:
        values = map(long, value.split(' '))
        print values
