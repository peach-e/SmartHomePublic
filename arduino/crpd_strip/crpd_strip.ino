/*******************************
   File:   crpd_strip.ino
   Author: peach
   Date:   4 May 2020
 *******************************/

#define NUMBER_FADE_STEPS 64
#define FADE_STEP_INTERVAL 20

#define I2C_ADDRESS I2C_ADDRESS_STRIP_1

#include "Constants.h"
#include "Delay.h"
#include "SoftwarePWM.h"
#include "Fader.h"

#include <TinyWire.h>

// Setup LEDs
DigitalPWM ledR(PIN_LED_R);
DigitalPWM ledG(PIN_LED_G);
DigitalPWM ledB(PIN_LED_B);
NonBlockingDelay fadeStepTimer(FADE_STEP_INTERVAL);

void setup() {
  TinyWire.begin(I2C_ADDRESS);
  TinyWire.onReceive(receiveEvent);
}

void receiveEvent(int bytes) {

  // We expect there to be 4 bytes. If there aren't, then waste the read operation.
  if (bytes != 4) {
    while (TinyWire.available()) TinyWire.read();
    return;
  }

  int r = TinyWire.read();
  int g = TinyWire.read();
  int b = TinyWire.read();
  TinyWire.read();

  // Request red to fade to the new value.
  addFadeJob(ledR.getPower(), r, NUMBER_FADE_STEPS, [](int p) {
    ledR.setPower(p);
  });
  addFadeJob(ledG.getPower(), g, NUMBER_FADE_STEPS, [](int p) {
    ledG.setPower(p);
  });
  addFadeJob(ledB.getPower(), b, NUMBER_FADE_STEPS, [](int p) {
    ledB.setPower(p);
  });
}

void loop() {
  if (fadeStepTimer.isExpired()) {
    fade();
    fadeStepTimer.reset();
  }

  ledR.step();
  ledG.step();
  ledB.step();
}
