#include <i2c_pi.h>
#include <Motor_Control.h>
#include <Adafruit_MotorShield.h>

#define DEFAULT_SPEED 100

i2c_pi pi = i2c_pi();
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *m1 = AFMS.getMotor(1);
Adafruit_DCMotor *m2 = AFMS.getMotor(2); 
Motor_Control motors = Motor_Control(m1,m2);
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
  pi.command_motors(data, motors, DEFAULT_SPEED);
  
  delay(500);
}
void receive_data(int byte_count){
    pi.receive_data(byte_count);
    
 
};

