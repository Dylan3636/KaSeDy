#include Motors.h
#include <AFMotor.h>

Motors::Motors(int m1, int m2){
	AF_DCMotor l(m1);
	AF_DCMotor r(m2);

}
void Motors::forward(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(FORWARD);
	r.run(FORWARD);
}

void Motors::backward(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(BACKWARD);
	r.run(BACKWARD);
}

void Motors::turn_clockwise(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(FORWARD);
	r.run(BACKWARD);
}

void Motors::turn_anticlockwise(int speed){
	l.run(RELEASE);
	r.run(RELEASE);
	l.setSpeed(speed);
	r.setSpeed(speed);
	l.run(BACKWARD);
	r.run(FORWARD);
}

