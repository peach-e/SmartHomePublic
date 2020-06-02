# ----------------------------------------------------------------- #
#  File   : preset.py
#  Author : peach
#  Date   : 20 Nov 2019
# ----------------------------------------------------------------- #

import tsl.database.sqlite
import tsl.model

MAX_NESTING_RECURSION = 5

#
# Private
#


def _get_preset_name(preset_id):
    query = 'SELECT * FROM presets WHERE id=?'
    rows = tsl.database.sqlite.execute_query(query, preset_id)
    if not len(rows):
        return None
    return rows[0][1]


def _get_preset(preset_id, nested_recursion=int(0)):
    assert nested_recursion < MAX_NESTING_RECURSION

    # First, get the name and in doing so, make sure that the
    # preset even exists.
    preset_name = _get_preset_name(preset_id)
    if preset_name is None:
        return None

    # Get Preset Items
    preset_items = _get_preset_items(preset_id)

    # Get Nested Presets
    nested_presets = []
    nested_preset_ids = _get_nested_preset_ids(preset_id)
    for nested_preset_id in nested_preset_ids:
        nested_presets.append(_get_preset(nested_preset_id, nested_recursion + 1))

    # now build the object.
    preset = tsl.model.Preset(preset_id, preset_name, preset_items, nested_presets)
    return preset


def _get_nested_preset_ids(preset_id):
    query = 'SELECT nested_preset_id FROM nested_presets WHERE preset_id = ?'
    results = tsl.database.sqlite.execute_query(query, preset_id)
    return [r[0] for r in results]


def _get_preset_items(preset_id):
    query = 'SELECT * FROM preset_items WHERE preset_id=?'
    result = tsl.database.sqlite.execute_query(query, preset_id)

    preset_items = []
    for row in result:
        state_str = row[5]
        state = tsl.model.State.create_from_json(state_str) if (state_str is not None) else None
        preset_item = tsl.model.PresetItem(row[0], row[1], row[2], row[3], row[4], state)
        preset_items.append(preset_item)
    return preset_items
#
# Public
#


def get_preset(preset_id):
    preset = _get_preset(preset_id)
    return preset


def get_presets():
    query = 'SELECT * FROM presets'
    preset_rows = tsl.database.sqlite.execute_query(query)

    presets = []
    for row in preset_rows:
        id = row[0]
        name = row[1]
        presets.append(_get_preset(id))
    return presets
