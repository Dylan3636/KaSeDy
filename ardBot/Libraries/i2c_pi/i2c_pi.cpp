#include "i2c_pi.h"

//i2c_pi
i2c_pi::i2c_pi(){
     Wire.begin(SLAVE_ADDRESSS);
        Wire.onReceive(receive_data);
        Wire.onRequest(send_data);
}

void i2c_pi::receive_data(int byte_count){
    while(!data.empty()){
        data.pop_back();
    }
    int operation = Wire.read(); // internal address read from Wire

    if (operation == 0x00)
        on = Wire.read;          //Turn Arduino on/off
    else{
        data.push_back(operation);
        while(Wire.available){
            data.push_back(Wire.read());
        }
    }
}

void i2c_pi::send_data(int number){

}

bool i2c_pi::on(){
    return on;
}

std::vector i2c_pi::data(){
    return data;
}
//i2c_pi_with_arg
i2c_pi_with_arg::i2c_pi_with_arg(int addr){
     SLAVE_ADDRESSS = addr;
     Wire.begin(SLAVE_ADDRESSS);
     Wire.onReceive(receive_data);
     Wire.onRequest(send_data);
}
