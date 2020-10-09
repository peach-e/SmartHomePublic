# ----------------------------------------------------------------- #
#  File   : rf24.py
#  Author : peach
#  Date   : 12 November 2019
# ----------------------------------------------------------------- #

import tsl.configuration
import tsl.constants
import tsl.rgb
import tsl.util.log


USE_MOCK = tsl.configuration.val('USE_MOCK_RF24')
if USE_MOCK:
    from tsl.hardware.mocks import RF24_lib as RF24
else:
    import RF24

from threading import Thread
from queue import Queue
from time import sleep

COMMAND_SET_RGB = tsl.constants.RF24_COMMAND_SET_RGB

_RADIO_INTERVAL = 0.5
_RADIO_MONITOR = None


class _RadioMonitor(Thread):

    def __init__(self):
        Thread.__init__(self)
        self._stop_requested = False
        self.daemon = True

        tsl.util.log.info('Initializing RF24 Radio')
        self._radio = RF24.RF24(RF24.RPI_BPLUS_GPIO_J8_15,
                                RF24.RPI_BPLUS_GPIO_J8_24,
                                RF24.BCM2835_SPI_SPEED_8MHZ)
        self._radio.begin()

        tsl.util.log.info('Setting max delay and retries to RF24 Radio')
        self._radio.setRetries(
            tsl.constants.RF24_RETRY_DELAY, tsl.constants.RF24_RETRY_ATTEMPTS)

        tsl.util.log.info('Initializing Transmission Request Queue')
        self._queue = Queue(tsl.constants.RF24_MAX_QUEUE_SIZE)

    def stop(self):
        self._stop_requested = True

    def run(self):
        while not self._stop_requested:
            sleep(_RADIO_INTERVAL)
            if not self._queue.empty():
                self.process_request(self._queue.get())

    def process_request(self, request):
        address = request.address
        payload = request.payload
        self._radio.stopListening()
        self._radio.openWritingPipe(request.address)
        self._radio.write(request.payload)

    def submit_request(self, request):
        self._queue.put(request)


class _TransmissionRequest():

    def __init__(self, address, payload):
        self.address = address
        self.payload = payload

def _get_address_string(address):
    return "{" + ' '.join([hex(x) for x in address]) + "}"

def _initialize():
    tsl.util.log.info('Initializing RF24 Radio Interface')
    global _RADIO_MONITOR
    _RADIO_MONITOR = _RadioMonitor()
    _RADIO_MONITOR.start()


def set_discrete_level(address, level):
    if not tsl.rgb.is_level_valid(level):
        tsl.util.log.error(
            'Invalid light level. Not integer between 0 and 255.')
        return 0
    request = _TransmissionRequest(address, bytes([level]))
    _RADIO_MONITOR.submit_request(request)

    tsl.util.log.info(f'Setting device {_get_address_string(address)} to level {level}.')
    return 1


def set_rgb_level(address, r, g, b):
    if not tsl.rgb.is_rgb_valid(r, g, b):
        tsl.util.log.error('Error setting RGB level.')
        return 0

    request = _TransmissionRequest(address, bytes([COMMAND_SET_RGB, r, g, b]))
    _RADIO_MONITOR.submit_request(request)

    tsl.util.log.info(f'Setting device {_get_address_string(address)} to {r}, {g}, {b}.')
    return 1

_initialize()