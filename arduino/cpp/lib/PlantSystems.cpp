/*
 **********************************************************************
 *  File   : PlantSystems.cpp
 *  Author : peach
 *  Date   : 28 Feb 2019
 **********************************************************************
 */

#include "Constants.h"
#include "Arduino.h"
#include "PlantSystems.h"

Fan::Fan(int pin) {
    _pin = pin;
    pinMode(_pin, OUTPUT);
    disable();
}

bool Fan::isEnabled() {
    return _isEnabled;
}

void Fan::enable() {
    digitalWrite(_pin, HIGH);
    _isEnabled = TRUE;
}

void Fan::disable() {
    digitalWrite(_pin, LOW);
    _isEnabled = FALSE;
}

LedLight::LedLight(int pin) {
    _pin = pin;
    _power = 0;

    pinMode(_pin, OUTPUT);
    disable();
}

bool LedLight::isEnabled() {
    return _isEnabled;
}

void LedLight::enable() {
    analogWrite(_pin, _power);
    _isEnabled = TRUE;
}

void LedLight::disable() {
    analogWrite(_pin, 0);
    _isEnabled = FALSE;
}

int LedLight::getPower() {
    return _power;
}

void LedLight::setPower(int power) {
    _power = power;
    if (_isEnabled) {
        analogWrite(_pin, _power);
    }
}
