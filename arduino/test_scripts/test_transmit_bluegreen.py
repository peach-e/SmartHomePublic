#!/usr/bin/env python

# This test script requires that the RF24 library be properly installed, as well as the RPi.GPIO library,
# but does not require any special virtual environment configuration in order to work.
#
# Just make sure you run it as root.
#
# Usage:
# $ sudo python3 test_transmit_blue_green.py 223


import RF24
import RPi.GPIO as GPIO
import sys

target_brightness = int(sys.argv[1])

radio = RF24.RF24(RF24.RPI_BPLUS_GPIO_J8_15, RF24.RPI_BPLUS_GPIO_J8_24,
                  RF24.BCM2835_SPI_SPEED_8MHZ)

# Last byte should be 0x01 for blue, 0x02 for green.
rx_addr = bytes([0xdc, 0x64, 0xb6, 0xe0, 0x01])

radio.begin()
radio.setRetries(15, 15)
radio.openWritingPipe(rx_addr)
radio.stopListening()

assert target_brightness <= 255 and target_brightness >= 0
message = bytes([target_brightness])
radio.write(message)
print('Sending Message...')
print(message)
