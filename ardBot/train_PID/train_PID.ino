#include <QTRSensors.h>
#include <AFMotor.h>
#include <time.h>
#include <Line_PID.h>
#include <i2c_pi.h>
#include <Wire.h>

// Defining constant global variables
#define NUM_SENSORS             4  // number of sensors used
#define NUM_SAMPLES_PER_SENSOR  4  // average 4 analog samples per sensor reading
#define EMITTER_PIN             QTR_NO_EMITTER_PIN // emitter is controlled by digital pin 2
#define CALIBRATE_SPEED         200
#define BASE_SPEED              100

// Defining global variables

//Motors
AF_DCMotor m1(1);
AF_DCMotor m2(2);
//Line Sensors
QTRSensorsAnalog qtra((unsigned char[]) {0, 1, 2, 3},NUM_SENSORS, NUM_SAMPLES_PER_SENSOR, EMITTER_PIN);

//PID
float gains[] = {1.0,1.0,1.0}; //default gains
Line_PID pidL(m1,'L',BASE_SPEED,qtra,NUM_SENSORS,gains);
Line_PID pidR(m2,'R',BASE_SPEED,qtra,NUM_SENSORS,gains);
bool new_gains = false;

//I2C
i2c_pi pi= i2c_pi();
bool on = false;

void setup() {
  Wire.onReceive(receive_data);
  Serial.begin(9600);
    while(!on){
      on = pi.get_on();
      Serial.println("Arduino sleeping. Waiting to be turned on...");
      delay(1500);
    }
    
    pinMode(13, OUTPUT);
    digitalWrite(13, HIGH);

    calibrate_run();
    //calibrate_run();
    //calibrate_run();
    //calibrate_run(); 

    digitalWrite(13, LOW);
    

}

void loop() {
  
  while(pi.get_on() == false){
    Serial.println("Arduino was put to sleep. Waiting to be turned on...");
    m1.run(RELEASE);
    m2.run(RELEASE);
    delay(1500);
  }
  //update_gains();
  
  //unsigned int position = qtra.readLine(sensorValues);
  
 //for (unsigned char i = 0; i < NUM_SENSORS; i++)
 //{
    //Serial.print(sensorValues[i]);
    //Serial.print('\t');
 //}
  Serial.println("loop");
  //pidL.update();
  pidR.update();
  delay(1000);
}

void receive_data(int byte_count){
    Serial.println(byte_count);
    int * data = nullptr; //pi.get_data();
    Serial.println("in receive");
    if(data !=  nullptr){
        Serial.println("receiver");
        delete data;
        data = nullptr;
    }
    Serial.println(1);
    data = new int[byte_count];
    pi.set_operation(Wire.read()); // internal address read from Wire
    Serial.println(2);
    if (pi.get_operation() == 0x00){
        pi.set_on(Wire.read()==1); //Turn Arduino on/off
        while(Wire.available()){Wire.read();} //Empty bus
        Serial.println(3);}      
    else{
        new_gains = true;
        int pos = (sizeof( data ) / sizeof( data[0] ));
        int i = 0;
        Serial.println(4);
        while(Wire.available()){
            if(i <= byte_count)
                data[i++] = Wire.read();
        }
        pi.set_data(data);
        Serial.println(5);
    }
 
};


void calibrate_run(){
    m1.setSpeed(CALIBRATE_SPEED);
    m2.setSpeed(CALIBRATE_SPEED);
        
    m1.run(RELEASE);
    m2.run(RELEASE);

    m1.run(FORWARD);
    m2.run(BACKWARD);

    for (int i = 0; i < 50; i++)  // make the calibration take about 10 seconds
  {
    //qtra.calibrate();       // reads all sensors 10 times at 2.5 ms per six sensors (i.e. ~25 ms per call)
  }
    m1.run(RELEASE);
    m2.run(RELEASE);

};
void update_gains(){
  
  if(!new_gains){ 
    Serial.println(0);
    return;
    }
  int* data = pi.get_data();
  
  if((data!=nullptr)){
    int op = pi.get_operation();
    if(op==0x01){
      for(int i = 0; i < 3; i++){
        gains[i] = data[i];
      }
      Serial.println(1);
    }
    Serial.println(2);
  }
  pidL.set_gains(gains);
  Serial.println(3);
  pidR.set_gains(gains);
  new_gains = false;
  
};


