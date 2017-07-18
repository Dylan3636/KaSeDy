#include "Motor_Control.h"
#include <Adafruit_MotorShield.h>

Motor_Control::Motor_Control(Adafruit_DCMotor* m1, Adafruit_DCMotor* m2):l{m1}, r{m2}{}

void Motor_Control::halt(){
	l -> run(RELEASE);
	r -> run(RELEASE);
}

void Motor_Control::forward_forever(int speed){
	l -> run(RELEASE);
	r -> run(RELEASE);
	l -> setSpeed(speed);
	r -> setSpeed(speed);
	l -> run(FORWARD);
	r -> run(FORWARD);
}
void Motor_Control::forward(int speed, int time){
	l -> run(RELEASE);
	r -> run(RELEASE);
	l -> setSpeed(speed);
	r -> setSpeed(speed);
	float t = millis();
	l -> run(FORWARD);
	r -> run(FORWARD);
	delay(time*1000);
	halt();
}

void Motor_Control::backward_forever(int speed){
	l -> run(RELEASE);
	r -> run(RELEASE);
	l -> setSpeed(speed);
	r -> setSpeed(speed);
	l -> run(BACKWARD);
	r -> run(BACKWARD);
}
void Motor_Control::backward(int speed, int time){
	l -> run(RELEASE);
	r -> run(RELEASE);
	l -> setSpeed(speed);
	r -> setSpeed(speed);
	float t = millis();
	l -> run(BACKWARD);
	r -> run(BACKWARD);
	delay(time*1000);
	halt();
}

void Motor_Control::turn_clockwise_forever(int speed){
	l -> run(RELEASE);
	r -> run(RELEASE);
	l -> setSpeed(speed);
	r -> setSpeed(speed);
	l -> run(FORWARD);
	r -> run(BACKWARD);
}
void Motor_Control::turn_clockwise(int speed, int time){
	l -> run(RELEASE);
	r -> run(RELEASE);
	l -> setSpeed(speed);
	r -> setSpeed(speed);
	l -> run(FORWARD);
	r -> run(BACKWARD);
	delay(time*1000);
	halt();
}

void Motor_Control::turn_anticlockwise_forever(int speed){
	l -> run(RELEASE);
	r -> run(RELEASE);
	l -> setSpeed(speed);
	r -> setSpeed(speed);
	l -> run(BACKWARD);
	r -> run(FORWARD);
}
void Motor_Control::turn_anticlockwise(int speed, int time){
	l -> run(RELEASE);
	r -> run(RELEASE);
	l -> setSpeed(speed);
	r -> setSpeed(speed);
	l -> run(BACKWARD);
	r -> run(FORWARD);
	delay(time*1000);
	halt();
}
