# ----------------------------------------------------------------- #
#  File   : model.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.constants
import tsl.database.sqlite
import tsl.rgb
import tsl.util.exception

from datetime import datetime
from croniter import croniter

import json


class Peripheral:

    def __init__(self, id, name, uuid, peripheral_type, state):
        self.id = id
        self.name = name
        self.uuid = uuid
        self.type = peripheral_type
        self.state = state

        state.validate(peripheral_type)

        if peripheral_type not in tsl.constants.PERIPHERAL_TYPES:
            raise tsl.util.exception.DataError(
                'Unknown type {}'.format(peripheral_type))

    def convert_to_dictionary(self):
        return {
            "id":         self.id,
            "name":       self.name,
            "uuid":       self.uuid,
            "type":       self.type,
            "state":      self.state.convert_to_dictionary(),
        }


class Preset:

    def __init__(self, id, name, is_public, preset_items, nested_presets):
        self.id = id
        self.name = name
        self.is_public = is_public
        self.preset_items = preset_items
        self.nested_presets = nested_presets

    def convert_to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_public": self.is_public,
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
        return Preset(None, None, None, preset_items, [])


class PresetItem:

    def __init__(self, id, peripheral_id, state):
        self.id = id
        self.peripheral_id = peripheral_id
        self.state = state

    def convert_to_dictionary(self):
        return {
            "id": self.id,
            "peripheral_id": self.peripheral_id,
            "state": self.state.convert_to_dictionary()
        }


class Schedule:

    def __init__(self, id, name, is_enabled, schedule_items):
        self.id = id
        self.name = name
        self.is_enabled = is_enabled
        self.schedule_items = schedule_items

    def convert_to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_enabled": self.is_enabled,
            "schedule_items": [item.convert_to_dictionary() for item in self.schedule_items],
        }


class ScheduleItem:

    def __init__(self, id, trigger, preset_id):
        self.id = id
        self.trigger = trigger
        self.preset_id = preset_id

        trigger.validate()

    def convert_to_dictionary(self):
        return {
            "id":        self.id,
            "trigger":   self.trigger.convert_to_dictionary(),
            "preset_id": self.preset_id
        }


class State:

    def __init__(self, enabled=None, level=None, r=None, g=None, b=None):
        self.enabled = enabled
        self.level = level
        self.r = r
        self.g = g
        self.b = b

        assert ((enabled is not None) or (level is not None) or
                (r is not None and g is not None and b is not None))

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

    def __init__(self, hour=None, minute=None):
        self.hour = hour
        self.minute = minute
        self.validate()

    def create_from_dictionary(dictionary):
        hour = dictionary.get('hour')
        minute = dictionary.get('minute')

        return Trigger(hour, minute)

    def create_from_json(json_str):
        return Trigger.create_from_dictionary(json.loads(json_str))

    def convert_to_dictionary(self):
        result = {}
        if self.hour is not None:
            result['hour'] = self.hour
        if self.minute is not None:
            result['minute'] = self.minute
        return result

    def convert_to_json(self):
        return json.dumps(self.convert_to_dictionary())

    def validate(self):
        h = self.hour
        m = self.minute

        if [h, m] == [None, None]:
            raise tsl.util.exception.DataError('Invalid Trigger')

        try:
            self.get_next(datetime.now())
        except:
            raise tsl.util.exception.DataError('Invalid Trigger')

    def get_next(self, reference_timestamp):
        h = str(self.hour) if self.hour is not None else '*'
        m = str(self.minute) if self.minute is not None else '*'

        cron_string = f'{m} {h} * * *'
        next_occurrence = croniter(
            cron_string, reference_timestamp).get_next(datetime)
        return next_occurrence
