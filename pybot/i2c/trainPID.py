from i2c.ardI2C import Arduino
ard = Arduino()

exit = 0
ard.talk([1])
while exit == 0:
    value = raw_input('Enter PID gains (q to quit): ')
    if value == 'q':
        exit = 1
    else:
        values = map(int, value.split(' '))
        print values
	ard.talk(values,0x01)
ard.talk([0])