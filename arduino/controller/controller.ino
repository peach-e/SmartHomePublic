/*
 ***********************************
    File   : controller.ino
    Author : peach
    Date   : 15 July 2019
 ***********************************
*/

#include "Constants.h"
#include "Comms.h"
#include "Fader.h"
#include "PlantSystems.h"

#define NUMBER_FADE_STEPS 255
#define FADE_STEP_INTERVAL 5

byte command[COMMAND_ARRAY_SIZE];
int deviceId = 0;
int commandSize = 0;

Fan* fan;
LedLight* ledR;
LedLight* ledG;
LedLight* ledB;

void fadeR(int);
void fadeG(int);
void fadeB(int);

void setup() {
  fan  = new Fan(PIN_FAN);
  ledR = new LedLight(PIN_LED_R);
  ledG = new LedLight(PIN_LED_G);
  ledB = new LedLight(PIN_LED_B);

  ledR->enable();
  ledG->enable();
  ledB->enable();

  setupSerial();
}

void loop() {

  // Wait till we have a command, then process it.
  getCommand(deviceId, commandSize, command);

  switch (deviceId) {
    case DEVICE_ID_FAN:
      // The only argument for command is 0x01 if you want it on
      // or 0x00 to turn off.
      command[0] ? fan->enable() : fan->disable();
      break;
    case DEVICE_ID_LED:
      // LED commands expect RGB values on 0-255
      addFadeJob(ledR->getPower(), command[0], NUMBER_FADE_STEPS, fadeR);
      addFadeJob(ledG->getPower(), command[1], NUMBER_FADE_STEPS, fadeG);
      addFadeJob(ledB->getPower(), command[2], NUMBER_FADE_STEPS, fadeB);
      break;
  }

  while (fade_DEPRECATED()) {
    delay(FADE_STEP_INTERVAL);
  }
  return 1;
}

void fadeR(int lvl) {
  ledR->setPower(lvl);
}

void fadeG(int lvl) {
  ledG->setPower(lvl);
}

void fadeB(int lvl) {
  ledB->setPower(lvl);
}
