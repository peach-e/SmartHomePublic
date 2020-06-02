# ----------------------------------------------------------------- #
#  File   : _pi2.py
#  Author : peach
#  Date   : 12 November 2019
# ----------------------------------------------------------------- #

import tsl.constants
import tsl.rgb
import tsl.util.log

import RF24
from threading import Thread
from queue import Queue

ADDRESS_BLUE = tsl.constants.RF24_NODE_ADDRESS_BLUE
ADDRESS_GREEN = tsl.constants.RF24_NODE_ADDRESS_GREEN
ADDRESS_RGB_BEDROOM = tsl.constants.RF24_NODE_ADDRESS_RGB_BEDROOM
ADDRESS_RGB_DOORFRAME = tsl.constants.RF24_NODE_ADDRESS_RGB_DOORFRAME
ADDRESS_RGB_TENSEGRITY = tsl.constants.RF24_NODE_ADDRESS_RGB_TENSEGRITY

COMMAND_SET_RGB = tsl.constants.RF24_COMMAND_SET_RGB

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


def _initialize():
    tsl.util.log.info('Initializing RF24 Radio Interface')
    global _RADIO_MONITOR
    _RADIO_MONITOR = _RadioMonitor()
    _RADIO_MONITOR.start()


def _set_discrete_level(address, level):
    if not tsl.rgb.is_level_valid(level):
        tsl.util.log.error(
            'Invalid light level. Not integer between 0 and 255.')
        return 0
    request = _TransmissionRequest(address, bytes([level]))
    _RADIO_MONITOR.submit_request(request)
    return 1


def _set_rgb_level(address, r, g, b):
    if not tsl.rgb.is_rgb_valid(r, g, b):
        tsl.util.log.error('Error setting RGB level.')
        return 0

    request = _TransmissionRequest(address, bytes([COMMAND_SET_RGB, r, g, b]))
    _RADIO_MONITOR.submit_request(request)
    return 1


def set_blue_level(level):

    if _set_discrete_level(ADDRESS_BLUE, level):
        tsl.util.log.info('Setting Blue Light to {}'.format(level))


def set_green_level(level):

    if _set_discrete_level(ADDRESS_GREEN, level):
        tsl.util.log.info('Setting Green Light to {}'.format(level))


def set_rgb_bedroom_level(r, g, b):

    if _set_rgb_level(ADDRESS_RGB_BEDROOM, r, g, b):
        tsl.util.log.info(f'Setting Bedroom RGB Light to {r}, {g}, {b}.')


def set_rgb_doorframe_level(r, g, b):

    if _set_rgb_level(ADDRESS_RGB_DOORFRAME, r, g, b):
        tsl.util.log.info(f'Setting Doorframe RGB Light to {r}, {g}, {b}.')


def set_rgb_tensegrity_level(r, g, b):

    if _set_rgb_level(ADDRESS_RGB_TENSEGRITY, r, g, b):
        tsl.util.log.info(f'Setting Tensegrity RGB Light to {r}, {g}, {b}.')

_initialize()
