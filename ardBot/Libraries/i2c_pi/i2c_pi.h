#ifndef _I2C_PI_H_
#define _I2C_PI_H_

#include <Wire.h>

class i2c_pi{
private:
    int operation = 0;
    bool on = false;
    int SLAVE_ADDRESSS = 0x04;
    int * data = nullptr;
public:
    i2c_pi();
    ~i2c_pi();
    //void receive_data(int byte_count);
    //void send_data(int number);
    bool get_on();
    int * get_data();
    int get_operation();

};

class i2c_pi_with_arg: public i2c_pi{
private:
    int operation = 0;
    bool on = false;
    int SLAVE_ADDRESSS = 0x04;
    int * data =  nullptr;
public:
    i2c_pi_with_arg(int addr);
};


#endif // _I2C_PI_H_


