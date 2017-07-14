#ifndef Line_PID_H_
#define Line_PID_H_

#include <QTRSensors.h>
#include <AFMotor.h>
#include <Arduino.h>
#include <PID.h>

class Line_PID{

private:
    AF_DCMotor motor;
    char motorType;
    int base_speed;
    int NUM_SENSORS;
    QTRSensorsAnalog qtra;
    PID * pid = nullptr;
public:
    Line_PID(AF_DCMotor motor,char motorType,int base_speed, QTRSensorsAnalog qtra,int NUM_SENSORS,float stupidGains[] );
    ~Line_PID();
    void update();
    void set_gains(float gains[]);
};

#endif // Line_PID_H_
