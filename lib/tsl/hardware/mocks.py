# ----------------------------------------------------------------- #
#  File   : mocks.py
#  Author : peach
#  Date   : 29 September 2020
# ----------------------------------------------------------------- #

import tsl.util.log

def join_args(self, *args):
    return ', '.join([str(arg) for arg in args])

class Mock():
    @staticmethod
    def explain(message):
        tsl.util.log.warn(f'MOCK - {message}')

class GPIO(Mock):
    BCM = 'BCM'
    OUT = 'OUT'
    @staticmethod
    def explain(message):
        Mock.explain(f'GPIO-{message}')
    @staticmethod
    def setwarnings(setting):
        return
    @staticmethod
    def setmode(mode):
        return
    @classmethod
    def setup(cls, *args):
        cls.explain(f'Setting up GPIO with args {join_args(args)}.')
    @classmethod
    def output(cls, pin, state):
        cls.explain(f'Outputting pin {pin} with state {state}.')

class RF24_lib():
    RPI_BPLUS_GPIO_J8_15 = '15'
    RPI_BPLUS_GPIO_J8_24 = '24'
    BCM2835_SPI_SPEED_8MHZ = '8e6'

    class RF24(Mock):
        def __init__(self, *args):
            self.explain('Creating Handle.')
        @staticmethod
        def explain(message):
            Mock.explain(f'RF24-{message}')
        def begin(self):
            self.explain('Starting RF24 Radio')
        def setRetries(self, *args):
            return
        def stopListening(self):
            return
        def openWritingPipe(self, addr):
            return
        def write(self, payload):
            self.explain(f'Writing payload {str(payload)}')

class Serial(Mock):
    def __init__(self, *args):
        self.explain(f'Creating Serial handle with args {join_args(args)}.')
    @staticmethod
    def explain(message):
        Mock.explain(f'Serial-{message}')
    def write(self, message):
        self.explain(f'Writing payload {message}')
    def close(self):
        self.explain('Closing handle')