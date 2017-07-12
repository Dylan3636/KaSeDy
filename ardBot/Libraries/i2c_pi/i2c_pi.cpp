#include "i2c_pi.h"

//i2c_pi
i2c_pi::i2c_pi(){
     Wire.begin(SLAVE_ADDRESSS);
        Wire.onReceive(receive_data);
        Wire.onRequest(send_data);
}


i2c_pi::~i2c_pi(){
     if(data !=  nullptr){
        delete data;
        data = nullptr;
    }
}

void i2c_pi::receive_data(int byte_count){
    if(data !=  nullptr){
        delete data;
        data = nullptr;
    }
    data = new int[byte_count];
    operation = Wire.read(); // internal address read from Wire

    if (operation == 0x00)
        on = Wire.read()==1;          //Turn Arduino on/off
    else{
        int pos = (sizeof( data ) / sizeof( data[0] ));
       // if(pos <= byte_count)
       //    data[pos] = operation;
        int i = 0;
        while(Wire.available()){
            if(i <= byte_count)
                data[i++] = Wire.read();
        }
    }
}

void i2c_pi::send_data(int number){

}

bool i2c_pi::get_on(){
    return on;
}

int * i2c_pi::get_data(){
    return data;
}

int i2c_pi::get_operation(){
    return operation;
}
//i2c_pi_with_arg
i2c_pi_with_arg::i2c_pi_with_arg(int addr){
     SLAVE_ADDRESSS = addr;
     Wire.begin(SLAVE_ADDRESSS);
     Wire.onReceive(receive_data);
     Wire.onRequest(send_data);
}
