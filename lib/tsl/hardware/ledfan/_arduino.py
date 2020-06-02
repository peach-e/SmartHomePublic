# ----------------------------------------------------------------- #
#  File   : _arduino.py
#  Author : peach
#  Date   : 20 July 2019
# ----------------------------------------------------------------- #

# Provide the interface for arduino in real life.

import tsl.util.log

import serial
import time

SERIAL_DEVICE = tsl.configuration.val('SERIAL_DEVICE')
SERIAL_BAUD_RATE = tsl.configuration.val('SERIAL_BAUD_RATE')

FAN_DEVICE_ID = 0x01
LED_DEVICE_ID = 0x02

INITIALIZATION_DELAY = 2
# Instruction Sizes
# Look up the ICD for instruction writing in Confluence.
INSTRUCTION_SIZE_FAN = 0x03
INSTRUCTION_SIZE_LED = 0x05

_SERIAL_HANDLE = None


def _write(instruction):
    try:
        _SERIAL_HANDLE.write(instruction)
    except Exception as e:
        tsl.util.log.error('Error writing to serial.')
        tsl.util.log.error(e)


def close():
    _SERIAL_HANDLE.close()


def initialize():
    global _SERIAL_HANDLE
    _SERIAL_HANDLE = serial.Serial(SERIAL_DEVICE, SERIAL_BAUD_RATE)
    time.sleep(INITIALIZATION_DELAY)


def set_led_levels(r, g, b):
    command_arr = [INSTRUCTION_SIZE_LED, LED_DEVICE_ID, r, g, b]
    instruction = bytes(command_arr)
    _write(instruction)


def set_fan_state(is_enabled):
    enabled_bit = 1 if is_enabled else 0
    command_arr = [INSTRUCTION_SIZE_FAN, FAN_DEVICE_ID, is_enabled]
    instruction = bytes(command_arr)
    _write(instruction)
