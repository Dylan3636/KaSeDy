#include <QTRSensors.h>
#include <AFMotor.h>
#include <time.h>
#include <PID.h>
#include <i2c_pi.h>
#include <Wire.h>

AF_DCMotor m1(1);
AF_DCMotor m2(2);


#define NUM_SENSORS             4  // number of sensors used
#define NUM_SAMPLES_PER_SENSOR  4  // average 4 analog samples per sensor reading
#define EMITTER_PIN             QTR_NO_EMITTER_PIN // emitter is controlled by digital pin 2


QTRSensorsAnalog qtra((unsigned char[]) {0, 1, 2, 3, 4}, 
  NUM_SENSORS, NUM_SAMPLES_PER_SENSOR, EMITTER_PIN);
unsigned int sensorValues[NUM_SENSORS];

float gains[] = {1.0,1.0,1.0};
PID pidL(m1,'L',qtra,gains);
i2c_pi pi= i2c_pi();
bool on = false;

void setup() {
  Wire.onReceive(receive_data);
  //Wire.onRequest(send_data);
    while(!on){
      on = pi.get_on();
      delay(50);
    }
    
    Serial.begin(9600);
    pinMode(13, OUTPUT);
    digitalWrite(13, HIGH);

    m1.setSpeed(175);
    m2.setSpeed(175);
        
    m1.run(RELEASE);
    m2.run(RELEASE);

    m1.run(FORWARD);
    m2.run(BACKWARD);

    for (int i = 0; i < 50; i++)  // make the calibration take about 10 seconds
  {
    qtra.calibrate();       // reads all sensors 10 times at 2.5 ms per six sensors (i.e. ~25 ms per call)
  }
    m1.run(RELEASE);
    m2.run(RELEASE);

    m2.run(FORWARD);
    m1.run(BACKWARD);

    for (int i = 0; i < 50; i++)  // make the calibration take about 10 seconds
  {
    qtra.calibrate();       // reads all sensors 10 times at 2.5 ms per six sensors (i.e. ~25 ms per call)
  }
    m1.run(RELEASE);
    m2.run(RELEASE);

    m1.setSpeed(200);
    m2.setSpeed(200);
        
    m1.run(RELEASE);
    m2.run(RELEASE);

    m1.run(FORWARD);
    m2.run(BACKWARD);

    for (int i = 0; i < 50; i++)  // make the calibration take about 10 seconds
  {
    qtra.calibrate();       // reads all sensors 10 times at 2.5 ms per six sensors (i.e. ~25 ms per call)
  }
    m1.run(RELEASE);
    m2.run(RELEASE);

    m2.run(FORWARD);
    m1.run(BACKWARD);

    for (int i = 0; i < 50; i++)  // make the calibration take about 10 seconds
  {
    qtra.calibrate();       // reads all sensors 10 times at 2.5 ms per six sensors (i.e. ~25 ms per call)
  }
    m1.run(RELEASE);
    m2.run(RELEASE);
    

    digitalWrite(13, LOW);
    

}

void loop() {
  while(on == false){
    bool on = pi.get_on();
  }
  int* data = pi.get_data();
  
  if((data!=nullptr)){
    int op = pi.get_operation();
    if(op==0x01){
      for(int i = 0; i < 3; i++){
        gains[i] = data[i];
      }
    }
  }
  unsigned int position = qtra.readLine(sensorValues);
 for (unsigned char i = 0; i < NUM_SENSORS; i++)
  {
    //Serial.print(sensorValues[i]);
    //Serial.print('\t');
  }
  //Serial.println(); // uncomment this line if you are using raw values
  //Serial.println(position); // comment this line out if you are using raw values
  pidL.update(sensorValues);
  delay(1000);
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
                data[i++] = Wire.read();
        }
    }
    pi.set_data(data);
};

void send_data(int number){

};



