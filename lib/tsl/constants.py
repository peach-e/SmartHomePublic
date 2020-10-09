# ----------------------------------------------------------------- #
#  File   : constants.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Server Settings
SERVER_HOSTNAME = "0.0.0.0"
SERVER_PORT = 8000

# Worker Settings
WORKER_POLL_INTERVAL = 10

# Relative to app root
CONFIG_FILE_LOCATION = "conf/main.conf"
SQLITE_DB_LOCATION = "db/system.db"

PERIPHERAL_TYPE_ONOFF = "ONOFF"
PERIPHERAL_TYPE_SLIDER = "SLIDER"
PERIPHERAL_TYPE_RGB = "RGB"

PERIPHERAL_TYPES = [
    PERIPHERAL_TYPE_ONOFF,
    PERIPHERAL_TYPE_SLIDER,
    PERIPHERAL_TYPE_RGB,
]

# RF24 Communication
RF24_MAX_QUEUE_SIZE = 100
RF24_RETRY_DELAY = 15
RF24_RETRY_ATTEMPTS = 15
RF24_NODE_ADDRESS_RGB_BEDROOM = bytes([0xdc, 0x64, 0xb6, 0xe0, 0x03])
RF24_NODE_ADDRESS_RGB_DOORFRAME = bytes([0xdc, 0x64, 0xb6, 0xe0, 0x04])
RF24_NODE_ADDRESS_RGB_TENSEGRITY = bytes([0xdc, 0x64, 0xb6, 0xe0, 0x05])
RF24_NODE_ADDRESS_RGB_KITCHEN = bytes([0xdc, 0x64, 0xb6, 0xe0, 0x06])
RF24_NODE_ADDRESS_RGB_OFFICE_CENTER = bytes([0xdc, 0x64, 0xb6, 0xe0, 0x07])
RF24_NODE_ADDRESS_RGB_OFFICE_LEFT = bytes([0xdc, 0x64, 0xb6, 0xe0, 0x08])

# HTTP Peripheral Communication
HTTP_CRPD_ROUTE = 'strip'
HTTP_CRPD_STRIP_1 = 1
HTTP_CRPD_STRIP_2 = 2
HTTP_CRPD_STRIP_3 = 3
HTTP_CRPD_STRIP_4 = 4

RF24_COMMAND_SET_RGB = 0x03
