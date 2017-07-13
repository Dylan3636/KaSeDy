#include <i2c_pi.h>
#include <Motor_Control.h>

i2c_pi pi = i2c_pi();
Motor_Control motors = Motor_Control(1,2) ;
bool on = false;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
    Wire.onReceive(receive_data);
    while(!on){
      on = pi.get_on();
      Serial.println("setup");
      delay(500);
    }

}

void loop() {
  while(on == false){
    on = pi.get_on();
    Serial.println(on);
    delay(500);
  }

  int* data = pi.get_data();
  //Serial.println(data[]);
  if((data!=nullptr)){
    int op = pi.get_operation();
    //Serial.println(op);
    if(op==0x02){
        int action = data[0];

        switch(action) {
          case 0: motors.halt();break;
          case 1: motors.forward_forever(150); break;
          case 2: motors.turn_anticlockwise_forever(150); break;
          case 3: motors.turn_clockwise_forever(150); break;
          case 4: motors.backward_forever(150); break;
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

    if (pi.get_operation() == 0x00)
        pi.set_on(Wire.read()==1);          //Turn Arduino on/off
    else{
        int pos = (sizeof( data ) / sizeof( data[0] ));
       // if(pos <= byte_count)
       //    data[pos] = operation;
        int i = 0;
        while(Wire.available()){
            if(i <= byte_count)
                Serial.println(data[i]);
                data[i++] = Wire.read();
        }
    }
    pi.set_data(data);
    Serial.println(pi.get_operation());
    Serial.println(pi.get_on());
};

