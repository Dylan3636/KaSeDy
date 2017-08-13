#ifndef Wheel_Encoders_H_
#define Wheel_Encoders_H_

class Wheel_Encoders{
public:
	Wheel_Encoders(unsigned int m1A, unsigned int m1B, unsigned int m2A, unsigned int m2B);
	static int get_m1_clicks();
	static int get_m2_clicks();
	static int* get_clicks();
	static void update();
};
#endif