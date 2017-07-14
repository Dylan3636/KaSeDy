#ifndef _PID_H_
#define _PID_H_

#include <QTRSensors.h>
#include <AFMotor.h>
#include <time.h>
#include <Arduino.h>

class PID{
    private:
        float * gains = nullptr;
        static const int WINDOW = 10;
        int * integralValues = nullptr;// [WINDOW];
        int * integralPos = nullptr;
        int * t = nullptr;
        int * previous_reading = nullptr;
    public:
        PID(float stupidGains[] );
        ~PID();
        float update(int reading);
        void set_gains(float gains[]);
};

#endif // _PID_H_
