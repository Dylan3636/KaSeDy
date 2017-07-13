#ifndef _MOTORS_H
#define _MOTORS_H

#include <AFMotor.h>

class Motors{
	private:
		AF_DCMotor l;
		AF_DCMotor r;
	
	public:
		Motors(AF_DCMotor l, AF_DCMotor r);
		void forward(int speed)
		void backward(int speed)
		void turn_clockwise(int speed)
		void turn_anticlockwise(int speed)

};

#endif 