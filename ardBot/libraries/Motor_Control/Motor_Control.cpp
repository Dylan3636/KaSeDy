#include "Motor_Control.h"
#include <AFMotor.h>

Motor_Control::Motor_Control(int m1, int m2):l{AF_DCMotor(m1)}, r{AF_DCMotor(m2)}{
	//l = AF_DCMotor(m1);
	//r = AF_DCMotor(m2);

}
void Motor_Control::forward_forever(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(FORWARD);
	r.run(FORWARD);
}

void Motor_Control::backward_forever(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(BACKWARD);
	r.run(BACKWARD);
}

void Motor_Control::turn_clockwise_forever(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(FORWARD);
	r.run(BACKWARD);
}

void Motor_Control::turn_anticlockwise_forever(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(BACKWARD);
	r.run(FORWARD);
}
void Motor_Control::halt(){
	l.run(RELEASE);
	r.run(RELEASE);
}
