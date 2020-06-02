# ----------------------------------------------------------------- #
#  File   : __init__.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Provide the interface for GPIO control.

import tsl.configuration

USE_MOCK = tsl.configuration.val('USE_MOCK_GPIO')
if USE_MOCK:
    from tsl.hardware.gpio import _mock as _platform
else:
    from tsl.hardware.gpio import _pi2 as _platform


def set_grow_lights(state):
    _platform.set_grow_lights(state)
