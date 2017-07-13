#ifndef _Motor_Control_H
#define _Motor_Control_H

#include <AFMotor.h>

class Motor_Control{
	private:
		AF_DCMotor l;
		AF_DCMotor r;
	
	public:
		Motor_Control(AF_DCMotor l, AF_DCMotor r);
		void forward(int speed)
		void backward(int speed)
		void turn_clockwise(int speed)
		void turn_anticlockwise(int speed)

};

#endif 