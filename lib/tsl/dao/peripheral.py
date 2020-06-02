# ----------------------------------------------------------------- #
#  File   : peripheral.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.model
import tsl.dao.schedule
import tsl.database.sqlite


def _create_peripheral_from_row(row):
    schedule_id = row[6]
    if schedule_id is not None:
        schedule = tsl.dao.schedule.get_schedule(schedule_id)
    else:
        schedule = None

    state = tsl.model.State.create_from_json(row[4])

    peripheral = tsl.model.Peripheral(
        row[0],
        row[1],
        row[2],
        row[3],
        state,
        row[5],
        schedule,
        row[7],
        row[6])

    return peripheral


def get_peripheral(peripheral_id):
    query = 'SELECT * FROM peripherals WHERE id=?'
    result_rows = tsl.database.sqlite.execute_query(query, peripheral_id)

    if not len(result_rows):
        return None

    peripheral = _create_peripheral_from_row(result_rows[0])
    return peripheral


def get_peripherals():
    query = 'SELECT * FROM peripherals'
    peripheral_rows = tsl.database.sqlite.execute_query(query)

    result = []
    for row in peripheral_rows:
        result.append(_create_peripheral_from_row(row))
    return result


def update_peripheral(peripheral):
    id = peripheral.id
    query = """
UPDATE peripherals
SET  name        = ?,
     uuid        = ?,
     type        = ?,
     state       = ?,
     mode        = ?,
     schedule_id = ?
    WHERE id = ?
"""
    tsl.database.sqlite.execute_query(query,
                                      peripheral.name,
                                      peripheral.uuid,
                                      peripheral.type,
                                      peripheral.state.convert_to_json(),
                                      peripheral.mode,
                                      peripheral.schedule.id if peripheral.schedule is not None else None,
                                      peripheral.id
                                      )
