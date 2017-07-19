#include "Wheel_Encoders.h"
#include <Arduino.h>



static int	m1_clicks;
static int	m2_clicks;

static unsigned int m1A_pin;
static unsigned int m1B_pin;
static unsigned int m2A_pin;
static unsigned int m2B_pin;
		
static unsigned char	m1A_prev_val;
static unsigned char	m1B_prev_val;
static unsigned char	m2A_prev_val;
static unsigned char	m2B_prev_val;

	void update(){
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
		m2A_prev_val = m1A_val;
		m2B_prev_val = m2B_val;
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


		
		attachInterrupt(digitalPinToInterrupt(m1A_pin),update,RISING);
		//attachInterrupt(digitalPinToInterrupt(m1B_pin),update,RISING);
		attachInterrupt(digitalPinToInterrupt(m2A_pin),update,RISING);
		//attachInterrupt(digitalPinToInterrupt(m2B_pin),update,RISING);

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