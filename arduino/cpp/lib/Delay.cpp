/*
 **********************************************************************
 *  File   : Delay.cpp
 *  Author : peach
 *  Date   : 4 May 2020
 **********************************************************************
 */

#include "Arduino.h"
#include "Delay.h"


NonBlockingDelay::NonBlockingDelay(int milliseconds) {
  reset(milliseconds);
}

bool NonBlockingDelay::isExpired() {
  long int currentTime = millis();

  // timer is expired if the current time is longer than target time
  // OR shorter than initial time. This is to catch the wraparound case.
  if ((currentTime > _targetTime) || (currentTime < _initialTime)) {
    return true;
  }

  return false;
}

void NonBlockingDelay::reset(int milliseconds) {
  _countdownTime = milliseconds;
  _initialTime = millis();
  _targetTime = _initialTime + _countdownTime;
}

void NonBlockingDelay::reset() {
  reset(_countdownTime);
}