#include "i2c_pi.h"



//i2c_pi
i2c_pi::i2c_pi(){
     Wire.begin(SLAVE_ADDRESSS);
//     Wire.onReceive(receive_data);
//     Wire.onRequest(send_data);
}


i2c_pi::~i2c_pi(){
     if(data !=  nullptr){
        delete data;
        data = nullptr;
    }
}

bool i2c_pi::get_on(){
    return on;
}

void i2c_pi::set_on(bool val){
	on=val;
}
int * i2c_pi::get_data(){
    return data;
}
void i2c_pi::set_data(int * val){

}
int i2c_pi::get_operation(){
    return operation;
}
int i2c_pi::set_operation(int val){
	operation = val;
}
//i2c_pi_with_arg
i2c_pi_with_arg::i2c_pi_with_arg(int addr){
     SLAVE_ADDRESSS = addr;
     Wire.begin(SLAVE_ADDRESSS);
//     Wire.onReceive(receive_data);
//     Wire.onRequest(send_data);
}
