# ----------------------------------------------------------------- #
#  File   : services.py
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
import tsl.util.log

from datetime import datetime

# ------------------------------------------------- #
#                    GENERAL                        #
# ------------------------------------------------- #


def apply_por_states():
    # As a worker module, I want to apply all states to
    # all hardware items on power on / reset.

    for peripheral in tsl.dao.peripheral.get_peripherals():
        tsl.hardware.psm.apply_hardware_state(peripheral)


# If you never called this, pass in None, and remember the timestamp it
# gives you back.
def apply_recent_triggers(timestamp_last_called):
    timestamp_now = datetime.now()
    if timestamp_last_called is None:
        return timestamp_now

    active_schedules = tsl.dao.schedule.get_schedules(True)
    for s in active_schedules:
        for si in s.schedule_items:
            next_occurrence = si.trigger.get_next(timestamp_last_called)
            if next_occurrence < timestamp_now:
                # Next occurrence happened sometime between last time we called
                # and now, so fire the preset.
                apply_preset(si.preset_id)
    return timestamp_now


# ------------------------------------------------- #
#                  PERIPHERALS                      #
# ------------------------------------------------- #


def get_peripherals():
    # As a web user, I want to view the status of each of the peripherals.
    return tsl.dao.peripheral.get_peripherals()


def set_peripheral_state(peripheral_id, state_dict):

    # As a web user, I want to manually set the state of a
    # peripheral and leave it fixed in that state.
    state = tsl.model.State.create_from_dictionary(state_dict)
    peripheral = tsl.dao.peripheral.get_peripheral(peripheral_id)

    if not peripheral:
        raise tsl.util.exception.DataError(
            'Invalid peripheral_id "{}"'.format(peripheral_id))

    # Validate the peripheral.
    state.validate(peripheral.type)

    # Update the peripheral in db.
    peripheral.state = state
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
        state = pi.state
        state_dict = state.convert_to_dictionary()
        set_peripheral_state(peripheral_id, state_dict)

    return True


def get_presets():
    # As a web user, I want to get and display a list of the presets.
    return tsl.dao.preset.get_public_presets()

# ------------------------------------------------- #
#                   SCHEDULES                       #
# ------------------------------------------------- #


def get_schedules():
    # As a web user, I want to view a list of all schedules.
    return tsl.dao.schedule.get_schedules()


def set_schedule_enabled(schedule_id, enabled):
    schedule = tsl.dao.schedule.get_schedule(schedule_id)
    if schedule is None:
        raise tsl.util.exception.DataError(
            f'Invalid schedule_id "{schedule_id}".')
    schedule.is_enabled = enabled

    tsl.dao.schedule.update_schedule(schedule)
    return True
