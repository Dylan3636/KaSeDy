#include <Wire.h>
#include <Wheel_Encoders.h>
#include <Motor_Control.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor * m1 = AFMS.getMotor(1);
Adafruit_DCMotor * m2 = AFMS.getMotor(2);

Wheel_Encoders we = Wheel_Encoders(2, 1, 3, 7);
Motor_Control mc = Motor_Control(m1, m2);



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  AFMS.begin();
  Serial.println("Beginning Encoder Test...");
  //mc.forward_forever(100);
  //pinMode(0,INPUT);
  //pinMode(1,INPUT);
  //pinMode(2,INPUT);
  //pinMode(3,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("Motor 1: ");
  Serial.println(we.get_m1_clicks());
  //Serial.print(digitalRead(0));
  //Serial.print('\t');
  //Serial.println(digitalRead(1));
    
    
  Serial.print("Motor 2: ");
  Serial.println(we.get_m2_clicks());
  //Serial.print(digitalRead(2));
  //Serial.print('\t');
  //Serial.println(digitalRead(3));
    
    
  delay(1000);
}

