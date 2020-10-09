# ----------------------------------------------------------------- #
#  File   : peripheral.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.model
import tsl.dao.schedule
import tsl.database.sqlite


def _create_peripheral_from_row(row):
    state = tsl.model.State.create_from_json(row[4])

    peripheral = tsl.model.Peripheral(
        row[0],
        row[1],
        row[2],
        row[3],
        state)

    return peripheral


def create_peripheral(peripheral):
    query = "INSERT INTO peripherals (name, uuid, type, state) VALUES (?,?,?,?)"
    result, peripheral_id = tsl.database.sqlite.execute_query(query,
                                                              peripheral.name,
                                                              peripheral.uuid,
                                                              peripheral.type,
                                                              peripheral.state.convert_to_json(),
                                                              )

    return peripheral_id


def get_peripheral(peripheral_id):
    query = 'SELECT * FROM peripherals WHERE id=?'
    result_rows = tsl.database.sqlite.execute_query(query, peripheral_id)[0]

    if not len(result_rows):
        return None

    peripheral = _create_peripheral_from_row(result_rows[0])
    return peripheral


def get_peripherals():
    query = 'SELECT * FROM peripherals'
    peripheral_rows = tsl.database.sqlite.execute_query(query)[0]

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
     state       = ?
WHERE id = ?
"""
    tsl.database.sqlite.execute_query(query,
                                      peripheral.name,
                                      peripheral.uuid,
                                      peripheral.type,
                                      peripheral.state.convert_to_json(),
                                      peripheral.id
                                      )
