#include "Wheel_Encoders.h"
#include <Arduino.h>
#include <Adafruit_MotorShield.h>



static int	m1_clicks;
static int	m2_clicks;

static Adafruit_DCMotor * m1;
static Adafruit_DCMotor * m2;
static int prev_clicks;
static bool record_1;
static bool record_2;
static bool check_1;
static bool check_2;
static int click_diff_1;
static int click_diff_2;


static unsigned int m1A_pin;
static unsigned int m1B_pin;
static unsigned int m2A_pin;
static unsigned int m2B_pin;
		
static unsigned char	m1A_prev_val;
static unsigned char	m1B_prev_val;
static unsigned char	m2A_prev_val;
static unsigned char	m2B_prev_val;

	void Wheel_Encoders::update(){
		unsigned char m1A_val = digitalRead(m1A_pin) == HIGH;
		unsigned char m1B_val = digitalRead(m1B_pin) == HIGH;
		unsigned char m2A_val = digitalRead(m2A_pin) == HIGH;
		unsigned char m2B_val = digitalRead(m2B_pin) == HIGH;

		char m1_plus = m1A_val ^ m1B_prev_val;
		char m1_minus = m1B_val ^ m1A_prev_val;
		char m2_plus = m2A_val ^ m2B_prev_val;
		char m2_minus = m2B_val ^ m2A_prev_val;

		m1_clicks += m1_plus;
		m1_clicks -= m1_minus;
		m2_clicks += m2_plus;
		m2_clicks -= m2_minus;
		
		m1A_prev_val = m1A_val;
		m1B_prev_val = m1B_val;
		m2A_prev_val = m2A_val;
		m2B_prev_val = m2B_val;

		if(record_1){
			prev_clicks = get_m1_clicks();
			record_1 = false;
			check_1 = true;
		}

		if(record_2){
			prev_clicks = get_m2_clicks();
			record_2 = false;
			check_2 = true;
		}
		if(check_1){
			if(prev_clicks-get_m1_clicks() >= click_diff_1){
				m1 -> run(RELEASE);
				check_1 = false;
			}
		}

		if(check_2){
			if(get_m2_clicks()-get_m2_clicks() >= click_diff_2){
				m2 -> run(RELEASE);
				check_2 = false;
			}
		}


		

	}

	Wheel_Encoders::Wheel_Encoders(unsigned int m1A, unsigned int m1B, unsigned int m2A, unsigned int m2B){

		m1A_pin = m1A;
		m1B_pin = m1B;
		m2A_pin = m2A;
		m2B_pin = m2B;

		pinMode(m1A_pin, INPUT);
		pinMode(m1B_pin, INPUT);
		pinMode(m2A_pin, INPUT);
		pinMode(m2B_pin, INPUT);

		m1_clicks = 0;
		m2_clicks = 0;

		m1A_prev_val = digitalRead(m1A_pin) == HIGH;
		m1B_prev_val = digitalRead(m1B_pin) == HIGH;
		m2A_prev_val = digitalRead(m2A_pin) == HIGH;
		m2B_prev_val = digitalRead(m2B_pin) == HIGH;


		
		attachInterrupt(digitalPinToInterrupt(m1A_pin),update,CHANGE);
		//attachInterrupt(digitalPinToInterrupt(m1B_pin),update,CHANGE);
		attachInterrupt(digitalPinToInterrupt(m2A_pin),update,CHANGE);
		//attachInterrupt(digitalPinToInterrupt(m2B_pin),update,CHANGE);

		record_1 = false;
		record_2 = false;

	}

	int* Wheel_Encoders::get_clicks(){
		int* clicks = new int[2];
		cli();
		clicks[0] = m1_clicks;
		clicks[1] = m2_clicks;
		sei();
		return clicks;
	}

	int Wheel_Encoders::get_m1_clicks(){
		cli();
		int tmp = m1_clicks;
		sei();
		return tmp;
	}

	int Wheel_Encoders::get_m2_clicks(){
		cli();
		int tmp = m2_clicks;
		sei();
		return tmp;
	}