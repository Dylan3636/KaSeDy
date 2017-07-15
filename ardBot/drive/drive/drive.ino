#include <i2c_pi.h>
#include <Motor_Control.h>

#define DEFAULT_SPEED 100

i2c_pi pi = i2c_pi();
Motor_Control motors = Motor_Control(1,2) ;
bool on = false;

void setup() { 
    Serial.begin(9600);
    Wire.onReceive(receive_data);
}

void loop() {
  
  while( !on){
    on = pi.get_on();
    delay(500);
  }

  int* data = pi.get_data();

  if((data!=nullptr)){   
    if(pi.get_operation()==0x02){
        int action = data[1];
        switch(action) {
          case 0: motors.halt();break;
          case 1: motors.forward_forever(DEFAULT_SPEED); break;
          case 2: motors.turn_anticlockwise_forever(DEFAULT_SPEED); break;
          case 3: motors.turn_clockwise_forever(DEFAULT_SPEED); break;
          case 4: motors.backward_forever(DEFAULT_SPEED); break;
      }
    }
  }
  delay(500);
}
void receive_data(int byte_count){
    int * data = pi.get_data();
    if(data !=  nullptr){
        delete data;
        data = nullptr;
    }
    data = new int[byte_count];
    pi.set_operation(Wire.read()); // internal address read from Wire
    if (pi.get_operation() == 0x00){
        pi.set_on(Wire.read()==1);
        while(Wire.available()){Wire.read();}}        //Turn Arduino on/off
    else{
        int i = 0;
        while(Wire.available()){
            if(i <= byte_count)
                data[i++] = Wire.read();
        }
            pi.set_data(data);
    }
 
};

