# ----------------------------------------------------------------- #
#  File   : _mock.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Fake functions to simulate RF24

import tsl.constants
import tsl.util.log


def _assert_byte(value):
    assert value >= 0
    assert value <= 255
    assert type(value) is int


def _initialize():
    tsl.util.log.warn('MOCK - Setting up RF24 Radio.')


def _set_discrete_level(l):
    try:
        _assert_byte(l)
    except AssertionError:
        tsl.util.log.error(
            'Invalid light level. Not integer between 0 and 255.')
        return 0
    return 1


def _set_rgb_level(r, g, b):

    try:
        _assert_byte(r)
        _assert_byte(g)
        _assert_byte(b)

    except AssertionError:
        tsl.util.log.error(
            'Invalid light level. Not integer between 0 and 255.')
        return 0

    return 1


def set_blue_level(level):

    if _set_discrete_level(level):
        tsl.util.log.warn('MOCK - Setting Blue Light to {}'.format(level))


def set_green_level(level):

    if _set_discrete_level(level):
        tsl.util.log.warn('MOCK - Setting Green Light to {}'.format(level))


def set_rgb_bedroom_level(r, g, b):
    if _set_rgb_level(r, g, b):
        tsl.util.log.warn(
            'MOCK - Setting RGB Bedroom Light to {}, {}, {}'.format(r, g, b))


def set_rgb_doorframe_level(r, g, b):
    if _set_rgb_level(r, g, b):
        tsl.util.log.warn(
            'MOCK - Setting RGB Doorframe Light to {}, {}, {}'.format(r, g, b))


def set_rgb_tensegrity_level(r, g, b):
    if _set_rgb_level(r, g, b):
        tsl.util.log.warn(
            'MOCK - Setting RGB Tensegrity Light to {}, {}, {}'.format(r, g, b))

_initialize()
