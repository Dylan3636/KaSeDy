#include "i2c_pi.h"

//i2c_pi
i2c_pi::i2c_pi(){
     Wire.begin(SLAVE_ADDRESSS);
}


i2c_pi::~i2c_pi(){
     if(data !=  nullptr){
        delete data;
        data = nullptr;
    }
    if(encoders != nullptr){
        delete encoders;
        encoders = nullptr;
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
void i2c_pi::set_data(int val[], int pos){
    if(data != nullptr){
        delete data;
        data = nullptr;
    }
    data = new int[pos];
    for(int i=0;i<pos;i++){
        data[i] = val[i];
    }
}
int i2c_pi::get_operation(){
    return operation;
}
int i2c_pi::set_operation(int val){
	operation = val;
}

void i2c_pi::set_encoders(Wheel_Encoders* enc){
    if(encoders != nullptr){
        delete encoders;
        encoders = nullptr;
    }
    encoders = enc;
}

void i2c_pi::command_motors(int* data, Motor_Control motors, int speed){
    if((data!=nullptr)){   
    if(get_operation()==0x02){
        int action = data[1];
        switch(action) {
          case 0: motors.halt(); break;
          case 1: motors.forward_forever(speed); break;
          case 2: motors.turn_anticlockwise_forever(speed); break;
          case 3: motors.turn_clockwise_forever(speed); break;
          case 4: motors.backward_forever(speed); break;
      }
    }
  }
}


void i2c_pi::receive_data(int byte_count ){
    Wire.read();
    if (! Wire.available()){
        return;
    }
    int * data = get_data();
    
    if(data !=  nullptr){
        delete data;
        data = nullptr;
    }
    
    data = new int[byte_count];
    set_operation(Wire.read()); // internal address read from Wire
    Serial.println(get_operation());

    if (get_operation() == 0x00){
    
        set_on(Wire.read()==1);
        while(Wire.available()){Wire.read();}        //Turn Arduino on/off
        }
    
    else if(get_operation() == 0x05) {
        while(Wire.available()){Wire.read();}
        Wire.beginTransmission(SLAVE_ADDRESSS);
        
        if (encoders == nullptr){
            Wire.write(-1); //Encoders not set

        }
        else {
            int* readings = encoders -> get_clicks();
            int m1_count = readings[0];
            int m2_count = readings[1];
            //int tmp[2] = {m1_count, m2_count};
            Wire.write(0x05);
            Wire.write(m1_count);
            //Wire.send(m1_count);
            Wire.write(m2_count);
            Serial.println(m2_count);
            delete[] readings;
        }
       
        int val = Wire.endTransmission();
        Serial.println(val);
        return;
    }
    else{
        int i = 0;
        while(Wire.available()){
            if(i <= byte_count)
                data[i++] = Wire.read();
        }
            set_data(data, byte_count-1);
    }

}
void request_data(Wheel_Encoders we, QTRSensorsAnalog qtra){
    if(get_operation()==0x05){
        int* ind = we.get_clicks();

          //Sending 1st encoder reading
        int num = ind[0];
        Wire.write(num & 0xFF);
        Wire.write((num >> 8) & 0xFF);
        Wire.write((num >> 16) & 0xFF);
        Wire.write((num >> 24) & 0xFF);

          //Sending 2nd encoder reading
        num = ind[1];
        Wire.write(num & 0xFF);
        Wire.write((num >> 8) & 0xFF);
        Wire.write((num >> 16) & 0xFF);
        Wire.write((num >> 24) & 0xFF);
    }
    else if(get_operation()==0x06){
        qtra

    }
}


//i2c_pi_with_arg
i2c_pi_with_arg::i2c_pi_with_arg(int addr){
     SLAVE_ADDRESSS = addr;
     Wire.begin(SLAVE_ADDRESSS);
}


