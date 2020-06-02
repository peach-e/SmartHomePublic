# ----------------------------------------------------------------- #
#  File   : rgb.py
#  Author : peach
#  Date   : 24 May 2020
# ----------------------------------------------------------------- #

# Application-specific utilitiy for working with and validating RGB values.
import tsl.constants
import tsl.util.log


def is_level_valid(level):

    try:
        assert type(level) is int
        assert level >= 0
        assert level <= 255
    except AssertionError:
        return False
    return True


def is_rgb_valid(r, g, b):
    return is_level_valid(r) and is_level_valid(g) and is_level_valid(b)
