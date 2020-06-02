# ----------------------------------------------------------------- #
#  File   : __init__.py
#  Author : peach
#  Date   : 12 November 2019
# ----------------------------------------------------------------- #

# nRF24L01 interface.

import tsl.configuration

USE_MOCK = tsl.configuration.val('USE_MOCK_RF24')
if USE_MOCK:
    from tsl.hardware.rf24._mock import *
else:
    from tsl.hardware.rf24._pi2 import *
