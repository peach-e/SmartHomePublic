# ----------------------------------------------------------------- #
#  File   : model.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.constants
import tsl.database.sqlite
import tsl.rgb
import tsl.util.exception


import json
import time

ONE_DAY_SECONDS = 86400


class Peripheral:

    def __init__(self, id, name, uuid, peripheral_type, state, mode, schedule, created_at, updated_at):
        self.id = id
        self.name = name
        self.uuid = uuid
        self.type = peripheral_type
        self.state = state
        self.mode = mode
        self.schedule = schedule
        self.created_at = created_at
        self.updated_at = updated_at

        state.validate(peripheral_type)

        if peripheral_type not in tsl.constants.PERIPHERAL_TYPES:
            raise tsl.util.exception.DataError(
                'Unknown type {}'.format(peripheral_type))

        if mode not in tsl.constants.PERIPHERAL_MODES:
            raise tsl.util.exception.DataError('Unknown mode {}'.format(mode))

    def convert_to_dictionary(self):
        return {
            "id":         self.id,
            "name":       self.name,
            "uuid":       self.uuid,
            "type":       self.type,
            "state":      self.state.convert_to_dictionary(),
            "mode":       self.mode,
            "schedule":   self.schedule.convert_to_dictionary() if self.schedule is not None else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Preset:

    def __init__(self, id, name, preset_items, nested_presets):
        self.id = id
        self.name = name
        self.preset_items = preset_items
        self.nested_presets = nested_presets

    def convert_to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "preset_items": [pi.convert_to_dictionary() for pi in self.preset_items],
            "nested_presets": [np.convert_to_dictionary() for np in self.nested_presets]
        }

    # Create a new Preset with no ID that is the flattened version of this.
    # Each nested preset we just harvest the preset items and boil them up.
    def flatten(self):
        preset_items = self.preset_items.copy()

        # For each nested preset, flatten it, and steal its preset items.
        for nested_preset in self.nested_presets:
            preset_items.extend(nested_preset.flatten().preset_items)

        # Create a new version of self that has no nested presets but all the
        # preset items.
        return Preset(None, None, preset_items, [])


class PresetItem:

    def __init__(self, id, preset_id, peripheral_id, mode, schedule_id=None, state=None):
        self.id = id
        self.preset_id = preset_id
        self.peripheral_id = peripheral_id
        self.mode = mode
        self.schedule_id = schedule_id
        self.state = state

        # Right now we just validate that the schedule and state are defined if we need them.
        # They will be further validated if we try to actually use this preset item to modify
        # a peripheral's state.
        if mode not in tsl.constants.PERIPHERAL_MODES:
            raise tsl.util.exception.DataError('Unknown mode {}'.format(mode))

        if mode == tsl.constants.PERIPHERAL_MODE_SCHEDULED and schedule_id is None:
            raise tsl.util.exception.DataError(
                'Invalid Schedule ID for Preset Item {}.'.format(id))

        if mode == tsl.constants.PERIPHERAL_MODE_FIXED and state is None:
            raise tsl.util.exception.DataError(
                'Invalid State for Preset Item {}.'.format(id))

    def convert_to_dictionary(self):
        return {
            "id": self.id,
            "preset_id": self.preset_id,
            "peripheral_id": self.peripheral_id,
            "mode": self.mode,
            "schedule_id": self.schedule_id,
            "state": self.state.convert_to_dictionary() if self.state else None
        }


class Schedule:

    def __init__(self, id, name, peripheral_type, schedule_items, created_at, updated_at):
        self.id = id
        self.name = name
        self.peripheral_type = peripheral_type
        self.schedule_items = schedule_items
        self.created_at = created_at
        self.updated_at = updated_at

        if peripheral_type not in tsl.constants.PERIPHERAL_TYPES:
            raise tsl.util.exception.DataError(
                'Unknown type {}'.format(peripheral_type))

        for schedule_item in schedule_items:
            schedule_item.state.validate(peripheral_type)

    def convert_to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "peripheral_type": self.peripheral_type,
            "schedule_items": [item.convert_to_dictionary() for item in self.schedule_items],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def validate(self, peripheral_type):

        is_valid = False

        try:
            # Schedule's peripheral type should match the normal type.
            assert self.peripheral_type == peripheral_type
            is_valid = True
        except:
            pass

        if not is_valid:
            raise tsl.util.exception.DataError(
                'Invalid Schedule {} for peripheral type {}'.format(self, peripheral_type))


