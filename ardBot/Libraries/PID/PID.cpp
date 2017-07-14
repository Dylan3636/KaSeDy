#include "PID.h"

PID::PID(float stupidGains[] ){
      for (int i =0;i<3;i++){
        gains[i] = stupidGains[i];
      }
      
 }
 void PID::set_gains(float new_gains[]){
 	 for (int i =0;i<3;i++){
        gains[i] = new_gains[i];
      }
 }

float PID::update(int reading){
      int t1 = t;
      int t2 = millis();
      float deltaT = (float)(t2-t1)/1000;
      t=t2;
      int error = 0-reading;
      int deltaError = reading - previous_reading;
      float derivVal = (float) deltaError/deltaT;
      previous_reading = reading;

      integralPos=(integralPos+1)%10;
      integralValues[integralPos] = error;
      
      int integralSum=0;
      
      for (int i = 0; i < WINDOW; i++){
          integralSum = integralSum + integralValues[i];
      }
      Serial.print(error);
      Serial.print('\t');

      Serial.print(derivVal);
      Serial.print('\t');

      Serial.print(integralSum);
      Serial.print('\t');

      Serial.println(NULL);
      return gains[0]*error + gains[1]*derivVal + gains[2]*integralSum;
}
