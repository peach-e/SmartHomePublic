# ----------------------------------------------------------------- #
#  File   : _mock.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Fake functions to simulate GPIO behavior.

import tsl.configuration
import tsl.util.log

GPIO_PIN_GROW_LIGHTS = tsl.configuration.val('GPIO_PIN_RB_LIGHT')


def _initialize():
    # Pin number in BCM notation.
    tsl.util.log.warn('MOCK - Setting pin {} to OUTPUT.'.format(GPIO_PIN_GROW_LIGHTS))


def set_grow_lights(state):
    state_str = "ON" if state else "OFF"
    message = 'MOCK - Turning {} pin {}.'.format(state_str, GPIO_PIN_GROW_LIGHTS)
    tsl.util.log.warn(message)

_initialize()
