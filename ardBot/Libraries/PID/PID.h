#ifndef _PID_H_
#define _PID_H_

#include <QTRSensors.h>
#include <AFMotor.h>
#include <time.h>
#include <Arduino.h>

class PID{
    private:
        float gains[];
        static const int WINDOW = 10;
        int integralValues[WINDOW];
        int integralPos;
        int prevVal;
        int t;
        int previous_reading = 0;
    public:
        PID(float stupidGains[] );
        float update(int reading);
        void set_gains(float gains[]);
};

#endif // _PID_H_
