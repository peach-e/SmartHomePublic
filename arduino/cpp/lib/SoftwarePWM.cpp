/*
 **********************************************************************
 *  File   : SoftwarePWM.cpp
 *  Author : peach
 *  Date   : 4 May 2020
 **********************************************************************
 */

#include "Arduino.h"
#include "SoftwarePWM.h"

#define MAX_DUTY_CYCLE 63

DigitalPWM::DigitalPWM(int pin) {
  _pin = pin;
  _dutyCycle = 0;
  _count = 0;
  pinMode(_pin, OUTPUT);
  digitalWrite(_pin, LOW);
}

DigitalPWM::~DigitalPWM() {
  digitalWrite(_pin, LOW);
}

void DigitalPWM::setPower(unsigned char power) {
  power >>= 2;
  _dutyCycle = power  > MAX_DUTY_CYCLE ? MAX_DUTY_CYCLE :
               power < 0 ? 0 :
               power;
}

int DigitalPWM::getPower() {
  return _dutyCycle;
}

void DigitalPWM::step() {
  // If counter is less than duty cycle, turn pin on.
  if (_count < _dutyCycle) {
    digitalWrite(_pin, HIGH);
  } else {
    digitalWrite(_pin, LOW);
  }

  // Increase count and loop around if at max duty cycle.
  _count = _count == MAX_DUTY_CYCLE - 1 ? 0 : _count + 1;
}
