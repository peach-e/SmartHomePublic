# ----------------------------------------------------------------- #
#  File   : schedule.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.database.sqlite
import tsl.model

import json


def create_schedule(schedule):
    # Create schedule.
    query = "INSERT INTO schedules (name, is_enabled) VALUES (?, ?)"
    result, schedule_id = tsl.database.sqlite.execute_query(
        query, schedule.name, schedule.is_enabled)

    # Insert schedule items.
    for schedule_item in schedule.schedule_items:
        query = "INSERT INTO schedule_items (schedule_id, trigger, preset_id) VALUES (?,?,?)"
        tsl.database.sqlite.execute_query(
            query, schedule_id, schedule_item.trigger.convert_to_json(), schedule_item.preset_id)
    return schedule_id


def get_schedule(schedule_id):
    query = '''
SELECT s.id, s.name, s.is_enabled, si.id, si.trigger, si.preset_id
FROM schedules as s
LEFT JOIN schedule_items as si
ON si.schedule_id = s.id
WHERE s.id = ?
'''
    result = tsl.database.sqlite.execute_query(query, schedule_id)[0]
    if len(result) == 0:
        return None

    id = result[0][0]
    name = result[0][1]
    is_enabled = result[0][2]
    schedule_items = []
    for row in result:
        trigger = tsl.model.Trigger.create_from_json(row[4])
        schedule_item = tsl.model.ScheduleItem(row[3], trigger, row[5])
        schedule_items.append(schedule_item)
    preset = tsl.model.Schedule(id, name, is_enabled, schedule_items)

    return preset


def get_schedules(where_is_enabled=None):

    if where_is_enabled:
        query = 'SELECT id FROM schedules WHERE is_enabled=TRUE'
    else:
        query = 'SELECT id FROM schedules'
    rows = tsl.database.sqlite.execute_query(query)[0]

    schedules = []
    for row in rows:
        id = row[0]
        schedules.append(get_schedule(id))
    return schedules


def update_schedule(schedule):
    query = 'UPDATE schedules SET name=?, is_enabled=? WHERE id=?'
    tsl.database.sqlite.execute_query(
        query, schedule.name, schedule.is_enabled, schedule.id)
