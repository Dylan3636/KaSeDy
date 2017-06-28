#include <QTRSensors.h>
#include <AFMotor.h>
#include <time.h>
#include <PID.h>

AF_DCMotor m1(1);
AF_DCMotor m2(2);


#define NUM_SENSORS             5  // number of sensors used
#define NUM_SAMPLES_PER_SENSOR  4  // average 4 analog samples per sensor reading
#define EMITTER_PIN             QTR_NO_EMITTER_PIN // emitter is controlled by digital pin 2


QTRSensorsAnalog qtra((unsigned char[]) {0, 1, 2, 3, 4, 5}, 
  NUM_SENSORS, NUM_SAMPLES_PER_SENSOR, EMITTER_PIN);
unsigned int sensorValues[NUM_SENSORS];

const float gains[] = {1.0,1.0,1.0};
PID pidL(m1,'L',qtra,gains);

void setup() {
    delay(500);
    int val = 0;
    while (val==0){
      val = Serial.read();
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
  // put your main code here, to run repeatedly:
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


