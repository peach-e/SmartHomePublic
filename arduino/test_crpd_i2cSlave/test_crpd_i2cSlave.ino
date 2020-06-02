/*******************************
   File:   test_crpd_i2cSlave.ino
   Author: peach
   Date:   4 May 2020
 *******************************/

/*
   This sketch is intended to be used on an Arduino
   Nano to test that the I2C Protocol is working and to
   practise some of the behavior that we're going to
   be seeing on the ATTiny85.

   Usage
   1. Program ESP8266 with the crpd_server sketch.
   2. Program the nano with this sketch.
        TIP: use the --preferences-file flag when starting Arduino IDE so that you can save the
             various config settings for each of the boards you're working with.
   3. Wire up the nano and ESP8266 accordingly:

       SIGNAL NANO     ESP8266     CIRCUIT
       ------ ----     -------     -------
       Vcc    Vin      VBat        Vcc (5V)
       SDA    A4       4
       SCL    A5       5
       GND    GND      GND

   4. Power on the Nano.
   5. In a web browser, execute the RESTful command to change the RGB state.

          let setLevels = (strip,r,g,b) => {
            const url = "http://192.168.0.45/LED/" + strip;
            const xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "POST", url, false );
            xmlHttp.send( JSON.stringify({r:r,g:g,b:b}) );
            return xmlHttp.responseText;
          }

   6. Run it with setLevels(9,0,0,0), making note of the I2C address of your arduino.
      The red level should fade to whatever level you set in the red channel.

*/

// Include the required Wire library for I2C
#include <Wire.h>
#include <Delay.h>
#include <SoftwarePWM.h>
#include <Fader.h>

#define NUMBER_FADE_STEPS 255
#define FADE_STEP_INTERVAL 5

DigitalPWM led(13);
NonBlockingDelay fadeStepTimer(FADE_STEP_INTERVAL);

void setLedPower_cb(int power) {
  led.setPower(power);
}

void setup() {
  Wire.begin(9);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);
}

void receiveEvent(int bytes) {
  Serial.print("Received: ");
  Serial.println(bytes);

  // We expect there to be 4 bytes. If there aren't, then waste the read operation.
  if (bytes != 4) {
    while (Wire.available()) Wire.read();
    return;
  }

  int r = Wire.read();    // read one character from the I2C
  int g = Wire.read();
  int b = Wire.read();
  Wire.read();

  Serial.println("Got " + String(r) + " " + String(g) + " " + String(b));

  // Request red to fade to the new value.
  int oldValue = led.getPower();
  addFadeJob(oldValue, r, NUMBER_FADE_STEPS, setLedPower_cb);
}

void loop() {
  if (fadeStepTimer.isExpired()) {
    fade();
    fadeStepTimer.reset();
  }

  led.step();
}
