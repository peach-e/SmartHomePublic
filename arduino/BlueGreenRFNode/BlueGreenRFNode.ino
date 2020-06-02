/************************************
    File   : BlueGreenRFNode.ino
    Author : peach
    Date   : 11 Nov 2019
 ************************************/

#define SERIAL_DEBUG 0
#define NUMBER_FADE_STEPS 255
#define FADE_STEP_INTERVAL 5

#include "Constants.h"
#include "Fader.h"
#include "PlantSystems.h"

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

const byte rxAddr[] = RF_ADDRESS_GREEN;

/*
 * The radio, the light and the function to set its brightness.
 */
RF24 radio(PIN_RF_CE, PIN_RF_CSN);
LedLight* lightBar;
void setLightBrightness(int);

void setup() {

  #if SERIAL_DEBUG
    while (!Serial);
    Serial.begin(9600);
    Serial.println("Debugging over Serial Active");
  #endif /*SERIAL_DEBUG*/

  lightBar = new LedLight(PIN_LIGHT_STRIP);
  lightBar->enable();
  setLightBrightness(0);

  radio.begin();
  radio.openReadingPipe(0, rxAddr);
  radio.startListening();
}

void loop() {

  if (radio.available())
  {
    unsigned char messagePayload[RF_PAYLOAD_SIZE];
    radio.read(&messagePayload, sizeof(messagePayload));

    int desiredBrightness = int(messagePayload[0]);
    addFadeJob(lightBar->getPower(), desiredBrightness, NUMBER_FADE_STEPS, setLightBrightness);

    #if SERIAL_DEBUG
      Serial.println(desiredBrightness);
    #endif /*SERIAL_DEBUG*/
  }

  while (fade_DEPRECATED()) {
    delay(FADE_STEP_INTERVAL);
  }
}

void setLightBrightness(int lvl) {
  lightBar->setPower(lvl);
}
