#include <Wire.h>

#define SLAVE_ADDRESS 0x04
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
  Serial.println(Wire.available());
  delay(1000);
}

void receiveData(int byteCount){
  while(Wire.available()){
    int number = Wire.read();
    Serial.print("data received: ");
    Serial.println(number);
  }
}

void sendData(int number){
  Wire.write(number);
}

