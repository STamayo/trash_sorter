#include <Arduino.h>
#include <hd44780.h>
#include <Servo.h>

// rest positions of the servos
#define servo1_rest 75 
#define servo2_rest 85 

// put function declarations here:
void servo_calc(int bin);
void next_state(int current, int input);

Servo servo1;
Servo servo2;

int current_state = 0; // start at neutral
int command;
const int pres = A0;
const int led = 2;
const int reset = 12;
const int trash = 10;
const int compost = 11;
const int recycle = 13;
int light_value = 0;

unsigned long int start_time;


void setup() {
  Serial.begin(9600);
  servo1.attach(5);
  servo2.attach(6);
  // put your setup code here, to run once:

  pinMode(led, OUTPUT);
  pinMode(pres, INPUT);  //set A0 as an input pin;
  pinMode(reset, INPUT); // reset button

  pinMode(recycle, INPUT);
  pinMode(trash, INPUT);
  pinMode(compost, INPUT);

  Serial.begin(9600);
  servo1.write(servo1_rest);
  servo2.write(servo2_rest);

  start_time = millis();
}


void loop() {
  if (Serial.available()) {
    command = Serial.readString().toInt();
    next_state(current_state, command);
  }

  if (current_state == 1) {
    servo_calc(command);
    current_state = 0;
  }

  if (digitalRead(reset)) {
    servo1.write(servo1_rest);
    servo2.write(servo2_rest);
  }

  if (millis() - start_time >= 2000) {
    light_value = analogRead(pres);
    Serial.write(light_value);
    start_time = millis();
  }

  if (digitalRead(recycle)) {
    servo1.write(servo1_rest + 36); // recycle
    servo2.write(servo2_rest + 53);
  } 

  if (digitalRead(trash)) {
    servo1.write(servo1_rest - 52); // trash
    servo2.write(servo2_rest);
  }

  if (digitalRead(compost)) {
    servo1.write(servo1_rest + 65); // compost
    servo2.write(servo2_rest - 85);
  }



  // if (digitalRead(13)) {
  //   servo1.write(servo1.read() + 1);

  // }
  // if (digitalRead(12)) {
  //   servo1.write(servo1.read() - 1);
}


void servo_calc(int bin) {
  switch(bin) {
    case 1: // trash
      servo1.write(servo1_rest - 52); // trash
      servo2.write(servo2_rest);
      break;
    case 0: // compost 
      servo1.write(servo1_rest + 65); // compost
      servo2.write(servo2_rest - 85);
      break;
    case 2: // recycle
      servo1.write(servo1_rest + 36); // recycle
      servo2.write(servo2_rest + 53);
      break;
    default:
     servo1.write(servo1_rest);
     servo2.write(servo2_rest);
     break;
  }
  delay(3000);
  servo1.write(servo1_rest);
  servo2.write(servo2_rest);
}

void next_state(int current, int input) {
  if (current == 0) { // in neutral
    if (input != 255) { // if input updates, state = 1 (change pos)
      current = 1;
    } // else stay neutral
  }
}