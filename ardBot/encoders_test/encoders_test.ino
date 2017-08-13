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
  AFMS.begin();
  Serial.println("Beginning Encoder Test...");
  mc.forward_forever(200);
  mc.halt();
  //pinMode(0,INPUT);
  //pinMode(1,INPUT);
  //pinMode(2,INPUT);
  //pinMode(3,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("Motor 1: ");
  Serial.println(we.get_m1_clicks());
  //Serial.print(digitalRead(ind_1));
  //Serial.print('\t');
  //Serial.println(digitalRead(ind_2));
    
    
  //Serial.print("Motor 2: ");
  Serial.println(we.get_m2_clicks());
  //Serial.print(digitalRead(ind_3));
  //Serial.print('\t');
  //Serial.println(digitalRead(ind_4));
    
    
  delay(1000);
}

