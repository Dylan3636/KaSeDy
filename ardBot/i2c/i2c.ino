#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define GO_ADDRESS 0x00

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);

  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  Serial.println("Ready!");
}

void loop() {
  // put your main code here, to run repeatedly:
//  if(Wire.available()){
//    Serial.println();
//    delay(1000);
//  }
}

void receiveData(int byteCouent){
  while(Wire.available()){
    int internal_addr = Wire.read();
    int number = Wire.read();
    Serial.print("data received from ");
    Serial.print(internal_addr);
    Serial.print(": ");
    Serial.println(number);
  }
}

void sendData(int number){
  Wire.write(number);
}

