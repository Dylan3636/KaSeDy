#include "PID.h"

PID::PID(AF_DCMotor motor,char motorType, QTRSensorsAnalog qtra,float stupidGains[] ): motor{motor}, motorType{motorType}, qtra{qtra}{
      for (int i =0;i<3;i++){
        gains[i] = stupidGains[i];
      }
      
 }

int PID::update(unsigned int sensorValues[]){
      int t1 = t;
      unsigned int position = qtra.readLine(sensorValues);
      int t2 = millis();
      float deltaT = (float)(t2-t1)/1000;
      t=t2;
      int val =0;
      if (motorType == 'L'){
        val = sensorValues[4];
      }
      else{
        val = sensorValues[2];
      }
      int error = 0-val;
      int deltaError = val-prevVal;
      float derivVal = (float) deltaError/deltaT;
      prevVal = val;

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
