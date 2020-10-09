#!/usr/bin/env python
# ----------------------------------------------------------------- #
#  File   : test_transmit_rgb.py
#  Author : peach
#  Date   : 14 Dec 2019
# ----------------------------------------------------------------- #

# This test script requires that the RF24 library be properly installed,
# as well as the RPi.GPIO library, but does not require any special
# virtual environment configuration in order to work.
#
# Just make sure you run it as root.
#
# Usage:
# $ sudo python3 test_transmit_rgb.py 0x03 123 043 255
#                                       ^   ^   ^   ^
#                                       |   |   |   |
# Last Address Byte---------------------+   |   |   |
# Red level --------------------------------+   |   |
# Green level ----------------------------------+   |
# Blue level ---------------------------------------+

import RF24
import RPi.GPIO as GPIO
import sys

# Target Levels
r = int(sys.argv[2])
g = int(sys.argv[3])
b = int(sys.argv[4])
rx_addr_last_byte = int(sys.argv[1], 16)

radio = RF24.RF24(RF24.RPI_BPLUS_GPIO_J8_15, RF24.RPI_BPLUS_GPIO_J8_24,
                  RF24.BCM2835_SPI_SPEED_8MHZ)

rx_addr = bytes([0xdc, 0x64, 0xb6, 0xe0, rx_addr_last_byte])

radio.begin()
radio.setRetries(15, 15)
radio.openWritingPipe(rx_addr)
radio.stopListening()

assert r <= 255 and r >= 0
assert g <= 255 and g >= 0
assert b <= 255 and b >= 0

# 3 corresponds to the "set rgb levels" command.
message = bytes([3, r, g, b])
radio.write(message)
print('Sending Message...')
print(message)