class ScheduleItem:

    def __init__(self, id, trigger, state, created_at, updated_at):
        self.id = id
        self.trigger = trigger
        self.state = state
        self.created_at = created_at
        self.updated_at = updated_at

        trigger.validate()

    def convert_to_dictionary(self):
        return {
            "id":         self.id,
            "trigger":    self.trigger.convert_to_dictionary(),
            "state":      self.state.convert_to_dictionary(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class State:

    def __init__(self, enabled=None, level=None, r=None, g=None, b=None):
        self.enabled = enabled
        self.level = level
        self.r = r
        self.g = g
        self.b = b

    def _get_defined_attributes(self):
        result = []
        for key in ['enabled', 'level', 'r', 'g', 'b']:
            attr = getattr(self, key)
            if attr is not None:
                result.append(key)
        return result

    def create_from_dictionary(state_dict):
        enabled = state_dict.get('enabled')
        level = state_dict.get('level')
        r = state_dict.get('r')
        g = state_dict.get('g')
        b = state_dict.get('b')
        return State(enabled, level, r, g, b)

    def create_from_json(json_str):
        return State.create_from_dictionary(json.loads(json_str))

    def convert_to_dictionary(self):
        result = {}
        for key in self._get_defined_attributes():
            result[key] = getattr(self, key)
        return result

    def convert_to_json(self):
        return json.dumps(self.convert_to_dictionary())

    def is_equivalent(self, other_state):
        result = True
        for attribute in self._get_defined_attributes():
            if (getattr(self, attribute) != getattr(other_state, attribute)):
                result = False
        return result

    def validate(self, peripheral_type):
        is_valid = False

        try:
            # ON OFF devices should have 'enabled' to be a boolean.
            if peripheral_type == tsl.constants.PERIPHERAL_TYPE_ONOFF:
                if (self.enabled == True) or (self.enabled == False):
                    is_valid = True
            # SLIDER devices should be an integer between 0 and 255
            elif peripheral_type == tsl.constants.PERIPHERAL_TYPE_SLIDER:
                is_valid = tsl.rgb.is_level_valid(self.level)
            # RGB sliders should have 3 compliant channels.
            elif peripheral_type == tsl.constants.PERIPHERAL_TYPE_RGB:
                is_valid = tsl.rgb.is_rgb_valid(self.r, self.g, self.b)
            else:
                pass
        except:
            pass

        if not is_valid:
            raise tsl.util.exception.DataError(
                'Invalid State {} for type {}'.format(self, peripheral_type))


class Trigger:

    def __init__(self, hour=None, minute=None, second=None):
        self.hour = hour
        self.minute = minute
        self.second = second

    def create_from_dictionary(dictionary):
        hour = dictionary.get('hour')
        minute = dictionary.get('minute')
        second = dictionary.get('second')

        return Trigger(hour, minute, second)

    def create_from_json(json_str):
        return Trigger.create_from_dictionary(json.loads(json_str))

    def convert_to_dictionary(self):
        result = {}
        for key in ['hour', 'minute', 'second']:
            attr = getattr(self, key)
            if attr is not None:
                result[key] = attr
        return result

    def convert_to_json(self):
        return json.dumps(self.convert_to_dictionary())

    def validate(self):
        h = self.hour
        m = self.minute
        s = self.second

        if [h, m, s] == [None, None, None]:
            raise tsl.util.exception.DataError('Invalid Trigger'.format(mode))
