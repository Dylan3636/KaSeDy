#include Motor_Control.h
#include <AFMotor.h>

Motor_Control::Motor_Control(int m1, int m2){
	AF_DCMotor l(m1);
	AF_DCMotor r(m2);

}
void Motor_Control::forward(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(FORWARD);
	r.run(FORWARD);
}

void Motor_Control::backward(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(BACKWARD);
	r.run(BACKWARD);
}

void Motor_Control::turn_clockwise(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(FORWARD);
	r.run(BACKWARD);
}

void Motor_Control::turn_anticlockwise(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(BACKWARD);
	r.run(FORWARD);
}

