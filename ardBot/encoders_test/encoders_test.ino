#include <Wire.h>
#include <Wheel_Encoders.h>
#include <Motor_Control.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor * m1 = AFMS.getMotor(1);
Adafruit_DCMotor * m2 = AFMS.getMotor(2);
int ind_1 = 2;
int ind_2 = 4;
int ind_3 = 3;
int ind_4 = 5;
Wheel_Encoders we = Wheel_Encoders(ind_1, ind_2, ind_3, ind_4);
Motor_Control mc = Motor_Control(m1, m2);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin(0x04);
  AFMS.begin();
  Wire.onRequest(request_data);
  Serial.println("Beginning Encoder Test...");
  mc.forward_forever(150);
  mc.halt();
  //pinMode(0,INPUT);
  //pinMode(1,INPUT);
  //pinMode(2,INPUT);
  //pinMode(3,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("Motor 1: ");
  //Serial.println(we.get_m1_clicks());
  //Serial.print(digitalRead(ind_1));
  //Serial.print('\t');
  //Serial.println(digitalRead(ind_2));
    
    
  //Serial.print("Motor 2: ");
  //Serial.println(we.get_m2_clicks());
  //Serial.print(digitalRead(ind_3));
  //Serial.print('\t');
  //Serial.println(digitalRead(ind_4));
    
    
  delay(1000);
}

void request_data(){
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

