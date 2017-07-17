#ifndef _Motor_Control_H_
#define _Motor_Control_H_

#include <AFMotor.h>

class Motor_Control{
	private:
		AF_DCMotor l;
		AF_DCMotor r;
	
	public:
		Motor_Control(int m1, int m2);
		void halt();
		void forward_forever(int speed);
		void forward(int speed, int time);
		void backward_forever(int speed);
		void backward(int speed, int time);
		void turn_clockwise_forever(int speed);
		void turn_clockwise(int speed, int time);
		void turn_anticlockwise_forever(int speed);
		void turn_anticlockwise(int speed, int time);


};

#endif 