# ----------------------------------------------------------------- #
#  File   : _mock.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Fake functions to simulate GPIO behavior.
import tsl.util.log


def close():
    tsl.util.log.warn('MOCK - Closing serial connection.')


def initialize():
    tsl.util.log.warn('MOCK - Initializing Serial Connection.')


def set_led_levels(r, g, b):
    tsl.util.log.warn('MOCK - Setting RGB Levels to {} {} {}.'.format(r, g, b))


def set_fan_state(is_enabled):
    tsl.util.log.warn(
        'MOCK - Setting fan state to {}.'.format('ON' if is_enabled else 'OFF'))
