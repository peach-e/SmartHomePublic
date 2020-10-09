# ----------------------------------------------------------------- #
#  File   : preset.py
#  Author : peach
#  Date   : 20 Nov 2019
# ----------------------------------------------------------------- #

import tsl.database.sqlite
import tsl.model

_MAX_NESTING_RECURSION = 5

#
# Private
#


def _get_nested_preset_ids(preset_id):
    query = 'SELECT nested_preset_id FROM nested_presets WHERE preset_id = ?'
    results = tsl.database.sqlite.execute_query(query, preset_id)[0]
    return [r[0] for r in results]


def _get_preset(preset_id, recursion):
    if recursion > _MAX_NESTING_RECURSION:
        raise tsl.util.exception.DataError(
            'Maximum recursion encountered while getting presets.')
    recursion += 1

    query = '''
SELECT p.id, p.name, p.is_public, pi.id, pi.peripheral_id, pi.state
FROM presets as p
LEFT JOIN preset_items as pi
ON pi.preset_id = p.id
WHERE p.id = ?
'''
    result = tsl.database.sqlite.execute_query(query, preset_id)[0]
    if len(result) == 0:
        return None

    id = result[0][0]
    name = result[0][1]
    is_public = result[0][2]
    preset_items = []
    for row in result:
        preset_item_id = row[3]
        if preset_item_id is None:
            # Terrible hack because SQLITE will apparently return results in query
            # where the ON condition clearly fails.
            continue
        state = tsl.model.State.create_from_json(row[5])
        preset_item = tsl.model.PresetItem(row[3], row[4], state)
        preset_items.append(preset_item)

    nested_presets = [_get_preset(npid, recursion)
                      for npid in _get_nested_preset_ids(id)]
    preset = tsl.model.Preset(
        id, name, is_public, preset_items, nested_presets)

    return preset

#
# Public
#

# Create a preset, but does not account for nested presets yet.


def associate_nested_preset(parent_id, child_id):
    query = 'INSERT INTO nested_presets (preset_id, nested_preset_id) VALUES (?,?)'
    result, association_id = tsl.database.sqlite.execute_query(
        query, parent_id, child_id)
    return association_id


def create_preset(preset):
    # Create the preset
    query = 'INSERT INTO presets (name, is_public) VALUES (?,?)'
    result, preset_id = tsl.database.sqlite.execute_query(
        query, preset.name, preset.is_public)

    # Create the preset items.
    for preset_item in preset.preset_items:
        query = 'INSERT INTO preset_items (preset_id, peripheral_id, state) VALUES (?,?,?)'
        tsl.database.sqlite.execute_query(
            query, preset_id, preset_item.peripheral_id, preset_item.state.convert_to_json())
    return preset_id


def get_preset(preset_id):
    return _get_preset(preset_id, 0)


def get_public_presets():
    query = 'SELECT id FROM presets WHERE is_public=TRUE'
    rows = tsl.database.sqlite.execute_query(query)[0]

    presets = []
    for row in rows:
        id = row[0]
        presets.append(get_preset(id))
    return presets
