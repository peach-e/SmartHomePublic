# ----------------------------------------------------------------- #
#  File   : sqlite.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.constants
import tsl.util.env
import tsl.util.exception
import tsl.util.path
import tsl.util.log

import sqlite3

_APP_ROOT = tsl.util.env.get_environment_variable('APP_ROOT')
_DB_FILE_LOCATION = tsl.util.path.join_paths(
    _APP_ROOT,
    tsl.constants.SQLITE_DB_LOCATION)

_MAX_NUMBER_OF_CONNECTIONS = 10
_NUMBER_OF_CONNECTIONS = 0


def execute_query(query, *parameters):
    handle = get_database_connection()
    result = handle.execute(query, (*parameters,)).fetchall()
    write_and_close_connection(handle)
    return result


def get_db_file_location():
    return _DB_FILE_LOCATION


def get_database_connection():
    handle = sqlite3.connect(_DB_FILE_LOCATION)
    global _NUMBER_OF_CONNECTIONS
    _NUMBER_OF_CONNECTIONS += 1
    if _NUMBER_OF_CONNECTIONS > _MAX_NUMBER_OF_CONNECTIONS:
        raise tsl.util.exception.DatabaseError(
            'Exceeded MAX_NUMBER_OF_CONNECTIONS ({}). You may have a connection leak.'.format(_MAX_NUMBER_OF_CONNECTIONS))
    return handle


def write_and_close_connection(handle):
    handle.commit()
    handle.close()
    global _NUMBER_OF_CONNECTIONS
    _NUMBER_OF_CONNECTIONS -= 1
