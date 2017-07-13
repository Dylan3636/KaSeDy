#from ardI2C import Arduino
#ard = Arduino()
import numpy as np
import click
exit = 0

while(exit == 0):
    #value = raw_input('Enter PID gains (q to quit): ')
    click.echo(message='Direct me! (Press q to quit.)')
    c=click.getchar()
    print 'here: '+c
    if c == 'q':
        exit = 1
    else:
        print c
