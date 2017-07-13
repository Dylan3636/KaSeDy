from ardI2C import Arduino
ard = Arduino()
#mport numpy as np
#mport _tkinter
import curses
exit = 0

ard.talk([1])
screen = curses.initscr()

try:
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

finally:
    curses.endwin()
    screen.addstr("Press a key\n")
code = 0
while(exit == 0):
    #value = raw_input('Enter PID gains (q to quit): ')

    event = screen.getch()
    #click.echo(message='Direct me! (Press q to quit.)')
    #c=click.getchar()
    ard.talk([code], 0x02)

    if event == 113:
        exit = 1
    elif event == 32:
        code = 0
    elif event == curses.KEY_UP:
        print "Pressed Up"
        code = 1
    elif event == curses.KEY_LEFT:
        print "Pressed Left"
        code = 2
    elif event == curses.KEY_RIGHT:
        print "Pressed Right"
        code = 3
    elif event == curses.KEY_DOWN:
        print "Pressed Down"
        code = 4
    else:
        print event

curses.endwin()

