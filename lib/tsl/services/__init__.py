# ----------------------------------------------------------------- #
#  File   : __init__.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Everything in here is basically a Use Case.
import tsl.constants
import tsl.dao.peripheral
import tsl.dao.preset
import tsl.dao.schedule
import tsl.hardware.psm
import tsl.model
import tsl.services.helper
import tsl.util.log

# ------------------------------------------------- #
#                    GENERAL                        #
# ------------------------------------------------- #


def apply_por_states():
    # As a worker module, I want to apply all states to
    # all hardware items on power on / reset.

    for peripheral in tsl.dao.peripheral.get_peripherals():
        tsl.hardware.psm.apply_hardware_state(peripheral)

# ------------------------------------------------- #
#                  PERIPHERALS                      #
# ------------------------------------------------- #


def enforce_peripheral_schedules():
    # As a worker module, I want to periodically go through each
    # peripheral and schedule and make everything is up to date.

    peripherals = tsl.dao.peripheral.get_peripherals()
    for peripheral in peripherals:
        if peripheral.schedule is None:
            continue
        schedule_items = peripheral.schedule.schedule_items
        active_schedule_item = tsl.services.helper.get_active_schedule_item(
            peripheral.schedule.schedule_items)
        # If state has changed, update the peripheral.
        if not peripheral.state.is_equivalent(active_schedule_item.state):
            peripheral.state = active_schedule_item.state
            tsl.dao.peripheral.update_peripheral(peripheral)
            tsl.hardware.psm.apply_hardware_state(peripheral)


def get_peripherals():
    # As a web user, I want to view the status of each of the peripherals.
    return tsl.dao.peripheral.get_peripherals()


def set_peripheral_schedule(peripheral_id, schedule_id):
    # As a web user, I want to manually set a schedule for a
    # peripheral so that the device takes on that schedule.
    mode = tsl.constants.PERIPHERAL_MODE_SCHEDULED
    peripheral = tsl.dao.peripheral.get_peripheral(peripheral_id)
    schedule = tsl.dao.schedule.get_schedule(schedule_id)

    if not peripheral:
        raise tsl.util.exception.DataError(
            'Invalid peripheral_id "{}"'.format(peripheral_id))
    if not peripheral:
        raise tsl.util.exception.DataError(
            'Invalid schedule_id "{}"'.format(schedule_id))

    # Validate the peripheral and schedule.
    schedule.validate(peripheral.type)

    # Update the peripheral in db.
    peripheral.schedule = schedule
    peripheral.mode = mode
    active_schedule_item = tsl.services.helper.get_active_schedule_item(
        schedule.schedule_items)
    peripheral.state = active_schedule_item.state
    tsl.dao.peripheral.update_peripheral(peripheral)
    tsl.hardware.psm.apply_hardware_state(peripheral)

    return True


def set_peripheral_state(peripheral_id, state_dict):

    # As a web user, I want to manually set the state of a
    # peripheral and leave it fixed in that state.
    state = tsl.model.State.create_from_dictionary(state_dict)
    mode = tsl.constants.PERIPHERAL_MODE_FIXED
    peripheral = tsl.dao.peripheral.get_peripheral(peripheral_id)

    if not peripheral:
        raise tsl.util.exception.DataError(
            'Invalid peripheral_id "{}"'.format(peripheral_id))

    # Validate the peripheral.
    state.validate(peripheral.type)

    # Update the peripheral in db.
    peripheral.state = state
    peripheral.mode = mode
    peripheral.schedule = None
    tsl.dao.peripheral.update_peripheral(peripheral)
    tsl.hardware.psm.apply_hardware_state(peripheral)

    return True
# ------------------------------------------------- #
#                    PRESETS                        #
# ------------------------------------------------- #


def apply_preset(preset_id):
    # As a web user, I want to activate a preset by clicking
    # on one of the buttons in the UI.

    preset = tsl.dao.preset.get_preset(preset_id)
    if not preset:
        raise tsl.util.exception.DataError(
            'Invalid preset_id "{}"'.format(preset_id))

    # Flatten the preset.
    preset = preset.flatten()
    # Enforce that the peripheral ids are unique.
    peripheral_ids = [pi.peripheral_id for pi in preset.preset_items]
    unique_peripheral_ids = set(peripheral_ids)
    if len(peripheral_ids) is not len(unique_peripheral_ids):
        raise tsl.util.exception.DataError(
            'Invalid preset "{}" with multiple configurations for one peripheral.'.format(preset.name))

    for pi in preset.preset_items:
        peripheral_id = pi.peripheral_id
        mode = pi.mode
        schedule_id = pi.schedule_id
        state = pi.state

        if mode == tsl.constants.PERIPHERAL_MODE_FIXED:
            state_dict = state.convert_to_dictionary()
            set_peripheral_state(peripheral_id, state_dict)
        else:
            set_peripheral_schedule(peripheral_id, schedule_id)

    return True


def get_presets():
    # As a web user, I want to get and display a list of the presets.
    return tsl.dao.preset.get_presets()
# ------------------------------------------------- #
#                   SCHEDULES                       #
# ------------------------------------------------- #


def get_schedules():
    # As a web user, I want to view a list of all schedules.
    return tsl.dao.schedule.get_schedules()
