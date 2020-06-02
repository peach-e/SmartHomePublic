# ----------------------------------------------------------------- #
#  File   : schedule.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.database.sqlite
import tsl.model

import json


def _create_schedule_from_row(row):
    schedule_id = row[0]
    schedule_items = get_schedule_items(schedule_id)
    schedule = tsl.model.Schedule(
        row[0],
        row[1],
        row[2],
        schedule_items,
        row[3],
        row[4])
    return schedule


def get_schedules():
    query = 'SELECT * FROM schedules'
    rows = tsl.database.sqlite.execute_query(query)

    schedules = []
    for row in rows:
        schedules.append(_create_schedule_from_row(row))
    return schedules


def get_schedule(schedule_id):
    query = 'SELECT * FROM schedules WHERE id=?'
    rows = tsl.database.sqlite.execute_query(query, schedule_id)

    if len(rows):
        row = rows[0]
        return _create_schedule_from_row(row)
    else:
        return None


def get_schedule_items(schedule_id):
    query = 'SELECT * FROM schedule_items WHERE schedule_id=?'
    schedule_item_rows = tsl.database.sqlite.execute_query(query, schedule_id)

    result = []
    for row in schedule_item_rows:
        schedule_item = tsl.model.ScheduleItem(
            row[0],
            tsl.model.Trigger.create_from_json(row[2]),
            tsl.model.State.create_from_json(row[3]),
            row[4],
            row[5])
        result.append(schedule_item)
    return result
