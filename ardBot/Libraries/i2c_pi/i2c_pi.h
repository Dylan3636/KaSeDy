#ifndef _I2C_PI_H_
#define _I2C_PI_H_

#include <Wire.h>
#include <Wheel_Encoders.h>
#include <Motor_Control.h>

class i2c_pi{
private:
    int operation = 0;
    bool on = false;
    int SLAVE_ADDRESSS = 0x04;
    int * data = nullptr;
    Wheel_Encoders * encoders = nullptr;
public:
    i2c_pi();
    ~i2c_pi();
    bool get_on();
    void set_on(bool val);
    int * get_data();
    void set_data(int val[], int pos);
    int get_operation();
    int set_operation(int val);
    void set_encoders(Wheel_Encoders* enc);
    void command_motors(int* data, Motor_Control motors, int speed);
    void receive_data(int byte_count);
    void request_data();
};

class i2c_pi_with_arg: public i2c_pi{
private:
    int operation = 0;
    bool on = false;
    int SLAVE_ADDRESSS = 0x04;
    int * data =  nullptr;
    Wheel_Encoders * encoders = nullptr;

public:
    i2c_pi_with_arg(int addr);
};


#endif // _I2C_PI_H_
