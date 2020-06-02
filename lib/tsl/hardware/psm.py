# ----------------------------------------------------------------- #
#  File   : psm.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Peripheral Synchronization Master
import tsl.constants
import tsl.hardware.gpio
import tsl.hardware.http
import tsl.hardware.ledfan
import tsl.hardware.rf24
import tsl.util.exception
import tsl.util.log

UUID_BREEZE_FANS = '6826ed06-c7d0-4538-97b8-491891fcc134'
UUID_COTS_GROW_LIGHTS = 'e2cdbfcc-02cf-4a19-aa81-8c000a2f8640'
UUID_LED_GROW_LIGHTS = 'b3c23f37-b7ae-45ec-9a7c-c162e061a826'
UUID_BLUE_PANEL = '34166325-2d5c-49bf-a89a-c36f991c07bd'
UUID_GREEN_PANEL = '8c639c8c-7c45-41cc-bb86-b11d0a98e90e'
UUID_RGB_BEDROOM = '6fa939de-3775-4159-85e4-bd2e4d38ffa2'
UUID_RGB_DOORFRAME = '516fab6b-6db0-4c68-a1f6-2fbf76f05920'
UUID_RGB_TENSEGRITY = '5eef849c-3533-4513-bfa0-a3010bf06858'
UUID_CRPD_PIXEL_1 = '296e9040-b70a-4661-ab2c-e024d77aa35b'
UUID_CRPD_PIXEL_2 = '022f9ea3-9d67-4e41-ac16-815f6883b910'
UUID_CRPD_PIXEL_3 = '85c87440-1b80-42e5-8416-aa902791930a'
UUID_CRPD_PIXEL_4 = 'da5e1db6-def8-4f7d-aa2d-803ac0e13753'

VALID_UUIDS = [
    UUID_BREEZE_FANS,
    UUID_COTS_GROW_LIGHTS,
    UUID_LED_GROW_LIGHTS,
    UUID_BLUE_PANEL,
    UUID_GREEN_PANEL,
    UUID_RGB_BEDROOM,
    UUID_RGB_DOORFRAME,
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
    elif uuid == UUID_BREEZE_FANS:
        tsl.hardware.ledfan.set_fan_state(state.enabled)
    elif uuid == UUID_LED_GROW_LIGHTS:
        tsl.hardware.ledfan.set_led_levels(state.r, state.g, state.b)
    elif uuid == UUID_BLUE_PANEL:
        tsl.hardware.rf24.set_blue_level(state.level)
    elif uuid == UUID_GREEN_PANEL:
        tsl.hardware.rf24.set_green_level(state.level)
    elif uuid == UUID_RGB_BEDROOM:
        tsl.hardware.rf24.set_rgb_bedroom_level(state.r, state.g, state.b)
    elif uuid == UUID_RGB_DOORFRAME:
        tsl.hardware.rf24.set_rgb_doorframe_level(state.r, state.g, state.b)
    elif uuid == UUID_RGB_TENSEGRITY:
        tsl.hardware.rf24.set_rgb_tensegrity_level(state.r, state.g, state.b)
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
    tsl.hardware.ledfan.initialize()

_initialize()
