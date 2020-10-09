# ----------------------------------------------------------------- #
#  File   : psm.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Peripheral Synchronization Master
import tsl.constants
import tsl.hardware.gpio
import tsl.hardware.http
import tsl.hardware.rf24
import tsl.util.exception
import tsl.util.log

UUID_COTS_GROW_LIGHTS = 'e2cdbfcc-02cf-4a19-aa81-8c000a2f8640'
UUID_RGB_OFFICE_LEFT = 'b69eee14-bb98-4236-84eb-45644479430d'
UUID_RGB_OFFICE_CENTER = '745b09f8-49e7-407b-b0d4-d70a248f9f2b'
UUID_RGB_BEDROOM = '6fa939de-3775-4159-85e4-bd2e4d38ffa2'
UUID_RGB_HALLWAY = '516fab6b-6db0-4c68-a1f6-2fbf76f05920'
UUID_RGB_KITCHEN = '9bbf883b-db13-4aca-ab08-16f71a769084'
UUID_RGB_TENSEGRITY = '5eef849c-3533-4513-bfa0-a3010bf06858'
UUID_CRPD_PIXEL_1 = '296e9040-b70a-4661-ab2c-e024d77aa35b'
UUID_CRPD_PIXEL_2 = '022f9ea3-9d67-4e41-ac16-815f6883b910'
UUID_CRPD_PIXEL_3 = '85c87440-1b80-42e5-8416-aa902791930a'
UUID_CRPD_PIXEL_4 = 'da5e1db6-def8-4f7d-aa2d-803ac0e13753'

VALID_UUIDS = [
    UUID_COTS_GROW_LIGHTS,
    UUID_RGB_OFFICE_LEFT,
    UUID_RGB_OFFICE_CENTER,
    UUID_RGB_BEDROOM,
    UUID_RGB_HALLWAY,
    UUID_RGB_KITCHEN,
    UUID_RGB_TENSEGRITY,
    UUID_CRPD_PIXEL_1,
    UUID_CRPD_PIXEL_2,
    UUID_CRPD_PIXEL_3,
    UUID_CRPD_PIXEL_4,
]


def apply_hardware_state(peripheral):
    if not peripheral.uuid in VALID_UUIDS:
        raise tsl.util.exception.DataError(
            'Unknown UUID {}'.format(peripheral.uuid))

    state = peripheral.state
    uuid = peripheral.uuid

    # Do what the UUID wants us to do.
    if uuid == UUID_COTS_GROW_LIGHTS:
        # Polarity is reversed because of how the relays on here work.
        tsl.hardware.gpio.set_grow_lights(not state.enabled)
    elif uuid == UUID_RGB_OFFICE_LEFT:
        addr = tsl.constants.RF24_NODE_ADDRESS_RGB_OFFICE_LEFT
        tsl.hardware.rf24.set_rgb_level(addr, state.r, state.g, state.b)
    elif uuid == UUID_RGB_OFFICE_CENTER:
        addr = tsl.constants.RF24_NODE_ADDRESS_RGB_OFFICE_CENTER
        tsl.hardware.rf24.set_rgb_level(addr, state.r, state.g, state.b)
    elif uuid == UUID_RGB_BEDROOM:
        addr = tsl.constants.RF24_NODE_ADDRESS_RGB_BEDROOM
        tsl.hardware.rf24.set_rgb_level(addr, state.r, state.g, state.b)
    elif uuid == UUID_RGB_HALLWAY:
        addr = tsl.constants.RF24_NODE_ADDRESS_RGB_DOORFRAME
        tsl.hardware.rf24.set_rgb_level(addr, state.r, state.g, state.b)
    elif uuid == UUID_RGB_KITCHEN:
        addr = tsl.constants.RF24_NODE_ADDRESS_RGB_KITCHEN
        tsl.hardware.rf24.set_rgb_level(addr, state.r, state.g, state.b)
    elif uuid == UUID_RGB_TENSEGRITY:
        addr = tsl.constants.RF24_NODE_ADDRESS_RGB_TENSEGRITY
        tsl.hardware.rf24.set_rgb_level(addr, state.r, state.g, state.b)
    elif uuid == UUID_CRPD_PIXEL_1:
        tsl.hardware.http.set_crpd_pixel(tsl.constants.HTTP_CRPD_STRIP_1, state.r, state.g, state.b)
    elif uuid == UUID_CRPD_PIXEL_2:
        tsl.hardware.http.set_crpd_pixel(tsl.constants.HTTP_CRPD_STRIP_2, state.r, state.g, state.b)
    elif uuid == UUID_CRPD_PIXEL_3:
        tsl.hardware.http.set_crpd_pixel(tsl.constants.HTTP_CRPD_STRIP_3, state.r, state.g, state.b)
    elif uuid == UUID_CRPD_PIXEL_4:
        tsl.hardware.http.set_crpd_pixel(tsl.constants.HTTP_CRPD_STRIP_4, state.r, state.g, state.b)
    return


def _initialize():
    # any peripherals that need initialization beyond importing
    # should be initialized here.
    return

_initialize()
