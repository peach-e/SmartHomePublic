# ----------------------------------------------------------------- #
#  File   : __init__.py
#  Author : peach
#  Date   : 20 July 2019
# ----------------------------------------------------------------- #

# Provide the interface for LED Fan Control.

import tsl.configuration
import tsl.util.log

import serial

USE_MOCK = tsl.configuration.val('USE_MOCK_LEDFAN')
if USE_MOCK:
    from tsl.hardware.ledfan import _mock as _platform
else:
    from tsl.hardware.ledfan import _arduino as _platform


def close():
    _platform.close()


def initialize():
    _platform.initialize()


def set_led_levels(r, g, b):
    _platform.set_led_levels(r, g, b)


def set_fan_state(is_enabled):
    _platform.set_fan_state(is_enabled)
