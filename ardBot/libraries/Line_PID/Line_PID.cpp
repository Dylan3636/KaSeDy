#include "Line_PID.h"

Line_PID::Line_PID(AF_DCMotor motor,char motorType,int base_speed, QTRSensorsAnalog qtra,int NUM_SENSORS,float stupidGains[] ): motor{motor}, motorType{motorType}, base_speed{base_speed}, qtra{qtra}{
	//unsigned int sensorValues[NUM_SENSORS];
    //pid = PID(stupidGains);
 }



void Line_PID::update(){
	unsigned int position = qtra.readLine(sensorValues);
	int reading =0;
	if (motorType == 'L'){
        reading = sensorValues[3];
      }
      else{
        reading = sensorValues[2];
      }
      float update = pid.update(reading);
      motor.run(RELEASE);
      motor.setSpeed(base_speed+update);
      motor.run(FORWARD);
}

void Line_PID::set_gains(float gains[]){
	pid.set_gains(gains);
}
