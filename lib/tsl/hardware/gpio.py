# ----------------------------------------------------------------- #
#  File   : gpio.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Functions to control pins on RPi GPIO

import tsl.configuration
import tsl.util.log

import time

USE_MOCK = tsl.configuration.val('USE_MOCK_GPIO')
if USE_MOCK:
    from tsl.hardware.mocks import GPIO
else:
    import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_PIN_GROW_LIGHTS = tsl.configuration.val('GPIO_PIN_RB_LIGHT')


def _initialize():
    # Pin number in BCM notation.
    tsl.util.log.info(
        '{} - Setting pin {} to OUTPUT.'.format(time.asctime(), GPIO_PIN_GROW_LIGHTS))
    GPIO.setup(GPIO_PIN_GROW_LIGHTS, GPIO.OUT)


def set_grow_lights(state):
    state_str = "ON" if state else "OFF"
    message = '{} - Turning {} pin {}.'.format(time.asctime(), state_str, GPIO_PIN_GROW_LIGHTS)
    tsl.util.log.info(message)
    GPIO.output(GPIO_PIN_GROW_LIGHTS, state)

_initialize()
