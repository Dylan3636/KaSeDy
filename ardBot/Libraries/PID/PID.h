#ifndef _PID_H_
#define _PID_H_

#include <QTRSensors.h>
#include <AFMotor.h>
#include <time.h>
#include <Arduino.h>

class PID{

private:
    AF_DCMotor motor;
    char motorType;
    QTRSensorsAnalog qtra;
    float gains[];
    static const int WINDOW = 10;
    int integralValues[WINDOW];
    int integralPos;
    int prevVal;
    int t;
public:
    PID(AF_DCMotor motor,char motorType, QTRSensorsAnalog qtra,float stupidGains[] );
    int update(unsigned int sensorValues[]);
};

#endif // _PID_H_
