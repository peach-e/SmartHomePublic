/*
 ***********************************
    File   : RgbRFNode.ino
    Author : peach
    Date   : 14 Dec 2019
 ***********************************
*/

#define SERIAL_DEBUG 0
#define NUMBER_FADE_STEPS 255
#define FADE_STEP_INTERVAL 5

#include "Constants.h"
#include "Fader.h"
#include "PlantSystems.h"

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

const byte rxAddr[] = RF_ADDRESS_RGB_OFFICE_C;

/*
 * The radio, the light and the function to set its brightness.
 */
RF24 radio(PIN_RF_CE, PIN_RF_CSN);
LedLight* channelR;
LedLight* channelG;
LedLight* channelB;
void setLightBrightness(int);

void setup() {

  #if SERIAL_DEBUG
    while (!Serial);
    Serial.begin(9600);
    Serial.println("Debugging over Serial Active");
  #endif /*SERIAL_DEBUG*/

  channelR = new LedLight(PIN_LED_R);
  channelG = new LedLight(PIN_LED_G);
  channelB = new LedLight(PIN_LED_B);
  channelR->enable();
  channelG->enable();
  channelB->enable();
  setR(0);
  setG(0);
  setB(0);

  radio.begin();
  radio.openReadingPipe(0, rxAddr);
  radio.startListening();
}

void loop() {

  if (radio.available())
  {
    unsigned char messagePayload[RF_PAYLOAD_SIZE];
    radio.read(&messagePayload, sizeof(messagePayload));

    // Only do something if the first byte corresponds to a legit command. Currently,
    // byte 0 must be RF_CMD_SET_RGBLEVEL, and then byte 1,2,3 are the RGB levels.
    int command = int(messagePayload[0]);
    if (command != RF_CMD_SET_RGBLEVEL) {
      return;
    }

    int desiredR = int(messagePayload[1]);
    int desiredG = int(messagePayload[2]);
    int desiredB = int(messagePayload[3]);
    addFadeJob(channelR->getPower(), desiredR, NUMBER_FADE_STEPS, setR);
    addFadeJob(channelG->getPower(), desiredG, NUMBER_FADE_STEPS, setG);
    addFadeJob(channelB->getPower(), desiredB, NUMBER_FADE_STEPS, setB);

    #if SERIAL_DEBUG
      Serial.println(desiredR);
      Serial.println(desiredG);
      Serial.println(desiredB);
    #endif /*SERIAL_DEBUG*/
  }

  while (fade_DEPRECATED()) {
    delay(FADE_STEP_INTERVAL);
  }
}

void setR(int lvl) {
  channelR->setPower(lvl);
}

void setG(int lvl) {
  channelG->setPower(lvl);
}

void setB(int lvl) {
  channelB->setPower(lvl);
}
